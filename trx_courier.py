from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from drivers import get_driver, login, close_browser
from config import user, password, cons_type
from drivers import hana_cursor


def enter_courier(driver):
    driver.find_element(By.CSS_SELECTOR, "button[name*='EXT_CONS']").click()
    driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_ADD2']").click()


def exit_courier(driver):
    driver.find_element_by_id("butback").click()
    driver.find_element_by_id("butback").click()


def get_data_for_courier(cursor, deliveries):
    cons_dict = {}
    type_dict = {"02": 0, "03": 0, "04": 0}
    for delivery in deliveries:
        cursor.execute(f"select ID, LOADING_TYPE from SAPECP.YECH_HU where vbeln='{delivery}' and STATUS = 'B'")
        cons_dict[delivery] = [(hu_info[0].lstrip("0"), hu_info[1]) for hu_info in cursor.fetchall()]
        for hu in cons_dict[delivery]:
            type_dict[hu[1]] += 1

    return cons_dict, type_dict


def get_courier_positions(cursor, type_of_cons):
    cursor.execute(
        f'select EXC_BARCODE from "SAPECP"."/S2IM/001_EXCPOS" where EXC_TYPE = \'2\' and EXC_LOADING_TYPE = \'{type_of_cons}\' and VBELN = \'\'')
    empty_cons_positions = [position[0] for position in cursor.fetchall() if not position[0].endswith("9999")]

    return empty_cons_positions


def change_workstation(driver, type):
    if type == "03":
        workstation = "$ALL_CHLAZ"
    elif type == "04":
        workstation = "$ALL_MRAZ"
    else:
        workstation = "$ALL"

    beep_field = driver.find_element_by_id("lv_beep_b")
    beep_field.send_keys(f"PLA{workstation}")
    beep_sim = driver.find_element_by_id("beep_sim")
    beep_sim.click()


def courier_over_type(driver, cursor, deliveries_and_boxes_dict, type_courier_dict, storage_type):
    if type_courier_dict[storage_type]:
        positions = get_courier_positions(cursor, storage_type)
        change_workstation(driver, storage_type)
        enter_courier(driver)

        for delivery in deliveries_and_boxes_dict.keys():

            for hu_data in deliveries_and_boxes_dict[delivery]:
                if hu_data[1] == storage_type:
                    insert_into_courier(driver, hu_data[0], positions.pop())

        exit_courier(driver)


def insert_into_courier(driver, box, position):
    box_field = driver.find_element_by_id("p_field")
    box_field.send_keys(box)
    box_field.send_keys(Keys.RETURN)

    field = driver.find_element_by_id("p_field")
    field.send_keys(position[0])
    field.send_keys(Keys.RETURN)

    field = driver.find_element_by_id("p_field")
    field.send_keys(position[1:])
    field.send_keys(Keys.RETURN)

    box_field = driver.find_element_by_id("p_field")
    box_field.send_keys(box)
    box_field.send_keys(Keys.RETURN)

    field = driver.find_element_by_id("p_field")
    field.send_keys(position[0])
    field.send_keys(Keys.RETURN)

    field = driver.find_element_by_id("p_field")
    field.send_keys(position[1:])
    field.send_keys(Keys.RETURN)
    print(f"COUR {position} - HU {box}")


def courier(driver, cursor, deliveries):
    deliveries_and_boxes_dict, type_courier_dict = get_data_for_courier(cursor, deliveries)
    storage_types = "02", "03", "04"
    for storage_type in storage_types:
        courier_over_type(driver, cursor, deliveries_and_boxes_dict, type_courier_dict, storage_type)

    change_workstation(driver, "02")


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)
    cursora = hana_cursor()
    deliveris = ['2000000578', '2000000579']
    print(courier(wd, cursora, deliveris))
