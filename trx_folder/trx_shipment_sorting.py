from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from other_folder.drivers import get_driver, login
from config import user, password, system
from other_folder.drivers import hana_cursor


def enter_cart_add2(driver):
    driver.find_element(By.CSS_SELECTOR, "button[name*='CART_ADD2']").click()


def open_route_for_shipping(driver, route):
    driver.find_element(By.CSS_SELECTOR, f"button[name*='{route}']").click()


def get_empty_cart(cursor):
    cursor.execute("select ID from SAPECP.YECH_SHIP_CART where ROUTE=''")
    empty_carts = sorted([cart[0] for cart in cursor.fetchall()], reverse=True)

    return empty_carts


def exit_cart_add2(driver):
    driver.find_element_by_id("butback").click()


def get_sorting_data(driver):
    table = driver.find_element_by_id("info_string_table").text
    table_data = {"cart_out": table.strip().split()[6], "hu": table.strip().split()[3],
                  "position": table.strip().split()[8].strip(".")}

    return table_data


def add_box_to_preparation_cart(driver, box_list, cart):
    for box in box_list:
        cart_field = driver.find_element_by_id("p_field")
        cart_field.send_keys(cart)
        cart_field.send_keys(Keys.RETURN)
        position_field = driver.find_element_by_id("p_field")
        position_field.send_keys(box)
        position_field.send_keys(Keys.RETURN)
        hu_field = driver.find_element_by_id("p_field")
        hu_field.send_keys(box)
        hu_field.send_keys(Keys.RETURN)


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


def shipment_over_type(driver, position_and_boxes_dict, type_consolidation_dict, storage_type, cart):
    if type_consolidation_dict[storage_type]:
        change_workstation(driver, storage_type)
        enter_cart_add2(driver)

        while type_consolidation_dict[storage_type]:
            type_consolidation_dict[storage_type] -= 1

            position = get_sorting_data(driver)
            add_box_to_preparation_cart(driver, position_and_boxes_dict[position], cart)

            if not type_consolidation_dict[storage_type]:
                driver.find_element(By.CSS_SELECTOR, "input[name*='answer_no']").click()


def shipment_sorted(driver, cursor, deliveries):
    position_and_boxes_dict, type_consolidation_dict, empty_carts = get_data_for_shipment(cursor, deliveries)
    storage_types = "02", "03", "04"
    for storage_type in storage_types:
        shipment_over_type(driver, position_and_boxes_dict, type_consolidation_dict, storage_type, empty_carts.pop())

    change_workstation(driver, "all")

    return driver


def shipment_development(driver, cursor, route):
    enter_cart_add2(driver)
    open_route_for_shipping(driver, route)
    table_data = get_sorting_data(driver)



if __name__ == '__main__':
    wd = get_driver("k4t")
    login(wd, user, password)
    cursora = hana_cursor("k4t")
    deliveris = ['2000000108', ]
    # shipment_unsorted(wd, cursora, deliveris)
    shipment_development(wd, cursora, "100003")
