import wx

def file_select_dlg(message,wildcard):
    with wx.FileDialog(parent=None, message=message, wildcard=wildcard,
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:

        if dlg.ShowModal() == wx.ID_CANCEL:
            exit(0)
        pathname = dlg.GetPath()
    return pathname

def folder_select_dlg(message,path):
    with wx.DirDialog(parent=None, message=message, defaultPath=path,
                       style=wx.DD_DEFAULT_STYLE) as dlg:

        if dlg.ShowModal() == wx.ID_CANCEL:
            exit(0)
        path = dlg.GetPath()
    return path