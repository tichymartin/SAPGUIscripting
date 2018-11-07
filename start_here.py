from main2 import make_dlv_and_to, append_to_user, plan_route, picking

data = make_dlv_and_to([5510001357, ])
data = append_to_user(data)
data = plan_route(data)
data = picking(data)
print(data)
