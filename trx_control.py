from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from drivers import get_driver, login, close_browser
from config import user, password
from drivers import hana_cursor


def get_data_for_control(cursor, deliveries):
    cont_dict = {}
    type_dict = {"02": 0, "03": 0, "04": 0}
    for delivery in deliveries:
        cursor.execute(
            f'select EXC_BARCODE, EXC_LOADING_TYPE from "SAPECP"."/S2IM/001_EXCPOS" where vbeln=\'{delivery}\' and EXC_TYPE = \'1\'')
        data = [pos for pos in cursor.fetchall()]
        for type_pos in data:
            type_dict[type_pos[1]] += 1
        for dat in data:
            cont_dict[dat[0]] = list()

    for position in cont_dict.keys():
        cursor.execute(
            f'select HU_ID from "SAPECP"."/S2IM/001_EXCP_I" where EXC_SECTION=\'{position[0]}\' and EXC_POSITION = \'{position[1:]}\'')
        [cont_dict[position].append(hu_id[0].lstrip("0")) for hu_id in cursor.fetchall()]

    return cont_dict, type_dict


def enter_control(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_CHECK']")
    elem.click()


def get_control_position(driver):
    table = driver.find_element_by_id("info_string_table").text
    return table.strip().split()[4]


def get_empty_hu(cursor):
    cursor.execute(f"select ID from sapecp.YECH_HU where STATUS = 'P' and VBELN=''")
    data = cursor.fetchall()
    data_list = [hu[0].lstrip("0") for hu in data if not len(hu[0].lstrip("0")) > 5]

    return data_list


def add_box_from_cons_to_control(driver, box_list):
    for box in box_list:
        hu_field = driver.find_element_by_id("p_field")
        hu_field.send_keys(box)
        hu_field.send_keys(Keys.RETURN)


def confirm_insert_to_control(driver):
    driver.find_element(By.CSS_SELECTOR, "input[name*='take_over']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name*='answer_yes']").click()


def short_control(driver, empty_hu):
    element = driver.find_element_by_id("p_field")
    element.send_keys(empty_hu)
    element.send_keys(Keys.RETURN)


def get_items_from_hu_for_control(cursor, handling_units):
    items = []
    for hu in handling_units:
        cursor.execute(f"select MATNR, LFIMG from sapecp.YECH_HU_ITEMS where ID = '{hu:0>20}'")
        data = cursor.fetchall()
        items.extend(data)

    return items


def complete_control(driver, items, empty_hu):
    for item in items:
        matnr_field = driver.find_element_by_id("p_field")
        matnr_field.send_keys(item[0])
        matnr_field.send_keys(Keys.RETURN)

        quantity_field = driver.find_element_by_id("p_field")
        quantity_field.send_keys(str(item[1]))
        quantity_field.send_keys(Keys.RETURN)

        hu_field = driver.find_element_by_id("p_field")
        hu_field.send_keys(empty_hu)
        hu_field.send_keys(Keys.RETURN)


def confirm_control(driver):
    driver.find_element(By.CSS_SELECTOR, "input[name*='end_check']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name*='answer_yes']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name*='answer_yes']").click()


def change_workstation(driver, storage_type):
    if storage_type == "03":
        workstation = "$ALL_CHLAZ"
    elif storage_type == "04":
        workstation = "$ALL_MRAZ"
    else:
        workstation = "$ALL"

    beep_field = driver.find_element_by_id("lv_beep_b")
    beep_field.send_keys(f"PLA{workstation}")
    beep_sim = driver.find_element_by_id("beep_sim")
    beep_sim.click()


def control_over_type(driver, position_and_boxes_dict, type_consolidation_dict, empty_hu_list, storage_type):
    if type_consolidation_dict[storage_type]:
        change_workstation(driver, storage_type)
        enter_control(driver)

        while type_consolidation_dict[storage_type]:
            type_consolidation_dict[storage_type] -= 1

            position = get_control_position(driver)
            add_box_from_cons_to_control(driver, position_and_boxes_dict[position])
            confirm_insert_to_control(driver)
            short_control(driver, empty_hu_list.pop())
            confirm_control(driver)

            if not type_consolidation_dict[storage_type]:
                driver.find_element(By.CSS_SELECTOR, "input[name*='answer_no']").click()


def exit_control(driver):
    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()


def control(driver, cursor, deliveries):
    position_and_boxes_dict, type_consolidation_dict = get_data_for_control(cursor, deliveries)
    empty_hu_list = get_empty_hu(cursor)
    storage_types = "02", "03", "04"
    for storage_type in storage_types:
        control_over_type(driver, position_and_boxes_dict, type_consolidation_dict, empty_hu_list, storage_type)

    change_workstation(driver, "02")


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)
    cursora = hana_cursor()
    deliveris = ['2000000638']
    control(wd, cursora, deliveris)
