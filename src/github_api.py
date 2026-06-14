import requests

url = "https://api.github.com/users/microsoft/repos"

response = requests.get(url)

print("Status Code:", response.status_code)

data = response.json()

print(type(data))
print("Number of repositories:", len(data))
print(data[0].keys())