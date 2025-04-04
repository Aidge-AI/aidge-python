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


def invoke_api(api_name, data):
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
    response = requests.post(url, data=data, headers=headers)

    # FAQ:https://app.gitbook.com/o/pBUcuyAewroKoYr3CeVm/s/cXGtrD26wbOKouIXD83g/getting-started/faq
    # FAQ(中文/Simple Chinese):https://aidge.yuque.com/org-wiki-aidge-bzb63a/brbggt/ny2tgih89utg1aha
    print(response.text)
    return response.text


if __name__ == '__main__':
    # Call api
    api_name = "/ai/hand-foot/repair"

    # Constructor request Parameters
    paramJson = [
        {
            "area": "hand",
            "imageUrl": "http://aibz-aigc-record.oss-ap-southeast-1.aliyuncs.com/skin_repaint_result%2Faa0d0023ea46464ebff4cda31ffcc312_20250124144712.png?OSSAccessKeyId=LTAI5tAGoBnm5eYsnZ5E1zMr&Expires=2737701232&Signature=kFfey2VgD%2FCxUUqHgdMJwdQyeFQ%3D",
            "imgNum": "1",
            "requestBizId": ""
        }
    ]

    param = {
        "paramJson": json.dumps(paramJson)
    }

    # Convert parameters to JSON string
    request = json.dumps(param)

    submit_result = invoke_api(api_name, request)

    submit_result_json = json.loads(submit_result)
    task_id = submit_result_json.get("data", {}).get("result", {}).get("taskId")

    # Query task status
    query_api_name = "/ai/hand-foot/repair-results"
    query_request = json.dumps({"taskId": task_id})
    query_result = None
    while True:
        try:
            query_result = invoke_api(query_api_name, query_request)
            query_result_json = json.loads(query_result)
            task_status = query_result_json.get("data", {}).get("taskStatus")
            if task_status == "finished":
                break
            time.sleep(5)
        except KeyboardInterrupt:
            break

    # Final result
    print(query_result)

    # Add a small delay between requests to avoid overwhelming the API
    time.sleep(1)
