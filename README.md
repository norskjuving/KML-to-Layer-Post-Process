
# KML-to-Layer-Post-Process

[How To](https://github.com/cameronezzi/KML-to-Layer-Post-Process#how-to) | [Results]

ArcPy script to process feature class attribute fields containing HTML.

Certain attribute fields contain information formatted as HTML tables
after running a 'KML to Layer' operation in ArcMap.This tool is designed
to parse the HTML in those fields and create new populated fields based
on the information in the HTML.

##IMPORTANT!

This script requires the python library BeautifulSoup 4 (it is an xml/html parsing library). You will notice a folder called 'bs4' in the repository. If you do not have Beautiful Soup 4 installed on your machine you will require the 'bs4' folder to be stored in the same location as the 'KML Processing' toolbox provided for the 'KML to Layer Post Processing' tool to run. 

Alternatively, if you do not have Beautiful Soup 4 installed on your machine I would highly recommend it as it is a fantastic HTML and XML parser and will eliminate the need for the 'bs4' folder! I have found that it is a little tricky to install in some cases so I have provided detailed instructions below that I found worked quite well.

[BeautifulSoup 4 - INSTALLATION INSTRUCTIONS](/../master/docs_images/bs4_install.md)


## How To...

1. Download the 'KML Processing.tbx' toolbox and 'KML to Layer Post Processing.py' to the same file folder.

2. Create a folder connection to the 'KML Processing.tbx' in ArcMap or ArcCatalog. You are ready to run the tool. 

3. The dialog should look like the following:



![Tool Dialogue Window](/../master/docs_images/GUI.png?raw=true)

### Result of KML to Layer Post Processing vs KML to Layer

#### KML to Layer

![Screenshot result of KML to Layer](/../master/docs_images/result_old.png?raw=true)

The result of the 'KML to Layer' tool contains all attribute information in a field called 'PopupInfo' and appears as an embedded HTML table. This is actually HTML markup contained in a text field. The user has no access to the attribute information when it is stored in this format. Additionally, there is only 1 attribute being displayed in this HTML table, where the highlighted feature has 3 attributes in reality. The 'KML to Layer' tool has generated 3 stacked polygons each containing a separate attribute in HTML format. (Note in the lower left corner of the Popup window we are viewing '1 of 3' stacked polygons).

#### KML to Layer Post Processing

![Screenshot result of KML to Layer](/../master/docs_images/result_new.png?raw=true)

The result of the 'KML to Layer Post Processing' tool dissolves the stacked geometries into a single geometry and then pulls the attribute information out of the 'PopupInfo' fields HTML markup using the BeautifulSoup 4 python library which is designed for HTML/XML parsing . The result as seen in the above image leaves us with a single geometry containing individual attribute fields and values.

[Top of Page](https://github.com/cameronezzi/KML-to-Layer-Post-Process)
 




 
 
