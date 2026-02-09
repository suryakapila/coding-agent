from functions.run_python_file import run_python_file

def test():
    # Test 1: Run a simple Python file without arguments
    result = run_python_file("calculator", "main.py")
    print(result)

    # Test 2: Run a python file with arguments
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)

    # Test 3: Attemp to run calculator with tests.py
    result = run_python_file("calculator", "tests.py")
    print(result)

    # Test 4: Attempt to run form a different directory
    result =  run_python_file("calculator", "../main.py")
    print(result)

    # Test 5: Attempt to run a non-xistent file
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    
    # Test 6: Attempt ti run a text file
    result = run_python_file("calculator", "lorem.txt")
    print(result)


if __name__ == "__main__":
    test()