import pytest
import pyhdb

from other_folder.drivers import initialization, get_driver, login, close_browser
from config import user, password

from sap_folder.sap_create_so import create_so_from_sa38
from other_folder.json_creater import create_json_for_so
from sap_folder.sap_vl01n_ylt03 import make_dlv, make_transport_order_in_ylt03
from sap_folder.sap_zmonex import zmonex
from sap_folder.sap_ywmqueue import ywmqueue
from trx_folder.trx_picking import picking


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


# single material
@pytest.fixture(scope="session")
def materials():
    materials = [(1000396, 1, "PC"), ]
    return materials


# use of parametrizide fixture
# @pytest.fixture(params=([(1000396, 1, "PC")], [(1000399, 1, "PC")], [(1000431, 1, "PC")]), scope="session")
# def materials(request):
#     return request.param


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


@pytest.fixture(scope="session")
def append_to_to_user(session, transport_order):
    ywmqueue(session, transport_order, user)


@pytest.fixture(scope="session")
def driver():
    return get_driver()


@pytest.fixture(scope="session")
def login_fix(driver):
    login(driver, user, password)

    yield

    close_browser(driver)


@pytest.fixture(scope="session")
def picking_fix(driver, login_fix, cursor):
    hu = picking(driver, cursor, user)
    return hu
