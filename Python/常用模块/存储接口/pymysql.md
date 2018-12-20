# 模块简介

> 第三方模块,提供标准MySQL数据库应用编程接口,同时支持Python2和Python3,而且可伪装为MySQLdb

# 快速部署

```bash
pip install PyMySQL
```


# 常规操作

> 由于PyMySQL和MySQLdb提供几乎相同的接口,此处不再重复说明

# 实战练习

* 在Django项目中如何使用PyMySQL代替MySQL-python作为存储引擎接口?

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com

import pymysql


pymysql.install_as_MySQLdb()

# 此文件可放在站点的__init__.py初始化文件中即可
```

