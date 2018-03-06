# AutoExportModelPlugin by Jeff Bush - 2018
# Auto-saves an OBJ files whenever a gcode file is sent to a device/printer

from PyQt5.QtCore import QObject

from UM.Application import Application
from UM.Extension import Extension
from UM.Logger import Logger

class AutoExportPlugin(QObject, Extension):
    """This plugin writes an OBJ file whenever a gcode file is sent to a device/printer."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Hook the "writeStarted" method. Whenever the gcode is about to be written to a device
        # (either locally or remotely) then the our execute method will be called.
        Application.getInstance().getOutputDeviceManager().writeStarted.connect(self.execute)

    def execute(self, output_device):
        app = Application.getInstance()

        # The current scene (used to get the 3D model being printed)
        scene = app.getController().getScene()

        # The OBJ writer plugin
        obj_writer = app.getPluginRegistry().getPluginObject('OBJWriter')

        # TODO: get name of output from these properties
        Logger.log("w", "ID:    %s" % output_device.getId())
        Logger.log("w", "Name:  %s" % output_device.getName())
        Logger.log("w", "Desc:  %s" % output_device.getDescription())
        Logger.log("w", "Short: %s" % output_device.getShortDescription())

        Logger.log("w", "*ID:   %s" % getattr(output_device, 'key', 'N/A'))
        Logger.log("w", "*Name: %s" % getattr(output_device, 'name', 'N/A'))
        Logger.log("w", "*Addr: %s" % getattr(output_device, 'address', 'N/A'))

        # Write the data out as an OBJ file
        # TODO: not hard-coded directory
        with open('/home/jbush/output-%s.obj'%output_device.getId(), 'w') as f:
            obj_writer.write(f, scene.getRoot().getAllChildren())
