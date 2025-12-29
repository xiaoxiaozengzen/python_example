import tempfile

def test():
    tmd_file = tempfile.NamedTemporaryFile()
    print("tmd_file.name: ", tmd_file.name)
    
if __name__ == '__main__':
    test()