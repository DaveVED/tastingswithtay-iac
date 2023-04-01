#!/usr/bin/env python3
import requests

# Replace with your actual access token
access_token = "12345678"

# Construct the request headers with the Authorization header
headers = {"Authorization": f"Bearer {access_token}"}

# Make the API request
response = requests.get(
    "https://dev-api.tastingswithtay.com/v1/content", headers=headers
)
print(response.json())
