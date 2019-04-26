from other_folder.drivers import create_hana_connection


def get_table(session):
    session.StartTransaction(Transaction="se16n")
    session.FindById("wnd[0]/usr/ctxtGD-TAB").text = "MARA"
    session.FindById("wnd[0]/usr/txtGD-MAX_LINES").text = 10

    session.FindById("wnd[0]/tbar[1]/btn[8]").Press()


def get_data(session):
    grid = session.FindById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell")

    print(grid.GetCellValue(grid.CurrentCellRow, "MATNR"))
    print(grid.GetCellValue(0, "MATNR"))


def get_trasa(session):
    session.StartTransaction(Transaction="ZMONEX")
    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()
    table = session.FindById("wnd[0]/usr/cntlGRID1/shellcont/shell")
    print(table.GetCellValue(1, "ROUTE"))


def ywmqueue_remove_tos_from_user(session):
    session.StartTransaction(Transaction="YWMQUEUE")

    session.FindById('wnd[0]/usr/radR1').select()
    session.FindById('wnd[0]/usr/chkP_ROUTEP').selected = True
    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()

    grid_to_stock = session.FindById("/app/con[0]/ses[0]/wnd[0]/usr/shell/shellcont[1]/shell/shellcont[0]/shell")
    to_for_user = range(grid_to_stock.RowCount)
    grid_to_stock.selectedRows = f"{to_for_user[0]} - {to_for_user[-1]}"
    grid_to_stock.pressToolbarButton("BT_DEL")


def get_su_from_hana(storage_unit):
    cursor = create_hana_connection()
    cursor.execute(f"select lenum from sapecp.lein where LENUM = '{storage_unit:0>20}'")

    return cursor.fetchone()[0].lstrip("0")


if __name__ == '__main__':
    # sess = initialization()
    # get_table(sess)
    # get_data(sess)
    # zmonex(sess)
    # get_trasa(sess)
    su = '2100000001'
    # print(f"su je {su:0>20}")
    print(get_su_from_hana(su))
