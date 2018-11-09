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
from sap_create_so import create_json_for_so, create_so_from_sa38


def make_session():
    session = initialization()
    data = {"session": session}
    return data


def make_so(data, data_for_sales_order):
    data["so"] = []
    for sales_order_data in data_for_sales_order:
        data["json"] = create_json_for_so(sales_order_data)
        data["so"].append(create_so_from_sa38(data["session"], data["json"]))

    return data


def make_dlv_and_to(data):
    """
    :param data: session for sap gui controller, sales_order
    :return data: dictionary of data from process
    """

    data["user"] = user
    data["dlv"] = []
    data["to"] = []

    for so in data["so"]:
        dlv = make_dlv(data["session"], so)
        data["dlv"].append(dlv)
        data["to"].append(make_transport_order_in_ylt03(data["session"], dlv))

    return data


def append_to_user(data):
    data["items"], data["materials"] = ywmqueue(data["session"], data["to"], data["user"])

    return data


def plan_route(data):
    data["route"] = zmonex(data["session"], data["dlv"])

    return data


def picking_main(data):
    wd = get_driver()
    data["web_driver"] = wd
    login(wd, user, password)
    data["boxes"] = picking(data["web_driver"], data["items"], data["materials"])

    return data


def consolidation_main(data):
    data["boxes_for_control"] = consolidation(data["web_driver"], data["boxes"])
    return data

#
# data["boxes_for_shipping"] = control_main(wd, ses, data["boxes_for_control"], data["dlv"])
# print(data["boxes_for_shipping"])
#
# shipment(wd, data["route"], data["user"], data["boxes_for_shipping"])
# # close_browser(wd)
# print(data)
