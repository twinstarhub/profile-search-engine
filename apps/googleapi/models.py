from flask_sqlalchemy import SQLAlchemy
from apps import db
import json

# Define the model
class SearchData(db.Model):
    # Specify the table name (optional - SQLAlchemy will create a default name if not specified)
    __tablename__ = 'search_data'

    # Define the columns of the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    search_result = db.Column(db.Text, nullable=True)
    # Add more columns as needed to store additional data

    def __repr__(self):
        return f"<SearchData id={self.id} username={self.username}>"

# Store the searched data into the database
def store_search_results(search_results):
    for i, search_result in enumerate(search_results):
        username = all_usernames[i]
        # Convert the search_result to JSON string before storing it in the database
        search_result_json = json.dumps(search_result)

        # Create a new SearchData object and add it to the database
        search_data = SearchData(username=username, search_result=search_result_json)
        db.session.add(search_data)

    # Commit the changes to the database
    db.session.commit()