from sap_vl01n_ylt03 import make_dlv, make_transport_order_in_ylt03
from sap_ywmqueue import ywmqueue
from trx_picking import picking_main
from trx_consolidation import consolidation
from trx_control import control_main
from trx_shipping import shipment
from sap_zmonex import zmonex
from sap_getdata import get_route_hana
from config import user, password
from drivers import login, get_driver, close_browser, initialization


def make_dlv_and_to(so):
    """
    :param so: list of standard orders
    :return data: dictionary of data from process
    """
    session = initialization()
    data = {"so": so,
            "user": user,
            "session": session,
            "dlv": [],
            "to": []}
    for so in data["so"]:
        dlv = make_dlv(session, so)
        data["dlv"].append(dlv)
        data["to"].append(make_transport_order_in_ylt03(session, dlv))

    return data


def append_to_user(data):
    data["items"], data["materials"] = ywmqueue(data["session"], data["to"], data["user"])

    return data


def plan_route(data):
    data["route"] = zmonex(data["session"], data["dlv"])

    return data


def picking(data):
    wd = get_driver()
    data["web_driver"] = wd
    login(wd, user, password)
    data["boxes"] = picking_main(data["web_driver"], data["items"], data["materials"])

    return data
# print(data["boxes"])
# data["boxes_for_control"] = consolidation(wd, data["boxes"])
# print(data["boxes_for_control"])
#
# data["boxes_for_shipping"] = control_main(wd, ses, data["boxes_for_control"], data["dlv"])
# print(data["boxes_for_shipping"])
#
# shipment(wd, data["route"], data["user"], data["boxes_for_shipping"])
# # close_browser(wd)
# print(data)
