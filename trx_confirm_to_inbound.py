from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from drivers import get_driver, login, close_browser
from config import user, password


def open_wm_cnf(driver):
    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#WM_CNF)']")
    button.click()

    button = driver.find_element(By.CSS_SELECTOR, "button[name*='#X_I01']")
    button.click()


def get_data_from_table(driver):
    table = driver.find_element_by_id("info_string_table").text
    data = table.split("\n")[0].split()
    storage = data[3] + data[4]
    return storage


def confirm_to(driver, pallets):
    for pallet in pallets:
        to_button = driver.find_element(By.CSS_SELECTOR, f"button[name*='{pallet}']")
        to_button.click()

        storage = get_data_from_table(driver)

        pallet_field = driver.find_element_by_id("p_field")
        pallet_field.send_keys(pallet)
        pallet_field.send_keys(Keys.RETURN)

        barcode_field = driver.find_element_by_id("lv_beep_b")
        barcode_field.send_keys(f"LVS{storage}")

        barcode_confirm = driver.find_element_by_id("beep_sim")
        barcode_confirm.click()

        print(f"TO for PALLET {pallet} confirmed")


def main_confirm_to(pallets):
    driver = get_driver()
    login(driver, user, password)
    open_wm_cnf(driver)
    confirm_to(driver, pallets)
    close_browser(driver)


if __name__ == '__main__':
    wd = get_driver()
    login(wd, user, password)
    palls = ["6595671840"]
    open_wm_cnf(wd)
    confirm_to(wd, palls)
