[English](./README.md) | 简体中文

<p align="center">

<h1 align="center">Aidge API Python 示例</h1>

Aidge API Python 示例为您提供了示例代码，用于访问包括文本翻译在内的Aidge API。

## 环境要求

- 要运行示例，您必须拥有 Aidge API 帐户以及 `API key name` 和 `API key secret`。您可以在 Aidge 管理后台上创建并查看您的 API key信息。您可以联系您的服务
- 要使用Aidge API 示例访问产品的 API，您必须先在 [Aidge 控制台](https://www.aidge.com) 上激活该产品。
- Aidge API 示例需要 JDK 1.8 或更高版本。

## 快速使用

以下这个代码示例向您展示了访问Aidge API的核心代码。

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

> 出于安全原因，我们不建议在源代码中硬编码凭据信息。您应该从外部配置或环境变量访问凭据。

## Changelog

每个版本的详细更改都记录在 [release notes](./ChangeLog.txt).


## References

- [Aidge官方网站](https://www.aidge.com/)

## License

This project is licensed under [Apache License Version 2](./LICENSE-2.0.txt) (SPDX-License-identifier: Apache-2.0).
