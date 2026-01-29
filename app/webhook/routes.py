from flask import Blueprint, request, jsonify, current_app
from app.models import WebhookEvent
from app.webhook.parser import GitHubWebhookParser

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get('X-GitHub-Event')
    delivery_id = request.headers.get('X-GitHub-Delivery')
    signature = request.headers.get('X-Hub-Signature-256')

    webhook_secret = current_app.config.get('GITHUB_WEBHOOK_SECRET', '')

    payload = request.json
    if not payload:
        return jsonify({'error': 'Invalid payload'}), 400

    if WebhookEvent.find_by_request_id(delivery_id):
        return jsonify({
            'message': 'Event already processed',
            'request_id': delivery_id
        }), 200

    try:
        parsed_data = None

        if event_type == 'push':
            parsed_data = GitHubWebhookParser.parse_push_event(payload)

        elif event_type == 'pull_request':
            if GitHubWebhookParser.is_merge_event(payload):
                parsed_data = GitHubWebhookParser.parse_merge_event(payload)
            else:
                parsed_data = GitHubWebhookParser.parse_pull_request_event(payload)

        else:
            return jsonify({
                'message': f'Event type "{event_type}" not supported'
            }), 200

        if not parsed_data:
            return jsonify({'error': 'Failed to parse event'}), 400

        WebhookEvent.create(
            request_id=delivery_id,
            author=parsed_data['author'],
            action=parsed_data['action'],
            from_branch=parsed_data['from_branch'],
            to_branch=parsed_data['to_branch'],
            timestamp=parsed_data['timestamp']
        )

        return jsonify({
            'message': 'Webhook received and stored successfully',
            'event_type': event_type,
            'action': parsed_data['action'],
            'request_id': delivery_id
        }), 201

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
