----

* [本章目录](#本章目录)
  * [multiprocessing](#multiprocessing)
  * [asyncio](#asyncio)

* [基础巩固](#基础巩固)
  * [相关概念](#相关概念)
    * [阻塞](#阻塞)
    * [非阻塞](#非阻塞)
    * [同步](#同步)
    * [异步](#异步)
    * [并发](#并发)
    * [并行](#并行)
  * [异步编程](#异步编程)
  * [异步进化](#异步进化)
    * [单进程(阻塞)](#单进程(阻塞))
    * [多进程(阻塞)](#多进程(阻塞))
    * [多线程(阻塞)](#多线程(阻塞))
    * [单进程(非阻塞)](#单进程(非阻塞))
    * [多路复用(回调)](#多路复用(回调))
    * [生成器协程(非阻塞)](#生成器协程(非阻塞))
    * [yield from(非阻塞)](#)
    * [原生协程(非阻塞)](#原生协程(非阻塞))

----



# 相关概念

## 阻塞

* 程序在执行某个操作后,如未返回,自身无法继续干别的事情,强调的是程序在等待结果时的状态

## 非阻塞

* 程序在执行某个操作后,立即返回,自身可以继续干别的事情,强调的是程序在等待结果时的状态

## 同步

* 程序在执行某个操作后,如未返回,主动轮询等待结果,强调的是消息通知的机制

## 异步

* 程序在执行某个操作后,立即返回,后续回调通知结果,强调的是消息通知的机制

## 并发

* 多个任务频繁切换上下文执行的状态称为并发,可能存在并发

## 并行

* 多个任务同时被执行的状态称为并行,通常依赖多核CPU环境

# 异步编程

> 通过进程,线程,协程,函数/方法作为执行任务程序的基本单位,结合回调,事件循环,信号等机制,提高程序整体执行效率和并发能力的编程方式

# 异步进化

## 单进程(阻塞)

> 如下程序请求监控大屏公共接口数据,sock.connect和sock.recv默认阻塞操作且不可预测,sock.send虽然也是阻塞操作但它只负责将数据拷贝到TCP/IP协议栈的系统缓冲区就直接返回,可忽略

````python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import socket
import operator


def blocking_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = '10.246.26.13', 80
    # 阻塞
    sock.connect((host, port))
    request = (
        'GET /ne_screen/jbscreen/lebo/screen/connect-totaltime/?from=2018-01-01&to=2018-12-3 HTTP/1.0\r\n'
        'HOST:{0}\r\n\r\n'.format(host, )
    )
    sock.send(request)
    response = ''
    # 阻塞
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # 阻塞
        chunk = sock.recv(4096)
    return response


if __name__ == '__main__':
    results = []
    # 存储耗时
    runcost = [time.time()]
    for _ in xrange(20):
        results.append(blocking_request())
    print results
    runcost.insert(0, time.time())
    print 'Request Times: {0}, Total Cost: {1} seconds'.format(len(results), operator.sub(*runcost))

"""
Request Times: 20, Total Cost: 13.220692873 seconds
"""
````

* 此方式问题在于阻塞过程循环10次,效率十分低下

## 多进程(阻塞)

> 如下程序请求监控大屏公共接口数据,sock.connect和sock.recv默认阻塞操作且不可预测,sock.send虽然也是阻塞操作但它只负责将数据拷贝到TCP/IP协议栈的系统缓冲区就直接返回,可忽略

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import socket
import operator
from concurrent import futures
from multiprocessing import cpu_count


def blocking_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = '10.246.26.13', 80
    # 阻塞
    sock.connect((host, port))
    request = (
        'GET /ne_screen/jbscreen/lebo/screen/connect-totaltime/?from=2018-01-01&to=2018-12-3 HTTP/1.0\r\n'
        'HOST:{0}\r\n\r\n'.format(host, )
    )
    sock.send(request)
    response = ''
    # 阻塞
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # 阻塞
        chunk = sock.recv(4096)
    return response


if __name__ == '__main__':
    results = []
    # 存储耗时
    runcost = [time.time()]
    # 多进程
    with futures.ProcessPoolExecutor(max_workers=cpu_count()) as executer:
        for _ in xrange(20):
            # 生成futures任务
            results.append(executer.submit(blocking_request))
    runcost.insert(0, time.time())
    print 'Request Times: {0}, Total Cost: {1} seconds'.format(
        # 获取结果
        len([f.result() for f in results]),
        operator.sub(*runcost)
    )

"""
Request Times: 20, Total Cost: 2.37551212311 seconds
"""
```

* 此方式问题在于虽然并行执行优化效果明显,但由于任务数大于CPU核数,导致进程切换, 而进程切换的开销还是很大的

## 多线程(阻塞)

> 如下程序请求监控大屏公共接口数据,sock.connect和sock.recv默认阻塞操作且不可预测,sock.send虽然也是阻塞操作但它只负责将数据拷贝到TCP/IP协议栈的系统缓冲区就直接返回,可忽略

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import socket
import operator
from concurrent import futures
from multiprocessing import cpu_count


def blocking_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = '10.246.26.13', 80
    # 阻塞
    sock.connect((host, port))
    request = (
        'GET /ne_screen/jbscreen/lebo/screen/connect-totaltime/?from=2018-01-01&to=2018-12-3 HTTP/1.0\r\n'
        'HOST:{0}\r\n\r\n'.format(host, )
    )
    sock.send(request)
    response = ''
    # 阻塞
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # 阻塞
        chunk = sock.recv(4096)
    return response


if __name__ == '__main__':
    results = []
    # 存储耗时
    runcost = [time.time()]
    # 多线程
    with futures.ThreadPoolExecutor(max_workers=cpu_count()) as executer:
        for _ in xrange(20):
            # 生成futures任务
            results.append(executer.submit(blocking_request))
    runcost.insert(0, time.time())
    print 'Request Times: {0}, Total Cost: {1} seconds'.format(
        # 获取结果
        len([f.result() for f in results]),
        operator.sub(*runcost)
    )

"""
Request Times: 20, Total Cost: 2.19818592072 seconds
"""
```

* 此方式问题在于虽然线程比进程更轻量级,也可支持大规模任务,但由于GIL锁的原因,只能并发模式运行,无法利用多核,而且线程切换以及竞态等都会产生开销

## 单进程(非阻塞)

> 如下程序请求监控大屏公共接口数据,sock.setblocking(False)使此sockt下的操作全部变为异步,所以在sock.send和sock.recv时并不知道是否准备就绪,所以使用while循环检测

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import socket
import operator


def unblocking_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = '10.246.26.13', 80
    # 非阻塞
    # 设置此sock上的调用全部改为非阻塞
    sock.setblocking(False)
    try:
        # 非阻塞模式会抛异常
        sock.connect((host, port))
    except socket.error:
        pass
    request = (
        'GET /ne_screen/jbscreen/lebo/screen/connect-totaltime/?from=2018-01-01&to=2018-12-3 HTTP/1.0\r\n'
        'HOST:{0}\r\n\r\n'.format(host, )
    )
    # 不知何时连接就绪,只能不断轮询发送检测
    while True:
        try:
            sock.send(request)
            break
        except socket.error:
            pass
    response = ''
    # 不知何时数据就绪,只能不断轮询接收检测
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            break
        except socket.error:
            pass
    return response

if __name__ == '__main__':
    results = []
    # 存储耗时
    runcost = [time.time()]
    for _ in xrange(20):
        results.append(unblocking_request())
    runcost.insert(0, time.time())
    print 'Request Times: {0}, Total Cost: {1} seconds'.format(
        len(results),
        operator.sub(*runcost)
    )

"""
Request Times: 20, Total Cost: 10.07249403 seconds
"""
```

* 此方式问题在于虽然是非阻塞,但空出来的时间CPU并未闲着,而是浪费在循环检测上面,导致和单进程阻塞模式耗时差不多,可以想象在多进程(非阻塞)和多线程(非阻塞)模式下也不相上下

## 多路复用(回调)

> 如下程序请求监控大屏公共接口数据,sock.setblocking(False)使此sockt下的操作全部变为异步,将IO事件的等待和监听交由OS,sock.send和sock.recv由回调驱动

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import select
import socket
import operator


# 静态类,零时存储可读可写连接
class Cache(object):
    can_read = {}
    can_write = {}


class Client(object):
    def __init__(self):
        self._socket = None

    def connect(self, host, port, uri, **kwargs):
        self._socket = socket.socket(**kwargs)
        # 设置此sock上的调用全部改为非阻塞
        self._socket.setblocking(False)
        try:
            # 非阻塞模式会抛异常
            self._socket.connect((host, port))
        except socket.error:
            pass
        # 创建完连接放入可写字典
        Cache.can_write[self._socket] = self

    def req_handle(self):
        _req = 'GET {0} HTTP/1.0\r\nHOST:{1}\r\n\r\n'.format(uri, host)
        self._socket.send(_req)
        # 发送完数据放入可读字典
        Cache.can_read[self._socket] = self

    def rsp_handle(self, buffersize=4096):
        _rsp = ''
        # select在非阻塞模式下可能出现误判导致数据未准备就绪,这里做一下简单处理
        while True:
            try:
                chunk = self._socket.recv(buffersize)
                while chunk:
                    _rsp += chunk
                    chunk = self._socket.recv(buffersize)
                break
            except socket.error:
                continue
        return _rsp


if __name__ == '__main__':
    results = []
    # 存存储耗时
    runcost = [time.time()]
    host, port, uri = '10.246.26.13', 80, '/ne_screen/jbscreen/lebo/screen/connect-totaltime/?from=2018-01-01&to=2018-12-3'
    for _ in xrange(20):
        c = Client()
        # 异步创建20个连接放入可写字典
        c.connect(host, port, uri)
    while True:
        # 处理完20个请求就退出
        if not Cache.can_read and not Cache.can_write:
            break
        # 监听读写事件
        rlist, wlist, _ = select.select(Cache.can_read, Cache.can_write, [])
        if rlist:
            # 可读就读取
            for sock in rlist:
                client = Cache.can_read.pop(sock)
                results.append(client.rsp_handle())
        if wlist:
            # 可写就请求
            for sock in wlist:
                client = Cache.can_write.pop(sock)
                client.req_handle()

    runcost.insert(0, time.time())
    print 'Request Times: {0}, Total Cost: {1} seconds'.format(
        len(results),
        operator.sub(*runcost)
    )

"""
Request Times: 20, Total Cost: 1.52134513855 seconds
"""
```

* 此方式问题在于虽然将I/O事件的等待和监听交由OS,当有读写事件发生时通过回调处理,但处理过程是同步阻塞的,依然耗时
* 事件循环+回调是异步编程的初期套路,但多层回调或回调依赖会导致代码臃肿和异常冒泡,导致无法定位到真实异常,于是在此之上衍生出了基于协程的解决方案

## 生成器协程(非阻塞)

> 如下程序请求监控大屏公共接口数据,sock.setblocking(False)使此sockt下的操作全部变为异步,将IO事件的等待和监听交由OS,由回调再次驱动生成器运行

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import select
import socket
import operator


# 静态类,零时存储可读可写字典
class Cache(object):
    can_read = {}
    can_write = {}


# 未来可能完成的任务结果类
class Future(object):
    def __init__(self):
        # 存放当前结果
        self.result = None
        self._callbacks = []

    # 注册回调
    def add_done_callback(self, callback):
        self._callbacks.append(callback)

    # 触发回调接口
    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)


# 未来可能完成的任务
class Task(object):
    def __init__(self, gen):
        self.gen = gen
        # 初始化时就调用
        self.next(Future())

    def next(self, future):
        try:
            # 让生成器继续执行并将结果对象的零时结果传递给协程
            next_future = self.gen.send(future.result)
        except StopIteration:
            return
        # 给yield返回的未来结果对象注册一个回调
        next_future.add_done_callback(self.next)


class Client(object):
    def __init__(self):
        self._socket = None
        # 存储结果数据
        self.response = ''

    def fetch(self, host, port, uri, **kwargs):
        self._socket = socket.socket(**kwargs)
        # 设置此sock上的调用全部改为非阻塞
        self._socket.setblocking(False)
        try:
            # 非阻塞模式会抛异常
            self._socket.connect((host, port))
        except socket.error:
            pass

        # 创建一个未来结果对象来注册可写socket,让select来接管IO事件检测
        _future = Future()
        # 加入可写字典
        Cache.can_write[self._socket] = _future
        # 第一次Task初始化注册回调后走到这一步,控制权交给主进程,此时发现可写列表中的socket已就绪,随即通过set_result发送请求并触发
        # 回调导致执行了之前注册的Task的的next方法,而对应的task的gen生成器也就是对应client.fetch的那个
        yield _future

        while True:
            # 创建一个未来结果对象来注册可读socket,让select来接管IO事件检测
            _future = Future()
            # 加入可写字典
            Cache.can_read[self._socket] = _future
            # 上面通过set_result触发了对应的gen生成器继续执行走到这里,再次将控制权交给主进程,select监听到可读事件后通过对应的
            # set_result回调再次send将接收到的部分数据传递过来
            chunk = yield _future
            if chunk:
                self.response += chunk
            else:
                break

if __name__ == '__main__':
    results = []
    runcost = [time.time()]
    host, port, uri = '', 80, ''
    for _ in xrange(20):
        c = Client()
        results.append(c)
        # 创建20个task,每个task必须是生成器
        Task(c.fetch(host, port, uri))
    while True:
        # 处理完20个请求就退出
        if not Cache.can_read and not Cache.can_write:
            break
        # 检测读写事件
        rlist, wlist, _ = select.select(Cache.can_read, Cache.can_write, [])
        if rlist:
            # 取出每个连接对应的future对象,然后通过.set_result回调让对应的client的生成器继续执行并传递当前收到的部分数据
            for sock in rlist:
                future = Cache.can_read.pop(sock)
                future.set_result(sock.recv(4096))
        if wlist:
            # 取出每个连接对应的的future对象,然后通过.set_result回调让对应的client的生成器继续执行
            for sock in wlist:
                future = Cache.can_write.pop(sock)
                _req = 'GET {0} HTTP/1.0\r\nHOST:{1}\r\n\r\n'.format(uri, host)
                future.set_result(sock.send(_req))

    runcost.insert(0, time.time())
    print 'Request Times: {0}, Total Cost: {1} seconds'.format(
        len(results),
        operator.sub(*runcost)
    )

"""
Request Times: 20, Total Cost: 0.979491949081 seconds
"""
```

* 此方式在多路复用(非阻塞)的基础上在将数据的发送和接收改为异步模式,借助事件循环频繁无序切换,避免无意义的阻塞等待
* 此方式的问题在于在生成器内操作生成器自身导致代码晦涩且丑陋

## yield from(非阻塞)

> 如下程序请求监控大屏公共接口数据,sock.setblocking(False)使此sockt下的操作全部变为异步,将IO事件的等待和监听交由OS,由回调再次驱动生成器运行

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import select
import socket
import operator


# 静态类,零时存储可读可写字典
class Cache(object):
    can_read = {}
    can_write = {}


# 未来可能完成的任务结果类
class Future(object):
    def __init__(self):
        # 存放当前结果
        self.result = None
        self._callbacks = []

    # 注册回调
    def add_done_callback(self, callback):
        self._callbacks.append(callback)

    # 触发回调接口
    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)


# 未来可能完成的任务
class Task(object):
    def __init__(self, gen):
        self.gen = gen
        # 初始化时就调用
        self.next(Future())

    def next(self, future):
        try:
            # 让生成器继续执行并将结果对象的零时结果传递给协程
            next_future = self.gen.send(future.result)
        except StopIteration:
            return
        # 给yield返回的未来结果对象注册一个回调
        next_future.add_done_callback(self.next)


class Client(object):
    def __init__(self):
        self._socket = None
        self._stop = False
        # 存储结果数据
        self.response = b''

    # 将connect分离出来,通过yield from建立的双向通道直接通信
    def connect(self, host, port, uri, **kwargs):
        self._socket = socket.socket(**kwargs)
        # 设置此sock上的调用全部改为非阻塞
        self._socket.setblocking(False)
        try:
            # 非阻塞模式会抛异常
            self._socket.connect((host, port))
        except socket.error:
            pass

        # 创建一个未来结果对象来注册可写socket,让select来接管IO事件检测
        _future = Future()
        # 加入可写字典
        Cache.can_write[self._socket] = _future
        # 第一次Task初始化注册回调后走到这一步,控制权交给主进程,此时发现可写列表中的socket已就绪,随即通过set_result发送请求并触发
        # 回调导致执行了之前注册的Task的的next方法,而对应的task的gen生成器也就是对应client.fetch的那个
        yield _future

    # 将readall分离出来,通过yield from建立的双向通道直接通信
    def readall(self):
        # 创建一个未来结果对象来注册可读socket,让select来接管IO事件检测
        _future = Future()
        # 加入可写字典
        Cache.can_read[self._socket] = _future
        # 上面通过set_result触发了对应的gen生成器继续执行走到这里,再次将控制权交给主进程,select监听到可读事件后通过对应的
        # set_result回调再次send将接收到的部分数据传递过来
        chunk = yield _future
        if not chunk:
            # 数据读完后设置标志位让生成器结束
            self._stop = True
        self.response += chunk

    def fetch(self, host, port, uri, **kwargs):
        yield from self.connect(host, port, uri, **kwargs)

        while not self._stop:
            yield from self.readall()

if __name__ == '__main__':
    results = []
    # 存储耗时
    runcost = [time.time()]
    host, port, uri = '', 80, ''
    for _ in range(20):
        c = Client()
        results.append(c)
        # 创建20个task,每个task必须是生成器
        Task(c.fetch(host, port, uri))
    while True:
        # 处理完20个请求就退出
        if not Cache.can_read and not Cache.can_write:
            break
        # 检测读写事件
        rlist, wlist, _ = select.select(Cache.can_read, Cache.can_write, [])
        if rlist:
            # 取出每个连接对应的future对象,然后通过.set_result回调让对应的client的生成器继续执行并传递当前收到的部分数据
            for sock in rlist:
                future = Cache.can_read.pop(sock)
                future.set_result(sock.recv(4096))
        if wlist:
            # 取出每个连接对应的的future对象,然后通过.set_result回调让对应的client的生成器继续执行
            for sock in wlist:
                future = Cache.can_write.pop(sock)
                _req = 'GET {0} HTTP/1.0\r\nHOST:{1}\r\n\r\n'.format(uri, host)
                future.set_result(sock.send(_req.encode('ascii')))

    runcost.insert(0, time.time())
    print('Request Times: {0}, Total Cost: {1} seconds'.format(
        len(results),
        operator.sub(*runcost)
    ))

"""
Request Times: 20, Total Cost: 0.8642621040344238 seconds
"""
```

* 此方式是Python3.3中引入的新语法,至此无需在生成器内循环迭代生成器,直接使用yield from,而且会在父生成器的调用者与父生成器下的子生成器之间建立通信双向通道,两者可以直接通信

## 原生协程(非阻塞)

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import operator
import asyncio
import aiohttp


loop = asyncio.get_event_loop()


# 通过async语法使此函数可以暂停和恢复,其实是将其包装为Task
async def fetch(url):
    # 通过async语法使此函数可以暂停和恢复,其实是将其包装为Task
    async with aiohttp.ClientSession(loop=loop) as session:
        # 通过async语法使此函数可以暂停和恢复,其实是将其包装为Task
        async with session.get(url) as response:
            # 通过await语法使耗时任务挂起,等待事件循环通知可读
            response = await response.read()
            return response

if __name__ == '__main__':
    # 存储任务
    tasks = []
    results = []
    # 存储耗时
    runcost = [time.time()]
    host, port, uri = '', 80, ''
    req_url = 'http://{0}:{1}{2}'.format(host, port, uri)
    # 创建20个任务
    for _ in range(20):
        task = loop.create_task(fetch(req_url))
        # task.add_done_callback(lambda f: results.append(f.result()))
        tasks.append(task)
    # 等待所有任务执行完毕
    loop.run_until_complete(asyncio.gather(*tasks))
    runcost.insert(0, time.time())
    print('Request Times: {0}, Total Cost: {1} seconds'.format(
        len(results),
        operator.sub(*runcost)
    ))

"""
Request Times: 20, Total Cost: 0.9909639358520508 seconds
"""
```

* 此方式是Python3.5中引入的新语法,至此将不再考虑yield和yield from有啥区别,asyncio成为标准库,提高了事件循环(EventLoop),协程(Coroutine),任务(Task),未来结果对象(Future)等核心组件,大大简化异步编程