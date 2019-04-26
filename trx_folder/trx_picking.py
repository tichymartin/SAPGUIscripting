import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from other_folder.drivers import get_driver, login
from other_folder.drivers import create_hana_connection
from sap_folder.sap_getdata import get_len_to_for_user, get_material_type_for_picking


def enter_wmq_add(driver):

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='WM_PICK']")
    button.click()


def close_wmq_add(driver):
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
    if len(table_data["location"]) > 10:
        table_data["location"] = table_data["location"].split(".")
        table_data["location"] = f'{table_data["location"][0]}{table_data["location"][1]}{table_data["location"][2]}{table_data["location"][3]}{table_data["location"][4]}'
    return table_data


def input_storage_loc(driver, table_data):
    beep_field = driver.find_element_by_id("lv_beep_b")
    beep_field.send_keys(f'LVS{table_data["location"][0:3]}{table_data["location"]}')
    beep_sim = driver.find_element_by_id("beep_sim")
    beep_sim.click()


def input_quantity(driver, amount):
    quantity_field = driver.find_element_by_id("p_field")
    quantity_field.send_keys(str(amount))
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
            print(f"{box_no}")
            return box_no


def input_box(driver, box_no):
    box_number = driver.find_element_by_id("p_field")
    box_number.send_keys(box_no)
    box_number.send_keys(Keys.RETURN)


def pick_meat(driver, box_no, partial_amount):
    table_data = get_table_data(driver)
    input_ean(driver, table_data)
    input_box(driver, box_no)
    input_quantity(driver, partial_amount)


def weight_ovozel(driver, ovozel_hu):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='WM_OVO']")
    button.click()

    for box in ovozel_hu:
        box_no = box[0]
        input_box(driver, box_no)

        zvolit_button = driver.find_element(By.CSS_SELECTOR, "input[name*='EV_ITEM|']")
        zvolit_button.click()

        input_quantity(driver, box[2])

    close_wmq_add(driver)


def get_table_data_alt_quantity(driver, material_type):
    table = driver.find_element_by_id("info_string_table").text

    if material_type == "MASO":
        table_text = table.split("\n")
        alt_quantity = table_text[0].split("Množství alt: ")[1].split(" ")[0].replace(",", ".")
        return float(alt_quantity)

    elif material_type == "OVOZEL":
        table_text = table.split("\n")
        alt_quantity = table_text[0].split("Váha: ")[1].split(" ")[0].replace(",", ".")
        return float(alt_quantity)

    else:
        return


def picking(driver, cursor, user):
    enter_wmq_add(driver)

    ovozel_hu = []
    picked_hu = []

    for item in range(get_len_to_for_user(cursor, user)):
        table_data = get_table_data(driver)
        input_storage_loc(driver, table_data)
        input_quantity(driver, table_data["amount"])
        input_ean(driver, table_data)

        mtn = get_matn_from_trx(driver)

        material_type = get_material_type_for_picking(cursor, mtn)
        table_data["alt_amount"] = get_table_data_alt_quantity(driver, material_type)

        box_no = box_creating_by_guess(driver)
        picked_hu.append(box_no)

        if material_type == "OVOZEL":
            ovozel_hu.append((box_no, mtn, table_data["alt_amount"]))

        if material_type == "MASO":

            partial_amount = str(round(table_data["alt_amount"] / int(table_data["amount"]), 3))
            input_quantity(driver, partial_amount)
            if int(table_data["amount"]) > 1:
                for _ in range(int(table_data["amount"]) - 1):
                    pick_meat(driver, box_no, partial_amount)

    close_wmq_add(driver)
    if ovozel_hu:
        weight_ovozel(driver, ovozel_hu)

    return picked_hu


# def get_no_items_in_transport_orders(cursor, transport_order):
#
#     cursor.execute(f'select * from "SAPECP"."LTAP" where TANUM = {transport_order}')
#     no_items = len(cursor.fetchall())
#     return int(no_items)


if __name__ == '__main__':
    wd = get_driver("k4t")
    login(wd)
    cursor = create_hana_connection()
    picking(wd, cursor, "S1268")
    # enter_wmq_add(wd)
    # print(get_table_data(wd))
