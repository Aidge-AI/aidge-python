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

if __name__ == '__main__':
    # your personal data
    accessKeyName = "your access key name"  # e.g. 512345
    accessKeySecret = "your access key secret"
    apiName = "api name"  # e.g. ai/text/translation/and/polishment
    apiDomain = "api domain"  # e.g. api.aidc-ai.com or cn-api.aidc-ai.com
    data = "{your api request params}"

    # basic url
    url = "https://[api domain]/rest/[api name]?partner_id=aidge&sign_method=sha256&sign_ver=v2&app_key=[you access key name]&timestamp=[timestamp]&sign=[HmacSHA256 sign]"

    # timestamp
    timestamp = str(int(time.time() * 1000))

    # calculate sha256 sign
    sign = str(hmac.new(accessKeySecret.encode("utf-8"), (accessKeySecret + timestamp).encode("utf-8"),
                        digestmod=hashlib.sha256).hexdigest()).upper()

    # replace the holder with real value
    url = url.replace("[api domain]", apiDomain)
    url = url.replace("[api name]", apiName)
    url = url.replace("[you access key name]", accessKeyName)
    url = url.replace("[timestamp]", timestamp)
    url = url.replace("[HmacSHA256 sign]", sign)

    # add "x-iop-trial": "true" for trial
    headers = {"Content-Type": "application/json"}

    # do http call
    response = requests.post(url, headers=headers, data=data)
    print(response.text)