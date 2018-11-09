from sap_vl01n_ylt03 import make_dlv, make_transport_order_in_ylt03
from sap_ywmqueue import ywmqueue
from trx_picking import picking
from trx_consolidation import consolidation
from trx_control import control_main
from trx_shipping import shipment
from sap_zmonex import zmonex
from sap_getdata import get_route_hana
from config import user, password
from drivers import login, get_driver, close_browser, initialization

if __name__ == '__main__':

    data = {"so": [5510001358,
                   ], "user": user}
    ses = initialization()
    data["dlv"] = []
    data["to"] = []
    for so in data["so"]:
        dlv = make_dlv(ses, so)
        data["dlv"].append(dlv)
        data["to"].append(make_transport_order_in_ylt03(ses, dlv))

    data["items"], data["materials"] = ywmqueue(ses, data["to"], data["user"])
    zmonex(ses, data["dlv"])

    data["route"] = get_route_hana(data["dlv"][0])
    print(data)

    wd = get_driver()
    login(wd, user, password)
    #
    data["boxes"] = picking(wd, data["items"], data["materials"])
    #
    # print(data["boxes"])
    # data["boxes_for_control"] = consolidation(wd, data["boxes"])
    # print(data["boxes_for_control"])
    #
    # data["boxes_for_shipping"] = control_main(wd, ses, data["boxes_for_control"], data["dlv"])
    # print(data["boxes_for_shipping"])
    #
    # shipment(wd, data["route"], data["user"], data["boxes_for_shipping"])
    # # close_browser(wd)
    print(data)
