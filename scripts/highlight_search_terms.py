#!/usr/bin/env python3

# Imports --------------------------------------
import docx
import StringIO

'''
doc = docx.Document('test.docx')
for block in iter_block_items(doc):
    print(block.text)
'''


# Pass in the file name to open:
def highlight_terms(file_name):
    # get the input from user about file name
    with open(file_name, 'rb') as f:
        source_stream = StringIO(f.read())

        # Check if it worked, should print True.
        print(source_stream.readable())

        # Get all the contents from the file.
        content = source_stream.getvalue()
        for line in content: 
            # code here for highlighting and boldening words
            line = line

    document = docx.Document(source_stream)
    source_stream.close()
    
    target_stream = StringIO()
    document.save(target_stream)

if __name__ == '__main__':
    # How can we pass in the file name to here?
    # highlight_terms(the_file)
    pass