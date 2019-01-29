from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from other_folder.drivers import get_driver, login
from config import user, password, system
from other_folder.drivers import hana_cursor
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


def add_boxes_to_shipment(driver, dvl_and_boxes_dict):
    for delivery in dvl_and_boxes_dict:
        for box in dvl_and_boxes_dict[delivery]:
            cart_field = driver.find_element_by_id("p_field")
            cart_field.send_keys(box)
            cart_field.send_keys(Keys.RETURN)

    driver.find_element_by_id("butback").click()

    #
    # button =
    # button.click()
    #
    # # todo na q se neuzavre... neni tam ridic...

    #
    # back_menu = driver.find_element_by_id("butback")
    # back_menu.click()
    #
    # back_menu = driver.find_element_by_id("butback")
    # back_menu.click()


def get_data_for_shipment(cursor, route):
    today = datetime.now().date().strftime('%Y%m%d')
    # cursor.execute(f"select VBELN from SAPECP.YECH_ROUTES_DLVS where ROUTE='{route}' and DATUM='{today}'")
    # deliveries = [dlv[0] for dlv in cursor.fetchall()]
    #
    # dvl_and_boxes_dict = {}
    # for delivery in deliveries:
    #     cursor.execute(f"select ID, LOADING_TYPE from SAPECP.YECH_HU where vbeln='{delivery}' and STATUS = 'T'")
    #     dvl_and_boxes_dict[delivery] = [hu_info[0].lstrip("0") for hu_info in cursor.fetchall()]

    cursor.execute(f"select ID from SAPECP.YECH_SHIP_CART where ROUTE='{route}' and LFDAT='{today}'")
    carts = [cart[0] for cart in cursor.fetchall()]
    carts_and_boxes_dict = {}


    today = datetime.now().date().strftime("%Y%m%d")
    cursor.execute(f"select shipment_id from sapecp.YECH_SHIP where ROUTE={route} and DATUM ='{today}'")
    shipment_id = cursor.fetchone()[0]

    return shipment_id, carts


def shipping(driver, cursor, route, user):
    enter_ship(driver)
    # create_shipment(driver, route, user)

    shipment_id, dvl_and_boxes_dict = get_data_for_shipment(cursor, route)
    print(f"shipment {shipment_id} opened for route {route}")

    enter_shipment(driver, shipment_id)

    cart_and_boxes_dict = get_data_for_cart()
    add_boxes_to_shipment(driver, dvl_and_boxes_dict)
    close_shipment(driver, user)


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)
    cursora = hana_cursor("k4t")

    route = "100004"
    print(get_data_for_shipment(cursora, route))
    # shipping(wd, cursora, route, user)
    # create_shipment(wd, rout, user)
    # cart_from_cons(wd, rout, boxes)
    # shipment_add_and_close(wd, boxes, user, rout)
