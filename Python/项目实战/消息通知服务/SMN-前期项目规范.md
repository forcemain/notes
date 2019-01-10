# 简单概述

> 规范化SMN(消息通知服务)组件项目

# 创建项目

> django-admin startproject smn_component
>
> tree smn_component/

```bash
mysite/               # 项目目录
├── manage.py         # 与项目交互的命令行工具,支持扩展django.core.management.base.BaseCommand
└── smn_component     # 入口包名,默认与项目同名,支持自定义,个人通常会自定义为entrance作为入口应用
    ├── __init__.py   
    ├── settings.py   # 项目配置
    ├── urls.py       # 项目URL路由入口
    └── wsgi.py       # WSGI服务器,仅用于测试环境
```

* 将原入口应用smn_component改为entrance涉及到manage.py,settings.py,wsgi.py文件

# 应用集配置

> cd smn_component
>
> vim smn_component/settings.py 

```bash
CUSTOMIZED_APPS = [
    'entrance',                       # 自定义的应用
]

INSTALLED_APPS = CUSTOMIZED_APPS + [
    'django.contrib.admin',           # 管理后台应用  
    'django.contrib.auth',            # 认证授权应用
    'django.contrib.contenttypes',    # 内容类型应用
    'django.contrib.sessions',        # 会话管理应用
    'django.contrib.messages',        # 消息传递应用
    'django.contrib.staticfiles',     # 静态文件应用
]

INSTALLED_APPS = INSTALLED_APPS + [

]
```

* INSTALLED_APPS中包含所有激活的应用,这些应用将被Django顺序加载并管理,所以将应用分为三层,清晰明了

# 数据库配置

> cd smn_component
>
> vim smn_component/settings.py 

```bash
DATABASES = {
    'default': {                                        # 默认使用的数据库,可配置多个选用
        'ENGINE': 'django.db.backends.sqlite3',         # 数据库引擎驱动
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),   # Sqlite3数据库文件绝对路径
    }
}
```

* DATABASES中包含数据库配置,django.db.backends还支持postgresql_psycopg2,mysql,oracle等众多主流[数据库](https://www.yiyibooks.cn/xx/django_182/ref/settings.html#databases)

```bash
python manage.py makemigrations
python manage.py migrate
```

* 由于INSTALLED_APPS中大部分应用都依赖数据库模型,所以首先需要通过makemigrations为这些激活的应用创建迁移脚本然后通过migrate命令将迁移脚本转换为Sql语句写入数据库

# 测试服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

* 通过runserver命令运行支持动态重载的测试服务器,可通过地址:端口形式自定义监听,[更多参数](https://www.yiyibooks.cn/xx/django_182/ref/django-admin.html#django-admin-runserver)

