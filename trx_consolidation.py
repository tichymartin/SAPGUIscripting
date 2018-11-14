from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from drivers import get_driver, get_driver_specific, login, close_browser
from config import user, password
from drivers import hana_cursor


def enter_consolidation(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXT_CONS']")
    elem.click()


def enter_cons_add(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_ADD)']")
    elem.click()


def close_consolidation(driver):
    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()


def insert_box(driver, box, position):
    # input boxes
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

    print(f"HU {box} - CONS {position}")


def consolidation(driver, cursor, deliveries):
    enter_consolidation(driver)
    enter_cons_add(driver)
    deliver_and_boxes_dict, type_consolidation_dict = get_data_for_consolidation(cursor, deliveries)
    if type_consolidation_dict["02"]:
        positions = get_cons_position(cursor, "02")
        for delivery in deliver_and_boxes_dict.keys():
            for hu_data in deliver_and_boxes_dict[delivery]:
                if hu_data[1] == "02":
                    insert_box(driver, hu_data[0], positions.pop())

    if type_consolidation_dict["03"]:
        close_browser(driver)
        wd_chlaz = get_driver_specific("03")
        login(wd_chlaz, user, password)
        enter_consolidation(wd_chlaz)
        enter_cons_add(wd_chlaz)
        positions = get_cons_position(cursor, "03")
        for delivery in deliver_and_boxes_dict.keys():
            for hu_data in deliver_and_boxes_dict[delivery]:
                if hu_data[1] == "03":
                    insert_box(wd_chlaz, hu_data[0], positions.pop())
        close_browser(wd_chlaz)

    if type_consolidation_dict["04"]:
        if not type_consolidation_dict["03"]:
            close_browser(driver)
        wd_mraz = get_driver_specific("04")
        login(wd_mraz, user, password)
        enter_consolidation(wd_mraz)
        enter_cons_add(wd_mraz)
        positions = get_cons_position(cursor, "04")
        for delivery in deliver_and_boxes_dict.keys():
            for hu_data in deliver_and_boxes_dict[delivery]:
                if hu_data[1] == "04":
                    insert_box(wd_mraz, hu_data[0], positions.pop())
        close_browser(wd_mraz)

    if type_consolidation_dict["03"] or type_consolidation_dict["04"]:
        driver = get_driver()
        login(driver, user, password)

    else:
        close_consolidation(driver)

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


def get_cons_position(cursor, type_of_cons):
    cursor.execute(
        f'select EXC_BARCODE from "SAPECP"."/S2IM/001_EXCPOS" where EXC_TYPE = \'1\' and EXC_LOADING_TYPE = \'{type_of_cons}\' and VBELN = \'\'')
    empty_cons_positions = [position[0] for position in cursor.fetchall() if not position[0].endswith("9999")]

    return empty_cons_positions


if __name__ == '__main__':
    # wd = get_driver()
    # login(wd, user, password)
    cursor = hana_cursor()
    deliveries = ['2000000748']
    # print(consolidation(wd, cursor, deliveries))
    # print(get_data_for_consolidation(del_dict))
    print(get_cons_position(cursor, "02"))
