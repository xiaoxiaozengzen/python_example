import alog

# sys模块：用于提供对解释器相关的操作
import sys

# 在 Python 中，模块和包的搜索路径由 `sys.path` 列表决定。`sys.path` 列表包含了 Python 解释器在导入模块时会搜索的目录。以下是 Python 搜索包的步骤：

#     ### 1. 当前目录
#     Python 首先会在当前脚本所在的目录中搜索模块或包。

#     ### 2. `PYTHONPATH` 环境变量
#     如果在当前目录中没有找到，Python 会检查 `PYTHONPATH` 环境变量中指定的目录。`PYTHONPATH` 是一个以冒号（在 Unix 系统上）或分号（在 Windows 系统上）分隔的目录列表。

#     ### 3. 标准库目录
#     如果在 `PYTHONPATH` 中也没有找到，Python 会搜索标准库目录。标准库目录包含了 Python 自带的模块和包。

#     ### 4. 第三方包目录
#     最后，Python 会搜索安装的第三方包目录，通常是 `site-packages` 目录。这个目录包含了通过 `pip` 等工具安装的第三方包。

from alog.sub import Sub

def print_sys():
    print("sys.argv = ", sys.argv)
    print("sys.version = ", sys.version)
    # 其值=当前路径+PYTHONPATH+标准库目录+第三方包目录
    print("sys.path = ", sys.path)
    print("sys.platform = ", sys.platform)

if __name__ == '__main__':
    print("==========Before==========")
    print_sys()
    print("==========After==========")
  
    ret = alog.add.Add(1, 2)
    print("ret = ", ret)

    ret = Sub(1, 2)
    print("ret = ", ret)
