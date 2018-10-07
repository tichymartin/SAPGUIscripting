import win32com.client
from config import system
from drivers import hana_cursor
from datetime import datetime


def get_route_hana(delivery):
    cursor = hana_cursor()
    cursor.execute(f"select route from sapecp.likp where vbeln={delivery}")
    return cursor.fetchone()[0]


def get_shipment_id_hana(route):
    today = datetime.now().date().strftime("%Y%m%d")
    cursor = hana_cursor()
    cursor.execute(f"select shipment_id from sapecp.YECH_SHIP where ROUTE={route} and DATUM ='{today}'")
    return cursor.fetchone()[0]


def get_cart_for_shipping():
    cursor = hana_cursor()
    cursor.execute(f"select ID from sapecp.YECH_SHIP_CART where STATUS='' and ROUTE='' and SHIPMENT_ID= '' ")
    cart_list = [cart[0] for cart in cursor.fetchall() if cart[0].startswith("M")]
    return cart_list


def get_indls_data_from_lips(cursor, indls):
    cursor.execute(f"select matnr, lfimg, XCHPF from sapecp.lips where vbeln={indls}")
    return cursor.fetchall()


def get_cons_positions():
    cursor = hana_cursor()
    cursor.execute(f'select * from "SAPECP"."/S2IM/001_EXCPOS"')
    return cursor.fetchone()


def get_su_from_hana(cursor, storage_unit):
    cursor.execute(f"select LENUM from sapecp.lein where LENUM = '{storage_unit:0>20}'")
    data = cursor.fetchone()
    if data is None:
        return
    else:
        return data[0].lstrip("0")


def get_items_from_hu_for_control(handling_units):
    cursor = hana_cursor()
    items = []
    for hu in handling_units:
        cursor.execute(f"select MATNR, LFIMG from sapecp.YECH_HU_ITEMS where ID = '{hu:0>20}'")
        data = cursor.fetchall()
        items.extend(data)
    return data


def get_empty_hu():
    cursor = hana_cursor()
    cursor.execute(f"select ID from sapecp.YECH_HU where STATUS = 'P' and VBELN=''")
    data = cursor.fetchall()
    data_list = [hu[0].lstrip("0") for hu in data if not len(hu[0].lstrip("0")) > 5]

    return data_list[0]


def get_courier_positions():
    cursor = hana_cursor()
    cursor.execute(
        f'select EXC_BARCODE from "SAPECP"."/S2IM/001_EXCPOS" where EXC_TYPE=2 and VBELN=\'\' and EXC_LOADING_TYPE=02')
    return [x[0] for x in cursor.fetchall()]


if __name__ == '__main__':
    dlv = "2000000243"
    to = "261"
    materials = ['1001618', '1001619']
    # cursor = hana_cursor()
    # print(get_route_hana(dlv))
    # print(get_shipment_id_hana(100003))
    # print(get_cart_for_shipping())

    hu = [26756]
    # print(get_items_from_hu_for_control(hu)[0][1])
    # x = str(get_items_from_hu_for_control(hu)[0][1])
    # print(x)
    print(get_empty_hu())

    # print(get_courier_positions())
