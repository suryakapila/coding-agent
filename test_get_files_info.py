# write test cases to execute the following calls and print the results matching the format below
#get_files_info("calculator", ".")
#Result for current directory:
  #- main.py: file_size=719 bytes, is_dir=False
  #- tests.py: file_size=1331 bytes, is_dir=False
  #- pkg: file_size=44 bytes, is_dir=True

from functions.get_files_info import get_files_info

# Test 1: List files in the calculator directory (current directory ".")
print("Result for current directory:")
result = get_files_info("calculator", ".")
print(result)

print()

# Test 2: List files in a subdirectory
print("Result for 'pkg' directory:")
result = get_files_info("calculator", "pkg")
print(result)

print()

#Test /bin
print("Result for '/bin' directory:")
result = get_files_info("calculator", "/bin")
print(result)

# Test "../"
print("Result for '../' directory:")
result = get_files_info("calculator", "../")
print(result)
