# Overview

`venv`类似docker的概念，创建一个独立的python环境。

# 使用

```bash
mkdir venv
cd venv
python3 -m venv .

# 创建完之后可以发现路径下有
# $ls
# bin  include  lib  lib64  pyvenv.cfg  share

# $whcih python3
# /mnt/workspace/cgz_workspace/Exercise/python_example/venv/bin/python3

# 查看当前的site-package所在路径
# python -m site
# python -c "import site; print(site.getsitepackages())"   # 全局 site-packages（may raise on some venvs）
# python -c "import site; print(site.getusersitepackages())" # 用户级 site-packages

# 查看某个package安装的路径
# pip show <package-name>   # 查 Location 字段
# # 或
# python -c "import <package_name> as m, inspect; print(inspect.getfile(m))"
```