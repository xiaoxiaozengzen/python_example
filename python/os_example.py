import os

def os_path():
    print("os.path.abspath(__file__): ", os.path.abspath(__file__))
    print("os.path.basename(__file__): ", os.path.basename(__file__))
    print("os.path.dirname(__file__): ", os.path.dirname(os.getcwd()))
    print("os.path.exists(__file__): ", os.path.exists(__file__))
    print("os.path.expnduser('~'): ", os.path.expanduser('~'))
    print("os.path.expandvars('$HOME'): ", os.path.expandvars('$HOME'))
    print("os.path.getatime(__file__): ", os.path.getatime(__file__))
    print("os.path.getmtime(__file__): ", os.path.getmtime(__file__))
    print("os.path.getctime(__file__): ", os.path.getctime(__file__))
    print("os.path.getsize(__file__): ", os.path.getsize(__file__))
    print("os.path.isabs(__file__): ", os.path.isabs(__file__))
    print("os.path.isfile(__file__): ", os.path.isfile(__file__))
    print("os.path.isdir(__file__): ", os.path.isdir(__file__))
    print("os.path.islink(__file__): ", os.path.islink(__file__))
    print("os.path.ismount(__file__): ", os.path.ismount(__file__))
    print("os.path.join('a', 'b', 'c'): ", os.path.join('a', 'b', 'c'))
    print("os.path.normcase(__file__): ", os.path.normcase(__file__))
    print("os.path.normpath(__file__): ", os.path.normpath(__file__))
    print("os.path.realpath(__file__): ", os.path.realpath(__file__))
    print("os.path.relpath(__file__): ", os.path.relpath(__file__))
    print("os.path.split(__file__): ", os.path.split(os.getcwd()))
    print("os.path.splitdrive(__file__): ", os.path.splitdrive(os.getcwd()))
    
def open_test():
    file = os.path.join(os.getcwd(), 'ignore_list')
    with open(file, 'r') as f:
        content = f.read()
    
    print("", content.splitlines())
    print("", content.split())
    
if __name__ == '__main__':
    os_path()
    open_test()