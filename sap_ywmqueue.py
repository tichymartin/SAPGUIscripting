import win32com.client
from drivers import initialization
from config import system


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
    materials_d = {}
    grid_to = session.FindById("wnd[0]/usr/shell/shellcont[0]/shell")

    for to in transport_orders:

        for line in range(grid_to.RowCount):
            # print(grid_to.GetCellValue(line, "TANUM"))
            if grid_to.GetCellValue(line, "TANUM") == to:
                to_for_pick_lines.append(line)

                matnr = grid_to.GetCellValue(line, "MATNR")
                if matnr not in materials_d.keys():
                    if grid_to.GetCellValue(line, "/CWM/XCWMAT") == "X":
                        if grid_to.GetCellValue(line, "MEINS") == "KG":
                            materials_d[matnr] = {"CW": "OVOZEL"}
                            # materials_d[matnr]["amount"] = grid_to.GetCellValue(line, "VSOLM")
                        else:
                            materials_d[matnr] = {"CW": "MASO"}
                            materials_d[matnr]["amount"] = str(
                                float(grid_to.GetCellValue(line, "/CWM/TGT_QTY").replace(",", ".")) / int(
                                    grid_to.GetCellValue(line, "VSOLM")))

                        # materials_d[matnr]["parallel_quantity"] = grid_to.GetCellValue(line, "/CWM/TGT_QTY")
                    else:
                        materials_d[matnr] = {"CW": ""}
                # # add line to line counter for line selecting
                # to_lines.append(line)

        if len(to_for_pick_lines) == 0:
            print(f"skpr {transport_orders} nejsou ve fronte")
            return

    grid_to.selectedRows = f"{to_for_pick_lines[0]} - {to_for_pick_lines[-1]}"
    grid_to.pressToolbarButton("BT_ASSIGN")

    print(f"TO {transport_orders} assigned to {user}")

    return materials_d

    # helpful methods
    # grid.RowCount
    # grid.ColumnCount
    # GetCellValue(line, "name of column")
    # selectedRows = "cislo" nebo rozsah 1-2 a nebo vycet 2,3,7


if __name__ == '__main__':
    sess = initialization()
    to = ["335", ]
    x, y = ywmqueue(sess, to, user="S1268")
    # print(x)
    # print(y)
