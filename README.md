# Forensic_Tools
A collection of tools for forensic analysis. Still a work in progress...

# Usage:
python [script name.py] -h at any time for help

exif_extractor: use to extract exif metadata from images that contain them
python exif_extractor.py -i [image file path] -s [(optional)True or False save results to a text file?] -v [(optional)True or False show results after extraction]

metadata_extractor: use to extract metadata from documents such as office files and pdf documents. Document type is detected automatically.
python metadata_extractor.py -p [document file path] -d [(optional)decryption key] -s [(optional)True or False save results to a text file?]

firefox_scanner:  parses Firefox profile  databases and can extract cookies, history, Google searches, downloads, and form history. For more  details script name -h
