# AutoExportModelPlugin by Jeff Bush - 2018

from . import AutoExportModelPlugin

def getMetaData():
    return {}

def register(_app):
    return {"extension": AutoExportModelPlugin.AutoExportModelPlugin()}
