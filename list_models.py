import requests
api_key = "AIzaSyBZidAshUk9cB3DuwY3kP2mPfnC4QXapj8"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)
print(response.text)
