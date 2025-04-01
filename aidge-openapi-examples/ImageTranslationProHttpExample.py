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


class ApiConfig:
    """
    API configuration class
    """
    # The name and secret of your api key. e.g. 512345 and S4etzZ73nF08vOXVhk3wZjIaLSHw0123
    access_key_name = "your api key name"
    access_key_secret = "your api key secret"

    # The domain of the API.
    # for api purchased on global site. set api_domain to "api.aidc-ai.com"
    # 中文站购买的API请使用"cn-api.aidc-ai.com"域名 (for api purchased on chinese site) set api_domain to "cn-api.aidc-ai.com"
    api_domain = "your api domain"

    # We offer trial quota to help you familiarize and test how to use the Aidge API in your account
    # To use trial quota, please set use_trial_resource to True
    # If you set use_trial_resource to False before you purchase the API
    # You will receive "Sorry, your calling resources have been exhausted........"
    # 我们为您的账号提供一定数量的免费试用额度可以试用任何API。请将use_trial_resource设置为True用于试用。
    # 如设置为False，且您未购买该API，将会收到"Sorry, your calling resources have been exhausted........."的错误提示
    use_trial_resource = False/True


def invoke_api(api_name, data, is_get):
    timestamp = str(int(time.time() * 1000))

    # Calculate sha256 sign
    sign_string = ApiConfig.access_key_secret + timestamp
    sign = hmac.new(ApiConfig.access_key_secret.encode('utf-8'), sign_string.encode('utf-8'),
                    hashlib.sha256).hexdigest().upper()

    url = f"https://{ApiConfig.api_domain}/rest{api_name}?partner_id=aidge&sign_method=sha256&sign_ver=v2&app_key={ApiConfig.access_key_name}&timestamp={timestamp}&sign={sign}"

    # Add "x-iop-trial": "true" for trial
    headers = {
        "Content-Type": "application/json",
        "x-iop-trial": str(ApiConfig.use_trial_resource).lower()
    }

    # Http request
    if is_get:
        response = requests.get(url, params=data, headers=headers)
    else:
        response = requests.post(url, data=data, headers=headers)
    print(response.text)
    return response.text


if __name__ == '__main__':
    # Call submit api
    api_name = "/ai/image/translation_mllm/batch"

    # Constructor request Parameters
    request_params = [
        {
            "imageUrl": "https://img.alicdn.com/imgextra/i1/1955749012/O1CN016P3Jas2GRY7vaevsK_!!1955749012.jpg",
            "sourceLanguage": "zh",
            "targetLanguage": "en"
        },
        {
            "imageUrl": "https://img.alicdn.com/imgextra/i1/1955749012/O1CN016P3Jas2GRY7vaevsK_!!1955749012.jpg",
            "sourceLanguage": "zh",
            "targetLanguage": "ko"
        }
    ]

    # Convert parameters to JSON string
    submit_request = {
        "paramJson": json.dumps(request_params)
    }

    # Convert parameters to JSON string
    submit_request_json = json.dumps(submit_request)

    submit_result = invoke_api(api_name, submit_request_json, False)

    submit_result_json = json.loads(submit_result)
    task_id = submit_result_json.get("data", {}).get("result", {}).get("taskId")

    # Query task status
    query_api_name = "/ai/image/translation_mllm/results"
    query_request = {"taskId": task_id}
    query_result = None
    while True:
        try:
            query_result = invoke_api(query_api_name, query_request, True)
            query_result_json = json.loads(query_result)
            task_status = query_result_json.get("data", {}).get("taskStatus")
            if task_status == "finished":
                break
            time.sleep(5)
        except KeyboardInterrupt:
            break

    # Final result
    print(query_result)


