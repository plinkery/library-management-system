with open('report_assets/generate_er_svg_v2.py', 'r') as f:
    code = f.read()

# 1. Update created_at
code = code.replace("add_attr('USERS', 'created_at', 1050, 1310, 105, 34)",
                    "add_attr('USERS', 'created_at', 980, 1260, 105, 34)")

# 2. Update Card:(0,N)
code = code.replace("add_cardinality('(0,N)', 990, 1330)",
                    "add_cardinality('(0,N)', 1030, 1360)")

# 3. Update RESERVATIONS attributes
old_res = """    add_attr('RESERVATIONS', 'reservation_id', 470, 1860, 125, 34, is_pk=True)
    add_attr('RESERVATIONS', 'reserved_at', 590, 1895, 110, 34)
    add_attr('RESERVATIONS', 'expires_at', 710, 1895, 105, 34)
    add_attr('RESERVATIONS', 'status', 830, 1860, 90, 34)"""

new_res = """    add_attr('RESERVATIONS', 'reservation_id', 450, 1860, 125, 34, is_pk=True)
    add_attr('RESERVATIONS', 'reserved_at', 585, 1895, 110, 34)
    add_attr('RESERVATIONS', 'expires_at', 715, 1895, 105, 34)
    add_attr('RESERVATIONS', 'status', 845, 1860, 90, 34)"""

code = code.replace(old_res, new_res)

with open('report_assets/generate_er_svg_v2.py', 'w') as f:
    f.write(code)
print("Updated generate_er_svg_v2.py successfully")
