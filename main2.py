from sap_vl01n_ylt03 import make_dlv, make_transport_order_in_ylt03
from sap_ywmqueue import ywmqueue
from trx_picking import picking
from trx_consolidation import consolidation
from trx_control import control
from trx_shipping import shipment
from sap_zmonex import zmonex
from sap_getdata import get_route_hana
from config import user, password
from drivers import login, get_driver, close_browser, initialization
from sap_create_so import create_json_for_so, create_so_from_sa38
from sap_ywmqueue_control import ywmqueue_control
from trx_courier import courier
from drivers import hana_cursor


def make_session():
    session = initialization()
    cursor = hana_cursor()
    data = {"session": session, "cursor": cursor, "user": user}
    return data


def make_so(data, data_for_sales_order):
    data["so"] = []
    for sales_order_data in data_for_sales_order:
        data["json"] = create_json_for_so(sales_order_data)
        data["so"].append(create_so_from_sa38(data["session"], data["json"]))

    return data


def make_deliveries(data):
    """
    :param data: session for sap gui controller, sales_order
    :return data: dictionary of data from process
    """

    data["deliveries"] = []

    for so in data["so"]:
        data["deliveries"].append(make_dlv(data["session"], data["cursor"], so))

    return data


def make_transport_orders(data):
    data["to"] = []
    for dlv in data["deliveries"]:
        data["to"].append(make_transport_order_in_ylt03(data["session"], data["cursor"], dlv))

    return data


def append_transport_orders(data):
    data["materials"] = ywmqueue(data["session"], data["to"], data["user"])

    return data


def plan_route(data):
    data["route"] = zmonex(data["session"], data["cursor"], data["deliveries"])

    return data


def picking_main(data):
    wd = get_driver()
    data["web_driver"] = wd
    login(data["web_driver"], data["user"], password)
    data["boxes_for_consolidation"] = picking(data["web_driver"], data["cursor"], data["to"], data["materials"])

    return data


def consolidation_main(data):
    data["web_driver"] = consolidation(data["web_driver"], data["cursor"], data["deliveries"])
    return data


def append_control_orders(data):
    ywmqueue_control(data["session"], data["deliveries"], data["user"])
    return data


def control_main(data):
    control(data["web_driver"], data["cursor"], data["deliveries"])
    return data


def courier_main(data):
    courier(data["web_driver"], data["cursor"], data["deliveries"])
    return data

#
# shipment(wd, data["route"], data["user"], data["boxes_for_shipping"])
# # close_browser(wd)
# print(data)
