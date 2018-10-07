import pytest
import pyhdb
from drivers import initialization
from config import headless_mode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from config import system, url_trx, user, password


@pytest.fixture()
def cursor():
    connection = pyhdb.connect(
        host="10.200.81.10",
        port=32015,
        user="TEST_RESULT",
        password="Results85!",
    )

    yield connection.cursor()

    # connection.close()


@pytest.fixture(scope='session')
def session():
    session = initialization()
    return session


@pytest.fixture(scope='session')
def driver():
    opts = Options()
    opts.headless = headless_mode

    driver = webdriver.Chrome(options=opts)
    if system == "k4d":
        page = url_trx["k4d"]
    elif system == "k4q":
        page = url_trx["k4q"]
    else:
        print("unknown system")
        page = None
    driver.get(page)

    return driver


@pytest.fixture()
def login(driver):
    elem = driver.find_element_by_id("iUSER")
    elem.clear()
    elem.send_keys(user)
    elem = driver.find_element_by_id("iPASSWORD")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    if "Přihlášení - kontrola instance" in driver.title:
        cont_button = driver.find_element_by_class_name("button_big")
        cont_button.click()


@pytest.fixture(scope='session')
def bussines_partner():
    return "5000000044"


@pytest.fixture(scope='session')
def materials():
    return ["1000357", "1000358"]


@pytest.fixture(scope='session')
def purchase_order(session, bussines_partner, materials):
    session.StartTransaction(Transaction="me21n")

    session.FindById(
        "wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB0:SAPLMEGUI:0030/subSUB1:SAPLMEGUI:1105/ctxtMEPO_TOPLINE-SUPERFIELD").text = bussines_partner
    session.FindById("wnd[0]").sendVKey(0)
    for count, material in enumerate(materials):
        session.FindById(
            f"wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-EMATN[5,{count}]").text = material
        session.FindById(
            f"wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/txtMEPO1211-MENGE[7,{count}]").text = "10"
    session.FindById("wnd[0]").sendVKey(0)
    session.FindById("wnd[0]/tbar[0]/btn[11]").press()
    session.FindById("wnd[1]/usr/btnSPOP-VAROPTION1").press()
    text_po = session.FindById("wnd[0]/sbar").text
    po_txt = text_po.split()[-1]

    return po_txt


@pytest.fixture(scope='session')
def indlvs(session, purchase_order):
    session.StartTransaction(Transaction="vl31n")
    session.FindById("wnd[0]/usr/txtLV50C-BSTNR").text = purchase_order
    session.FindById("wnd[0]").sendVKey(0)
    session.FindById("wnd[0]/tbar[0]/btn[11]").press()
    text_indls = session.FindById("wnd[0]/sbar").text
    indls_text = text_indls.split()[-2]

    return indls_text


@pytest.fixture(scope="session")
def open_indls_for_trx(session, indlvs):
    session.StartTransaction(Transaction="/s2ap/les_idlvmon")
    session.FindById("wnd[0]/usr/ctxtP_VBELN-LOW").text = indlvs
    session.FindById("wnd[0]/tbar[1]/btn[8]").press()

    session.FindById("wnd[0]/usr/cntlGRID1/shellcont/shell").selectedRows = "0"
    session.FindById("wnd[0]/tbar[1]/btn[9]").press()
    session.FindById("wnd[1]/tbar[0]/btn[0]").press()

    return indlvs
