from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from other_folder.drivers import get_driver, login
from other_folder.drivers import create_hana_connection
from datetime import datetime


def enter_cart_add2(driver):
    driver.find_element(By.CSS_SELECTOR, "button[name*='CART_ADD2']").click()


def open_route_for_shipping(driver, route):
    driver.find_element(By.CSS_SELECTOR, f"button[name*='{route}']").click()


def exit_cart_add2(driver):
    driver.find_element_by_id("butback").click()
    driver.find_element_by_id("butback").click()


def get_sorting_data(driver):
    table = driver.find_element_by_id("info_string_table").text
    table_data = {"cart_out": table.strip().split()[6], "hu": table.strip().split()[3],
                  "position": table.strip().split()[8].strip(".")}

    return table_data


def get_data_for_route(cursor, route):
    today = datetime.now().date().strftime('%Y%m%d')
    cursor.execute(f"select VBELN from SAPECP.YECH_ROUTES_DLVS where ROUTE='{route}' and DATUM='{today}'")
    deliveries = [dlv[0] for dlv in cursor.fetchall()]

    dvl_and_boxes_dict = {}
    type_dict = {"02": 0, "03": 0, "04": 0}
    for delivery in deliveries:
        cursor.execute(f"select ID, LOADING_TYPE from SAPECP.YECH_HU where vbeln='{delivery}' and STATUS = 'S'")
        dvl_and_boxes_dict[delivery] = [(hu_info[0].lstrip("0"), hu_info[1]) for hu_info in cursor.fetchall()]
        for hu in dvl_and_boxes_dict[delivery]:
            type_dict[hu[1]] += 1

    cursor.execute("select ID from SAPECP.YECH_SHIP_CART where ROUTE=''")
    empty_carts = sorted([cart[0] for cart in cursor.fetchall()], reverse=True)

    return dvl_and_boxes_dict, type_dict, empty_carts


def add_box_to_sorted_cart(driver, data, empty_cart):
    # source_cart_field = driver.find_element_by_id("p_field")
    # source_cart_field.send_keys(data["cart_out"])
    # source_cart_field.send_keys(Keys.RETURN)
    # source_cart_position_field = driver.find_element_by_id("p_field")
    # source_cart_position_field.send_keys(data["position"])
    # source_cart_position_field.send_keys(Keys.RETURN)
    hu_field = driver.find_element_by_id("p_field")
    hu_field.send_keys(data["hu"])
    hu_field.send_keys(Keys.RETURN)
    target_cart_field = driver.find_element_by_id("p_field")
    target_cart_field.send_keys(empty_cart)
    target_cart_field.send_keys(Keys.RETURN)
    target_cart_position_field = driver.find_element_by_id("p_field")
    target_cart_position_field.send_keys(data["position"])
    target_cart_position_field.send_keys(Keys.RETURN)


def change_workstation(driver, storage_type):
    if storage_type == "02":
        workstation = "$MTSUCH"
    elif storage_type == "03":
        workstation = "$MTCHLAZ"
    elif storage_type == "04":
        workstation = "$MTMRAZ"
    else:
        workstation = "$ALL"

    beep_field = driver.find_element_by_id("lv_beep_b")
    beep_field.send_keys(f"PLA{workstation}")
    beep_sim = driver.find_element_by_id("beep_sim")
    beep_sim.click()


def shipment_over_type(driver, route, type_hu_dict, storage_type, empty_cart):
    if type_hu_dict[storage_type]:
        change_workstation(driver, storage_type)
        enter_cart_add2(driver)
        open_route_for_shipping(driver, route)

        while type_hu_dict[storage_type]:
            type_hu_dict[storage_type] -= 1

            data = get_sorting_data(driver)
            add_box_to_sorted_cart(driver, data, empty_cart)

        exit_cart_add2(driver)


def shipment_sorted(driver, cursor, route):
    dlv_and_boxes_dict, type_hu_dict, empty_carts = get_data_for_route(cursor, route)
    storage_types = "02", "03", "04"
    for storage_type in storage_types:
        shipment_over_type(driver, route, type_hu_dict, storage_type, empty_carts.pop())

    change_workstation(driver, "all")

    return driver


if __name__ == '__main__':
    wd = get_driver("k4d")
    login(wd)
    cursora = create_hana_connection("k4d")
    route = 100007
    shipment_sorted(wd, cursora, route)
    # print(get_data_for_route(cursora, route))

