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
import hmac
import hashlib
import json
import os
from base64 import b64encode


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

    api_domain = "api.aidc-ai.com"  # for api purchased on global site
    # api_domain = "cn-api.aidc-ai.com" # 中文站购买的API请使用此域名 (for api purchased on chinese site)

    # Call submit api
    api_name = "/ai/virtual/tryon"
    submit_request = "{\"requestParams\":\"[{\\\"clothesList\\\":[{\\\"imageUrl\\\":\\\"https://ae-pic-a1.aliexpress-media.com/kf/H7588ee37b7674fea814b55f2f516fda1z.jpg\\\",\\\"type\\\":\\\"tops\\\"}],\\\"model\\\":{\\\"base\\\":\\\"General\\\",\\\"gender\\\":\\\"female\\\",\\\"style\\\":\\\"universal_1\\\",\\\"body\\\":\\\"slim\\\"},\\\"viewType\\\":\\\"mixed\\\",\\\"inputQualityDetect\\\":0,\\\"generateCount\\\":4}]\"}"
    submit_result = invoke_api(access_key_name, access_key_secret, api_name, api_domain, submit_request)

    submit_result_json = json.loads(submit_result)
    task_id = submit_result_json.get("data", {}).get("result", {}).get("taskId")

    # Query task status
    query_api_name = "/ai/virtual/tryon-results"
    query_request = json.dumps({"task_id": task_id})
    query_result = None
    while True:
        try:
            query_result = invoke_api(access_key_name, access_key_secret, query_api_name, api_domain, query_request)
            query_result_json = json.loads(query_result)
            task_status = query_result_json.get("data", {}).get("taskStatus")
            if task_status == "finished":
                break
            time.sleep(1)
        except KeyboardInterrupt:
            break

    # Final result
    print(query_result)


