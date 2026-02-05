import python_client.desc

def pretty_print_desc(desc):
    print(desc)

def main():
    operation = "TESTING_OPERATION"
    invobjpath = "LICENSE"
    outvobjpath = "README.md"
    args = ["arg1","arg2","arg3","arg4","arg5"]

    test_desc = python_client.desc.Descriptor(operation, args, [invobjpath, outvobjpath], [outvobjpath])
    pretty_print_desc(test_desc)

    serialized_desc = test_desc.serialize()
    #print(serialized_desc)
    #print("-----------------------------------------------")
    deserialized_desc = python_client.desc.deserialize(serialized_desc)

    pretty_print_desc(deserialized_desc)

if __name__ == '__main__':
    main()