from other_folder.main import make_session, web_driver_and_login, make_so, make_deliveries, make_transport_orders, \
    append_transport_orders, \
    plan_route, picking_main, consolidation_main, append_control_orders, control_main, courier_main, \
    append_shipment_orders, unsorted_shipment, sorted_shipment, finalized_shipment
from time import sleep

if __name__ == '__main__':
    data = make_session("k4q")
    data = web_driver_and_login(data)

    """
    CW_MASO - chlazene

    
    CW_OVOZEL

    
    Suche_PC
    1001488
    
    Chlazene_PC

    
    Mrazene_PC



    
    
    """
    data = make_so(data,
                   [
                       [
                           (1001488, 1, "PC"),
                           (1001488, 1, "PC"),
                           (1001488, 1, "PC"),
                       ],
                       # [
                       #     (1002351, 1, "PC"),
                       # ],
                       # [
                       #     (1011751, 3, "PC"),
                       #     # (1002351, 40, "PC"),
                       #     # (1002351, 2, "PC"),
                       # ],
                   ],
                   # you can add business partner
                   # "1000001289",
                   )

    # data["so"] = ["5510000821", ]
    # data["deliveries"] = ["2000000222", ]
    # data["route"] = "100001"

    data = make_deliveries(data)
    data = make_transport_orders(data)
    append_transport_orders(data)
    sleep(3)
    #
    data = picking_main(data)
    #
    data = plan_route(data, terminal="TEST")
    #
    data = consolidation_main(data)
    append_control_orders(data)
    # data = control_main(data)
    # data = plan_route(data, terminal="TEST")
    # data = courier_main(data)
    #
    # append_shipment_orders(data)
    # data = unsorted_shipment(data)
    # data = sorted_shipment(data)
    # data = finalized_shipment(data)
