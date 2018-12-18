----

* [模块由来](#模块由来)
* [模块简介](#模块简介)
* [实现方式](#实现方式)
  * [基于类的实现](#基于类的实现)
  * [基于生成器+contextlib.contextmanager装饰器实现](#基于生成器+contextlib.contextmanager装饰器实现)
* [属性方法](#属性方法)

----

# 模块由来

> 通常希望在某语句块儿运行直至结束保持某种状态(上下文),精确的分配和释放资源.

# 模块简介

> 内置模块,简化上下文管理器的声明来支持with语句

# 实现方式

> 上下文管理器的实现方式通常可以基于类的\_\_exit\_\_和\_\_enter\_\_实现,也可以基于yield生成器和contextlib.contextmanager装饰器实现

## 基于类的实现

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


class FileWithContextManager(object):
    def __init__(self, *args, **kwargs):
        self.fobj = file(*args, **kwargs)

    def __enter__(self):
        return self.fobj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.fobj.closed: self.fobj.close()


if __name__ == '__main__':
    with FileWithContextManager('/etc/passwd') as f:
        for line in f:
            print line,
```

* with语句首先暂存了FileWithContextManager的\_\_exit\_\_方法,然后调用\_\_enter\_\_返回给with通过as赋值给变量f,当with内部语句块儿执行完毕时调用之前暂存的\_\_exit\_\_方法
* 如果语句块儿内异常则会将exc_type, exc_val, exc_tb传递给\_\_exit\_\_方法,但需要注意的是_\_exit\_\_如果返回True则会优雅忽略,否则会被重新抛出

## 基于生成器+contextlib.contextmanager装饰器实现

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from contextlib import contextmanager


@contextmanager
def open_file(*args, **kwargs):
    try:
        f = open(*args, **kwargs)
        yield f
    except Exception as e:
        f = None
        raise e
    finally:
        if f and not f.closed: f.close()


if __name__ == '__main__':
    with open_file('/etc/passwd') as f:
        for line in f:
            print line,
```

* contextmanager其实内部封装了open\_file(*args, **kwargs)为GeneratorContextManager对象,此对象在其\_\_enter\_\_中调用open\_file(*args, **kwargs).next()方法,在\_\_exit\_\_中再次调用open_file(*args, **kwargs).next()方法,所以被修饰的函数或方法必须是一个生成器

# 属性方法

| 方法                 | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| closing(thing)       | 配合with..as语句在语句块儿执行完毕后调用被封装对象的.close() |
| nested(*managers)    | 配合with..as语句同时创建多个上下文管理器                     |
| contextmanager(func) | 作为装饰器装饰被yield分隔为2部分的函数或方法或对象,yield前交由\_\_enter\_\_处理,yield后交由\_\_exit\_\_处理,yield的值可通过as传递 |

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import contextlib


if __name__ == '__main__':
    # < Python2.7
    with contextlib.nested(open('/etc/passwd', 'rb'), open('passwd', 'ab')) as (src_passwd, dst_passwd):
        for line in src_passwd:
            dst_passwd.write(line)

    # >= Python2.7
    with open('/etc/passwd', 'rb') as src_passwd, open('passwd', 'ab') as dst_passwd:
        for line in src_passwd:
            dst_passwd.write(line)
```

