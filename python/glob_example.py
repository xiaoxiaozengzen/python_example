import glob
import sys
import os

def glob_test():
    for file in glob.glob(os.path.join(os.getcwd(), '*.py')):
        print(file)
    
if __name__ == '__main__':
    glob_test()