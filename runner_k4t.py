from other_folder.main import make_session, make_so, make_deliveries, make_transport_orders, append_transport_orders, \
    plan_route, picking_main, consolidation_main, append_control_orders, control_main, courier_main
from time import sleep

if __name__ == '__main__':
    data = make_session("k4t")

    """
    mat no batch - 1002181
    mat maso - 1002345
    mat ovozel - 1002185 
    mat batch pc - 1002338
    mat_pc - 1002351
    mat_pc 10kg - 1002352
    
    """
    data = make_so(data,
                   [
                       [
                           (1002351, 1, "PC"),
                           (1002351, 1, "PC"),
                           (1002351, 1, "PC"),
                           (1002351, 1, "PC"),
                       ],
                   ],
                   # "1000001288",
                   )
    # data["so"] = ["5510000821", ]
    data = make_deliveries(data)
    data = make_transport_orders(data)
    append_transport_orders(data)
    # data = plan_route(data, terminal="TEST")
    sleep(3)
    data = picking_main(data)

    data = consolidation_main(data)
    append_control_orders(data)
    data = control_main(data)
    # data = courier_main(data)
