----

* [模块简介](#模块简介)
* [安装部署](#安装部署)
* [常规套路](#常规套路)
  * [全局环境变量设置](#全局环境变量设置)
  * [创建独立虚拟环境](#创建独立虚拟环境)
  * [管理第三方依赖包](#管理第三方依赖包)
  * [更新PYPI源的地址](#更新PYPI源的地址)
  * [利用虚拟环境开发](#利用虚拟环境开发)
* [错误汇总](#错误汇总)

----

# 模块简介

> 第三方模块,可实现一台主机上轻松安装管理切换Python虚拟开发环境

* 此模块是Python官方推荐的包管理工具,综合了virtualenv,pip,pyenv三者的功能,使用Pipfile和Pipfile.lock来自动管理依赖包,当通过pipenv添加或删除包时,它会自动维护Pipfile文件并同时生成Pipfile.lock来锁定安装包的版本和依赖信息,避免构建错误

# 安装部署

```bash
pip install pipenv
```

# 常规套路

## 全局环境变量设置

```bash
echo -e '# pipenv\nexport PIPENV_VENV_IN_PROJECT=1' >> ~/.bash_profile
source ~/.bash_profile
```

* 设置在每个项目根目录下创建虚拟环境.venv

## 创建独立虚拟环境

```python
mkdir myproject
pipenv --python ~/.pyenv/versions/3.6.6/bin/python
```

## 管理第三方依赖包

> pipenv操作指令和pip完全一致,不再重复说明

```bash
pipenv install django==1.11.5
# 安装MySQL-python For Mac, 其它系统比较简单,略
# ---可能出现的问题
# fatal error: 'my_config.h' file not found	
# ---
# 已安装可跳过
brew install mysql
brew unlink mysql
brew install mysql-connector-c
sed -i -e 's/libs="$libs -l "/libs="$libs -lmysqlclient -lssl -lcrypto"/g' /usr/local/bin/mysql_config
pip install MySQL-python
brew unlink mysql-connector-c
brew link --overwrite mysql
```



## 更新PYPI源的地址

> vim myproject/Pipfile

```ini
[[source]]
name = "pypi"
url = "https://pypi.doubanio.com/simple"
verify_ssl = true
```

* 可改为国内[豆瓣源](https://pypi.doubanio.com/simple/),加快下载速度

## 利用虚拟环境开发

```bash
pipenv shell
```

* 通过如上指令即可进入virtualenv虚拟开发环境,此虚拟环境默认Python Shll为3.6.6

# 错误汇总

```bash
# 错误详情
---
Uninstalling setuptools-18.5:
Could not install packages due to an EnvironmentError: [('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/markers.pyc', '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/markers.pyc', "[Errno 1] Operation not permitted: '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/markers.pyc'"), ('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/__init__.py', '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/__init__.py', "[Errno 1] Operation not permitted: '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/__init__.py'"), ('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/markers.py', '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/markers.py', "[Errno 1] Operation not permitted: '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/markers.py'"), ('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/__init__.pyc', '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/__init__.pyc', "[Errno 1] Operation not permitted: '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib/__init__.pyc'"), ('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib', '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib', "[Errno 1] Operation not permitted: '/private/tmp/pip-uninstall-xG0njw/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/_markerlib'")]
---
# 解决办法
---
pip install pipenv --upgrade --ignore-installed
---
```

