----

* [简单介绍](#简单介绍)
* [功能演示](#功能演示)
* [调试日志](#调试日志)
* [扩展命令](#扩展命令)

----

# 简单介绍

> 主要用于命令行管理由(Typora+Xnip+Github)实现的在线开源笔记,同类产品如有道,印象笔记等

# 功能演示

> 灵感来源于Django灵活的Management.BaseCommand

> python manage.py

````bash

Type 'manage.py <subcommand> -h or --help' for help on a specific subcommand.

Available subcommands:
[ typora_manage.core ]
clean_images
clean_pycfiles
generate_toc

````

> python manage.py clean --help

````python
usage: manage.py clean [-h] -p PATH

Auto clean unused typaro assets images

optional arguments:
  -h, --help  show this help message and exit
  -p PATH     typaro notes root directory
````

# 调试日志

> python manage.py clean -p .

```bash
2019-01-02 16:15:15,024 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20190102141005340.png) in ../Python/中级教程/魔术方法/__ror__.assets, deleted
2019-01-02 16:15:15,036 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181219174246463.png) in ../Python/常用模块/存储接口/MySQL-python.assets, deleted
2019-01-02 16:15:15,052 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181213161310651.png) in ../Python/常用模块/进线协程/multiprocessing.assets, deleted
2019-01-02 16:15:15,052 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181215082826704.png) in ../Python/常用模块/进线协程/multiprocessing.assets, deleted
2019-01-02 16:15:15,161 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181230084044645.png) in ../Django/基础教程/入门相关/投票应用-管理站点.assets, deleted
2019-01-02 16:15:15,161 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181230081414337.png) in ../Django/基础教程/入门相关/投票应用-管理站点.assets, deleted
2019-01-02 16:15:15,161 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181230084207425.png) in ../Django/基础教程/入门相关/投票应用-管理站点.assets, deleted
2019-01-02 16:15:15,162 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181230081648946.png) in ../Django/基础教程/入门相关/投票应用-管理站点.assets, deleted
2019-01-02 16:15:15,162 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181230084907752.png) in ../Django/基础教程/入门相关/投票应用-管理站点.assets, deleted
2019-01-02 16:15:15,162 - typora_manage.core.management.commands.clean - /Users/manmanli/Github/notes/TYPORA_manage/typora_manage/core/management/commands/clean.py - 59 - WARNING - Found unused image(image-20181230084428624.png) in ../Django/基础教程/入门相关/投票应用-管理站点.assets, deleted
```

# 扩展命令

> 只需在TYPORA_manage/typora_manage/core/management/commands下仿照clean.py编写Py文件,编写继承自BaseCommand实现add_parser_arguments和handle方法的Command类即可,略

