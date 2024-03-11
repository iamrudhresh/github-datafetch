import requests
from datetime import datetime, timedelta

# Configuration
username = ''
token = ''

# Headers for authentication and to use the search API for commits
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
}

# GitHub API endpoints
user_url = f'https://api.github.com/users/{username}'

def fetch_user_details():
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching user details: {response.status_code}")
        return None

def fetch_repos(repo_url):
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repositories: {response.status_code}")
        return []

def fetch_commit_count(username, headers):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = f'{start_date.strftime("%Y-%m-%d")}..{end_date.strftime("%Y-%m-%d")}'
    commit_search_url = f'https://api.github.com/search/commits?q=author:{username}+committer-date:{date_range}'
    headers.update({'Accept': 'application/vnd.github.cloak-preview'})
    response = requests.get(commit_search_url, headers=headers)
    if response.status_code == 200:
        return response.json()['total_count']
    else:
        print(f"Error fetching commit count: {response.status_code}")
        return 0

def print_user_details(user_details, repos):
    print(f"Username: {user_details['login']}")
    print(f"Display Name: {user_details.get('name', 'No name')}")
    print(f"Number of Public Repositories: {user_details['public_repos']}")
    print(f"Number of Followers: {user_details['followers']}")
    print(f"Number of Users Following: {user_details['following']}")
    print(f"Starred Repositories: {user_details['starred_url']}")
    print(f"Contribution Data: {fetch_commit_count(username, headers)}")
    print(f"Last Active Date: {user_details['updated_at']}")

    print("Repositories:")
    for repo in repos:
        print(f"- Repository Name: {repo['name']}")
        print(f"  Programming Language: {repo['language']}")
        print(f"  Forks Count: {repo['forks_count']}")
        print(f"  Stars Count: {repo['stargazers_count']}")
        print(f"  Watchers Count: {repo['watchers_count']}")
        print()

# Main script execution
user_details = fetch_user_details()
if user_details:
    repos = fetch_repos(user_details['repos_url'])
    print_user_details(user_details, repos)
else:
    print("Failed to retrieve user details.")

