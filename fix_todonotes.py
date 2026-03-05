import re
import os
import glob

files = glob.glob('lab/baldo_*.tex')
for f in files:
    with open(f, 'r') as file:
        content = file.read()

    # Remove all \todo commands
    # This regex handles simple \todo{...} and \todo[...]{...}
    # It might need adjustment if there are nested braces inside \todo

    # Using a simpler approach since we know the structure
    # We'll just use regex for the \todo[...] or \todo{...}

    content = re.sub(r'\\todo(?:\[[^\]]*\])?\{[^\}]*\}', '', content)

    with open(f, 'w') as file:
        file.write(content)
