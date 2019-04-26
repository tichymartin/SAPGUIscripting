import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from other_folder.drivers import get_driver, login
from other_folder.drivers import create_hana_connection
from datetime import datetime


def enter_ship(driver):
    driver.find_element(By.CSS_SELECTOR, "button[name*='#SHIP']").click()


def create_shipment(driver, route, user):
    driver.find_element(By.CSS_SELECTOR, "button[name*='#NEW']").click()

    car_field = driver.find_element_by_id("p_field")
    car_field.send_keys(user)
    car_field.send_keys(Keys.RETURN)

    route_field = driver.find_element_by_id("p_field")
    route_field.send_keys(route)
    route_field.send_keys(Keys.RETURN)


def enter_shipment(driver, shipment_id):
    driver.find_element(By.CSS_SELECTOR, f"button[name*='{shipment_id})']").click()
    driver.find_element(By.CSS_SELECTOR, "button[name*='#SHIP_ADD']").click()


def close_shipment(driver, user):
    driver.find_element(By.CSS_SELECTOR, "button[name*='#SHIP_CLOSE']").click()

    cons_position_field = driver.find_element_by_id("p_field")
    cons_position_field.send_keys(user)
    cons_position_field.send_keys(Keys.RETURN)

    driver.find_element_by_id("butback").click()


def get_cart_from_table(driver):
    table = driver.find_elements_by_xpath("//*[contains(text(), 'Naložte MJ z vozíku')]")[0].text
    cart_out = table.split()[4].rstrip(".")

    return cart_out


def add_boxes_to_shipment(driver, carts_and_boxes_dict):
    for _ in range(len(carts_and_boxes_dict)):
        cart_out = get_cart_from_table(driver)
        for box in carts_and_boxes_dict[cart_out]:
            cart_field = driver.find_element_by_id("p_field")
            cart_field.send_keys(box)
            cart_field.send_keys(Keys.RETURN)

    driver.find_element_by_id("butback").click()


def get_data_for_shipment(cursor, route):
    today = datetime.now().date().strftime('%Y%m%d')

    cursor.execute(f"select ID from SAPECP.YECH_SHIP_CART where ROUTE='{route}' and LFDAT='{today}'")
    carts = [cart[0] for cart in cursor.fetchall()]

    carts_and_boxes_dict = {}
    for cart in carts:
        cursor.execute(f"select HU_ID from SAPECP.YECH_SHIP_CART_I where CART_ID='{cart}'")
        carts_and_boxes_dict[cart] = [hu[0].lstrip("0") for hu in cursor.fetchall()]

    cursor.execute(f"select shipment_id from sapecp.YECH_SHIP where ROUTE={route} and DATUM ='{today}'")
    shipment_id = cursor.fetchone()[0]

    return shipment_id, carts_and_boxes_dict


def shipping(driver, cursor, route, user):
    enter_ship(driver)
    create_shipment(driver, route, user)
    shipment_id, carts_and_boxes_dict = get_data_for_shipment(cursor, route)
    print(f"SHIP {shipment_id} - ROUTE {route}")

    enter_shipment(driver, shipment_id)
    add_boxes_to_shipment(driver, carts_and_boxes_dict)
    close_shipment(driver, user)

    return driver


if __name__ == '__main__':
    wd = get_driver("k4d")
    login(wd)
    cursora = create_hana_connection("k4d")

    route = "100007"
    shipping(wd, cursora, route, os.environ.get("SAP_USER"))

