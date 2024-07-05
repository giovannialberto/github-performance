import requests

class GitHubManager:
    def __init__(self, org_name, repo_name, token):
        self.org_name = org_name
        self.repo_name = repo_name
        self.api_url = f'https://api.github.com/repos/{org_name}/{repo_name}'
        self.headers = {
            'Authorization': f'token {token}'
        }

    def fetch_active_branches(self):
        response = requests.get(f'{self.api_url}/branches', headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch branches: {response.status_code} - {response.text}")
            return []
        return response.json()

    def fetch_branch_details(self, branch_name):
        response = requests.get(f'{self.api_url}/commits/{branch_name}', headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch branch details for {branch_name}: {response.status_code} - {response.text}")
            return None
        return response.json()

    def fetch_pull_requests(self, branch_name):
        response = requests.get(f'{self.api_url}/pulls?state=all&head={self.org_name}:{branch_name}', headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to fetch pull requests for {branch_name}: {response.status_code} - {response.text}")
            return []
        return response.json()
    