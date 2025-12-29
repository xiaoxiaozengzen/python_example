import shutil
import os

if __name__ == '__main__':
    if not os.path.exists("file.bak"):
        with open('file.bak', 'w') as f:
            f.write('Hello, world!')
    shutil.copy('ignore_list', 'file.bak')
    shutil.move('file.bak', 'file.bak.bak')
    shutil.copytree(os.getcwd(), 'test')
    shutil.rmtree('test')
    shutil.copyfile('ignore_list', 'file.bak')
    os.remove('file.bak')
    os.remove('file.bak.bak')