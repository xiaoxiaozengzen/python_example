import sys

def list_test():
    def_list = ["my", "name", "is", "kele"]
    print("deff_list[0]: ", def_list[0])
    
    def_list[-1] = "kelechi"
    print("deff_list[3]: ", def_list[3])
    
    del def_list[0]
    print("deff_list[0]: ", def_list[0])
    
    def_list2 = def_list + ["kelechi"]
    print("deff_list2: ", def_list2)
    
    print("def_list[0:2]: ", def_list[0:2])
    
    def_list.append("kelechi")
    print("def_list: ", def_list)
    
    def_list.extend(["kelechi", "is", "my", "name"])
    print("def_list: ", def_list)
    
    
if __name__ == "__main__":
    list_test()