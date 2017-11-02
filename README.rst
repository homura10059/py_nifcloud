py_nifcloud
================

Description
-----------

python から NifCloud の REST API を実行するための sdk です


Requirements
------------

このプロジェクトを実行するには以下が必要です:

* `python`_ 3.4.+

Install
-------

::

    pip install py-nifcloud

Preparation
-----------

config file
~~~~~~~~~~~


ACCESS_KEY_ID と SECRET_ACCESS_KEY を含んだconfigファイルを準備してください (デフォルト:  ~/.nifcloud.yml)

::

    ACCESS_KEY_ID: 'your access key'
    SECRET_ACCESS_KEY: 'your secret access key'


environment
~~~~~~~~~~~

ACCESS_KEY_ID と SECRET_ACCESS_KEY を環境変数に設定して準備することもできます
config file より優先されます

::


    export ACCESS_KEY_ID="your access key"
    export SECRET_ACCESS_KEY="your secret access key"


Usage
-----

NifCloudClient
~~~~~~~~~~~~~~

::

    from py_nifcloud.nifcloud_client import NifCloudClient

    client = NifCloudClient(service_name="computing", region_name="jp-east-1", base_path="api",)
    params = {
        'Action': 'DescribeRegions',
    }

    response = client.request(method="GET", query=params)

ComputingClient
~~~~~~~~~~~~~~~

::

    from py_nifcloud.computing_client import ComputingClient

    client = ComputingClient(region_name="jp-east-1")
    params = {
        'Action': 'DescribeRegions',
    }

    response = client.request(method="GET", query=params)

Contributing
------------

PR歓迎


Support and Migration
---------------------

特に無し

License
-------

`MIT License`_

.. _python: https://www.python.org
.. _MIT License: http://petitviolet.mit-license.org/