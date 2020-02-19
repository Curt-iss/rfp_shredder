#!/usr/bin/env python3


# Imports ---------------------------------------------------------------------

from pathlib import Path
import subprocess
import sys

# Functions -------------------------------------------------------------------

# Main ------------------------------------------------------------------------

if __name__ == '__main__':
    # Use sys.argv to get a list of command line arguments
    # If you execute the scripts like: python3 pdf_to_docx.py some/file/path
    #
    # Then sys.argv[1] is the string 'some/file/path'
    #
    # FYI: sys.argv[0] is always the name of the script file, so 'pdf_to_docx.py'
    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])
        
        #Check the file extension for 'pdf'
        if pdf_path.suffix == '.pdf':
            # Format the command 
            command_str = f'lowriter --invisible --convert-to docx "{pdf_path}"'

            # Make a call to libreoffice
            subprocess.call(command_str, shell = True)

        else:
            print('Please give me a path to a pdf...')
            sys.exit(1)
    else:
        print('Please give me a path to a pdf...')
        sys.exit(1)