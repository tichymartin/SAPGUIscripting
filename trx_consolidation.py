from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from drivers import get_driver, login, close_browser
from config import user, password
from bs4 import BeautifulSoup


def enter_consolidation(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXT_CONS']")
    elem.click()


def enter_cons_add(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_ADD']")
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

    print(f"position {position} filled with {box}")


def get_data_for_consolidation(delivery_dict):
    list_of_boxes = []

    for delivery in list(delivery_dict.keys()):
        box_l = []
        for box_d in delivery_dict[delivery]:
            box = list(box_d.keys())[0]
            box_l.append(box)
        list_of_boxes.append(box_l)

    return list_of_boxes


def consolidation(driver, delivery_dict):
    enter_consolidation(driver)
    positions = get_cons_position(driver)
    enter_cons_add(driver)
    list_of_boxes = get_data_for_consolidation(delivery_dict)
    list_of_boxes_with_position = {}
    for boxes in list_of_boxes:
        position = positions.pop()

        for box in boxes:
            insert_box(driver, box, position)

        list_of_boxes_with_position[position] = boxes

    close_consolidation(driver)

    return list_of_boxes_with_position


def get_cons_position(driver):
    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_INFO']")
    elem.click()

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    tab_data = soup.find(class_="info_table").find_all("tr")

    empty_cons_positon = []
    for tr in tab_data:
        for td in tr.find_all("td"):
            if td.string == "Suché oddělení":
                if td.previous_sibling.previous_sibling.string == "Konsolidace":
                    if td.next_sibling.next_sibling.string is None:
                        position = td.previous_sibling.previous_sibling.previous_sibling.previous_sibling.string.strip().split()
                        position = position[0] + position[1]
                        empty_cons_positon.append(position)

                        break

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    if not empty_cons_positon:
        print("neni volna pozice")

    return empty_cons_positon


if __name__ == '__main__':
    wd = get_driver()
    # wd = None
    login(wd, user, password)
    del_dict = {'2000000246': [{56072: {'CW': ''}}]}
    # print(consolidation(wd, delivery_dict))
    print(get_data_for_consolidation(del_dict))
    enter_consolidation(wd)
    print(get_cons_position(wd))


