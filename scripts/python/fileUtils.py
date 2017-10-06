import pymel.core as pm
import os

def clear_window(window_name):
    if pm.window (window_name, exists = True):
            pm.deleteUI(window_name)

def inc_save(*args):
    if os.path.exists(pm.sceneName()):
        version_up()
    else:
        w = IncSaveWin()

def version_up():

    path, file = os.path.split(pm.sceneName())
    file = file.partition('.')[0][:-5]
    curdir_files = os.listdir(path)
    inc_files = []

    for item in curdir_files:
        if file in item:
            inc_files.append(item)
    inc_files.sort()
    last_ver = int(inc_files[-1].partition('.')[0][-3:])
    new_file = file + '_v' + str(last_ver + 1).zfill(3)
    updated_path = os.path.join(path, new_file + ".ma").replace('\\', '/')
    pm.saveAs(updated_path, force = True)

def file_open():
    
    def save_file(*args):
        inc_save()
        clear_window(winID)
        pm.openFile(updated_path, force = True)

    def clear_me(*args):
        clear_window(winID)
        pm.openFile(updated_path, force = True)

    multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
    try:
        file_path = pm.fileDialog2(fileFilter=multipleFilters, dialogStyle=1, fileMode=1, startingDirectory='//medusa/cyberwitch/assets')[0]
    except TypeError:
        return
    updated_path = file_path.replace('\\', '/')

    winID = 'assertWindow'
    clear_window(winID)

    win = pm.window(winID, title = "Save", widthHeight=(188, 399), sizeable = False)
    layout = pm.columnLayout('mainColumn', parent = win, adjustableColumn = True)
    pm.separator(h = 5, style = 'none')
    pm.rowLayout('row1', numberOfColumns = 1, columnAttach = [(1, "left", 5)])
    pm.text("Do you want to save the current scene?")
    pm.setParent('mainColumn')

    pm.separator(h = 5, style = 'none')

    pm.rowLayout('row2', numberOfColumns = 2, columnAttach = [(1, "both", 5), (2, "both", 5)])
    pm.button(label = "Yes", width = 50, command = save_file)
    pm.button(label = "No", width = 50, command = clear_me)
    pm.setParent('mainColumn')
    pm.separator(h = 5, style = 'none')
    pm.showWindow()

class IncSaveWin(object):

    def __init__(self):
        self.asset_name = ""
        self.save_path = ""

        clear_window('incremental_save')

        self.win = pm.window("incremental_save", title = "Initial Save", sizeable = False)
        self.layout = pm.columnLayout('mainColumn', parent=self.win, adjustableColumn = True)
        pm.separator(h = 5, style = 'none')
        pm.rowLayout('row1', numberOfColumns = 3, columnAttach = [(1, "left", 5), (2, "both", 5), (3, "both", 5)])
        pm.text("Filepath:")
        assets_path = '//medusa/cyberwitch/assets'
        pm.textField("FilePathTF", width = 300, text = assets_path)
        pm.button(label = "Browse", width = 50, command=self.find_save_path)
        pm.setParent('mainColumn')

        pm.separator(h = 5, style = 'none')

        pm.rowLayout('row2', numberOfColumns = 3, columnAttach = [(1, "both", 5), (2, "both", 5), (3, "both", 5)])
        pm.text( label='Asset name:')
        self.asset_name = pm.textField(width = 100)
        pm.button(label = "Save", width = 100, command=self.save_file)
        pm.setParent('mainColumn')

        pm.showWindow()

    def find_save_path(self, *args):
        multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        try:
            self.save_path = pm.fileDialog2(fileFilter=multipleFilters, dialogStyle=1, fileMode=3, startingDirectory='//medusa/cyberwitch/assets')[0]
        except TypeError:
            self.save_path = '//medusa/cyberwitch/assets'
        pm.textField("FilePathTF", edit= True, text= self.save_path)
        pm.separator(h = 5, style = 'none')

    def save_file(self, *args):
        file = pm.textField(self.asset_name, query=True, text=True )
        new_file = file + '_v' + '001'
        updated_path = os.path.join(self.save_path, new_file + ".ma").replace('\\', '/')
        pm.saveAs(updated_path, force = True)
        clear_window('incremental_save')