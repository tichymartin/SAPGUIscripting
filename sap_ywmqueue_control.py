import win32com.client
from drivers import initialization
from config import system


def ywmqueue_control(session, deliveries, user):
    session.StartTransaction(Transaction="YWMQUEUE")

    session.FindById('wnd[0]/usr/radR3').select()
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

    dlv_for_control_lines = []
    grid_to = session.FindById("wnd[0]/usr/shell/shellcont[0]/shell")

    for delivery in deliveries:

        for line in range(grid_to.RowCount):
            if grid_to.GetCellValue(line, "VBELN") == delivery:
                dlv_for_control_lines.append(line)

    if len(dlv_for_control_lines) == 0:
        print(f"DLV {deliveries} nejsou ve fronte")
        return

    dlv_for_control_lines = sorted(dlv_for_control_lines)
    grid_to.selectedRows = f"{dlv_for_control_lines[0]} - {dlv_for_control_lines[-1]}"
    grid_to.pressToolbarButton("BT_ASSIGN")

    print(f"DLV {deliveries} assigned to {user}")

    return

    # helpful methods
    # grid.RowCount
    # grid.ColumnCount
    # GetCellValue(line, "name of column")
    # selectedRows = "cislo" nebo rozsah 1-2 a nebo vycet 2,3,7


if __name__ == '__main__':
    sess = initialization()
    deliveries = ['2000000578', '2000000579']
    user = "S1268"

    ywmqueue_control(sess, deliveries, user)
