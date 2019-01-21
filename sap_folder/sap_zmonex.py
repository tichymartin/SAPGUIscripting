import win32com.client
from sap_folder.sap_getdata import get_route_hana
from other_folder.drivers import hana_cursor


def initialization():
    sap_gui = win32com.client.GetObject("SAPGUI").GetScriptingEngine
    session = sap_gui.FindById("ses[0]")

    return session


def verify_button_and_press(session=None, control=None):
    try:
        session.FindById(control)
        session.FindById(control).Press()

    except:
        # Do something else here if needed
        pass


def verify(session=None, control=None):
    try:
        return session.FindById(control)

    except:
        # Do something else here if needed
        return


def zmonex(session, cursor, delivery, terminal):
    session.StartTransaction(Transaction="ZMONEX")

    # today = datetime.now().date().strftime("%d.%m.%Y")
    # session.FindById('wnd[0]/usr/txt%_P_LFDAT_%_APP_%-TEXT').text = today

    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()
    session.FindById('wnd[0]/tbar[1]/btn[7]').Press()

    grid_dlv = session.FindById("wnd[0]/usr/cntlGRID1/shellcont/shell")

    len_row = grid_dlv.RowCount - 1

    if len_row > len(delivery):
        list_dlvs = list(range(len_row))
        for dlv in delivery:

            for line in range(len_row):
                # print(grid_dlv.GetCellValue(line, "VBELN"))
                if grid_dlv.GetCellValue(line, "VBELN") == dlv:
                    list_dlvs.remove(line)

            if len(list_dlvs) == len_row:
                print(f"delivery {delivery} neni ve fronte zmonex")
                return

        string_dlvs = "".join(str(list_dlvs))
        grid_dlv.selectedRows = f"{string_dlvs}"

        session.FindById("wnd[0]/tbar[1]/btn[18]").Press()

    grid_dlv.selectedRows = f"{list(range(grid_dlv.RowCount - 1))}"
    session.FindById("wnd[0]/tbar[1]/btn[13]").Press()
    verify_button_and_press(session, "wnd[1]/usr/btnBUTTON_1")
    # or verify and if not None, than press
    session.FindById("wnd[1]/tbar[0]/btn[0]").Press()
    session.FindById("wnd[0]/tbar[1]/btn[14]").Press()
    session.FindById("wnd[1]/tbar[0]/btn[0]").Press()

    route = get_route_hana(cursor, delivery[0])

    session.FindById("wnd[0]/tbar[0]/btn[3]").Press()
    session.FindById("wnd[0]/tbar[1]/btn[8]").Press()

    zmon_main_grid = session.FindById("wnd[0]/usr/cntlGRID1/shellcont/shell")
    main_len_row = zmon_main_grid.RowCount - 1
    for zmon_row in range(main_len_row)[1:]:
        if zmon_main_grid.GetCellValue(zmon_row, "ROUTE") == route:
            # zmon_main_grid.selectedRows = zmon_row
            zmon_main_grid.setCurrentCell(zmon_row, "ROUTE")
            break

    session.FindById("wnd[0]/tbar[1]/btn[20]").Press()
    session.FindById("wnd[1]/usr/ctxtYECH_POS_TERM-TERM_ID").text = terminal
    session.FindById("wnd[1]/tbar[0]/btn[8]").Press()

    print(f"DLV {delivery} - ROUTE {route}")


def get_route(session, delivery):
    session.StartTransaction(Transaction="se16n")
    session.FindById("wnd[0]/usr/ctxtGD-TAB").text = "LIKP"
    session.FindById("wnd[0]").sendVKey(0)
    session.FindById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,1]").text = delivery
    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()
    table = session.FindById('wnd[0]/usr/cntlRESULT_LIST/shellcont/shell')
    route = table.GetCellValue(0, "ROUTE")

    return route


def get_matn_from_to(session, transport_order):
    session.StartTransaction(Transaction="se16n")
    session.FindById("wnd[0]/usr/ctxtGD-TAB").text = "LTAP"
    session.FindById("wnd[0]").sendVKey(0)
    session.FindById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,2]").text = transport_order
    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()
    table = session.FindById('wnd[0]/usr/cntlRESULT_LIST/shellcont/shell')
    materials = []
    for item in range(table.RowCount):
        materials.append(table.GetCellValue(item, "MATNR"))

    return materials


def check_CW_matn(session, materials):
    # materials = ['1001618', '1001619']
    mat_dict = {}
    for material in materials:
        session.StartTransaction(Transaction="se16n")
        session.FindById("wnd[0]/usr/ctxtGD-TAB").text = "MARA"
        session.FindById("wnd[0]").sendVKey(0)
        session.FindById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxtGS_SELFIELDS-LOW[2,1]").text = material
        session.FindById('wnd[0]/tbar[1]/btn[8]').Press()
        table = session.FindById('wnd[0]/usr/cntlRESULT_LIST/shellcont/shell')
        # print(table.GetCellValue(0, "CWQREL"), table.GetCellValue(0, "MEINS"))
        mat_dict[material] = (table.GetCellValue(0, "CWQREL"), table.GetCellValue(0, "MEINS"))

    return mat_dict


def tzmonex(session, delivery):
    session.StartTransaction(Transaction="ZMONEX")

    # today = datetime.now().date().strftime("%d.%m.%Y")
    # session.FindById('wnd[0]/usr/txt%_P_LFDAT_%_APP_%-TEXT').text = today

    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()
    session.FindById('wnd[0]/tbar[1]/btn[7]').Press()

    route = get_route_hana(delivery[0])

    session.FindById("wnd[0]/tbar[0]/btn[3]").Press()
    session.FindById("wnd[0]/tbar[1]/btn[8]").Press()

    zmon_main_grid = session.FindById("wnd[0]/usr/cntlGRID1/shellcont/shell")
    main_len_row = zmon_main_grid.RowCount - 1
    for zmon_row in range(main_len_row)[1:]:
        if zmon_main_grid.GetCellValue(zmon_row, "ROUTE") == route:
            # zmon_main_grid.selectedRows = zmon_row
            zmon_main_grid.setCurrentCell(zmon_row, "ROUTE")
            break

    session.FindById("wnd[0]/tbar[1]/btn[20]").Press()
    session.FindById("wnd[1]/usr/ctxtYECH_POS_TERM-TERM_ID").text = "TEST"
    session.FindById("wnd[1]/tbar[0]/btn[8]").Press()

    print(f"DLV {delivery} - ROUTE {route}")


if __name__ == '__main__':
    sess = initialization()
    cursor = hana_cursor("k4t")
    dlv = ['2000000090', ]

    zmonex(sess, cursor, dlv, terminal="TEST")
