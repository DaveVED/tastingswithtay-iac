#!/usr/bin/env python3
import requests

# Replace with your actual access token
access_token = "12345678"

# Construct the request headers with the Authorization header
headers = {"Authorization": f"{access_token}"}

# Make the API request
response = requests.get(
    "https://wzaygu7rgf.execute-api.us-east-1.amazonaws.com/v1/content", headers=headers
)
print(response.text)
