from main2 import make_session, make_so, make_dlv_and_to, append_transport_orders, plan_route, picking_main, \
    consolidation_main, append_control_orders, control_main

data = make_session()
data = make_so(data,
               [[(1000435, 2, "PC"),
                 ],
                # [(1002180, 1, "PC"), (1000071, 1, "KG"), ],
                ]
               )
# data["so"] = ["5510000821", ]
data = make_dlv_and_to(data)
# data = append_transport_orders(data)
data = plan_route(data)
data = picking_main(data)
# data = consolidation_main(data)
# data = append_control_orders(data)
# data = control_main(data)
# print(data)
