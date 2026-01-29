class GitHubWebhookParser:
    """Parser for GitHub webhook payloads."""

    @staticmethod
    def parse_push_event(payload):
        # Extract author
        author = payload.get('pusher', {}).get('name', 'Unknown')

        action = 'PUSH'
        from_branch = None

        # Extract branch name from ref
        ref = payload.get('ref', '')
        to_branch = ref.replace('refs/heads/', '') if ref.startswith('refs/heads/') else ref

        # Extract commit timestamp
        timestamp = payload.get('head_commit', {}).get('timestamp', '')

        return {
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }

    @staticmethod
    def parse_pull_request_event(payload):
        pull_request = payload.get('pull_request', {})

        author = pull_request.get('user', {}).get('login', 'Unknown')
        action = 'PULL_REQUEST'
        from_branch = pull_request.get('head', {}).get('ref', '')
        to_branch = pull_request.get('base', {}).get('ref', '')
        timestamp = pull_request.get('created_at', '')

        return {
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }

    @staticmethod
    def parse_merge_event(payload):
        pull_request = payload.get('pull_request', {})

        author = pull_request.get('merged_by', {}).get('login', 'Unknown')
        action = 'MERGE'
        from_branch = pull_request.get('head', {}).get('ref', '')
        to_branch = pull_request.get('base', {}).get('ref', '')
        timestamp = pull_request.get('merged_at', '')

        return {
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }

    @staticmethod
    def is_merge_event(payload):
        pull_request = payload.get('pull_request', {})
        return pull_request.get('merged', False) is True
