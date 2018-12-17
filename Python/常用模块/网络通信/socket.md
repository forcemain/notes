# 常规套路

## 服务端

```python
#! -*- coding: utf-8 -*-


import crcmod
import socket
import struct
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseServer(object):
    def __init__(self, **kwargs):
        self.sock = None
        self.host = kwargs.get('host', '0.0.0.0')
        self.port = kwargs.get('port', 51314)
        self.addr = (self.host, self.port)
        self.handler = kwargs.get('handler', self._handler)

    def _handler(self, data):
        logger.debug('Recv data {0}'.format(data))

    @staticmethod
    def _sock_initopts(sock, opts=None):
        user_opts = set()
        user_opts.update([
            (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
            (socket.SOL_SOCKET, socket.SO_REUSEPORT, 1),
        ])
        if isinstance(opts, (set, list, tuple)):
            user_opts.update(opts)
        map(lambda opt: sock.setsockopt(*opt), user_opts)
    
    def run(self):
        raise NotImplementedError


class TcpServer(BaseServer):
    MODE = 'TcpServer'

    def __init__(self, **kwargs):
        super(TcpServer, self).__init__(**kwargs)
        self.listen = kwargs.get('listen', 1024)
        self.buffer = kwargs.get('buffer', 1024)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock_initopts(self.sock)
        self.sock.bind(self.addr)
        self.sock.listen(self.listen)

    def run(self):
        pass


class CrcTcpServer(TcpServer):
    MODE = 'CrcTcpServer'
    PACK_HEAD_SIZE = 12

    def __init__(self, **kwargs):
        super(CrcTcpServer, self).__init__(**kwargs)

    def run(self):
        data_buffer = bytes()
        while True:
            logger.debug('Wait for connection...')
            conn, addr = self.sock.accept()
            logger.debug('Connection from {0}'.format(addr))
            
            while True:
                data = conn.recv(self.buffer)
                if not data:
                    break
                data_buffer += data
                while True:
                    data_buffer_size = len(data_buffer)
                    if data_buffer_size < self.PACK_HEAD_SIZE:
                        logger.debug('Data buffer size {0} < {1}, break'.format(data_buffer_size,
                                                                                self.PACK_HEAD_SIZE))
                        break
                    version, bodysize, crcsize = struct.unpack('!3I', data_buffer[:self.PACK_HEAD_SIZE])
                    total_size = self.PACK_HEAD_SIZE + bodysize
                    if data_buffer_size < total_size:
                        logger.debug('Data buffer size {0} < {1}, break'.format(data_buffer_size,
                                                                                total_size))
                        break
                    checkdata = data_buffer[self.PACK_HEAD_SIZE:total_size]
                    print '=' * 100
                    print bin(int(checkdata.encode('hex'), 16))
                    print '=' * 100
                    real_data = data_buffer[self.PACK_HEAD_SIZE:total_size-crcsize]
                    self.handler(real_data)
                    data_buffer = data_buffer[total_size:]


class Reciver(object):
    def __init__(self, **kwargs):
        self.server_classes = {}

    def create_server(self, mode, context=None):
        context = context or {}
        assert mode in self.server_classes, '{0} server klass not registed'.format(mode)
        server_class = self.server_classes[mode]
        return server_class(**context)

    def register_server_classes(self, *klasses):
        for klass in klasses:
            if not hasattr(klass, 'MODE'):
                print 'MODE undefined in {0}, ignore'.format(klass.__name__)
                continue
            self.server_classes[klass.MODE] = klass

if __name__ == '__main__':
    crc_tcp_server_context = {
        'host': '0.0.0.0', 
        'port': 51314,
    }
    reciver = Reciver()
    reciver.register_server_classes(CrcTcpServer)
    server = reciver.create_server('CrcTcpServer', crc_tcp_server_context)
    server.run()
```

## 客户端

```python
#! -*- coding: utf-8 -*-


import json
import crcmod
import socket
import struct
import logging
import binascii


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 51314))

    # real_data = json.dumps({'name': u'李满满', 'age': 27})

    real_data = 'a'
    crc32 = crcmod.predefined.Crc('crc-8')
    hex_real_data = binascii.hexlify(real_data)
    crc32.update(hex_real_data)
    real_data_crc = crc32.hexdigest()
    real_data_crc_bytes = real_data_crc.decode('hex')
    body_with_crc_hex = hex_real_data+real_data_crc
    body_with_crc_bytes = body_with_crc_hex.decode('hex')

    version, bodysize, crcsize = 1, len(body_with_crc_bytes), len(real_data_crc_bytes)
    head_packed = struct.pack('!3I', *[version, bodysize, crcsize])

    data = head_packed+body_with_crc_bytes
    sock.sendall(data)
```

# 实战练习

* [编写SOCKET5服务器](#https://hatboy.github.io/2018/04/28/Python%E7%BC%96%E5%86%99socks5%E6%9C%8D%E5%8A%A1%E5%99%A8/)

