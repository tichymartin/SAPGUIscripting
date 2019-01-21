from other_folder.main import make_session, make_so, make_deliveries, make_transport_orders, append_transport_orders, \
    plan_route, picking_main, consolidation_main, append_control_orders, control_main, courier_main

if __name__ == '__main__':
    data = make_session("k4d")

    """
    maso - 1000439 
    ovozel - 1000399 
    normal - 1000441
    normal_long - 1000442
    mrazeny - 1000437 
    """
    data = make_so(data,
                   [
                       [
                           (1000441, 1, "PC"),
                       ],
                   ]
                   )
    # data["so"] = ["5510000821", ]
    data = make_deliveries(data)
    data = make_transport_orders(data)
    append_transport_orders(data)
    data = plan_route(data, terminal="TEST")

    data = picking_main(data)
    #
    data = consolidation_main(data)
    append_control_orders(data)
    # data = control_main(data)
    # data = courier_main(data)
