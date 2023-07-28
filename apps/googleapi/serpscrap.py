import json
import os
import time
import logging
from apps.googleapi.actor import Actor
from apps.ugen.generator import UserNameGenerator

class Serpscrap():
    def __init__(self, query, *args, **kwargs):
        self.query:str = query


    def scrap_google_search_result(self,query,maxPagesPerQuery=50,resultsPerPage=100,maxConcurrency=50):
        """Scrap Google Search Result per query"""
        # Prepare the Actor input
        run_input = {
            "queries": query,
            "maxPagesPerQuery": maxPagesPerQuery,
            "resultsPerPage": resultsPerPage,
            "mobileResults": False,
            "countryCode": "",
            "languageCode": "",
            "maxConcurrency": maxConcurrency,
            "saveHtml": False,
            "saveHtmlToKeyValueStore": False,
            "includeUnfilteredResults": False,
            "customDataFunction": """async ({ input, $, request, response, html }) => {
        return {
            pageTitle: $('title').text(),
        };
        };""",
        }

        gserp_actor = Actor("google-search-scraper",run_input)
        return gserp_actor.run_actor()

    def scrap_insta_offloading(self,username_list):
        """Scrap Instagram Profile Offloading"""
        run_input = { "usernames": username_list }
        insta_actor = Actor("instagram-profile-scraper",run_input)
        return insta_actor.run_actor()

    def generate_usernames(self):
        # Create a UserNameGenerator instance and generate usernames
        generator = UserNameGenerator(fullname, favorite, birthday, count)
        all_usernames = generator.cycle_usernames()
        return all_usernames

    def integrate_google_search_result(self, all_usernames):
        # Initialize a list to store the search results for each username
        search_results = []

        # Loop through each username and scrape Google search results
        for username in all_usernames:
            search_result = self.scrap_google_search_result(username)
            search_results.append(search_result)

        return search_results