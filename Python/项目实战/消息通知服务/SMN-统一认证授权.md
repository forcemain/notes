# 简单概述

> 为SMN(消息通知服务)组件提供WEB层和API层统一认证授权支持

# 创建AUTH应用

> cd smn_component
>
> python manage.py startapp auth
>
> \# 初始结构 
>
> tree auth/

```bash
auth/                  # 应用名
├── __init__.py        # 表示应用是一个包
├── admin.py           # 管理站点配置,深度定制通常创建admin包,内部再对每个模型独立定制化
├── apps.py            # 应用加载入口文件,可通过钩子函数在加载前加载指定配置,如Django Signal
├── migrations         # 创建的历史迁移脚本目录
│   └── __init__.py 
├── models.py          # 数据库驱动应用的模型文件,深度定制通常创建models包,内部再对每个模型独立定制化
├── tests.py           # 单元测试文件,深度定制通常创建tests包,内部再对每个模型独立定制化
└── views.py           # 视图处理文件,深度定制通常创建views包,内部再对每个模型独立定制化
```

> \# 规范结构
>
>  tree auth/

```bash
auth/
├── __init__.py
├── admin
│   └── __init__.py
├── apps.py
├── migrations
│   └── __init__.py
├── models
│   ├── __init__.py
├── tests
│   └── __init__.py
└── views
    └── __init__.py
```

- 应用是一个Web应用程序(必须是一个Python包),它完成具体事项,如博客应用,投票应用等,项目是相关配置和应用的集合,一个项目可以包含多个应用,一个应用也可以被打包分发给不同的项目使用
- 通过startapp命令可以自动生成应用的基本目录结构,由于manage.py与应用同级,所以可以在代码中任意位置直接引用这些应用甚至自定义的Python包

# 创建AUTH应用模型

> cd smn_component

