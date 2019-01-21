from other_folder.drivers import initialization
from other_folder.json_creater import create_json_for_so


def create_so_from_sa38(session, json):
    session.StartTransaction(Transaction="sa38")
    session.FindById("wnd[0]/usr/ctxtRS38M-PROGRAMM").text = "YECH_UT_WEB_CREATE_ORDER_JSON"
    session.FindById("wnd[0]/tbar[1]/btn[8]").press()
    session.FindById("wnd[0]/usr/cntlTEXTEDITOR1/shellcont/shell").text = json
    session.FindById("wnd[0]/tbar[0]/btn[11]").press()

    line_counter = 3
    while True:

        order_line = session.FindById(f"wnd[1]/usr/lbl[9,{line_counter}]").text
        if order_line.startswith(".ECH"):
            sales_order = int(order_line.split()[2])
            print(f"SO {sales_order}")
            break
        elif order_line.startswith("<<<< Chyba"):
            raise Exception("ERROR - SO not created, check JSON")
        else:
            line_counter += 1
            if line_counter == 30:
                break

    session.FindById("wnd[1]").close()

    return sales_order


if __name__ == '__main__':

    materials = [(1000357, 1, "PC"), ]
    json = create_json_for_so(materials)

    session = initialization()

    create_so_from_sa38(session, json)
