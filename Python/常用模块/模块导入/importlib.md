----

* [模块简介](#模块简介)
* [属性方法](#属性方法)
* [应用场景](#应用场景)
  * [声明位置](#声明位置)
  * [调用位置](#调用位置)
* [实战练习](#实战练习)
* [实战总结](#实战总结)

----

# 模块简介

> 内置模块,默认提供import语句和\_\_import\_\_底层实现,包括动态导入,导入检查等特性

#  属性方法

| 属性                              | 说明                                                         |
| :-------------------------------- | ------------------------------------------------------------ |
| import_module(name, package=None) | dotted_path导入模块,当name为.开头的相对导入字符串,package必须存在 |

# 应用场景

> Django框架中自动加载应用集配置中的中间件.

## 声明位置

> django.utils.module_loading

```python
# 用于导入点连接的导入字符串,例如django.contrib.sessions.middleware.SessionMiddleware
def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        # 首先按.分隔,如上
        # module_path为django.contrib.sessions.middleware
        # class_name为SessionMiddleware
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        # 主要为了兼容Py2和Py3,其实就是调用raise重新抛出了ImportError
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])
    # 调用import_module直接导入点连接module_path返回模块对象
    module = import_module(module_path)

    try:
        # 尝试运行时反省获取模块中名称为class_name的类
        return getattr(module, class_name)
    except AttributeError:
        # 重新抛出异常,依然定义为导入错误ImportError
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])
```

## 调用位置

> django.core.handlers.base

```python
class BaseHandler(object):

    def __init__(self):
        self._request_middleware = None
        self._view_middleware = None
        self._template_response_middleware = None
        self._response_middleware = None
        self._exception_middleware = None
        self._middleware_chain = None
    # 加载配置中的中间件
    def load_middleware(self):
        """
        Populate middleware lists from settings.MIDDLEWARE (or the deprecated
        MIDDLEWARE_CLASSES).

        Must be called after the environment is fixed (see __call__ in subclasses).
        """
        self._request_middleware = []
        self._view_middleware = []
        self._template_response_middleware = []
        self._response_middleware = []
        self._exception_middleware = []

        if settings.MIDDLEWARE is None:
            warnings.warn(
                "Old-style middleware using settings.MIDDLEWARE_CLASSES is "
                "deprecated. Update your middleware and use settings.MIDDLEWARE "
                "instead.", RemovedInDjango20Warning
            )
            handler = convert_exception_to_response(self._legacy_get_response)
            for middleware_path in settings.MIDDLEWARE_CLASSES:
                # 尝试导入settings.MIDDLEWARE_CLASSES中定义的中间件
                mw_class = import_string(middleware_path)
                try:
                    mw_instance = mw_class()
                except MiddlewareNotUsed as exc:
                    if settings.DEBUG:
                        if six.text_type(exc):
                            logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                        else:
                            logger.debug('MiddlewareNotUsed: %r', middleware_path)
                    continue

                if hasattr(mw_instance, 'process_request'):
                    self._request_middleware.append(mw_instance.process_request)
                if hasattr(mw_instance, 'process_view'):
                    self._view_middleware.append(mw_instance.process_view)
                if hasattr(mw_instance, 'process_template_response'):
                    self._template_response_middleware.insert(0, mw_instance.process_template_response)
                if hasattr(mw_instance, 'process_response'):
                    self._response_middleware.insert(0, mw_instance.process_response)
                if hasattr(mw_instance, 'process_exception'):
                    self._exception_middleware.insert(0, mw_instance.process_exception)
        else:
            handler = convert_exception_to_response(self._get_response)
            for middleware_path in reversed(settings.MIDDLEWARE):
                # 尝试导入settings.MIDDLEWARE中定义的中间件
                middleware = import_string(middleware_path)
                try:
                    mw_instance = middleware(handler)
                except MiddlewareNotUsed as exc:
                    if settings.DEBUG:
                        if six.text_type(exc):
                            logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                        else:
                            logger.debug('MiddlewareNotUsed: %r', middleware_path)
                    continue

                if mw_instance is None:
                    raise ImproperlyConfigured(
                        'Middleware factory %s returned None.' % middleware_path
                    )

                if hasattr(mw_instance, 'process_view'):
                    self._view_middleware.insert(0, mw_instance.process_view)
                if hasattr(mw_instance, 'process_template_response'):
                    self._template_response_middleware.append(mw_instance.process_template_response)
                if hasattr(mw_instance, 'process_exception'):
                    self._exception_middleware.append(mw_instance.process_exception)

                handler = convert_exception_to_response(mw_instance)

        # We only assign to this when initialization is complete as it is used
        # as a flag for initialization being complete.
        self._middleware_chain = handler
```



# 实战练习

* 如何实现项目中模块和包的递归自动导入 ?
  * 思考
    * 怎么配合元类实现自动注册功能 ?
    * 尝试模块化Django应用的后台,模型,视图,测试并实现自动导入 ?

> mysite/utils/module_loading.py

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import imp
import importlib


def import_sub_module(package, name):
    # 第三方包默认都存在__path__,如果不存在则说明传参错误
    try:
        m = importlib.import_module(package)
        path = m.__path__
    except AttributeError:
        return
    # 从包路径查找模块或包
    try:
        imp.find_module(name, path)
    except ImportError:
        return
    # 按照绝对路径导入字符串导入
    dotted_path = '{0}.{1}'.format(package, name)
    return importlib.import_module(dotted_path)


def autodiscovery_modules(package, entrance):
    # 记录导入的模块对象
    modules = []

    cur_dir = os.path.dirname(entrance)
    pyfiles = os.listdir(cur_dir)
    # 遍历当前目录尝试导入目录下模块和包
    for f_name in pyfiles:
        f_path = os.path.join(cur_dir, f_name)
        if os.path.isfile(f_path):
            if not f_name.endswith('.py'):
                continue
            m_name, _, _ = f_name.rpartition('.')
            if m_name == '__init__':
                continue
        else:
            # 假设目录就是Python包
            m_name = f_name
        # 尝试导入
        m = import_sub_module(package, m_name)
        if not m:
            continue
        modules.append(m)
    return modules
```

> mysite/polls/models/\_\_init\_\_.py

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from functools import partial
from utils.module_loading import autodiscovery_modules

# 当尝试导入此包下的模块或包时就会自动预导入,由于Django默认模型使用元类注册,所以导入时就会自动到基类注册,所以makemigrations不受影响
modules = autodiscovery_modules(__name__, __file__)


# 注入全局变量,并不推荐,只是模拟from x import *,让Django模型和原来一样类似from polls.models import Question, Choice一样正常调用
g_data = {}
map(lambda m: g_data.update(m.__dict__), modules)
globals().update(g_data)

autodiscovery = partial(autodiscovery_modules,__name__, __file__)
```

# 实战总结

* 自动导入通常配合元类注册才能发挥其优势,如上由于Django框架的模型基于元类注册所以才能完美配合自动导入使用

