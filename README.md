# KML-to-Layer-Post-Process
ArcPy script to process feature class attribute fields containing HTML

Certain attribute fields contain information formatted as HTML tables
after running a 'KML to Layer' operation in ArcMap.This tool is designed
to parse the HTML in those fields and create new populated fields based
on the information in the HTML.

<b>IMPORTANT!</b>

This script requires the python library BeautifulSoup 4 (it is an xml/html parsing library). You will notice a folder called 'bs4' in the repository. If you do not have Beautiful Soup 4 installed on your machine you will require the 'bs4' folder to be stored in the same location as the 'KML Processing' toolbox provided for the 'KML to Layer Post Processing' tool to run. 

Alternatively, if you do not have Beautiful Soup 4 installed on your machine I would highly recommend it as it is a fantastic HTML and XML parser and will eliminate the need for the 'bs4' folder! I have found that it is a little tricky to install in some cases so I have provided detailed instructions below that I found worked quite well.

<b>STEP 1 - DOWNLOAD PIP INSTALLER</b>

Use the Python Package Index (better known as pip) to install beautiful soup. If you do not have pip installed navigate to
https://pip.pypa.io/en/latest/installing.html. To install right-click the link in figure 1 and select 'Save link as' to download the installer; save it to your desktop.

Figure 1:

 ![Alt text](/../master/ReadMe_images/Pip.png?raw=true "Install link")
 
<b>STEP 2 - INSTALL PIP</b>

Run the script in commandline as seen in figure 2, keep in mind that you must change the path to the location of the get-pip.py script, in our case it should be the desktop (Figure 2). When you run 'python get-pip.py' command as seen in figure 2, pip should install and the result should look like figure 3. If you receive an error <b>"'python' is not recognized as an internal or external command, operable program or batch file."</b>  the python environment variable is not set on your system (tells your computer where python is). See STEP 3 (optional) below figure 3 for adding this. Otherwise skip to <b>STEP 4</b>.

Figure 2:

 ![Alt text](/../master/ReadMe_images/commandline1.png?raw=true "Install link")
 
Figure 3:

 ![Alt text](/../master/ReadMe_images/commandline2.png?raw=true "Install link")

<b>STEP 3 (optional) - SET PYTHON ENVIRONMENT VARIABLES</b>

Navigate to Start > Right-click Computer > Properties > Advanced System Settings > Environment Variables. This will open the dialogue seen in figure 4 called "Environment Variables". Scrool down the 'System variables' list to the 'Path' variable (circled in red) select it and click it. In the "Variable Value" text box got the the very end of the string and add in 

;C:\Python27\ArcGIS10.3;C:\Python27\ArcGIS10.3\Scripts        

This could be different depending on your version of python, for example if you are at version 10.1 it would look like so

;C:\Python26\ArcGIS10.1;C:\Python26\ArcGIS10.1\Scripts

Keep clicking OK to exit all of the dialogues. Return to STEP 2. You should no longer get the <b>"'python' is not recognized as an internal or external command, operable program or batch file."</b> when running the 'python get-pip.py' command.

Figure 4:

 ![Alt text](/../master/ReadMe_images/env_var.png?raw=true "Install link")
 
 <b>STEP 4 - INSTALL BEAUTIFUL SOUP</b>
 
 Now the easiest part....open up command line and type the following command:
 
 pip install beautifulsoup4 
 
 and you should see the result in figure 5. Congratulations, you have installed Beautiful Soup 4!
 
  ![Alt text](/../master/ReadMe_images/commandline3.png?raw=true "Install link")
 
 




 
 
