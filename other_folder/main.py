import os
from sap_folder.sap_create_so import create_json_for_so, create_so_from_sa38
from sap_folder.sap_vl01n_ylt03 import make_dlv, make_transport_order_in_ylt03
from sap_folder.sap_zmonex import zmonex
from sap_folder.sap_ywmqueue import ywmqueue
from sap_folder.sap_ywmqueue_control import ywmqueue_control
from sap_folder.sap_ywmqueue_shipping import ywmqueue_shiping

from trx_folder.trx_picking import picking
from trx_folder.trx_consolidation import consolidation
from trx_folder.trx_control import control
from trx_folder.trx_courier import courier
from trx_folder.trx_shipment_preparation import shipment_unsorted
from trx_folder.trx_shipment_sorting import shipment_sorted
from trx_folder.trx_shipping import shipping

from other_folder.drivers import login, get_driver, initialization, cls_session
from other_folder.drivers import create_hana_connection, close_hana_connection


# def make_session(system):
#     session = initialization()
#     cursor = hana_cursor(system)
#     data = {"session": session, "cursor": cursor, "user": os.environ.get("SAP_USER"), "system": system}
#     return data

def make_session(system):
    session, connection, application, sap_gui_auto = initialization()
    db_connection = create_hana_connection(system)
    cursor = db_connection.cursor()
    data = {"session": session, "connection": connection, "application": application, "sap_gui_auto": sap_gui_auto,
            "cursor": cursor, "user": os.environ.get("SAP_USER"), "system": system, "db_connection": db_connection}
    return data


def close_session(data):
    cls_session(data["session"], data["connection"], data["application"], data["sap_gui_auto"])
    close_hana_connection(data["db_connection"], data["cursor"])


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


def web_driver_and_login(data):
    data["web_driver"] = get_driver(data["system"])
    login(data["web_driver"])

    return data


def picking_main(data):
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


def append_shipment_orders(data):
    ywmqueue_shiping(data["session"], data["deliveries"], data["user"])


def unsorted_shipment(data):
    data["web_driver"] = shipment_unsorted(data["web_driver"], data["cursor"], data["deliveries"])

    return data


def sorted_shipment(data):
    data["web_driver"] = shipment_sorted(data["web_driver"], data["cursor"], data["route"])

    return data


def finalized_shipment(data):
    data["web_driver"] = shipping(data["web_driver"], data["cursor"], data["route"], data["user"])

    return data
