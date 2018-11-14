

def enter_courier(driver):
    back_menu = driver.find_element_by_id("butback")
    back_menu.click()

    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXT_CONS']")
    elem.click()

    elem = driver.find_element(By.CSS_SELECTOR, "button[name*='EXC_ADD2']")
    elem.click()


def insert_into_courier(driver, hu_to_courier):
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


def courier(driver, hu_to_courier):
    enter_courier(driver)
    boxes = insert_into_courier(driver, hu_to_courier)
    exit_control(driver)

    return boxes