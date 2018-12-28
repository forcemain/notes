----

* [模块由来](#模块由来)
* [发展历史](#发展历史)
* [环境依赖](#环境依赖)
* [模块简介](#模块简介)
  * [相关概念](#相关概念)
  * [核心原理](#核心原理)
  * [模拟实现](#模拟实现)
    * [基于Yield+字典+事件循环+异步回调](#基于Yield+字典+事件循环+异步回调)
    * [基于Yield+队列+事件循环+系统调用](#基于Yield+队列+事件循环+系统调用)
  * [事件循环](#事件循环)
    * [回调式](#回调式)
    * [原生式](#原生式)

----



# 模块由来

> GIL锁的存在,多线程环境下IO密集型任务的瓶颈在于上下文切换和线程锁竞争,所以引入协程的概念,协程的上下文切换由程序控制而非内核,相当于单线程,不存在锁的概念,所以速度和性能上都比线程更有优势,但需要注意的是往往长处也是它的短处,协程更适合处理IO密集型任务而非CPU密集型任务,对于后者更推荐配合多进程使用

# 发展历史

* Python2对异步编程支持有限,主要通过生成器yield实现,知名库包括但不限于Twisted,Tornado,Gevent
* Python3对异步编程完美支持,3.5使用async和await分别代替3.4标准库asyncio中的coroutine和yield from,至此协程成为一种新的语法

# 环境依赖

| 操作系统    | PYTHON | 编辑器  |
| ----------- | ------ | ------- |
| macOS 10.14 | 3.6.6  | PyCharm |

# 模块简介

## 相关概念

* 事件循环,不断等待事件发生,并通过回调处理事件
* 协程,可以在执行过程中暂停和恢复
* Future,未来完成的任务结果对象
* Task,继承扩展自Future,封装和管理协程的执行,回调结果对象

## 核心原理

> 将生成器包装为Task任务对象,并触发生成器执行,内部自动为其创建Future未来结果对象并存储对应socket和Future的关系,并将这些socket交由事件循环监测,一旦socket有事件发生找到对应的Future并对其进行处理

## 模拟实现

### 基于Yield+字典+事件循环+异步回调

### 基于Yield+队列+事件循环+系统调用

> 如下是通过原生生成器实现的协程TCP服务器的核心服务端和客户端代码,帮助大家快速理解异步编程套路

#### 服务端

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import socket
import select
import struct


from Queue import Queue


# 将生成器封装为任务对象,在对生成器.send(None)调用时可能需要将任务对象的gen和scheduler传递给生成器返回的模拟系统调用,这样内部可以操作整个调度器数据
class GenerateTask(object):
    def __init__(self, gen, scheduler):
        self.gen = gen
        self.scheduler = scheduler

    def next(self):
        return self.gen.send(None)

    def __str__(self):
        return '<{0}:{1}>'.format(self.__class__.__name__, self.gen.__name__)

    
# 模拟系统调用
class SysCall(object):
    def __init__(self):
        self.gen_task = None
        self.scheduler = None

    def handle(self):
        raise NotImplementedError


# 模拟系统调用,通知socket可读 
class CanReadCall(SysCall):
    def __init__(self, sock):
        self._sock = sock
        super(CanReadCall, self).__init__()

    def handle(self):
        self.scheduler.can_read(self._sock, self.gen_task)


# 模拟系统调用,创建新的任务并写入任务队列
class ForkHandleCall(SysCall):
    def __init__(self, gen):
        self._gen = gen
        super(ForkHandleCall, self).__init__()

    def handle(self):
        handle_gen_task = self.scheduler.new_gen_task(self._gen)
        self.scheduler.put_gen_task(handle_gen_task)


# 一个简单的TCP服务器
class TCPServer(object):
    pack_head_size = 4

    def __init__(self, host='localhost', port=1314):
        self.host = host
        self.port = port

        self._sock = None

    def _open_nfiles(self):
        import resource
        return resource.getrlimit(resource.RLIMIT_NOFILE)[0]

    def _setsockopts(self, *opts):
        map(lambda opt: self._sock.setsockopt(*opt), opts)

    def init(self, **kwargs):
        self._sock = socket.socket(**kwargs)
        self._setsockopts(*[
            (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
            (socket.SOL_SOCKET, socket.SO_REUSEPORT, 1),
        ])
        self._sock.bind((self.host, self.port))
        self._sock.listen(self._open_nfiles())

    def handle(self, sock, addr):
        data_buffer = bytes()
        while True:
            # 通知客户端socket可读,系统调用后此任务对象虽然没有再被写入任务队列,但被保存在了调度器的_can_read_socks字典中,等待select检测事件,一旦存在事件则将会被再次放入任务队列调度
            yield CanReadCall(sock)
            # 常规解包套路: 头部4字节数据长度+真实数据
            data = sock.recv(4096)
            data_buffer += data
            data_buffer_size = len(data_buffer)
            if data_buffer_size < self.pack_head_size:
                continue
            (body_size,) = struct.unpack('!1I', data_buffer[:self.pack_head_size])
            totalsize = self.pack_head_size + body_size
            if data_buffer_size < totalsize:
                continue
            real_data = data_buffer[self.pack_head_size:totalsize]
            print 'Recv data {0}'.format(real_data)
            sock.sendall('Succ')
            data_buffer = data_buffer[totalsize:]

    # 首次会将此生成器封装为任务对象写入任务队列调度
    def run(self):
        while True:
            # 通知服务端的socket可读,系统调用后此任务对象虽然没有再被写入任务队列,但被保存在了调度器的_can_read_socks字典中,等待select检测事件,一旦存在事件则将会被再次放入任务队列调度
            yield CanReadCall(self._sock)
            client, addr = self._sock.accept()
            print 'New conn from {0}'.format(addr)
            # 将处理器生成器封装为任务对象写入任务队列
            yield ForkHandleCall(self.handle(client, addr))


class Scheduler(object):
    def __init__(self):
        # 存放可读socket和对应生成器的关系
        self._can_read_socks = {}
        # 存放可写socket和对应生成器的关系
        self._can_write_socks = {}
        # 调度器任务队列
        self._gen_task_queue = Queue()

    def can_read(self, sock, gen_task):
        self._can_read_socks[sock] = gen_task

    def can_write(self, sock, gen_task):
        self._can_write_socks[sock] = gen_task

    def put_gen_task(self, *args, **kwargs):
        self._gen_task_queue.put(*args, **kwargs)

    def pop_gen_task(self, *args, **kwargs):
        return self._gen_task_queue.get(*args, **kwargs)

    # 将生成器封装为任务对象
    def new_gen_task(self, gen):
        return GenerateTask(gen, self)

    # 实时获取socket事件,如果有事件则将socket对应的任务对象写入任务队列等待调度器处理
    def loop_select(self, timeout=0):
        while True:
            rlist, wlist, elist = select.select(self._can_read_socks.keys(), self._can_write_socks.keys(), [], timeout)
            for rsock in rlist:
                self.put_gen_task(self._can_read_socks[rsock])
            for wsock in wlist:
                self.put_gen_task(self._can_write_socks[wsock])
            yield

    def loop(self, select_timeout=0):
        # 将loop_select封装为任务对象写入任务队列循环调度执行
        loop_select_gen_task = self.new_gen_task(self.loop_select(select_timeout))
        self.put_gen_task(loop_select_gen_task)
        while True:
            # 从任务队列取出任务
            gen_task = self.pop_gen_task()
            print 'Pop {0} from {1}'.format(gen_task, self._gen_task_queue)
            try:
                # 调用生成器send(None)方法获取yield返回值
                task_call = gen_task.next()
            except StopIteration:
                print 'Finish {0}'.format(gen_task)
                continue
            # 如果是模拟系统调用对象,则调用完毕后就不再放入任务队列    
            if isinstance(task_call, SysCall):
                # 为系统调用传递所属任务信息
                task_call.gen_task = gen_task
                task_call.scheduler = self
                # 执行系统调用
                task_call.handle()
                continue
            # 对于loop_select这种通用生成器任务继续放入任务队列
            self.put_gen_task(gen_task)
            print 'Put {0} to {1}'.format(gen_task, self._gen_task_queue)


if __name__ == '__main__':
    scheduler = Scheduler()
    # 将TCPServer的run生成器也封装为任务对象放入任务队列调度
    tcpserver = TCPServer()
    tcpserver.init()
    tcpserver_run_gen_task = scheduler.new_gen_task(tcpserver.run())
    scheduler.put_gen_task(tcpserver_run_gen_task)
    scheduler.loop()
```

#### 客户端

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import json
import socket
import struct
import threading


class TCPClient(object):
    def __init__(self, host='localhost', port=1314):
        self.host = host
        self.port = port

        self._sock = None

    def init(self, **kwargs):
        self._sock = socket.socket(**kwargs)
        self._sock.connect((self.host, self.port))

    # 常规封包套路: 头部N字节数据+真实数据
    def pack_data(self, data):
        data_length = len(data)
        data_header = struct.pack('!1I', *[data_length])
        send_data = data_header + bytes(data)

        return send_data

    @property
    def socket(self):
        return self._sock


# 并发测试,请修改ulimit后再改大数值
def concurrent_send(data):
    client = TCPClient()
    client.init()
    send_data = client.pack_data(data)
    client.socket.sendall(send_data)
    print '{0} recv: {1}'.format(threading.currentThread(), client.socket.recv(4096))

if __name__ == '__main__':
    send_data = json.dumps({
        'name': u'李满满',
        'addr': u'滨江区',
    })
    send_threads = []
    map(lambda _: send_threads.append(threading.Thread(target=concurrent_send, args=(send_data,))), xrange(1000))
    for t in send_threads:
        t.setDaemon(True)
        t.start()
    for t in send_threads:
        t.join()
```

# 事件循环

## 回调式

### 创建事件循环

| 方法             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| new_event_loop() | 同get_event_loop_policy().new_event_loop(),根据当前系统创建一个新的事件循环 |
| get_event_loop() | 如果在如下方法内调用则返回已存在的事件循环,否则调用new_event_loop()创建新的事件循环 |

#### 属性方法

| 方法                                    | 说明                                                         |
| --------------------------------------- | ------------------------------------------------------------ |
| loop.call_soon(callback, *args)         | 注册一个立即任务,由事件循环立即调用                          |
| loop.call_later(delay, callback, *args) | 注册一个延迟任务,在delay秒内可通过返回对象.cancel()取消任务,由事件循环延迟调用 |
| loop.time()                             | 事件循环的内部clock时间,单位秒                               |
| loop.call_at(when, callback, *args)     | 同loop.call_later但when表示以loop.time()为基准的绝对时间     |
| loop.run_forever()                      | 一直运行直到显式调用loop.stop()                              |
| loop.stop()                             | 停止事件循环,                                                |
| loop.close()                            | 关闭事件循环,强制清空任务队列,强制关闭执行中的任务,但需要注意的是必须提前调用loop.stop()保证事件循环已停止 |

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com

import json
import copy
import time
import pprint
import asyncio


# 基类模型
class BaseModel(object):
    def __init__(self):
        self._dict = None

    @classmethod
    def from_dict(cls, data):
        instance = cls(**data)
        instance._dict = data

        return instance

    @classmethod
    def from_json(cls, data):
        dict_data = json.loads(data)

        return cls.from_dict(dict_data)

    def to_json(self, indent=4):
        json_data = json.dumps(self._dict, indent=indent)

        return json_data

    def __str__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.to_json())


# 告警消息模型
class AlarmMsg(BaseModel):
    def __init__(self, **kwargs):
        super(AlarmMsg, self).__init__()

        self.status = kwargs.get('status', None)
        self.iocount = kwargs.get('iocount', None)
        self.cpuload = kwargs.get('cpuload', None)
        self.memfree = kwargs.get('memfree', None)
        self.runtime = kwargs.get('runtime', None)
        self.hostname = kwargs.get('hostname', None)
        self.itemvalue = kwargs.get('itemvalue', None)
        self.hostgroup = kwargs.get('hostgroup', None)
        self.ipaddress = kwargs.get('ipaddress', None)
        self.triggerkey = kwargs.get('triggerkey', None)
        self.triggername = kwargs.get('triggername', None)
        self.triggeritems = kwargs.get('triggeritems', None)
        self.triggervalue = kwargs.get('triggervalue', None)
        self.triggernseverity = kwargs.get('triggernseverity', None)

    @classmethod
    def from_strs(cls, data):
        dict_data = dict(map(lambda s:s.split('|'), data.split('#')))

        return cls.from_dict(dict_data)


# 告警项目模型
class AlarmItem(BaseModel):
    def __init__(self, **kwargs):
        super(AlarmItem, self).__init__()

        self.status = kwargs.get('status', None)
        self.source = kwargs.get('source', None)
        self.sendto = kwargs.get('sendto', None)
        self.message = kwargs.get('message', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.mediatype = kwargs.get('mediatype', None)


# 告警收敛任务
class AlarmConverge(object):
    def __init__(self, loop, source):
        self._loop = loop
        self.source = source

        self._init()

    # 初始化
    def _init(self):
        attrs = dir(self)
        for method_name in attrs:
            method = getattr(self, method_name)
            if not callable(method):
                continue
            if not method_name.startswith('by_'):
                continue
            new_method_name = '{0}_data'.format(method_name)
            setattr(self, new_method_name, None)

    # 第1步:开始
    def start(self):
        _predata, _nxtdata = self.source, self.source
        # do something
        self._loop.call_soon(self.by_status, _predata, _nxtdata)

    # 第2步:基于第1步,根据状态聚合
    def by_status(self, predata, nxtdata):
        _predata, _nxtdata = predata, [[], []]
        for item in _predata:
            _nxtdata[item.status].append(item)
        self.by_status_data = copy.deepcopy(_nxtdata)
        self._loop.call_soon(self.by_sendto, _predata, _nxtdata)

    # 第3步:基于第2步,根据发送人聚合
    def by_sendto(self, predata, nxtdata):
        _predata, _nxtdata = nxtdata, [{}, {}]
        _predata_recovery, _predata_problem = _predata
        for item in _predata_recovery:
            _nxtdata[0].setdefault(item.sendto, []). \
                        append(item)
        for item in _predata_problem:
            _nxtdata[1].setdefault(item.sendto, []). \
                        append(item)
        self.by_sendto_data = copy.deepcopy(_nxtdata)
        self._loop.call_soon(self.by_policy, _predata, _nxtdata)

    # 第4步:基于第3步,根据主机和告警聚合
    def by_policy(self, predata, nxtdata):
        _predata, _nxtdata = nxtdata, [{}, {}]
        _predata_recovery, _predata_problem = _predata
        for sendto in _predata_recovery:
            for item in _predata_recovery[sendto]:
                _nxtdata[0].setdefault(sendto, {}). \
                            setdefault('hosts', {}). \
                            setdefault(item.message.hostname, []). \
                            append(item)
                _nxtdata[0].setdefault(sendto, {}). \
                            setdefault('triggers', {}). \
                            setdefault(item.message.triggername, []). \
                            append(item)
        for sendto in _predata_problem:
            for item in _predata_problem[sendto]:
                _nxtdata[1].setdefault(sendto, {}). \
                            setdefault('triggers', {}). \
                            setdefault(item.message.triggername, []). \
                            append(item)
                _nxtdata[1].setdefault(sendto, {}). \
                            setdefault('hosts', {}). \
                            setdefault(item.message.hostname, []). \
                            append(item)
        self.by_policy_data = copy.deepcopy(_nxtdata)
        self._loop.call_soon(self.by_merge, _predata, _nxtdata)

    # 第5步:基于第4步,合并主机和告警数据
    def by_merge(self, predata, nxtdata):
        _predata, _nxtdata = nxtdata, copy.deepcopy(nxtdata)
        _predata_recovery, _predata_problem = _predata
        for sendto in _predata_recovery:
            sendto_data = _predata_recovery[sendto]
            by_triggers = len(sendto_data['hosts']) > len(sendto_data['triggers'])
            if by_triggers:
                _nxtdata[0][sendto].pop('hosts', None)
            else:
                _nxtdata[0][sendto].pop('triggers', None)
        for sendto in _predata_problem:
            sendto_data = _predata_problem[sendto]
            by_triggers = len(sendto_data['hosts']) > len(sendto_data['triggers'])
            if by_triggers:
                _nxtdata[1][sendto].pop('hosts', None)
            else:
                _nxtdata[1][sendto].pop('triggers', None)
        self.by_merge_data = copy.deepcopy(_nxtdata)
        self._loop.call_soon(self.finish, _predata, _nxtdata)

    # 第6步:完成
    def finish(self, predata, nxtdata):
        _predata, _nxtdata = predata, nxtdata
        # do something
        self._loop.stop()

    def debug(self):
        cls_name = self.__class__.__name__
        pprint.pprint('{0} Source: '.format(cls_name))
        pprint.pprint(self.source)
        pprint.pprint('{0} By Status:'.format(cls_name))
        pprint.pprint(self.by_status_data)
        pprint.pprint('{0} By Sendto:'.format(cls_name))
        pprint.pprint(self.by_sendto_data)
        pprint.pprint('{0} By Policy: '.format(cls_name))
        pprint.pprint(self.by_policy_data)
        pprint.pprint('{0} By Merge: '.format(cls_name))
        pprint.pprint(self.by_merge_data)

if __name__ == '__main__':
    # Zabbix告警
    alarm_msg_1 = (
        'triggervalue|1#hostname|HZ-DHCPMASTER-VM#ipaddress|192.168.130.3#hostgroup|DHCP#triggernseverity|3'
        '#triggername|可用IP数10.247.4.0#triggerkey|dhcp[ScopeFree,10.247.4.0]#triggeritems|可用IP数 10.247.4.0'
        '#itemvalue|9#status|1#cpuload|11.42 %#memfree|6.12 GB#iocount|40.33 Kb#runtime|91 days, 22:39:55'
    )
    alarm_msg_2 = (
        'triggervalue|1#hostname|HZ-DHCPMASTER-VM#ipaddress|192.168.130.3#hostgroup|DHCP#triggernseverity|3'
        '#triggername|可用IP数10.247.4.0#triggerkey|dhcp[ScopeFree,10.247.4.0]#triggeritems|可用IP数 10.247.4.0'
        '#itemvalue|9#status|1#cpuload|11.42 %#memfree|6.12 GB#iocount|40.33 Kb#runtime|91 days, 22:39:55'
    )
    alarm_msg_3 = (
        'triggervalue|1#hostname|HZ-DHCPSLAVE-VM#ipaddress|10.246.86.74#hostgroup|DHCP#triggernseverity|3'
        '#triggername|可用IP数10.247.4.0#triggerkey|dhcp[ScopeFree,10.247.4.0]#triggeritems|可用IP数 10.247.4.0'
        '#itemvalue|9#status|1#cpuload|13.46 %#memfree|6.88 GB#iocount|33.78 Kb#runtime|93 days, 00:25:34'
    )
    alarm_msg_4 = (
        'triggervalue|0#hostname|HZ-YFTDC06-VM#ipaddress|10.240.215.215#hostgroup|AD&DNS#triggernseverity|2'
        '#triggername|cpu processor usage is greater than 70%#triggerkey|perf_counter[\Processor(_Total)\% Processor Time'
        '#triggeritems|cpu usage rate#itemvalue|66.03 %#status|0#cpuload|66.03 %#memfree|22.74 GB#iocount|185.52 Kb'
        '#runtime|223 days, 08:04:33'
    )
    # 封装数据源
    ac_source = [
        AlarmItem(
            status=1, source='zabbix', sendto='limanman', message=AlarmMsg.from_strs(alarm_msg_1),
            timestamp=time.time(), mediatype=5
        ),
        AlarmItem(
            status=1, source='zabbix', sendto=u'manmanli', message=AlarmMsg.from_strs(alarm_msg_1),
            timestamp=time.time(), mediatype=5
        ),
        AlarmItem(
            status=1, source='zabbix', sendto=u'limanman', message=AlarmMsg.from_strs(alarm_msg_2),
            timestamp=time.time(), mediatype=5
        ),
        AlarmItem(
            status=1, source='zabbix', sendto=u'manmanli', message=AlarmMsg.from_strs(alarm_msg_2),
            timestamp=time.time(), mediatype=5
        ),
        AlarmItem(
            status=1, source='zabbix', sendto=u'limanman', message=AlarmMsg.from_strs(alarm_msg_3),
            timestamp=time.time(), mediatype=5
        ),
        AlarmItem(
            status=1, source='zabbix', sendto=u'manmanli', message=AlarmMsg.from_strs(alarm_msg_3),
            timestamp=time.time(), mediatype=5
        ),
        AlarmItem(
            status=1, source='zabbix', sendto=u'limanman', message=AlarmMsg.from_strs(alarm_msg_4),
            timestamp=time.time(), mediatype=5
        ),
    ]
    # 创建事件循环
    loop = asyncio.new_event_loop()
    # 创建告警聚合对象
    ac = AlarmConverge(loop, ac_source)
    # 创建任务
    loop.call_soon(ac.start)
    # 运行直至显式调用loop.stop()
    loop.run_forever()
    # 强制关闭事件循环
    not loop.is_closed() and loop.close()

    # 简单调试
    ac.debug()
```

## 原生式







