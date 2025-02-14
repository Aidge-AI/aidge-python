"""
Copyright (C) 2024 NEURALNETICS PTE. LTD.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
import time
import hashlib
import hmac
import os


def invoke_api(access_key_name, access_key_secret, api_name, api_domain, data):
    timestamp = str(int(time.time() * 1000))

    # Calculate sha256 sign
    sign_string = access_key_secret + timestamp
    sign = hmac.new(access_key_secret.encode('utf-8'), sign_string.encode('utf-8'), hashlib.sha256).hexdigest().upper()

    url = f"https://{api_domain}/rest{api_name}?partner_id=aidge&sign_method=sha256&sign_ver=v2&app_key={access_key_name}&timestamp={timestamp}&sign={sign}"

    # Add "x-iop-trial": "true" for trial
    headers = {
        "Content-Type": "application/json",
        # "x-iop-trial": "true"
    }

    # Http request
    response = requests.post(url, data=data, headers=headers)
    print(response.text)
    return response.text


if __name__ == '__main__':
    # Your personal data. In this example, we get data from os env
    access_key_name = os.environ.get("accessKey")  # e.g. "512345"
    access_key_secret = os.environ.get("secret")

    api_domain = "api.aidc-ai.com"  # cn-api.aidc-ai.com for cn region

    # Call api
    api_name = "/ai/image/cropping"
    submit_request = "{\"imageBase64\":\"\",\"targetHeight\":\"200\",\"imageUrl\":\"https://ae01.alicdn.com/kf/S99cb7e78ba2b46cc9134b87c323bb617x.png\",\"targetWidth\":\"200\"}"
    submit_result = invoke_api(access_key_name, access_key_secret, api_name, api_domain, submit_request)

    # Add a small delay between requests to avoid overwhelming the API
    time.sleep(1)
