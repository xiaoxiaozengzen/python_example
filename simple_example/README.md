# pip

```bash

# 安装
# 最新版本
pip install Django
# 指定版本号
pip install Django==2.0.0
# 最小版本
pip install 'Django>=2.0.0'

# 升级包
pip install --upgrade Django
# 卸载包
pip uninstall SomePackage
# 搜索包
pip search SomePackage
# 显示安装包信息
pip show
# 查看指定包的详细信息
pip show -f SomePackage
# 列出已安装的包
pip list
# 查看可升级的包
pip list -o

pip freeze > requirement.txt # 锁版本
pip install -r requirement.txt # 指定安装版本
pip install --user install black # 安装到用户级目录`
```
