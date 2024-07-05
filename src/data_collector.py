import requests
import time
from dotenv import load_dotenv
import os
from utils.utils import generate_hash
from database.database import DatabaseManager
from github.github import GitHubManager

# Load environment variables from .env file
load_dotenv()

# GitHub repository details
ORG_NAME = os.getenv('ORG_NAME')
REPOSITORIES = os.getenv('REPOSITORIES').split(',')  # Split the comma-separated string into a list
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

def update_db(db_manager, org_name, repo_name, token):
    github_manager = GitHubManager(org_name, repo_name, token)

    # Fetch details for each active branch
    active_branches = github_manager.fetch_active_branches()
    for branch in active_branches:
        branch_name = branch['name']
        if branch_name != 'main':
            fetch_and_save_active_branch_details(db_manager, github_manager, branch_name, repo_name)

    # Fetch updates for each unmerged branch that might have been deleted
    unmerged_branches = db_manager.fetch_unmerged_branches()
    for branch_name, db_repo_name in unmerged_branches:
        if db_repo_name == repo_name:
            fetch_and_save_deleted_branch_details(db_manager, github_manager, branch_name, repo_name)

def fetch_and_save_active_branch_details(db_manager, github_manager, branch_name, repo_name):
    branch_details = github_manager.fetch_branch_details(branch_name)
    if not branch_details:
        return

    creator = branch_details['commit']['author']['name']
    created_at = branch_details['commit']['author']['date']
    
    pr_opened_at = None
    merged_at = None
    merger = None
    reviewers = []
    
    pulls = github_manager.fetch_pull_requests(branch_name)
    for pull in pulls:
        pr_opened_at = pull['created_at']
        if pull['merged_at']:
            merged_at = pull['merged_at']
            # merger = pull['merged_by']['login'] if pull['merged_by'] else None
            
            reviews_response = requests.get(f'{github_manager.api_url}/pulls/{pull["number"]}/reviews', headers=github_manager.headers)
            if reviews_response.status_code == 200:
                reviews = reviews_response.json()
                reviewers = list(set([review['user']['login'] for review in reviews if review['user']]))
            break
    
    reviewers_str = ','.join(reviewers)
    details_hash = generate_hash(branch_name, repo_name, creator, created_at, pr_opened_at, merger, merged_at, reviewers_str)

    # Fetch the stored hash from the database
    stored_hash = db_manager.fetch_branch_hash(branch_name, repo_name)

    if stored_hash != details_hash:
        db_manager.save_branch_details(branch_name, repo_name, creator, created_at, pr_opened_at, merger, merged_at, reviewers_str, details_hash)

def fetch_and_save_deleted_branch_details(db_manager, github_manager, branch_name, repo_name):
    merged_at = None
    merger = None
    pr_opened_at = None
    reviewers = []

    pulls = github_manager.fetch_pull_requests(branch_name)
    for pull in pulls:
        pr_opened_at = pull['created_at']
        if pull['merged_at']:
            merged_at = pull['merged_at']
            # merger = pull['merged_by']['login'] if pull['merged_by'] else None
            
            reviews_response = requests.get(f'{github_manager.api_url}/pulls/{pull["number"]}/reviews', headers=github_manager.headers)
            if reviews_response.status_code == 200:
                reviews = reviews_response.json()
                reviewers = list(set([review['user']['login'] for review in reviews if review['user']]))
            break
    
    reviewers_str = ','.join(reviewers)
    details_hash = generate_hash(branch_name, repo_name, pr_opened_at, merger, merged_at, reviewers_str)

    # Fetch the stored hash from the database
    stored_hash = db_manager.fetch_branch_hash(branch_name, repo_name)

    if stored_hash != details_hash:
        db_manager.update_branch_details(branch_name, repo_name, pr_opened_at, merger, merged_at, reviewers_str, details_hash)

def main():
    db_manager = DatabaseManager()
    while True:
        for repo_name in REPOSITORIES:
            update_db(db_manager, ORG_NAME, repo_name, GITHUB_TOKEN)
        db_manager.fetch_all_branches()
        time.sleep(3600)  # Run every hour

if __name__ == "__main__":
    main()
