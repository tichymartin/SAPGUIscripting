from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drivers import get_driver, login, close_browser
from config import user, password
from sap_getdata import get_shipment_id_hana, get_cart_for_shipping


def create_shipment(driver, route, user):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#SHIP']")
    button.click()

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#NEW']")
    button.click()

    car_field = driver.find_element_by_id("p_field")
    car_field.send_keys(user)
    car_field.send_keys(Keys.RETURN)

    route_field = driver.find_element_by_id("p_field")
    route_field.send_keys(route)
    route_field.send_keys(Keys.RETURN)

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    return get_shipment_id_hana(route)


def cart_from_cons(driver, route, boxes, cart_list):
    cart = cart_list.pop()
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#CART_ADD']")
    button.click()

    field = driver.find_element_by_id("p_field")
    field.send_keys(cons_type)
    field.send_keys(Keys.RETURN)

    route_field = driver.find_element_by_id("p_field")
    route_field.send_keys(route)
    route_field.send_keys(Keys.RETURN)

    cart_field = driver.find_element_by_id("p_field")
    cart_field.send_keys(cart)
    cart_field.send_keys(Keys.RETURN)

    for delivery in boxes:

        table = driver.find_element_by_id("info_string_table").text
        table_text = table.split("oknu")[1].split("a")[0].split(" ")
        position = table_text[1] + table_text[2]

        cons_position_field = driver.find_element_by_id("p_field")
        cons_position_field.send_keys(position[0])
        cons_position_field.send_keys(Keys.RETURN)

        cons_position_field = driver.find_element_by_id("p_field")
        cons_position_field.send_keys(position[1])
        cons_position_field.send_keys(Keys.RETURN)

        for box in boxes[position]:
            box_field = driver.find_element_by_id("p_field")
            box_field.send_keys(box)
            box_field.send_keys(Keys.RETURN)

    # BACK
    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    return cart


def shipment_add_and_close(driver, boxes, user, route, shipment_id):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#SHIP']")
    button.click()

    button = driver.find_element(By.CSS_SELECTOR, f"button[name*='{shipment_id})']")
    button.click()

    # button = driver.find_element_by_xpath(f"//*[contains(text(), '{user} - {route}')]")
    # button.click()

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#SHIP_ADD']")
    button.click()

    for delivery in boxes:
        for box in boxes[delivery]:
            cart_field = driver.find_element_by_id("p_field")
            cart_field.send_keys(box)
            cart_field.send_keys(Keys.RETURN)

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#SHIP_CLOSE']")
    button.click()

    # todo na q se neuzavre... neni tam ridic...
    cons_position_field = driver.find_element_by_id("p_field")
    cons_position_field.send_keys(user)
    cons_position_field.send_keys(Keys.RETURN)

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()


def shipment(driver, route, user, boxes):
    shipment_id = create_shipment(driver, route, user)
    print(f"shipment {shipment_id} created for {user} and route {route}")
    cart = cart_from_cons(driver, route, boxes, get_cart_for_shipping())
    print(f"cart {cart} filled for {route}")
    shipment_add_and_close(driver, boxes, user, route, shipment_id)
    print(f"shipment '{user} - {route}' closed")


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)

    rout = 100005
    boxes = {'X6': [19175], 'X4': [40555]}
    # shipment(wd, rout, user, boxes)
    # create_shipment(wd, rout, user)
    # cart_from_cons(wd, rout, boxes)
    # shipment_add_and_close(wd, boxes, user, rout)
