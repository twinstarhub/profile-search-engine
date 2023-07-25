import json
import os
from apify_client import ApifyClient
API_KEY = os.getenv("APIFY_API_KEY","apify_api_IId4wcbVOnfGV0mN0y9q3V3vV8ppmF2P52yG")

class Actor():
    """Apify Actor runner"""
    def __init__(self,actor_name,run_input):
        self.actor_name:str = actor_name
        self.run_input:object = run_input


    def run_actor(self):
        """Send Request to Run Actor """
        client = ApifyClient(API_KEY)
        run_input = self.run_input
           
        # Run the Actor and wait for it to finish
        try:
           run = client.actor(f"apify/{self.actor_name}").call(run_input=run_input)
        except:
            return None    

        # Fetch and print Actor results from the run's dataset (if there are any)
        actor_result = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if item["#error"]:
                continue
            else:
                actor_result.append(item)

        return actor_result

   