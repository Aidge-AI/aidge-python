English | [简体中文](./README-CN.md)

<p align="center">

<h1 align="center">Aidge API Examples for Python</h1>

The Aidge API examples for Python provide you  to access Aidge services such as Text Translation.

## Requirements

- To run the examples, you must have an Aidge API account as well as an `API Key Name` and an `API Key Secret`. Create and view your AccessKey on Aidge dashboard.
- To use the Aidge API examples for Python to access the APIs of a product, you must first activate the product on the [Aidge console](https://www.aidge.com) if required.

## Quick Examples

The following code example:

```python
import requests
import time
import hashlib
import hmac

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
    api_domain = "api.aidc-ai.com"
    # api_domain = "cn-api.aidc-ai.com"

    # We offer trial quota to help you familiarize and test how to use the Aidge API in your account
    # To use trial quota, please set use_trial_resource to True
    # If you set use_trial_resource to False before you purchase the API
    # You will receive "Sorry, your calling resources have been exhausted........"
    # 我们为您的账号提供一定数量的免费试用额度可以试用任何API。请将use_trial_resource设置为True用于试用。
    # 如设置为False，且您未购买该API，将会收到"Sorry, your calling resources have been exhausted........."的错误提示
    use_trial_resource = False
    # use_trial_resource = True

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
    print(response.text)
    return response.text

if __name__ == '__main__':
    # your personal data
    api_name = "api name"  # e.g. ai/text/translation/and/polishment
    data = "{your api request params}"

    result = invoke_api(api_name, data)

    # Add a small delay between requests to avoid overwhelming the API
    time.sleep(1)

```

> For security reason, we don't recommend to hard code credentials information in source code. You should access
> credentials from external configurations or environment variables.

## Changelog

Detailed changes for each release are documented in the [release notes](./ChangeLog.txt).


## References

- [Aidge Home Page](https://www.aidge.com/)

## License

This project is licensed under [Apache License Version 2](./LICENSE-2.0.txt) (SPDX-License-identifier: Apache-2.0).
