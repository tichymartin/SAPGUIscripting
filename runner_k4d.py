import sys
from other_folder.main import make_session, web_driver_and_login, make_so, make_deliveries, make_transport_orders, \
    append_transport_orders, \
    plan_route, picking_main, consolidation_main, append_control_orders, control_main, courier_main, \
    append_shipment_orders, unsorted_shipment, sorted_shipment, finalized_shipment, close_session
from time import sleep

if __name__ == '__main__':

    try:
        data = make_session("k4d")
        """
        maso - 1000439 
        ovozel - 1000399 
        normal_new - 1000536
        mrazeny - 1000437 
        bezobalu - 1000547 
        """
        data = make_so(data,
                       [
                           [
                               (1000536, 2, "PC"),
                               # (1000536, 2, "PC"),
                           ],
                       ],
                       # "1000001337",
                       )
        # data["so"] = ["5510000821", ]
        data = make_deliveries(data)
        data = make_transport_orders(data)
        append_transport_orders(data)
        # # #
        # sleep(3)
        data = web_driver_and_login(data)
        data = picking_main(data)
        #
        data = consolidation_main(data)
        append_control_orders(data)
        data = control_main(data)
        data = courier_main(data)
        data = plan_route(data, terminal="TEST")
        append_shipment_orders(data)
        data = unsorted_shipment(data)
        data = sorted_shipment(data)
        data = finalized_shipment(data)

    except:
        print(sys.exc_info()[0])
        print("error nekde")

    finally:
        data = close_session(data)
