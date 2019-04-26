from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from other_folder.drivers import get_driver, login, create_hana_connection
from config import user, password
from sap_folder.sap_getdata import get_indls_data_from_lips, get_su_from_hana
import random
from datetime import datetime, timedelta


def open_indls_menu(driver):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#INDLS']")
    button.click()


def open_indls(driver, indls):
    button = driver.find_element_by_xpath(f"//*[contains(text(), '{indls}')]")
    button.click()


def open_indls_add(driver):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#INDLS_ADD']")
    button.click()


def navigate_in(driver, indls):
    open_indls_menu(driver)
    open_indls(driver, indls)
    open_indls_add(driver)


def create_pallet(cursor):
    while True:
        pallet = random.randint(2000000000, 9999999999)
        if not get_su_from_hana(cursor, pallet):
            break

    return pallet


def input_pallet(driver, pallet):
    pallet_field = driver.find_element_by_id("p_field")
    pallet_field.send_keys(pallet)
    pallet_field.send_keys(Keys.RETURN)

    return pallet


def input_material(driver, material):
    matnr_field = driver.find_element_by_id("p_field")
    matnr_field.send_keys(material)
    matnr_field.send_keys(Keys.RETURN)


def input_quantity(driver, quantity):
    quantity_field = driver.find_element_by_id("p_field")
    quantity_field.send_keys(quantity)
    quantity_field.send_keys(Keys.RETURN)


def input_charge_date(driver, cursor, material):
    cursor.execute(f"select MHDRZ from sapecp.mara where matnr = {material}")
    days_to_expiration = int(cursor.fetchone()[0])
    today = datetime.now().date()
    expiration_date = (today + timedelta(days_to_expiration)).strftime("%Y%m%d")

    charge_field = driver.find_element_by_id("p_field")
    charge_field.send_keys(expiration_date)
    charge_field.send_keys(Keys.RETURN)


def close_pallet(driver):
    close_button = driver.find_element_by_id("but_close_hu")
    close_button.click()

    ano_button = driver.find_element(By.CSS_SELECTOR, "input[value='Ano']")
    ano_button.click()

    quantity_field = driver.find_element_by_id("p_field")
    quantity_field.send_keys("E0")
    quantity_field.send_keys(Keys.RETURN)


def navigate_out(driver):
    back_button = driver.find_element_by_id("butback")
    back_button.click()

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#INDLS_CLS']")
    button.click()

    check_button = driver.find_element_by_id("butcheck")
    check_button.click()

    ok_button = driver.find_element_by_id("butok")
    ok_button.click()

    back_button = driver.find_element_by_id("butback")
    back_button.click()


def inbound(indls):
    driver = get_driver()
    login(driver, user, password)

    navigate_in(driver, indls)
    cursor = create_hana_connection()
    item_list = get_indls_data_from_lips(cursor, indls)
    pallets = []
    for item in item_list:

        matnr, quantity, charge = item
        matnr = matnr.lstrip("0")
        quantity = str(quantity)

        pallets.append(input_pallet(driver, create_pallet(cursor)))
        input_material(driver, matnr)
        input_quantity(driver, quantity)
        if charge == "X":
            input_charge_date(driver, cursor, matnr)

        close_pallet(driver)
    navigate_out(driver)
    print(f"PALLETS = {pallets}")
    return pallets


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)

    delivery = "180000189"
    palts = inbound(delivery)
    print(palts)

    # matnr = 1000357
    # input_charge_date(matnr)
