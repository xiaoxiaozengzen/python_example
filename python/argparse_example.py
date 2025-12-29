import argparse
import sys

if __name__ == '__main__':
    print("sys.argc:", len(sys.argv))
    print("sys.argv:", sys.argv)
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-fl', '--file', help='file help', action='store', default='', required=True)
    parser.add_argument('-f', '--foo', help='foo help', action='store_true', default=False)
    parser.add_argument('-b', '--bar', help='bar help', action='store', default=10, type=int)
    parser.add_argument('-a', '--arch', help='arch help', action='store', default='x86', choices=['x86', 'x64'])
    parser.add_argument('-v', '--var', help='var help', action='store', default='var', dest='my_var')
    
    parser_ret = parser.parse_args()
    print("parser_ret:", parser_ret)
    
    print("file:", parser_ret.file)
    print("foo:", parser_ret.foo)
    print("bar:", parser_ret.bar)
    print("arch:", parser_ret.arch)
    print("var:", parser_ret.my_var)