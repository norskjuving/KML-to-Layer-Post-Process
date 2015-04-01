#-------------------------------------------------------------------------------
# Name:        KML to Layer Post-Processing

# Purpose:     Certain attribute fields contain information formatted as HTML tables
#              after running a 'KML to Layer' operation in ArcMap.This tool is designed
#              to parse the HTML in those fields and create new populated fields based
#              on the information in the HTML.
#
# Author:      Cameron McEvenue, Esri Canada
#
# Created:     20/03/2015
# Copyright:   (c) Cameron McEvenue, Esri Canada 2015

#-------------------------------------------------------------------------------


import arcpy, os, sys, time, datetime,traceback, numpy
from bs4 import BeautifulSoup


def postProcess(featureClass,htmlField,outWorkspace,outFC,UID_field):

    try:
        arcpy.env.workspace = outWorkspace
        arcpy.SetLogHistory(True)
        arcpy.env.overwriteOutput = True


        desc = arcpy.Describe(featureClass)

        new_fc = os.path.join(outWorkspace,outFC)

        fields = [UID_field, htmlField]

        readTime = 2.5

        #Create list of unique field values for UID_field variable
        UID_list = arcpy.da.TableToNumPyArray(featureClass,UID_field)
        UID_list = numpy.unique(UID_list[UID_field])
        UID_list = UID_list.tolist()


        #Create new feature class to dissolve stacked geometries/insert HTML attributes
        arcpy.SetProgressor("default", "Creating new feature class...")
        arcpy.AddMessage("Creating new feature class '{0}'...10%".format(outFC))
        time.sleep(readTime)
        arcpy.CreateFeatureclass_management(outWorkspace,outFC,desc.shapeType.upper(),featureClass,"DISABLED","DISABLED",desc.spatialReference)
        new_fc = os.path.join(outWorkspace,outFC)

        #get the unique field names from the HTML fields of the first UID in UID_list
        where = """ {0} = '{1}' """.format(arcpy.AddFieldDelimiters(featureClass,fields[0]),UID_list[0])

        arcpy.SetProgressor("default", "Adding new attribute fields...")
        arcpy.AddMessage("Adding new attribute fields...")
        time.sleep(readTime)
        new_fields_list = []
        for row in arcpy.da.SearchCursor(featureClass,fields, where):
            soup = BeautifulSoup(row[1])
            elements = soup.findAll('td',text=True)
            fieldName = (elements[3].text).replace(" ","_")

            #create a list of new fields (to use with insert cursor)
            new_fields_list.append(fieldName)
            arcpy.AddField_management(new_fc,fieldName, field_type='TEXT')


        #Create a temporary dissolved feature class to retrieve geometries
        #This step is necessary when two features have the same UID (ran into this case with 1 test dataset)
        aggregateGeom = arcpy.Dissolve_management(featureClass,"_dissolve",["Shape_Area",UID_field],"","SINGLE_PART","DISSOLVE_LINES")

        arcpy.SetProgressor("default", "Building geometry...")
        arcpy.AddMessage("Building geometry...50%")
        time.sleep(readTime)
        #Generates unique geometries in new feature class
        with arcpy.da.InsertCursor(new_fc,["SHAPE@",UID_field]) as i_cursor:
            for s_row in arcpy.da.SearchCursor(aggregateGeom,["SHAPE@",UID_field],"","",sql_clause=(None, 'ORDER BY ' + UID_field + ' ASC')):
                    i_cursor.insertRow(s_row)
        del i_cursor

        arcpy.Delete_management(aggregateGeom)

        new_fields_list.insert(0,UID_field)
        new_fields_list.insert(1,arcpy.Describe(new_fc).OIDFieldName)

        arcpy.SetProgressor("default", "Parsing HTML and populating attributes...")
        arcpy.AddMessage("Parsing HTML and populating attributes...75%")
        time.sleep(readTime)

        objID = 1
        #Populate attribute fields with Data contained in HTML block
        with arcpy.da.UpdateCursor(new_fc,new_fields_list) as u_cursor:
            for u_row in u_cursor:

                sql = """{0} = {1}""".format(arcpy.AddFieldDelimiters(new_fc,new_fields_list[1]),objID)
                arcpy.MakeFeatureLayer_management(new_fc,"source_layer",sql)
                arcpy.MakeFeatureLayer_management(featureClass,"target_layer")
                arcpy.SelectLayerByLocation_management("target_layer","ARE_IDENTICAL_TO","source_layer","","NEW_SELECTION")

                for s_row in arcpy.da.SearchCursor("target_layer",fields,sql_clause=(None, 'ORDER BY ' + fields[0] + ' ASC')):
                    if s_row[0] == u_row[0]:
                        soup = BeautifulSoup(s_row[1])
                        elements = soup.findAll('td',text=True)
                        fieldName = (elements[3].text).replace(" ","_")
                        value = elements[4].text
                        field_index = new_fields_list.index(fieldName)
                        u_row[field_index] = value
                        u_cursor.updateRow(u_row)
                objID += 1

        arcpy.AddMessage("Finished Processing...100%")
        time.sleep(readTime)
        del s_row
        del u_row
        del u_cursor
    except arcpy.ExecuteError:
        # Get the tool error messages
        #
        msgs = arcpy.GetMessages(2)

        # Return tool error messages for use with a script tool
        #
        arcpy.AddError(msgs)

        # Print tool error messages for use in Python/PythonWin
        #
        #change this file path to a location on your computer
        text_file = open("C://log.txt",'w')
        text_file.write(msgs)
        text_file.close()
        print msgs

    except:
        # Get the traceback object
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]

        # Concatenate information together concerning the error into a message string
        #
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
        msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

        # Return python error messages for use in script tool or Python Window
        #
        arcpy.AddError(pymsg)
        arcpy.AddError(msgs)

        # Print Python error messages for use in Python / Python Window
        #

        #change this file path to a location on your computer
        text_file = open("C://log.txt",'w')
        text_file.write(pymsg + "\n")
        text_file.write(msgs)
        text_file.close()

        print pymsg + "\n"
        print msgs



if __name__ == "__main__":

    # Gather inputs
    featureClass = arcpy.GetParameterAsText(0)
    htmlField = arcpy.GetParameterAsText(1)
    outWorkspace = arcpy.GetParameterAsText(2)
    outFC = arcpy.GetParameterAsText(3)
    UID_field = arcpy.GetParameterAsText(4)
##    featureClass = r"D:\SIDE_PROJECTS\K_27_Mississauga_GF_Character_Areav3.gdb\Placemarks\Polygons"
##    htmlField = "PopupInfo"
##    outWorkspace= r"D:\SIDE_PROJECTS\K_27_Mississauga_GF_Character_Areav3.gdb"
##    outFC = "test1"
##    UID_field = "Name"
    postProcess(featureClass,htmlField,outWorkspace,outFC,UID_field)