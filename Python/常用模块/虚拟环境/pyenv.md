

---

* [模块简介](#模块简介)
* [实现原理](#实现原理)
* [调用顺序](#调用顺序)
* [安装部署](#安装部署)
* [常规套路](#常规套路)
  * [查看可安装版本](#查看可安装版本)
  * [安装指定的版本](#安装指定的版本)
  * [查看已安装版本](#查看已安装版本)
  * [卸载指定的版本](#卸载指定的版本)
  * [环境变量切换版本](#环境变量切换版本)
  * [删除版本环境变量](#删除版本环境变量)
  * [本地切换解释器](#本地切换解释器)
  * [全局切换解释器](#全局切换解释器)
*  [自动初始化](#自动初始化)

----

# 模块简介

> 第三方模块,可实现一台主机上轻松安装管理切换多个Python解释器版本

# 实现原理

> 借助PATH搜索优先级,将生成的\~/.pyenv/shims插入PATH的头部,调用并执行shims目录下的垫片程序

# 调用顺序

* 查看PYENV_VERSION环境变量是否设置,可通过pyenv shell指定或删除
* 查看当前目录是否存在.python-version文件,可通过pyenv local设置或切换
* 查看\~/.pyenv/下是否存在version文件,可通过pyenv global设置或切换

# 安装部署

```bash
pip install pyenv
```

# 常规套路

## 查看可安装版本

```bash
pyenv install --list
```

## 安装指定的版本

```bash
pyenv install 3.6.6
pyenv rehash
```

## 查看已安装版本

```bash
pyenv versions
```

## 卸载指定的版本

```bash
pyenv uninstall 3.7.0
pyenv rehash
```

## 环境变量切换版本

```python
pyenv shell 3.6.6
echo ${PYENV_VERSION}
```

## 删除版本环境变量

```bash
pyenv shell --unset
```

## 本地切换解释器

```bash
pyenv local 3.6.6
```

* 设置的值将写入./python-version中,下次启动时shims垫片程序会尝试读取此文件并启动指定解释器

## 全局切换解释器

```bash
pyenv global system
```

* 设置的值将写入~/.pyenv/version中,下次启动时shims垫片程序会尝试读取此文件并启动指定解释器

# 自动初始化

```bash
echo -e '# pyenv\nif command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
```

