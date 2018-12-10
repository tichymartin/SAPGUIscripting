from main2 import make_session, make_so, make_deliveries, make_transport_orders, append_transport_orders, plan_route, picking_main, \
    consolidation_main, append_control_orders, control_main, courier_main

data = make_session()
data = make_so(data,
               [[(1000397, 1, "PC"),
                 (1000397, 1, "PC"),
                 ],
                # [(1000397, 1, "PC"),
                # # (1000071, 1, "KG"),
                #  ],
                ]
               )
# data["so"] = ["5510000821", ]
# data = make_deliveries(data)
# data = make_transport_orders(data)
data = append_transport_orders(data)
# data = plan_route(data)
#
# data = picking_main(data)
#
# consolidation_main(data)
# append_control_orders(data)
# control_main(data)
# courier_main(data)
# print(data)
