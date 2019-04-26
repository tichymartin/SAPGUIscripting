import win32com.client
from time import sleep
from datetime import datetime, timedelta
from other_folder.drivers import create_hana_connection


def initialization():
    sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    session = sap_gui.FindById("ses[0]")

    return session


def make_dlv(session, cursor, sales_order):
    # make dlv from SO
    session.StartTransaction(Transaction="VL01N")
    today = datetime.now().date().strftime("%d.%m.%Y")
    # today = datetime.now().date()
    # tomorrow = today + timedelta(days=1)
    # tomorrow = tomorrow.strftime("%d.%m.%Y")

    session.FindById('wnd[0]/usr/ctxtLIKP-VSTEL').text = 1000
    session.FindById('wnd[0]/usr/ctxtLV50C-DATBI').text = today
    session.FindById('wnd[0]/usr/ctxtLV50C-VBELN').text = sales_order
    # time.sleep(1)
    session.FindById('wnd[0]/tbar[0]/btn[0]').Press()
    session.FindById('wnd[0]/tbar[0]/btn[11]').Press()
    sleep(4)
    dlv = get_dlv_for_so(cursor, sales_order)
    print(f"SO {sales_order} - DLV {dlv}")

    return dlv


def make_transport_order_in_ylt03(session, cursor, delivery):
    session.StartTransaction(Transaction="YLT03")

    today = datetime.now().date().strftime("%d.%m.%Y")
    # today = datetime.now().date()
    # tomorrow = today + timedelta(days=1)
    # tomorrow = tomorrow.strftime("%d.%m.%Y")

    session.FindById('wnd[0]/usr/ctxtP_DATUM').text = today
    session.FindById('wnd[0]/usr/ctxtS_VBELN-LOW').text = delivery
    session.findById("wnd[0]/usr/chkP_TEST").selected = False

    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()

    transport_order = get_to_for_dlv(cursor, delivery)

    print(f"DLV {delivery} - TO", end=" ")
    for to in transport_order:
        print(f"{to}", end=" ")
    print()
    return transport_order[0]


def get_dlv_for_so(cursor, sales_order):
    cursor.execute(f"select VBELN from SAPECP.VBFA where VBELV='{sales_order}' ")
    try:
        return cursor.fetchone()[0]
    except TypeError:
        raise Exception(f"k zakazce {sales_order} se nepodarilo zalozit dodavku")


def get_to_for_dlv(cursor, dlv):
    cursor.execute(f"select VBELN from SAPECP.VBFA where VBTYP_N='Q' and  VBELV='{dlv}' ")
    try:
        to_list = [to[0].lstrip("0") for to in cursor.fetchall()]
        to_list = set(to_list)
        to_list = list(to_list)

        assert len(to_list) > 0, f"K dodavce {dlv} se nepovedlo zalozit skladove prikazy"

        return to_list
    except TypeError:
        raise Exception(f"k dodavce {dlv} se nepovedlo zalozit skladove prikazy")


if __name__ == '__main__':
    dlv = 2000000328
    so = 5510000972
    sess = initialization()
    cursor = create_hana_connection()
    # dlv = make_dlv(sess, so)
    # print(get_dlv_for_so(cursor, so))
    tos = make_transport_order_in_ylt03(sess, cursor, dlv)
