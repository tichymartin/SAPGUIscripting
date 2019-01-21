from other_folder.drivers import initialization


def ywmqueue(session, transport_orders, user):
    session.StartTransaction(Transaction="YWMQUEUE")

    session.FindById('wnd[0]/usr/radR1').select()
    session.FindById('wnd[0]/usr/chkP_ROUTEP').selected = True
    session.FindById('wnd[0]/tbar[1]/btn[8]').Press()

    grid_users = session.FindById("wnd[0]/usr/shell/shellcont[1]/shell/shellcont[1]/shell")
    for lin in range(grid_users.RowCount):
        if grid_users.GetCellValue(lin, "QUEUE_ID") == user:
            grid_users.currentCellRow = lin
            break
    grid_users.doubleClickCurrentCell()

    grid_to_stock = session.FindById("wnd[0]/usr/shell/shellcont[1]/shell/shellcont[0]/shell")
    if grid_to_stock.RowCount > 0:
        to_for_user = range(grid_to_stock.RowCount)
        grid_to_stock.selectedRows = f"{to_for_user[0]} - {to_for_user[-1]}"
        grid_to_stock.pressToolbarButton("BT_DEL")

    to_for_pick_lines = []

    grid_to = session.FindById("wnd[0]/usr/shell/shellcont[0]/shell")

    for to in transport_orders:

        for line in range(grid_to.RowCount):
            if grid_to.GetCellValue(line, "TANUM") == to:
                to_for_pick_lines.append(line)

        # if not to.intersection(set(to_for_pick_lines)):
        #     print(f"{to} nenalezen v YWMQUEUE")

    assert len(to_for_pick_lines) > 0, "Neprirazen zadny skladovy prikaz"

    grid_to.selectedRows = f"{to_for_pick_lines[0]} - {to_for_pick_lines[-1]}"
    grid_to.pressToolbarButton("BT_ASSIGN")

    print(f"TO {transport_orders} assigned to {user}")

    # helpful methods
    # grid.RowCount
    # grid.ColumnCount
    # GetCellValue(line, "name of column")
    # selectedRows = "cislo" nebo rozsah 1-2 a nebo vycet 2,3,7


if __name__ == '__main__':
    sess = initialization()
    to = ["2057", ]
    ywmqueue(sess, to, user="S1268")
    # print(x)
    # print(y)
