[![Digital-Forensics-eDiscovery-and-eInvestigation.jpg](https://s10.postimg.org/4cb5qvth5/Digital-_Forensics-e_Discovery-and-e_Investigation.jpg)](https://postimg.org/image/p97dvjrhx/)

# Forensic_Tools
A collection of tools for forensic analysis. Still a work in progress...

# Disclaimer
For educational use only. Author not responsible for malicious use!

# Dependencies:
lxml: https://pypi.python.org/pypi/lxml/3.7.3

olefile: https://pypi.python.org/pypi/olefile/0.44

PyPDF2: https://pypi.python.org/pypi/PyPDF2/1.26.0

# Usage:
python [script name.py] -h at any time for help

exif_extractor: use to extract exif metadata from images that contain them
python exif_extractor.py -i [image file path] -s [(optional)True or False save results to a text file?] -v [(optional)True or False show results after extraction]

metadata_extractor: use to extract metadata from documents such as office files and pdf documents. Document type is detected automatically.
python metadata_extractor.py -p [document file path] -d [(optional)decryption key] -s [(optional)True or False save results to a text file?]

firefox_scanner: use to parse Firefox profile  databases and can extract cookies, history, Google searches, downloads, and form history. Results are saved to a html table with background highlighting for easier reading. For more  details script name -h

facebook_scanner.py: use to analyze facebook app and facebook messenger app artifacts, still fairly new and currently only tested with lite versions. Can extract messages with time, links, attachments, contacts with profile pictures and profile links, and details regarding the accounts used to log into the app plus more.

skype_scanner: use to parse Skype database. Can extract account details, contacts with their full details, call log, and messages. Results are saved to a html table with background highlighting for easier reading. For details, script name -h

whatsapp_scanner: use to parse What'sapp msgstoremsgstore and wa databases. Can extract messages with timestamps, location coordinates, media with media type, url, duration, timestamps and more, and contacts with full details. For details, script name -h

chrome_scanner: use to parse chrome databases. Can extract downloads with full details (like start and end times, download links, full download size, percentage downloaded etc), History, cookies, Google searches, and login credentials. python chrome_scanner.py -h for details.

wlan_reader: use to get WIFI network history from windows registry. You don't have to give it any arguments, just make sure you run the command prompt as administrator, then enter python wlan_reader.py.

The common_methods.py file contains functions that are necessary for some scripts to work. The templates directory contains static html templates required to organize the results in neat html tables. Both need to be present and unmodified in order for the scripts to work properly.
