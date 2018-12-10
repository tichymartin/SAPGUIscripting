import pytest
import pyhdb

from sap_create_so import create_so_from_sa38
from json_creater import create_json_for_so
from sap_vl01n_ylt03 import make_dlv, make_transport_order_in_ylt03
from sap_zmonex import zmonex

from drivers import initialization


@pytest.fixture(scope="session")
def cursor():
    connection = pyhdb.connect(
        host="10.200.81.10",
        port=32015,
        user="TEST_RESULT",
        password="Results85!",
    )

    yield connection.cursor()

    connection.close()


@pytest.fixture(scope='session')
def session():
    session = initialization()
    return session


@pytest.fixture(scope="session")
def materials():
    materials = [(1000396, 1, "PC"), ]
    return materials


@pytest.fixture(scope="session")
def sales_order(session, materials):
    json = create_json_for_so(materials)
    so = create_so_from_sa38(session, json)
    return so


@pytest.fixture(scope="session")
def delivery(session, cursor, sales_order):
    dlv = make_dlv(session, cursor, sales_order)
    return dlv


@pytest.fixture(scope="session")
def transport_order(session, cursor, delivery):
    to = make_transport_order_in_ylt03(session, cursor, delivery)
    return to


@pytest.fixture(scope="session")
def route(session, cursor, delivery):
    dlv_list = [delivery]
    zmonex(session, cursor, dlv_list)
