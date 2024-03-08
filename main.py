import requests

def fetch_user_details(username, access_token):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user = response.json()
        return {
            "Name": user['name'],
            "Username": user['login'],
            "Repo Count": user['public_repos'],
            "Followers": user['followers'],
            "Following": user['following']
        }
    else:
        return None

# Example usage
access_token = ''
username = ''
user_details = fetch_user_details(username, access_token)
if user_details:
    print(user_details)
else:
    print("Failed to retrieve user details")
