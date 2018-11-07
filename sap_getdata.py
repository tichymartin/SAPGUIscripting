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


def get_dlv_for_so(sales_order):
    cursor = hana_cursor()
    cursor.execute(f"select VBELN from SAPECP.VBFA where VBELV='{sales_order}' ")
    try:
        return cursor.fetchone()[0]
    except TypeError:
        raise Exception(f"k zakazce {sales_order} se nepodarilo zalozit dodavku")


def get_to_for_dlv(dlv):
    cursor = hana_cursor()
    cursor.execute(f"select VBELN from SAPECP.VBFA where VBTYP_N='Q' and  VBELV='{dlv}' ")
    try:
        to_list = [to[0].lstrip("0") for to in cursor.fetchall()]
        to_list = set(to_list)
        to_list = list(to_list)
        return to_list
    except TypeError:
        raise Exception(f"k dodavce {dlv} se nepovedlo zalozit skladove prikazy")


def get_tst_data():
    cursor = hana_cursor()
    cursor.execute(f'select POSNR, MATNR from SAPECP.VBAP where VBELN=5510001340 ')
    return [print(_) for _ in cursor.fetchall()]


if __name__ == '__main__':

    dlv = 2000000845
    print(get_to_for_dlv(dlv))
