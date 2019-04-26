import subprocess
import os
import win32com.client
import time
from other_folder.drivers import initialization


def open_sap_gui():
    system = '-system=10.200.81.10'
    client = '-client=001'
    sys_name = '-sysname=K4D'
    sap_server = '-sapserver=21'
    user = f'-user={os.environ.get("SAP_USER")}'
    password = f'-pw={os.environ.get("SAP_PASS")}'
    language = '-language=CS'

    gui_path = 'C:/Program Files (x86)/SAP/FrontEnd/SAPgui/'
    cmd_string = os.path.join(gui_path,
                              f"sapshcut.exe {system} {client} {sys_name} {sap_server} {user} {password} {language}")
    subprocess.call(cmd_string)


def make_session():
    win_title = "SAP"
    shell = win32com.client.Dispatch("WScript.Shell")
    while not shell.AppActivate(win_title):
        time.sleep(1)

    while True:
        try:
            sap = win32com.client.GetObject("SAPGUI").GetScriptingEngine
            full_attr = sap.Children(0).Children(0).Info.SystemName

            print(full_attr)
            sess = sap.FindById("ses[0]")
            sess.FindById("wnd[0]").maximize()
            break

        except:
            time.sleep(1)

    return sess


if __name__ == '__main__':
    # pass
    # open_sap_gui()
    # session = make_session()
    session = initialization()
    session.StartTransaction(Transaction="YWMQUEUE")

    session.FindById('wnd[0]/usr/radR1').select()
    session.FindById('wnd[0]/usr/chkP_ROUTEP').selected = True
    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()

    grid_users = session.FindById("wnd[0]/usr/shell/shellcont[1]/shell/shellcont[1]/shell")
    ps = session.FindById("wnd[0]/usr/").verticalScrollbar.PageSize
    print(ps)
    session.FindById("wnd[0]/usr").horizontalScrollbar.position = 100
    session.EndTransaction()
