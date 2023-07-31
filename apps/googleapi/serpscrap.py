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
    
     def scrap_youtube(self, query):
        """Scrap YouTube search results"""
        # Assuming you have a method in your ApifyAPI for YouTube scraping
        youtube_search_results = ApifyAPI.scrap_youtube_results(query)
        return youtube_search_results

    def scrap_facebook(self, query):
        """Scrap Facebook search results"""
        # Assuming you have a method in your ApifyAPI for Facebook scraping
        facebook_search_results = ApifyAPI.scrap_facebook_results(query)
        return facebook_search_results

    def scrap_twitter(self, query):
        """Scrap Twitter search results"""
        # Assuming you have a method in your ApifyAPI for Twitter scraping
        twitter_search_results = ApifyAPI.scrap_twitter_results(query)
        return twitter_search_results

    def scrap_tiktok(self, query):
        """Scrap TikTok search results"""
        # Assuming you have a method in your ApifyAPI for TikTok scraping
        tiktok_search_results = ApifyAPI.scrap_tiktok_results(query)
        return tiktok_search_results

    def integrate_all_search_results(self, all_usernames):
        # Initialize a dictionary to store the search results for each username
        all_search_results = {}

        # Loop through each username and scrape search results from all platforms
        for username in all_usernames:
            search_results = {}
            search_results['Google'] = self.scrap_google_search_result(username)
            search_results['Instagram'] = self.scrap_insta_offloading(username)
            search_results['YouTube'] = self.scrap_youtube(username)
            search_results['Facebook'] = self.scrap_facebook(username)
            search_results['Twitter'] = self.scrap_twitter(username)
            search_results['TikTok'] = self.scrap_tiktok(username)

            all_search_results[username] = search_results

        return all_search_results