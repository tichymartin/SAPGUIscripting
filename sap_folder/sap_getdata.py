from other_folder.drivers import hana_cursor
from datetime import datetime


def get_route_hana(cursor, delivery):
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


def get_items_from_hu_for_control(cursor, handling_units):
    items = []
    for hu in handling_units:
        cursor.execute(f"select MATNR, LFIMG from sapecp.YECH_HU_ITEMS where ID = '{hu:0>20}'")
        data = cursor.fetchall()
        items.extend(data)
    return data


def get_courier_positions():
    cursor = hana_cursor()
    cursor.execute(
        f'select EXC_BARCODE from "SAPECP"."/S2IM/001_EXCPOS" where EXC_TYPE=2 and VBELN=\'\' and EXC_LOADING_TYPE=02')
    return [x[0] for x in cursor.fetchall()]








def get_tst_data():
    cursor = hana_cursor()
    cursor.execute(f'select POSNR, MATNR from SAPECP.VBAP where VBELN=5510001340 ')
    return [print(_) for _ in cursor.fetchall()]


def get_to_from_dlv(dlv):
    cursor = hana_cursor()
    cursor.execute(f"select VBELN from SAPECP.VBFA where VBELV='{dlv}' ")
    return cursor.fetchone()[0].lstrip("0")


def get_len_to_for_user(cursor, user):
    cursor.execute(f'select TANUM from "SAPECP"."/S2AP/LES_WMQUE" where QUEUE_ID=\'{user}\' ')
    transport_order_list = [to[0].lstrip("0") for to in cursor.fetchall()]
    return len(transport_order_list)


def get_material_type_for_picking(cursor, material):
    cursor.execute(f'select "/CWM/XCWMAT", MEINS  from "SAPECP"."MARA" where MATNR={material} ')
    data = cursor.fetchone()
    if not data[0]:
        return
    elif data[1] == "KG":
        return "OVOZEL"
    else:
        return "MASO"


if __name__ == '__main__':
    dlv = 2000001051
    so = 5510001719
    user = "S1268"
    material = 1000398
    # print(get_tst_data())
    cursor = hana_cursor()
    print(get_dlv_for_so(cursor, so))
