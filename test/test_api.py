#!/usr/bin/env python3
import requests

# Replace with your actual access token
access_token = "auth12345678"

# Construct the request headers with the Authorization header
headers = {"Authorization": f"{access_token}"}

# Make the API request
response = requests.get("https://dev-api.tastingswithtay.com/content", headers=headers)
print(response.text)
