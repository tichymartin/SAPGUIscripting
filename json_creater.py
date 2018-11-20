import json
import codecs
import copy
from datetime import datetime


def create_json_for_so(materials):

    header = {
        "sd_doc": "",
        "sales_org": "1000",
        "plant": "1000",
        "purch_no_c": "test",
        "purch_date": "",
        "pymt_meth": "H",
        "create_date": "20180503",
        "create_time": "080106",
        "eshop_id": "eshop_id_frotest",
        "dlv_block": "",
        "support_note": "",
        "client_note": "",
        "payId": "payIDGOGOGO",
        "conditions": [],
    }

    data = {"header": header}

    item = {
        "itm_number": "10",
        "hg_lv_item": "",
        "free_item ": "X",
        "material": "10000",
        "batch": "",
        "item_categ": "",
        "short_text": "Doprava",
        "long_text": "",
        "target_qty": 1,
        "target_qu": "LE",
        "dlv_group": "",
        "req_date_from": "20181003",
        "req_time_from": "235900",
        "req_date_to": "20181003",
        "req_time_to": "235900",
        "purch_no_c": "",
        "conditions": [
            {
                "cond_type": "PR01",
                "cond_value": "100",
                "currency": "CZK"
            }
        ]
    }
    today = datetime.now().date().strftime("%Y%m%d")
    item["req_date_from"] = today
    item["req_date_to"] = today

    data["items"] = [copy.deepcopy(item) for _ in range(len(materials) + 1)]

    for count, itm in enumerate(data["items"]):
        data["items"][count]["itm_number"] = str((count + 1) * 10)
        if count > 0:
            data["items"][count]["free_item "] = ""
            data["items"][count]["short_text"] = ""
            data["items"][count]["material"] = str(materials[count - 1][0])
            data["items"][count]["target_qty"] = materials[count - 1][1]
            data["items"][count]["target_qu"] = materials[count - 1][2]
        else:
            data["items"][count]["conditions"] = []

    partner = {
        "partn_numb": "1000001224",
        "partn_role": "AG",
        "name1": "Ondřeja",
        "name2": "Bílá",
        "city": "Praha",
        "street": "Kožená",
        "house_number": "11",
        "post_code1": "170 00",
        "country": "CZ",
        "tel_number": "774927254",
        "mob_number": "",
        "email": "petrkovar@gmail.com",
        "tax_no_1": "",
        "tax_no_2": "",
        "vat_reg_no": "",
        "language": "cs",
        "latitude": "55.29659",
        "longitude": "22.394016"
    }

    data["partners"] = [copy.deepcopy(partner) for _ in range(3)]

    data["partners"][1]["partn_numb"] = ""
    data["partners"][1]["partn_role"] = "WE"
    data["partners"][1]["transpzone"] = "TEST_2"

    data["partners"][2]["partn_numb"] = ""
    data["partners"][2]["partn_role"] = "RE"

    jsdata = json.dumps(data, ensure_ascii=False)

    # print(jsdata)

    with codecs.open('json.txt', 'w', encoding="UTF-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

    return jsdata


if __name__ == '__main__':
    materials = [(1000357, 5, "PC"), ]
    create_json_for_so(materials)
