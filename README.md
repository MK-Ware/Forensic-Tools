# Forensic_Tools
A collection of tools for forensic analysis. Still a work in progress...

# Disclaimer
For educational use only. Author not responsible for malicious use!

# Dependencies:
lxml: https://pypi.python.org/pypi/lxml/3.7.3

PyPDF2: https://pypi.python.org/pypi/PyPDF2/1.26.0

# Usage:
python [script name.py] -h at any time for help

exif_extractor: use to extract exif metadata from images that contain them
python exif_extractor.py -i [image file path] -s [(optional)True or False save results to a text file?] -v [(optional)True or False show results after extraction]

metadata_extractor: use to extract metadata from documents such as office files and pdf documents. Document type is detected automatically.
python metadata_extractor.py -p [document file path] -d [(optional)decryption key] -s [(optional)True or False save results to a text file?]

firefox_scanner: use to parse Firefox profile  databases and can extract cookies, history, Google searches, downloads, and form history. Results are saved to a html table with background highlighting for easier reading. For more  details script name -h

skype_scanner: use to parse Skype database. Can extract account details, contacts with their full details, call log, and messages. Results are saved to a html table with background highlighting for easier reading. For details, script name -h

The common_methods.py file contains functions that are necessary for some scripts to work. The templates directory contains static html templates required to organize the results in neat html tables. Both need to be present and unmodified in order for the scripts to work properly.
