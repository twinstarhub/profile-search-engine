import json
import os
import time
import logging
from apps.googleapi.actor import Actor

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

    