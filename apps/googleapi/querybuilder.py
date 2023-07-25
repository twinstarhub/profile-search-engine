import time
import os
import json

dir_name = os.path.dirname(os.path.abspath(__file__))
working_dir = os.path.dirname(dir_name)
querytemplist = os.path.join(working_dir, 'googleapi/resources/querytemplate.json')
with open(querytemplist, "r") as file:
    QUERY_TEMP_LIST = json.load(file)

class QueryBuilder():
    """Query Builder by User Input"""
    def __init__(self,fullname, favostr, location):
        pass

    def createquery(self):
        querylist = []
        
        pass
