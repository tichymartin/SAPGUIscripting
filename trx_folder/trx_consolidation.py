from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from other_folder.drivers import get_driver, login
from config import user, password, system
from other_folder.drivers import hana_cursor


def enter_consolidation(driver):
    driver.find_element(By.CSS_SELECTOR, "button[name*='EXT_CONS']").click()
    driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_ADD)']").click()


def close_consolidation(driver):
    driver.find_element_by_id("butback").click()
    driver.find_element_by_id("butback").click()


def enter_box(driver, box):
    box_field = driver.find_element_by_id("p_field")
    box_field.send_keys(box)
    box_field.send_keys(Keys.RETURN)


def enter_position(driver, position):
    field = driver.find_element_by_id("p_field")
    field.send_keys(position[0:3])
    field.send_keys(Keys.RETURN)

    field = driver.find_element_by_id("p_field")
    field.send_keys(position[4:])
    field.send_keys(Keys.RETURN)


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


def courier_over_type(driver, deliver_and_boxes_dict, type_consolidation_dict, storage_type):
    if type_consolidation_dict[storage_type]:

        change_workstation(driver, storage_type)
        enter_consolidation(driver)

        for delivery in deliver_and_boxes_dict.keys():

            for hu_data in deliver_and_boxes_dict[delivery]:
                if hu_data[1] == storage_type:

                    enter_box(driver, hu_data[0])
                    position = get_position_from_table(driver)
                    enter_position(driver, position)
                    enter_box(driver, hu_data[0])
                    enter_position(driver, position)


        close_consolidation(driver)


def consolidation(driver, cursor, deliveries):
    deliver_and_boxes_dict, type_consolidation_dict = get_data_for_consolidation(cursor, deliveries)

    storage_types = "02", "03", "04"
    for storage_type in storage_types:
        courier_over_type(driver, deliver_and_boxes_dict, type_consolidation_dict, storage_type)

    change_workstation(driver, "02")

    return driver


def get_data_for_consolidation(cursor, deliveries):
    cons_dict = {}
    type_dict = {"02": 0, "03": 0, "04": 0}
    for delivery in deliveries:
        cursor.execute(f"select ID, LOADING_TYPE from SAPECP.YECH_HU where vbeln='{delivery}' and STATUS = 'V'")
        cons_dict[delivery] = [(hu_info[0].lstrip("0"), hu_info[1]) for hu_info in cursor.fetchall()]
        for hu in cons_dict[delivery]:
            type_dict[hu[1]] += 1

    return cons_dict, type_dict


def get_cons_position(type_of_cons):
    cursor = hana_cursor()
    cursor.execute(
        f'select EXC_BARCODE from "SAPECP"."/S2IM/001_EXCPOS" where EXC_TYPE = \'1\' and EXC_LOADING_TYPE = \'{type_of_cons}\' and VBELN = \'\'')
    empty_cons_positions = [position[0] for position in cursor.fetchall() if not position[0].endswith("9999")]

    return empty_cons_positions


def get_position_from_table(driver):
    table = driver.find_element_by_id("success").text
    position = table.split()[0].strip(",")
    return position


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)
    cursora = hana_cursor()
    deliveris = ['2000000062', ]
    consolidation(wd, cursora, deliveris)
