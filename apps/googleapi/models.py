from apps.mongodb_connector import MongoDBConnector

# Store the searched data into the MongoDB database
def store_search_results(search_results):
    data_to_store = []
    for i, search_result in enumerate(search_results):
        username = all_usernames[i]
        # Convert the search_result to a dictionary before storing it in the database
        search_result_dict = {
            'username': username,
            'search_result': search_result,
        }
        data_to_store.append(search_result_dict)

    # Save the data to MongoDB
    with MongoDBConnector() as connector:
        connector.bulk_upsert('search_data', data_to_store)
