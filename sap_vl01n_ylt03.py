import win32com.client
import time
from datetime import datetime
from sap_getdata import get_dlv_for_so, get_to_for_dlv


def initialization():
    sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    session = sap_gui.FindById("ses[0]")

    return session


def make_dlv(session, sales_order):
    # make dlv from SO
    session.StartTransaction(Transaction="VL01N")
    today = datetime.now().date().strftime("%d.%m.%Y")
    session.FindById('wnd[0]/usr/ctxtLIKP-VSTEL').text = 1000
    session.FindById('wnd[0]/usr/ctxtLV50C-DATBI').text = today
    session.FindById('wnd[0]/usr/ctxtLV50C-VBELN').text = sales_order
    time.sleep(1)
    session.FindById('wnd[0]/tbar[0]/btn[0]').Press()
    session.FindById('wnd[0]/tbar[0]/btn[11]').Press()

    dlv = get_dlv_for_so(sales_order)
    print(f"SO {sales_order} - DLV {dlv}")

    return dlv


def make_transport_order_in_ylt03(session, delivery):
    # make transport order from delivery
    session.StartTransaction(Transaction="YLT03")

    today = datetime.now().date().strftime("%d.%m.%Y")
    session.FindById('wnd[0]/usr/ctxtP_DATUM').text = today
    session.FindById('wnd[0]/usr/ctxtS_VBELN-LOW').text = delivery
    session.findById("wnd[0]/usr/chkP_TEST").selected = False

    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()

    transport_order = get_to_for_dlv(delivery)

    # for line_no in range(2, 10):
    #     if session.FindById(f'wnd[0]/usr/lbl[0,{line_no}]').text.startswith("Vytvořen"):
    #         transport_order = session.FindById(f'wnd[0]/usr/lbl[0,{line_no}]').text.split()[3].lstrip("0")
    #         break

    print(f"DLV {delivery} - TO", end=" ")
    for to in transport_order:
        print(f"{to}", end=" ")
    print()
    return transport_order[0]


if __name__ == '__main__':
    so = 5510001340
    sess = initialization()
    dlv = make_dlv(sess, so)
    tos = make_transport_order_in_ylt03(sess, dlv)

