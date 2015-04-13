# KML-to-Layer-Post-Process

ArcPy script to process feature class attribute fields containing HTML.

Certain attribute fields contain information formatted as HTML tables
after running a 'KML to Layer' operation in ArcMap.This tool is designed
to parse the HTML in those fields and create new populated fields based
on the information in the HTML.

<b>IMPORTANT!</b>

This script requires the python library BeautifulSoup 4 (it is an xml/html parsing library). You will notice a folder called 'bs4' in the repository. If you do not have Beautiful Soup 4 installed on your machine you will require the 'bs4' folder to be stored in the same location as the 'KML Processing' toolbox provided for the 'KML to Layer Post Processing' tool to run. 

Alternatively, if you do not have Beautiful Soup 4 installed on your machine I would highly recommend it as it is a fantastic HTML and XML parser and will eliminate the need for the 'bs4' folder! I have found that it is a little tricky to install in some cases so I have provided detailed instructions below that I found worked quite well.

[Beautiful Soup 4 - INSTALLATION INSTRUCTIONS](/../master/docs_images/bs4_install.md)


 
 




 
 
