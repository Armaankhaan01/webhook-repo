from app.extensions import mongo
from datetime import datetime


class WebhookEvent:
     
    COLLECTION_NAME = 'webhook_events'
    
    @staticmethod
    def create(request_id, author, action, from_branch, to_branch, timestamp):
       
        event_data = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
        
        # Insert into MongoDB
        result = mongo.db[WebhookEvent.COLLECTION_NAME].insert_one(event_data)
        event_data['_id'] = result.inserted_id
        
        return event_data
    
    @staticmethod
    def find_all(limit=50):
       
        events = mongo.db[WebhookEvent.COLLECTION_NAME].find().sort('timestamp', -1).limit(limit)
        return list(events)
    
    @staticmethod
    def find_by_request_id(request_id):
       
        return mongo.db[WebhookEvent.COLLECTION_NAME].find_one({'request_id': request_id})