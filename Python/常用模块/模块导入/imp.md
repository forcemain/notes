

----

* [模块简介](#模块简介)
* [属性方法](#属性方法)
* [实战练习](#实战练习)

----

# 模块简介

> 内置模块,默认提供import语句实现,内部依赖importlib,从Python3.4已废弃,相关方法已迁移至importlib

# 属性方法

| 属性                      | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| find_module(name, [path]) | path未指定则从sys.path查找name,否则从path查找name,path通常为module_obj.\_\_path\_\_,如果未找到抛出ImportError异常 |



# 实战练习

* 查询django.contrib.sessions包下是否包含middleware模块 ?

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import imp
import importlib


def has_module(package, name):
    # 尝试导入导入字符串表示的包
    try:
        pkg_path = importlib.import_module(package).__path__
    except AttributeError:
        return False

    # 在模块所在的路径下查找指定模块
    try:
        imp.find_module(name, pkg_path)
    except ImportError:
        return False

    return True


if __name__ == '__main__':
    print has_module('django.contrib.sessions', 'middleware')
```

