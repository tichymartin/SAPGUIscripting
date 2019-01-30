from other_folder.main import make_session, make_so, make_deliveries, make_transport_orders, append_transport_orders, \
    plan_route, picking_main, consolidation_main, append_control_orders, control_main, courier_main, \
    append_shipment_orders, unsorted_shipment, sorted_shipment, finalized_shipment
from time import sleep

if __name__ == '__main__':
    data = make_session("k4t")

    """
    CW_MASO - chlazene
    1009885 - 5000000432 - 291210 - 2912100003707, 2912100003714
    *1009886
    *1009887
    *1009888
    *1009889
    
    CW_OVOZEL
    1011725 - 06
    # 1011739 - 05 - 3,125kg 
    1011741 - 05 - 0,200kg - 5000000062
    *1011743 - 04 - 5000000062
    
    Suche_PC
    1002351 - 5000000053
    1002352 - 5000000053
    
    Chlazene_PC
    1009987 - 5000000327
    *1009988
    
    Mrazene_PC
    1009801
    1009802


    
    
    """
    data = make_so(data,
                   [
                       [
                           (1002351, 2, "PC"),
                       ],
                   ],
                   # "1000001289",
                   )
    # data["so"] = ["5510000821", ]
    data = make_deliveries(data)
    data = make_transport_orders(data)
    append_transport_orders(data)

    sleep(3)
    data = picking_main(data)

    data = consolidation_main(data)
    append_control_orders(data)
    data = control_main(data)
    data = courier_main(data)
    data = plan_route(data, terminal="TEST")
    append_shipment_orders(data)
    data = unsorted_shipment(data)
    data = sorted_shipment(data)
    data = finalized_shipment(data)
