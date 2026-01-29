from flask import Blueprint, jsonify
from app.models import WebhookEvent
from bson import ObjectId

# Create API blueprint with /api prefix
api = Blueprint('API', __name__, url_prefix='/api')


def serialize_event(event):
    """
    Serialize a MongoDB document for JSON response.
    Converts ObjectId to string.
    
    Args:
        event (dict): MongoDB document
    
    Returns:
        dict: Serialized document
    """
    if event and '_id' in event:
        event['_id'] = str(event['_id'])
    return event


@api.route('/events', methods=['GET'])
def get_events():
    """
    GET /api/events
    
    Retrieve all webhook events from MongoDB, sorted by timestamp (newest first).
    
    Returns:
        JSON response containing list of events
    """
    try:
        # Fetch all events from database
        events = WebhookEvent.find_all(limit=100)
        
        # Serialize events (convert ObjectId to string)
        serialized_events = [serialize_event(event) for event in events]
        
        return jsonify({
            'success': True,
            'count': len(serialized_events),
            'events': serialized_events
        }), 200
    
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch events',
            'details': str(e)
        }), 500


@api.route('/events/<request_id>', methods=['GET'])
def get_event_by_id(request_id):
    """
    GET /api/events/<request_id>
    
    Retrieve a specific webhook event by its request_id (GitHub delivery ID).
    
    Args:
        request_id (str): GitHub delivery ID
    
    Returns:
        JSON response containing the event
    """
    try:
        event = WebhookEvent.find_by_request_id(request_id)
        
        if not event:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404
        
        return jsonify({
            'success': True,
            'event': serialize_event(event)
        }), 200
    
    except Exception as e:
        print(f"Error fetching event: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch event',
            'details': str(e)
        }), 500