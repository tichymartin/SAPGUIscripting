from main2 import make_session, make_so, make_dlv_and_to, append_to_user, plan_route, picking_main

data = make_session()
data = make_so(data, [[(1000397, 1, "PC"), ], [(1000397, 1, "PC"), ]])
data = make_dlv_and_to(data)
data = append_to_user(data)
data = plan_route(data)
data = picking_main(data)
print(data)
