py_nifcloud
================

Table of Contents
-----------------

* [Description](#description)
* [Requirements](#requirements)
* [Install](#install)
* [Usage](#usage)
* [Contributing](#contributing)
* [Support and Migration](#support-and-migration)
* [License](#license)

Description
-----------

python から NifCloud の REST API を実行するための sdk です


Requirements
------------

このプロジェクトを実行するには以下が必要です:

* [python][python] 3.4.+

Install
-------

* [ ] TODO: PyPI へ登録

Usage
-----

### preparation

ACCESS_KEY_ID と SECRET_ACCESS_KEY を含んだconfigファイルを準備してください (デフォルト:  ~/.nifcloud.yml)

```yaml
ACCESS_KEY_ID: 'your access key'
SECRET_ACCESS_KEY: 'your secret access key'
```

### NifCloudClient
```python
client = NifCloudClient(service_name="computing", region_name="jp-east-1", base_path="api",)
params = {
    'Action': 'DescribeRegions',
}

response = client.request(method="GET", query=params)
```

### ComputingClient

```python
client = ComputingClient(region_name="jp-east-1")
params = {
    'Action': 'DescribeRegions',
}

response = client.request(method="GET", query=params)
```

Contributing
------------

PR歓迎


Support and Migration
---------------------

特に無し

License
-------

[MIT License](http://petitviolet.mit-license.org/)

[python]: https://www.python.org