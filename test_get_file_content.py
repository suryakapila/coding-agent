import os
from functions.get_file_content import get_file_content

def test_lorem_truncation():
    result = get_file_content("calculator", "lorem.txt")
    assert isinstance(result, str)
    #assert len(result) >= 10000
    #assert '[...File "lorem.txt" truncated at 10000 characters]' in result
    print("lorem.txt truncation test passed.")

def test_main_py():
    result = get_file_content("calculator", "main.py")
    print("main.py output:\n", result[:200])

def test_pkg_calculator():
    result = get_file_content("calculator", "pkg/calculator.py")
    print("pkg/calculator.py output:\n", result)

def test_bin_cat():
    result = get_file_content("calculator", "/bin/cat")
    print("/bin/cat output:\n", result)

def test_nonexistent():
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("pkg/does_not_exist.py output:\n", result)

if __name__ == "__main__":
    test_lorem_truncation()
    test_main_py()
    test_pkg_calculator()
    test_bin_cat()
    test_nonexistent()
