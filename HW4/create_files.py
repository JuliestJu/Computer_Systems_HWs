def create_test_files():
    file_contents = {
        'file1.txt': """This is a sample text file.
It contains multiple lines.
This file is used to test the keyword search.
keyword1 is present in this file.""",
        'file2.txt': """Another example text file for testing.
This one also has multiple lines.
We are testing keyword2 in this file.
Let's see if the script can find keyword2.""",
        'file3.txt': """This is the third text file.
It contains different content.
We need to search for keyword3 in this file.
keyword3 should be found by the script. keyword3 keyword3 keyword3"""
    }

    for file_name, content in file_contents.items():
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content)

if __name__ == "__main__":
    create_test_files()