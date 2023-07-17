import os
import re
import requests
import threading
import time

from torrequest import TorRequest
from time import monotonic
from requests_futures.sessions import FuturesSession
from .notify import QueryNotifyPrint
from .sites import SitesInformation
from .result import QueryStatus
from .result import QueryResult

import concurrent.futures

def get_response(request_future, error_type, social_network):
    # Default for Response object if some failure occurs.
    response = None

    error_context = "General Unknown Error"
    exception_text = None
    try:
        response = request_future.result()
        if response.status_code:
            # Status code exists in response object
            error_context = None

            # Check for redirection for instagram, linkedin
            # if response.history:
            #     # Redirection occurred
            #     print("Redirection occurred:")
            #     for redirect in response.history:
            #         print(redirect.status_code, redirect.url)
            #     print("Final URL:", response.url)

            #     error_context = "Redirection"
            #     exception_text = "Redirection"

    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        exception_text = str(errh)
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        exception_text = str(errp)
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        exception_text = str(errc)
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        exception_text = str(errt)
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        exception_text = str(err)


    return response, error_context, exception_text


def interpolate_string(object, username):
    """Insert a string into the string properties of an object recursively."""

    if isinstance(object, str):
        return object.replace("{}", username)
    elif isinstance(object, dict):
        for key, value in object.items():
            object[key] = interpolate_string(value, username)
    elif isinstance(object, list):
        for i in object:
            object[i] = interpolate_string(object[i], username)

    return object

class MultithreadigSession(FuturesSession):
    # Async sending requests and multithreading session class
    def request(self,method,url,hooks=None, *args, **kwargs):
        # Record the start time for the request.
        if hooks is None:
            hooks = {}
        start = monotonic()

        def response_time(resp, *args, **kwargs):
            # Response hook
            resp.elapsed = monotonic() - start
            return

            # Install hook to execute when response completes.
            # Make sure that the time measurement hook is first, so we will not
            # track any later hook's execution time
        try:
            if isinstance(hooks["response"], list):
                hooks["response"].insert(0, response_time)
            elif isinstance(hooks["response"], tuple):
                # Convert tuple to list and insert time measurement hook first.
                hooks["response"] = list(hooks["response"])
                hooks["response"].insert(0, response_time)
            else:
                # Must have previously contained a single hook function,
                # so convert to list.
                hooks["response"] = [response_time, hooks["response"]]
        except KeyError:
            # No response hook was already defined, so install it ourselves.
            hooks["response"] = [response_time]
        return super(MultithreadigSession, self).request(method,
                                                           url,
                                                           hooks=hooks,
                                                           *args, **kwargs)    


class UrlFinder:
    def __init__(self, username_list):
        # Constructor for UrlFinder
        # username_list: generated usernames (4000)
        #
        self.username_list = username_list
        self.result_url_list = []
        self.event = threading.Event()

    def find_profile(self,username,tor=False, unique_tor=False,proxy=None,timeout=60):
        # Create session based on request methodology
        sites = []
        sites = SitesInformation(os.path.join(os.path.dirname(__file__), "resources/platform_list.json"))
        site_data_all = {site.name: site.information for site in sites}
        site_data = site_data_all
        # Create notify object for query results.
        query_notify = QueryNotifyPrint(result=None,
                                    verbose=False,
                                    print_all=False,
                                    browse=False)
        query_notify.start(username)
        if tor or unique_tor:
            # Requests using Tor obfuscation
            underlying_request = TorRequest()
            underlying_session = underlying_request.session
        else:
            # Normal requests
            underlying_session = requests.session()
            underlying_request = requests.Request()
        # Limit number of workers to 20.
        # This is probably vastly overkill.
        if len(site_data) >= 300:
            max_workers = 300
        else:
            max_workers = len(site_data)
        
        session = MultithreadigSession(max_workers=max_workers,session=underlying_session)
        
        # Results from analysis of all sites
        results_total = {}



        #######################################################################################
        #
        #                Checking Profiles from profile URL
        #
        #######################################################################################

        # First create futures for all requests. This allows for the requests to run in parallel
        for social_network, net_info in site_data.items():
            # Results from analysis of this specific site
            results_site = {"url_main": net_info.get("urlMain")}

            # Record URL of main site
            # A user agent is needed because some sites don't return the correct
            # information since they think that we are bots (Which we actually are...)
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
            }
            
            if "headers" in net_info:
                # Override/append any extra headers required by a given site.
                headers.update(net_info["headers"])

            # URL of user on site (if it exists)
            url = interpolate_string(net_info["url"], username)
            # Don't make request if username is invalid for the site
            regex_check = net_info.get("regexCheck")
            if regex_check and re.search(regex_check, username) is None:
                # No need to do the check at the site: this username is not allowed.
                # results_site["status"] = QueryResult(username,
                #                                     social_network,
                #                                     url,
                #                                     QueryStatus.ILLEGAL)
                results_site["status"] = QueryResult(username,
                                                 social_network,
                                                 url,
                                                 QueryStatus.ILLEGAL)
                results_site["url_user"] = ""
                results_site["http_status"] = ""
                results_site["response_text"] = ""
                query_notify.update(results_site["status"])
            else:
                # URL of user on site (if it exists)
                results_site["url_user"] = url
                url_probe = net_info.get("urlProbe")
                request_method = net_info.get("request_method")
                request_payload = net_info.get("request_payload")
                request = None

                if request_method is not None:
                    if request_method == "GET":
                        request = session.get
                    elif request_method == "HEAD":
                        request = session.head
                    elif request_method == "POST":
                        request = session.post
                    elif request_method == "PUT":
                        request = session.put
                    else:
                        raise RuntimeError(f"Unsupported request_method for {url}")

                if request_payload is not None:
                    request_payload = interpolate_string(request_payload, username)

                if url_probe is None:
                    # Probe URL is normal one seen by people out on the web.
                    url_probe = url
                else:
                    # There is a special URL for probing existence separate
                    # from where the user profile normally can be found.
                    url_probe = interpolate_string(url_probe, username)

                if request is None:
                    if net_info["errorType"] == "status_code":
                        # In most cases when we are detecting by status code,
                        # it is not necessary to get the entire body:  we can
                        # detect fine with just the HEAD response.
                        request = session.head
                    else:
                        # Either this detect method needs the content associated
                        # with the GET response, or this specific website will
                        # not respond properly unless we request the whole page.
                        request = session.get

                if net_info["errorType"] == "response_url":
                    # Site forwards request to a different URL if username not
                    # found.  Disallow the redirect so we can capture the
                    # http status from the original URL request.
                    allow_redirects = False
                else:
                    # Allow whatever redirect that the site wants to do.
                    # The final result of the request will be what is available.
                    allow_redirects = True

                # proxy = 'http://7b26afa746c5aa85d837d1440875a2c44279615a:@proxy.zenrows.com:8001'

                # This future starts running the request in a new thread, doesn't block the main thread
                if proxy is not None:
                    proxies = {"http": proxy, "https": proxy}
                    future = request(url=url_probe, headers=headers,
                                    proxies=proxies,
                                    allow_redirects=allow_redirects,
                                    timeout=timeout,
                                    json=request_payload
                                    )
                else:
                    future = request(url=url_probe, headers=headers,
                                    allow_redirects=allow_redirects,
                                    timeout=timeout,
                                    json=request_payload
                                    )

                # Store future in data for access later
                net_info["request_future"] = future
                # Reset identify for tor (if needed)
                if unique_tor:
                    underlying_request.reset_identity()

            # Add this site's results into final dictionary with all the other results.
            results_total[social_network] = results_site
        
        # Open the file containing account links
        # Core logic: If tor requests, make them here. If multi-threaded requests, wait for responses
        for social_network, net_info in site_data.items():
            # Retrieve results again
            results_site = results_total.get(social_network)
            # Retrieve other site information again
            url = results_site.get("url_user")


            status = results_site.get("status")
            if status is not None:
                # We have already determined the user doesn't exist here
                continue 

                # Get the expected error type
            error_type = net_info["errorType"]
            error_code = net_info.get("errorCode")

            # Retrieve future and ensure it has finished
            future = net_info["request_future"]
            r, error_text, exception_text = get_response(request_future=future,
                                                        error_type=error_type,
                                                        social_network=social_network)

            # Get response time for response of our request.
            try:
                response_time = r.elapsed
            except AttributeError:
                response_time = None

            # Attempt to get request information
            try:
                http_status = r.status_code
            except:
                http_status = "?"
            try:
                response_text = r.text.encode(r.encoding or "UTF-8")
            except:
                response_text = ""
            
            query_status = QueryStatus.UNKNOWN
            error_context = None
            if error_text is not None:
                error_context = error_text
            elif error_type == "message":
                # error_flag True denotes no error found in the HTML
                # error_flag False denotes error found in the HTML
                error_flag = True
                errors = net_info.get("errorMsg")
                # errors will hold the error message
                # it can be string or list
                # by isinstance method we can detect that
                # and handle the case for strings as normal procedure
                # and if its list we can iterate the errors
                if isinstance(errors, str):
                    # Checks if the error message is in the HTML
                    # if error is present we will set flag to False
                    if errors in r.text:
                        error_flag = False
                else:
                    # If it's list, it will iterate all the error message
                    for error in errors:
                        if error in r.text:
                            error_flag = False
                            break
                if error_flag:
                    query_status = QueryStatus.CLAIMED
                else:
                    query_status = QueryStatus.AVAILABLE
            elif error_type == "status_code":
                # Checks if the Status Code is equal to the optional "errorCode" given in 'data.json'
                if error_code == r.status_code:
                    query_status = QueryStatus.AVAILABLE
                # Checks if the status code of the response is 2XX
                elif not r.status_code >= 300 or r.status_code < 200:
                    query_status = QueryStatus.CLAIMED
                else:
                    query_status = QueryStatus.AVAILABLE
            elif error_type == "response_url":
                # For this detection method, we have turned off the redirect.
                # So, there is no need to check the response URL: it will always
                # match the request.  Instead, we will ensure that the response
                # code indicates that the request was successful (i.e. no 404, or
                # forward to some odd redirect).
                # print(r.status_code)

                ####
                #
                ###
                if 200 <= r.status_code < 300:
                    query_status = QueryStatus.CLAIMED
                else:
                    query_status = QueryStatus.AVAILABLE
            else:
                # It should be impossible to ever get here...
                raise ValueError(f"Unknown Error Type '{error_type}' for "
                                f"site '{social_network}'")
            # Notify caller about results of query.
            result = QueryResult(username=username,
                                site_name=social_network,
                                site_url_user=url,
                                status=query_status,
                                query_time=response_time,
                                context=error_context)
            

            query_notify.update(result)
            # Checking Claimed from response
            # if result.isclaimed():
            #     profile_url.append(results_site.get("url_user"))
            # else:
            #     continue
            # Save status of request
            # print(result,results_site.get("url_user"))

            results_site["status"] = result
            # if result == QueryStatus.CLAIMED:
            # profile_url.append({username, results_site.get("url_user")})
            # profile_url.append(results_site.get("url_user"))
            # Save results from request
            results_site["http_status"] = http_status
            results_site["response_text"] = response_text

            # Add this site's results into final dictionary with all of the other results.
            results_total[social_network] = results_site

        profile_url = []

        for site in results_total:
            print(results_total[site]["status"].status)
            if results_total[site]["status"].status != QueryStatus.CLAIMED:
                continue
            # print(results_total[site]["url_main"])
            # print(results_total[site]["url_user"])
            profile_url.append(results_total[site]["url_user"])
        # return results_total
        return profile_url

    def handle_find_profile_(self,username):
        result = self.find_profile(username)
        self.result_url_list.append(result) 
        print(len(self.result_url_list))
        # print(self.result_url_list)

        # if len(self.result_url_list) == len(self.username_list):
        if len(self.result_url_list) == len(self.username_list):
            # All results have been collected, set the event
            self.event.set()

    def handle_find_profile(self,username):
        result = self.find_profile(username)
        # self.result_url_list.append(result) 
        return result
    
    def multiple_search(self):
        print('max_workers 20')
        max_workers = 30  # Adjust this value as per your requirements
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit each username to the executor as a separate task
            # The executor will automatically schedule and run the tasks in parallel
            futures = [executor.submit(self.handle_find_profile, username) for username in self.username_list]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
        
        # Retrieve results from completed tasks
        for future in futures:
            result = future.result()  # Get the result of each task
            self.result_url_list.append(result)

        print(self.result_url_list)
        print("Ending Request")
        return self.result_url_list

    def multiple_search_(self):
        print("--->multiple search")
        self.result_url_list = []
        # Create and start threads for each request
        print("---> Create threading")
        start_time = time.time()
        threads = []
        # for username in self.username_list[:30]:
        for username in self.username_list:
            thread = threading.Thread(target=self.handle_find_profile, args=(username,))
            thread.start()
            threads.append(thread)

        print("---> Waiting")
        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print("---> Result Returing")

        # Wait until all results are collected
        self.event.wait()

        print("---> Result")
        # Process the collected results
        # You can send them to the frontend or perform any other operations
        # for profile_url in self.result_url_list:
            # Process each result here
            # print(profile_url)

        # for username in self.username_list:
        #     sub_result = self.find_profile(username)
        #     result.extend(sub_result)
        response_time = time.time() - start_time
        # print(self.result_url_list)
        print(f"Pairing time: {response_time} seconds")
        return self.result_url_list



