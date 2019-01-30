from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from other_folder.drivers import get_driver, login
from config import user, password, system
from other_folder.drivers import hana_cursor


def get_data_for_shipment(cursor, deliveries):
    cont_dict = {}
    type_dict = {"02": 0, "03": 0, "04": 0}
    for delivery in deliveries:
        cursor.execute(
            f'select EXC_BARCODE, EXC_LOADING_TYPE from "SAPECP"."/S2IM/001_EXCPOS" where vbeln=\'{delivery}\' and EXC_TYPE = \'2\'')
        data = [pos for pos in cursor.fetchall()]
        for type_pos in data:
            type_dict[type_pos[1]] += 1
        for dat in data:
            cont_dict[dat[0]] = list()

    for position in cont_dict.keys():
        cursor.execute(
            f'select HU_ID from "SAPECP"."/S2IM/001_EXCP_I" where EXC_SECTION=\'{position[0:3]}\' and EXC_POSITION = \'{position[4:]}\'')

        [cont_dict[position].append(hu_id[0].lstrip("0")) for hu_id in cursor.fetchall()]

    cursor.execute("select ID from SAPECP.YECH_SHIP_CART where ROUTE=''")
    empty_carts = sorted([cart[0] for cart in cursor.fetchall()], reverse=True)

    return cont_dict, type_dict, empty_carts
    # return empty_carts


def enter_cart_add1(driver):
    driver.find_element(By.CSS_SELECTOR, "button[name*='CART_ADD1']").click()


def exit_cart_add1(driver):
    driver.find_element_by_id("butback").click()


def get_shipment_position(driver):
    table = driver.find_element_by_id("info_string_table").text
    position = table.strip().split()[4]

    return position


def add_box_to_preparation_cart(driver, box_list, cart):
    for box in box_list:
        cart_field = driver.find_element_by_id("p_field")
        cart_field.send_keys(cart)
        cart_field.send_keys(Keys.RETURN)
        position_field = driver.find_element_by_id("p_field")
        position_field.send_keys(f"pos_{box}")
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
        enter_cart_add1(driver)

        while type_consolidation_dict[storage_type]:
            type_consolidation_dict[storage_type] -= 1

            position = get_shipment_position(driver)
            add_box_to_preparation_cart(driver, position_and_boxes_dict[position], cart)

            if not type_consolidation_dict[storage_type]:
                driver.find_element(By.CSS_SELECTOR, "input[name*='answer_no']").click()


def shipment_unsorted(driver, cursor, deliveries):
    position_and_boxes_dict, type_consolidation_dict, empty_carts = get_data_for_shipment(cursor, deliveries)
    storage_types = "02", "03", "04"
    for storage_type in storage_types:
        shipment_over_type(driver, position_and_boxes_dict, type_consolidation_dict, storage_type, empty_carts.pop())

    change_workstation(driver, "all")

    return driver


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)
    cursora = hana_cursor()
    deliveris = ['2000000108', ]
    shipment_unsorted(wd, cursora, deliveris)

