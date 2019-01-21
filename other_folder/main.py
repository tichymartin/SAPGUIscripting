from sap_folder.sap_vl01n_ylt03 import make_dlv, make_transport_order_in_ylt03
from sap_folder.sap_ywmqueue import ywmqueue
from trx_folder.trx_picking import picking
from trx_folder.trx_consolidation import consolidation
from trx_folder.trx_control import control
from sap_folder.sap_zmonex import zmonex
from config import user, password
from other_folder.drivers import login, get_driver, initialization
from sap_folder.sap_create_so import create_json_for_so, create_so_from_sa38
from sap_folder.sap_ywmqueue_control import ywmqueue_control
from trx_folder.trx_courier import courier
from other_folder.drivers import hana_cursor


def make_session(system):
    session = initialization()
    cursor = hana_cursor(system)
    data = {"session": session, "cursor": cursor, "user": user, "system": system}
    return data


def make_so(data, data_for_sales_order, customer=None):
    data["so"] = []
    for sales_order_data in data_for_sales_order:
        data["json"] = create_json_for_so(sales_order_data, customer)
        data["so"].append(create_so_from_sa38(data["session"], data["json"]))

    return data


def make_deliveries(data):
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
    ywmqueue(data["session"], data["to"], data["user"])

    return data


def plan_route(data, terminal):
    data["route"] = zmonex(data["session"], data["cursor"], data["deliveries"], terminal)

    return data


def picking_main(data):
    data["web_driver"] = get_driver(data["system"])
    login(data["web_driver"], data["user"], password)
    picking(data["web_driver"], data["cursor"], data["user"])

    return data


def consolidation_main(data):
    data["web_driver"] = consolidation(data["web_driver"], data["cursor"], data["deliveries"])

    return data


def append_control_orders(data):
    ywmqueue_control(data["session"], data["deliveries"], data["user"])


def control_main(data):
    data["web_driver"] = control(data["web_driver"], data["cursor"], data["deliveries"])

    return data


def courier_main(data):
    data["web_driver"] = courier(data["web_driver"], data["cursor"], data["deliveries"])

    return data

#
# shipment(wd, data["route"], data["user"], data["boxes_for_shipping"])
# # close_browser(wd)
# print(data)
