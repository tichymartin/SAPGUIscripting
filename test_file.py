import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# @pytest.fixture(params=["2000000185", ])
# def delivery(request):
#     return request.param


# @pytest.mark.parametrize("bussines_partner, materials", [("5000000044", ["1000357", "1000358"]), ])
# @pytest.mark.parametrize("delivery", ["2000000185", "2000000186"])


# def test_get_route_hana(cursor, delivery):
#     cursor.execute(f"select route from sapecp.likp where vbeln={delivery}")
#     assert cursor.fetchone()[0] == "100000"


def test_po_in_ekko(cursor, purchase_order):
    cursor.execute(f"select ebeln from sapecp.ekko where ebeln={purchase_order}")
    assert cursor.fetchone()[0] == purchase_order


def test_indls_in_likp(cursor, indlvs):
    cursor.execute(f"select vbeln from sapecp.likp where vbeln={indlvs}")
    assert cursor.fetchone()[0].lstrip("0") == indlvs


def test_open_indls_is_in_trx(open_indls_for_trx, driver, login):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#INDLS']")
    button.click()

    button = driver.find_element_by_xpath(f"//*[contains(text(), '{open_indls_for_trx}')]")
    assert button.is_displayed()
