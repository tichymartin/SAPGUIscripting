from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drivers import get_driver, login, close_browser
from config import user, password
import random


def enter_wmq_add(driver):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='WM_PICK']")
    button.click()

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='WMQ_ADD']")
    button.click()


def close_wmq_add(driver):
    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    back_menu = driver.find_element_by_id("butback")
    back_menu.click()


def get_table_data(driver):
    table = driver.find_element_by_id("info_string_table").text
    table_text = table.split("\n")
    table_data = {"location": table_text[0].split()[1],
                  "amount": table_text[0].split()[3].split()[0],
                  "ean": table_text[1].split()[1],
                  "dlv": table_text[3].split()[1],
                  }

    # if __name__ == '__main__':
    #     print(table_data)
    return table_data


def input_storage_loc(driver, table_data):
    beep_field = driver.find_element_by_id("lv_beep_b")
    beep_field.send_keys(f'LVS{table_data["location"][0:3]}{table_data["location"]}')
    beep_sim = driver.find_element_by_id("beep_sim")
    beep_sim.click()


def input_quantity(driver, table_data):
    quantity_field = driver.find_element_by_id("p_field")
    quantity_field.send_keys(table_data["amount"])
    quantity_field.send_keys(Keys.RETURN)


def input_ean(driver, table_data):
    beep_field = driver.find_element_by_id("lv_beep_b")
    beep_field.send_keys(table_data["ean"])
    beep_sim = driver.find_element_by_id("beep_sim")
    beep_sim.click()


def get_matn_from_trx(driver):
    matnr_text = driver.find_element(By.CSS_SELECTOR, "tr[onmouseover*='MATNR'] td:nth-of-type(4)").text
    matnr = matnr_text.split("(")[1].split(")")[0]

    return matnr


def box_creating_by_guess(driver):
    while True:
        box_number = driver.find_element_by_id("p_field")
        box_no = random.randint(10000, 69999)
        box_number.send_keys(box_no)
        box_number.send_keys(Keys.RETURN)
        try:
            error = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "error")))
            if error.is_displayed():
                continue

        except:
            print(f"HU {box_no}")
            return box_no


def input_box(driver, box_no):
    box_number = driver.find_element_by_id("p_field")
    box_number.send_keys(box_no)
    box_number.send_keys(Keys.RETURN)


def pick_meat(driver, box_no, mtn_cw):
    table_data = get_table_data(driver)
    input_ean(driver, table_data)
    input_box(driver, box_no)
    input_quantity(driver, mtn_cw)


def ovozel_boxes(driver, dlv_dict):
    # dlv_dict = {'2000000312': [{50413: {'CW': 'OVOZEL', 'parallel_quantity': '4'}}]}
    boxes_list = check_ovozel_boxes(dlv_dict)
    if boxes_list:
        print(boxes_list)
        weight_ovozel(driver, boxes_list)
        close_wmq_add(driver)


#       #todo kontrola zavreni


def check_ovozel_boxes(dlv_dict):
    boxes_for_weight = []
    for dlv in dlv_dict.values():
        for box in dlv:
            for data in box.values():
                if data["CW"] == "OVOZEL":
                    boxes_for_weight.append(box)
    return boxes_for_weight


def weight_ovozel(driver, boxes_list):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='WM_PICK']")
    button.click()

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='WMQ_WGH_OZ']")
    button.click()

    for box in boxes_list:
        box_no = list(box.keys())[0]
        input_box(driver, box_no)
        zvolit_button = driver.find_element(By.CSS_SELECTOR, "input[name*='EV_ITEM|']")
        zvolit_button.click()

        input_quantity(driver, box[box_no])


def get_table_data_alt_quantity(driver):
    table = driver.find_element_by_id("info_string_table").text
    table_text = table.split("\n")
    alt_quantity = table_text[0].split("Váha: ")[1].split(" ")[0]

    return alt_quantity


def picking_main(driver, items, material_d):
    enter_wmq_add(driver)

    deliveries_d = {}

    for item in range(items):
        table_data = get_table_data(driver)
        input_storage_loc(driver, table_data)
        input_quantity(driver, table_data)
        input_ean(driver, table_data)

        mtn = get_matn_from_trx(driver)

        if material_d[mtn]["CW"] == "OVOZEL":
            alt_amount = get_table_data_alt_quantity(driver)
            material_d[mtn]["amount"] = alt_amount
        #     TODO amount is copied  to older dict

        box_no = box_creating_by_guess(driver)

        if material_d[mtn]["CW"] == "MASO":
            input_quantity(driver, material_d[mtn])
            if int(table_data["amount"]) > 1:
                for cw_maso in range(int(table_data["amount"]) - 1):
                    pick_meat(driver, box_no, material_d[mtn])

        if table_data["dlv"] not in deliveries_d:
            deliveries_d[table_data["dlv"]] = []
        deliveries_d[table_data["dlv"]].append({box_no: material_d[mtn]})

    close_wmq_add(driver)
    ovozel_boxes(driver, deliveries_d)

    return deliveries_d


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)

    items = 1
    materials = {'1000397': {'CW': ''}}

    deliveries = picking(wd, items, materials)
    print(deliveries)
