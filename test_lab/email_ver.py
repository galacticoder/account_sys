import requests
import json

email = "xivesa7195@cubene.com"
api_key = "d2cc1e7dc7c64f78b66ed5b843cc5689"

url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx status codes)

    result_dict = response.json()
    print(result_dict)
    
    if result_dict.get('is_temporary'):
        print(f"The email {email} is temporary.")
    else:
        print(f"The email {email} is not temporary.")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
