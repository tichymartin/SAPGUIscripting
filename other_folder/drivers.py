import os
import pyhdb
import win32com.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from config import url_trx, port_s, pass_s


def get_driver(system):
    opts = Options()
    opts.headless = False

    driver = webdriver.Chrome(options=opts)
    # driver = webdriver.Ie(options=opts)
    if system == "K4D":
        page = url_trx["K4D"]
    elif system == "K4Q":
        page = url_trx["K4Q"]
    elif system == "K4T":
        page = url_trx["K4T"]
    elif system == "K4L":
        page = url_trx["K4L"]
    else:
        print("unknown system")
        page = None
    driver.get(page)

    return driver


def login(driver):
    elem = driver.find_element_by_id("iUSER")
    elem.clear()
    elem.send_keys(os.environ.get("SAP_USER"))
    elem = driver.find_element_by_id("iPASSWORD")
    elem.send_keys(os.environ.get("SAP_PASS"))
    elem.send_keys(Keys.RETURN)
    if "Přihlášení - kontrola instance" in driver.title:
        cont_button = driver.find_element_by_class_name("button_big")
        cont_button.click()


def close_browser(driver):
    menu = driver.find_element_by_id("butmenu")
    menu.click()
    logoff = driver.find_element_by_id("ButnApp")
    logoff.click()
    driver.close()


# def initialization():
#     sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
#     session = sap_gui.FindById("ses[0]")
#
#     # Run transaction RZ11. Specify the parameter name sapgui/user_scripting
#
#     return session


def initialization():
    sap_gui_auto = win32com.client.GetObject("SAPGUI")
    if not type(sap_gui_auto) == win32com.client.CDispatch:
        return

    application = sap_gui_auto.GetScriptingEngine
    if not type(application) == win32com.client.CDispatch:
        sap_gui_auto = None
        return

    connection = application.Children(0)
    if not type(connection) == win32com.client.CDispatch:
        application = None
        sap_gui_auto = None
        return

    session = connection.Children(0)
    if not type(session) == win32com.client.CDispatch:
        connection = None
        application = None
        sap_gui_auto = None
        return

    return session, connection, application, sap_gui_auto


def cls_session(session, connection, application, sap_gui_auto):
    session = None
    connection = None
    application = None
    SapGuiAuto = None


def create_hana_connection(system):
    connection = pyhdb.connect(
        host="10.200.81.10",
        port=port_s[system],
        user="TEST_RESULT",
        password=pass_s[system],
    )

    return connection


def close_hana_connection(cursor, connection):
    cursor.close()
    connection.close()

