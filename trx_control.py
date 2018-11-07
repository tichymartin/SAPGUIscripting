from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drivers import get_driver, login, close_browser
from config import user, password, cons_type
from sap_ywmqueue_control import ywmqueue_control
from drivers import initialization
from sap_getdata import get_items_from_hu_for_control, get_empty_hu, get_courier_positions


def enter_control(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_CHECK']")
    elem.click()


def control_for_delivery(driver, boxes_dict):
    hu_to_courier = []
    for position in boxes_dict.keys():
        boxes = add_box_from_cons_to_control(driver, boxes_dict[position])

        items = get_items_from_hu_for_control(boxes)

        control_hu = get_empty_hu()
        confirm_insert_to_control(driver)
        control_items(driver, items, control_hu)
        confirm_control(driver)
        hu_to_courier.append(control_hu)

    return hu_to_courier


def add_box_from_cons_to_control(driver, boxes_list):
    boxes = []
    for box in boxes_list:
        hu_field = driver.find_element_by_id("p_field")
        hu_field.send_keys(box)
        hu_field.send_keys(Keys.RETURN)
        boxes.append(box)
        print(f"box {box} entered control station")

    return boxes


def confirm_insert_to_control(driver):
    back_menu = driver.find_element_by_id("butmenu")
    back_menu.click()

    elem = driver.find_element(By.CSS_SELECTOR, "input[name*='take_over']")
    elem.click()

    elem = driver.find_element(By.CSS_SELECTOR, "input[name*='answer_yes']")
    elem.click()


def control_items(driver, items, empty_hu):
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

    print(f"materials repacked to hu {empty_hu}")


def confirm_control(driver):
    back_menu = driver.find_element_by_id("butmenu")
    back_menu.click()

    elem = driver.find_element(By.CSS_SELECTOR, "input[name*='end_full_check']")
    elem.click()

    elem = driver.find_element(By.CSS_SELECTOR, "input[name*='answer_yes']")
    elem.click()


def enter_courier(driver):
    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXT_CONS']")
    elem.click()

    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_ADD2']")
    elem.click()


def courier(driver, hu_to_courier):
    courier_loc = get_courier_positions()
    boxes_for_shipping = {}
    for box in hu_to_courier:
        position = courier_loc.pop()
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

        boxes_for_shipping[position] = []
        boxes_for_shipping[position].append(box)

    return boxes_for_shipping


def exit_control(driver):
    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()


def control_main(driver, session, boxes, deliveries):
    ywmqueue_control(session, deliveries, user)
    enter_control(driver)
    hu_to_courier = control_for_delivery(driver, boxes)
    enter_courier(driver)
    boxes = courier(driver, hu_to_courier)
    exit_control(driver)
    print(boxes)
    return boxes


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)
    boxess = {'X6': [65070]}
    deliveries = ["2000000280"]

    sess = initialization()
    control_main(wd, sess, boxess)
