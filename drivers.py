from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import win32com.client
from config import headless_mode, system, url_trx, port_s
import pyhdb


def get_driver():
    opts = Options()
    opts.headless = headless_mode

    driver = webdriver.Chrome(options=opts)
    if system == "k4d":
        page = url_trx["k4d"]
    elif system == "k4q":
        page = url_trx["k4q"]
    elif system == "k4t":
        page = url_trx["k4t"]
    else:
        print("unknown system")
        page = None
    driver.get(page)

    return driver


def login(driver, user, password):
    elem = driver.find_element_by_id("iUSER")
    elem.clear()
    elem.send_keys(user)
    elem = driver.find_element_by_id("iPASSWORD")
    elem.send_keys(password)
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


def initialization():
    sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    session = sap_gui.FindById("ses[0]")

    # Run transaction RZ11. Specify the parameter name sapgui/user_scripting

    return session


def hana_cursor():
    connection = pyhdb.connect(
        host="10.200.81.10",
        port=port_s[system],
        user="TEST_RESULT",
        password="Results85!",
    )

    # cursor = connection.cursor()
    return connection.cursor()
