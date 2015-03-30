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

    arcpy.env.workspace = outWorkspace
    arcpy.SetLogHistory(True)
    arcpy.env.overwriteOutput = True

    desc = arcpy.Describe(featureClass)

##    wkspDesc = arcpy.Describe(arcpy.env.workspace)
##
##    if wkspDesc.workspaceType == "FileSystem":
##       outFC = outFC + ".shp"

    new_fc = os.path.join(outWorkspace,outFC)

    fields = [UID_field, htmlField]



    #Create list of unique field values for UID_field variable
    UID_list = arcpy.da.TableToNumPyArray(featureClass,UID_field)
    UID_list = numpy.unique(UID_list[UID_field])
    UID_list = UID_list.tolist()

    #Create new feature class to dissolve stacked geometries/insert HTML attributes
    arcpy.CreateFeatureclass_management(outWorkspace,outFC,desc.shapeType.upper(),featureClass,"DISABLED","DISABLED",desc.spatialReference)
    new_fc = os.path.join(outWorkspace,outFC)

    #get the unique field names from the HTML fields of the first UID in UID_list
    where = """ {0} = '{1}' """.format(arcpy.AddFieldDelimiters(featureClass,fields[0]),UID_list[0])

    new_fields_list = []
    for row in arcpy.da.SearchCursor(featureClass,fields, where):
        soup = BeautifulSoup(row[1])
        elements = soup.findAll('td',text=True)
        fieldName = (elements[3].text).replace(" ","_")

        #create a list of new fields (to use with insert cursor)
        new_fields_list.append(fieldName)
        arcpy.AddField_management(new_fc,fieldName, field_type='TEXT')


    #retrieve geometries from original KML feature class
    currentUID = ''

    #Generates unique geometries in new feature class
    with arcpy.da.InsertCursor(new_fc,["SHAPE@",UID_field]) as i_cursor:
        for s_row in arcpy.da.SearchCursor(featureClass,["SHAPE@",UID_field],"","",sql_clause=(None, 'ORDER BY ' + UID_field + ' ASC')):
            if s_row[1] != currentUID:
                currentUID = s_row[1]
                i_cursor.insertRow(s_row)
    del i_cursor

    new_fields_list.insert(0,UID_field)


    #Populate attribute fields with Data contained in HTML block
    with arcpy.da.UpdateCursor(new_fc,new_fields_list) as u_cursor:
        for u_row in u_cursor:
            for s_row in arcpy.da.SearchCursor(featureClass,fields,"","",sql_clause=(None, 'ORDER BY ' + fields[0] + ' ASC')):
                if s_row[0] == u_row[0]:
                    soup = BeautifulSoup(s_row[1])
                    elements = soup.findAll('td',text=True)
                    fieldName = (elements[3].text).replace(" ","_")
                    value = elements[4].text
                    field_index = new_fields_list.index(fieldName)
                    u_row[field_index] = value
                    u_cursor.updateRow(u_row)

    del u_cursor


if __name__ == "__main__":

    # Gather inputs
    featureClass = arcpy.GetParameterAsText(0)
    htmlField = arcpy.GetParameterAsText(1)
    outWorkspace = arcpy.GetParameterAsText(2)
    outFC = arcpy.GetParameterAsText(3)
    UID_field = arcpy.GetParameterAsText(4)
##    featureClass = r"D:\SIDE_PROJECTS\K_26_Mississauga_GF_Wardv3.gdb\Placemarks\Polygons"
##    htmlField = "PopupInfo"
##    outWorkspace= r"D:\SIDE_PROJECTS\K_26_Mississauga_GF_Wardv3.gdb"
##    outFC = "test"
##    UID_field = "Name"
    postProcess(featureClass,htmlField,outWorkspace,outFC,UID_field)