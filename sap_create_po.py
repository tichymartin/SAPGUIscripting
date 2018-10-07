from drivers import initialization


def create_po(session, bussines_partner, materials):
    session.StartTransaction(Transaction="me21n")

    session.FindById(
        "wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB0:SAPLMEGUI:0030/subSUB1:SAPLMEGUI:1105/ctxtMEPO_TOPLINE-SUPERFIELD").text = bussines_partner
    session.FindById("wnd[0]").sendVKey(0)
    for count, material in enumerate(materials):
        session.FindById(
            f"wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-EMATN[5,{count}]").text = material
        session.FindById(
            f"wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/txtMEPO1211-MENGE[7,{count}]").text = "10"
    session.FindById("wnd[0]").sendVKey(0)
    session.FindById("wnd[0]/tbar[0]/btn[11]").press()
    session.FindById("wnd[1]/usr/btnSPOP-VAROPTION1").press()
    text_po = session.FindById("wnd[0]/sbar").text
    po_txt = text_po.split()[-1]

    return po_txt


def create_indlvs(session, purchase_order):
    session.StartTransaction(Transaction="vl31n")
    session.FindById("wnd[0]/usr/txtLV50C-BSTNR").text = purchase_order
    session.FindById("wnd[0]").sendVKey(0)
    session.FindById("wnd[0]/tbar[0]/btn[11]").press()
    text_indls = session.FindById("wnd[0]/sbar").text
    indls_text = text_indls.split()[-2]

    return indls_text


def open_indls_for_trx(session, inbound_delivery):
    session.StartTransaction(Transaction="/s2ap/les_idlvmon")
    session.FindById("wnd[0]/usr/ctxtP_VBELN-LOW").text = inbound_delivery
    session.FindById("wnd[0]/tbar[1]/btn[8]").press()

    session.FindById("wnd[0]/usr/cntlGRID1/shellcont/shell").selectedRows = "0"
    session.FindById("wnd[0]/tbar[1]/btn[9]").press()
    session.FindById("wnd[1]/tbar[0]/btn[0]").press()


def main_po(bussines_partner, materials):
    session = initialization()
    purchase_order = create_po(session, bussines_partner, materials)
    print(f"PO {purchase_order}")
    inbound_delivery = create_indlvs(session, purchase_order)
    print(f"INDLS {inbound_delivery}")
    open_indls_for_trx(session, inbound_delivery)
    print(f"INDLS {inbound_delivery} opened in TRX")
    return inbound_delivery


if __name__ == '__main__':
    sess = initialization()
    bp = "5000000044"
    materials = ["1000357", "1000358"]
    # data = {}
    #
    # # data["purchase_order"] = create_po(sess, bp, materials)
    # data["purchase_order"] = "4500000352"
    # data["indls"] = create_indlvs(sess, data["purchase_order"])
    # # data["indls"] = "180000240"
    # open_indls_for_trx(sess, data["indls"])
    # # print(data)

    main_po(sess, bp, materials)
