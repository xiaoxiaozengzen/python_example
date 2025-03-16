import sys

if __name__ == "__main__":
    sys.path.append("build/")
    from MyMath import MyClass

    obj = MyClass(10)
    obj.run()