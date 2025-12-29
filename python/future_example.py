# 在 Python 中，from __future__ import annotations 语句是用来引入 Python 3.7 中引入的类型注解功能的。
# 这个语句允许你在程序中声明变量或函数的类型，并由编译器或其他工具来检查代码的类型是否正确。

# 例如，下一个例子中，我们定义了一个 Node 类，它有一个整数值和一个指向下一个节点的指针。


from __future__ import annotations

class Node:
    def __init__(self, value: int, next: Node = None):
        self.value = value
        self.next = next

if __name__ == "__main__":
    # 创建节点
    node1 = Node(1)
    node2 = Node(2, node1)