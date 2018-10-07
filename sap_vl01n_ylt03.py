import win32com.client


def initialization():
    sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    session = sap_gui.FindById("ses[0]")

    return session


def make_dlv(session, sales_order):
    # make dlv from SO
    session.StartTransaction(Transaction="VL01N")

    session.FindById('wnd[0]/usr/ctxtLIKP-VSTEL').text = 1000
    session.FindById('wnd[0]/usr/ctxtLV50C-VBELN').text = sales_order

    session.FindById('wnd[0]/tbar[0]/btn[0]').Press()
    session.FindById('wnd[0]/tbar[0]/btn[11]').Press()

    dlv = session.FindById('wnd[0]/sbar/pane[0]').text.split()[1]

    print(f"from {sales_order} created delivery {dlv}")
    return dlv


def make_transport_order_in_ylt03(session, delivery):
    # make transport order from delivery
    session.StartTransaction(Transaction="YLT03")

    # session.FindById('wnd[0]/usr/ctxtP_DATUM').text = "21.8.2018"
    session.FindById('wnd[0]/usr/ctxtS_VBELN-LOW').text = delivery
    session.findById("wnd[0]/usr/chkP_TEST").selected = False
    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()
    # print(dir(session.FindById('wnd[0]/usr/ctxtS_VBELN-LOW'))).

    for line_no in range(2, 10):
        if session.FindById(f'wnd[0]/usr/lbl[0,{line_no}]').text.startswith("Vytvořen"):
            transport_order = session.FindById(f'wnd[0]/usr/lbl[0,{line_no}]').text.split()[3].lstrip("0")
            break

    print(f"for delivery {delivery} created transport order {transport_order}")
    return transport_order


if __name__ == '__main__':
    so = 5510000585
    sess = initialization()
    dlv = make_dlv(sess, so)
    print(f"delivery {dlv}")
    to = make_transport_order_in_ylt03(sess, dlv)
    print(f"transport order {to}")
    # print(dlv)
