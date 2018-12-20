

----

* [模块简介](#模块简介)
* [快速部署](#快速部署)
* [创建连接](#创建连接)
* [常规操作](#常规操作)
  * [增加](#增加)
  * [删除](#删除)
  * [查询](#查询)
  * [修改](#修改)
  * [事务](#事务)
* [实战练习](#实战练习)

----

# 模块简介

>   第三方模块,提供标准MySQL数据库应用编程接口,但暂不支持Python3,如有需求可用pymysql库代替

# 快速部署

* For MAC

```bash
brew install mysql
brew unlink mysql
brew install mysql-connector-c
brew link --overwrite mysql-connector-c
sed -i -e 's/libs="$libs -l "/libs="$libs -lmysqlclient -lssl -lcrypto"/g' /usr/local/bin/mysql_config
sudo pip install MySQL-python
brew unlink mysql-connector-c
brew link --overwrite mysql
```

* For Linux

```bash
pip install MySQL-python
```

# 创建连接

| 方法                     | 说明                                                         |
| ------------------------ | ------------------------------------------------------------ |
| Connect(*args, **kwargs) | 创建连接对象,常用命名参数有host,port,user,passwd,db,charset,cursorclass分别表示主机,端口,账户,密码,数据库,编码,游标类 |

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import MySQLdb
import settings


if __name__ == '__main__':
    create_table_sql = '''
      CREATE TABLE IF NOT EXISTS REGUSER (
         NAME CHAR(20) NOT NULL,
         AGE  INT,  
         SEX  CHAR(1))
    '''
    # 方式一: Windows下可能不兼容with上下文管理可用如下方式或配合contextlib.closing使用
    # 获取连接
    conn = MySQLdb.connect(host=settings.HOST, port=settings.PORT,
                           user=settings.USER, passwd=settings.PASSWD,
                           db=settings.DB)
    # 获取游标
    cursor = conn.cursor()
    # 执行语句
    cursor.execute(create_table_sql)
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

    # 方式二,非Windows强烈推荐
    # 获取游标
    with MySQLdb.connect(host=settings.HOST, port=settings.PORT,
                         user=settings.USER, passwd=settings.PASSWD,
                         db=settings.DB) as cursor:
        cursor.execute(create_table_sql)
```

# 常规操作

![image-20181219174246463](MySQL-python.assets/image-20181219174246463-5212566.png)

## 增加

````python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import MySQLdb
import settings


if __name__ == '__main__':
    insert_table_sql = 'INSERT INTO REGUSER(NAME, AGE, SEX) VALUES (%s, %s, %s)'

    with MySQLdb.connect(host=settings.HOST, port=settings.PORT,
                         user=settings.USER, passwd=settings.PASSWD,
                         db=settings.DB) as cursor:
        # SQL中的参数强烈推荐使用通过args传递,否则可能出现SQL注入漏洞利用
        cursor.execute(insert_table_sql, args=('李满满', 27, 0))
        # 返回受影响的行数
        print cursor.rowcount
````

## 删除

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import MySQLdb
import settings


if __name__ == '__main__':
    delete_table_sql = "DELETE FROM REGUSER WHERE NAME=%s"

    with MySQLdb.connect(host=settings.HOST, port=settings.PORT,
                         user=settings.USER, passwd=settings.PASSWD,
                         db=settings.DB) as cursor:
        # SQL中的参数强烈推荐使用通过args传递,否则可能出现SQL注入漏洞利用
        cursor.execute(delete_table_sql, args=('李满满',))
        # 返回影响的行数
        print cursor.rowcount
```



## 查询

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import MySQLdb
import settings


from MySQLdb.cursors import DictCursor

if __name__ == '__main__':
    select_table_sql = 'SELECT * from REGUSER WHERE NAME=%s'

    with MySQLdb.connect(host=settings.HOST, port=settings.PORT,
                         user=settings.USER, passwd=settings.PASSWD,
                         db=settings.DB, cursorclass=DictCursor) as cursor:
        # SQL中的参数强烈推荐使用通过args传递,否则可能出现SQL注入漏洞利用
        cursor.execute(select_table_sql, args=('李满满',))
        # 返回查询结果集
        print cursor.fetchall()
```

* 对于查询其实cursor对象提供了fetchone(),fetchmany(size),fetchall()方法,分别用于取出单条记录,多条记录,所有记录

## 修改

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import MySQLdb
import settings


if __name__ == '__main__':
    update_table_sql = 'UPDATE REGUSER SET AGE=AGE+1 WHERE NAME=%s'

    with MySQLdb.connect(host=settings.HOST, port=settings.PORT,
                         user=settings.USER, passwd=settings.PASSWD,
                         db=settings.DB) as cursor:
        cursor.execute(update_table_sql, args=('李满满',))
        # 返回受影响的行数
        print cursor.rowcount
```

## 事务

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import MySQLdb
import settings


if __name__ == '__main__':
    drop_table_sql = "DROP TABLE REGUSER"

    with MySQLdb.connect(host=settings.HOST, port=settings.PORT,
                         user=settings.USER, passwd=settings.PASSWD,
                         db=settings.DB) as cursor:
        try:
            cursor.execute(drop_table_sql)
            # 提交事务
            cursor.connection.commit()
            # 返回影响的行数
            print cursor.rowcount
        except:
            # 发生错误时回滚
            cursor.connection.rollback()
```

* 对于事务其实conn对象提供了commit(),rollback()方法,分别用于事务提交(在初始化cursor对象的时候库内部就隐式的开启了一个新的事务)和事务回滚

# 实战练习

* 在无法指定cursorclass的情况下如何获取列名?

```python
#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.db import connections


class SqlResultMixin(object):
    sql = None
    sql_params = ()
    connection_name = None

    def get_connection(self):
        # 从Django settings.py设置中获取初始化后对应的connection
        return connections[self.connection_name]

    def get_cursor(self):
        conn = self.get_connection()
        return conn.cursor()

    def dict_fetchall(self):
        with self.get_cursor() as cursor:
            cursor.execute(self.sql, self.sql_params)
            # 通过cursor.description中每个元素的第一个元素来获取列名
            desc = cursor.description

            return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

    def dict_fetchone(self):
        with self.get_cursor() as cursor:
            cursor.execute(self.sql, self.sql_params)
            # 通过cursor.description中每个元素的第一个元素来获取列名
            desc = cursor.description

            return dict(zip([col[0] for col in desc], cursor.fetchone()))
```

