# 模块简介

> 内置模块,默认提供import语句底层实现,包括动态导入,导入检查等特性

# 属性方法

| 属性                                        | 说明                                                         |
| ------------------------------------------- | ------------------------------------------------------------ |
| importlib.import_module(name, package=None) | 字符串的形式动态导入模块,当name为.开头的相对导入字符串,package必须存在 |

# 源码分析

* 定义: django.utils.module_loading

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

* 使用: django.core.handlers.base

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

* 如何实现项目中模块和包的自动导入 ?
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
    # 尝试获取包所在路径
    try:
        m = importlib.import_module(package)
        path = m.__path__
    except AttributeError:
        return
    # 尝试查找模块是否存在
    try:
        imp.find_module(name, path)
    except ImportError:
        return
    # 真正导入
    dotted_path = '{0}.{1}'.format(package, name)
    importlib.import_module(dotted_path)


def autodiscovery_modules(package, entrance):
    cur_dir = os.path.dirname(entrance)
    pyfiles = os.listdir(cur_dir)
    # 遍历entrance所在目录下的模块或包
    for f_name in pyfiles:
        f_path = os.path.join(cur_dir, f_name)
        if os.path.isfile(f_path):
            if not f_name.endswith('.py'):
                continue
            # 如果为模块则获取模块名    
            m_name, _, _ = f_name.rpartition('.')
        else:
            # 如果为目录则假设为包名
            m_name = f_name
        # 尝试导入
        import_sub_module(package, m_name)
```

> mysite/polls/models.py

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ._models import *
```

> mysite/polls/_models/\_\_init\_\_.py

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from functools import partial
from utils.module_loading import autodiscovery_modules


# 需要注意是的要实现无限递归自动导入需要将如下代码加入需要自动导入的包的__init__.py文件
autodiscovery_modules(__name__, __file__)


autodiscovery = partial(autodiscovery_modules,__name__, __file__)
```

