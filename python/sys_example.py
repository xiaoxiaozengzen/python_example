import sys

def sys_test():
    print("sys.argv: ", sys.argv)
    print("sys.executable: ", sys.executable)
    print("sys.byteorder: ", sys.byteorder)
    
if __name__ == '__main__':
    sys_test()