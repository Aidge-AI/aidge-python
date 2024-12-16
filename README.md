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

    headers = {"Content-Type": "application/json"}

    # do http call
    response = requests.post(url, headers=headers, data=data)
    print(response.text)

```

> For security reason, we don't recommend to hard code credentials information in source code. You should access
> credentials from external configurations or environment variables.

## Changelog

Detailed changes for each release are documented in the [release notes](./ChangeLog.txt).


## References

- [Aidge Home Page](https://www.aidge.com/)

## License

This project is licensed under [Apache License Version 2](./LICENSE-2.0.txt) (SPDX-License-identifier: Apache-2.0).
