----

* [模块简介](#模块简介)
* [安装部署](#安装部署)
* [常规套路](#常规套路)
  * [全局环境变量设置](#全局环境变量设置)
  * [创建独立虚拟环境](#创建独立虚拟环境)
  * [管理第三方依赖包](#管理第三方依赖包)
  * [更新PYPI源的地址](#更新PYPI源的地址)
  * [在虚拟环境中运行](#在虚拟环境中运行)
  * [一键激活虚拟环境](#一键激活虚拟环境)
* [团队协作](#团队协作)
* [错误汇总](#错误汇总)

----

# 模块简介

> 第三方模块,可实现一台主机上轻松安装管理切换Python虚拟开发环境,通过Pipfile和Pipfile.lock来代替Virtualenv和pip虚拟环境包管理

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
cd myproject
pipenv --python ~/.pyenv/versions/3.6.6/bin/python
```

## 管理第三方依赖包

> 允许我们在未激活虚拟环境的情况下优雅管理虚拟环境第三方依赖包

```bash
# 只安装Pipfile.lock中正式环境包
pipenv install
# 安装Pipfile.lock中正式环境包和开发环境包
pipenv sync
# 卸载虚拟环境所有包,但不会自动更新Pipfile和Pipfile.lock
pipenv uninstall --all
# 删除Pipfile和Pipfile.lock中所有条目并更新
pipenv uninstall --all-dev
# 卸载虚拟环境指定包,会自动更新Pipfile和Pipfile.lock
pipenv uninstall django
pipenv uninstall pymysql
# 安装指定版本的包到虚拟环境,可加-r参数指定requirements.txt文件
pipenv install django
pipenv install PyMySQL
# 安装最新版本的包到虚拟环境,-d标记开发环境依赖的包,可加-r参数指定requirements.txt文件
pipenv install selenium --dev
```

## 查看虚拟环境包依赖

```bash
# 可加--json输出json形式
pipenv graph
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

## 在虚拟环境中运行

```bash
pipenv run pip freeze
# 尝试启动Django应用
pipenv run python manage.py runserver 0.0.0.0:80
```

## 一键激活虚拟环境

```bash
pipenv shell
```

* 通过如上指令即可进入virtualenv虚拟开发环境,此虚拟环境默认Python Shll为3.6.6

# 团队协作

> 推荐将Pipfile和Pipfile.lock基于版本控制管理

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

