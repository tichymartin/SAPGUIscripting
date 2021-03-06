import json
import codecs
import copy
from datetime import datetime, timedelta


def create_json_for_so(materials, customer=None):

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
        "distr_chan": "10",
        "ship_cond": "10",
        "conditions": [
            {
                "cond_type": "YDO1",
                "cond_value": "100",
                "currency": "CZK"
            }
        ],
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
        "req_time_from": "202200",
        "req_date_to": "20181003",
        "req_time_to": "212200",
        "purch_no_c": "",
        "conditions": [
            {
                "cond_type": "PR01",
                "cond_value": "10000",
                "currency": "CZK"
            }
        ]
    }
    today = datetime.now().date().strftime("%Y%m%d")
    # today = datetime.now().date()
    # tomorrow = today + timedelta(days=1)
    # tomorrow = tomorrow.strftime("%Y%m%d")

    item["req_date_from"] = today
    item["req_date_to"] = today

    data["items"] = [copy.deepcopy(item) for _ in range(len(materials))]

    for count, itm in enumerate(data["items"]):
        data["items"][count]["itm_number"] = str((count + 1) * 10)
        data["items"][count]["free_item "] = ""
        data["items"][count]["short_text"] = ""
        data["items"][count]["material"] = str(materials[count][0])
        data["items"][count]["target_qty"] = materials[count][1]
        data["items"][count]["target_qu"] = materials[count][2]

    if not customer:
        customer = "1000001400"
    partner = {

        "partn_numb": customer,
        "partn_role": "AG",
        "name1": "Karel",
        "name2": "Černý",
        "city": "Praha",
        "street": "Písková",
        "house_number": "12",
        "post_code1": "170 00",
        "country": "CZ",
        "tel_number": "774927254",
        "mob_number": "",
        "email": "karelcerny@gmail.com",
        "tax_no_1": "",
        "tax_no_2": "",
        "vat_reg_no": "",
        "language": "cs",
        "longitude": "14.4105535315",
        "latitude": "50.0012306417",
        "transpzone": "TEST_2"

    }


    data["partners"] = [copy.deepcopy(partner) for _ in range(1)]

    jsdata = json.dumps(data, ensure_ascii=False)

    # print(jsdata)

    with codecs.open('json.txt', 'w', encoding="UTF-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

    return jsdata


if __name__ == '__main__':
    materials = [
                (1000441, 10, "PC"),
                (1000441, 100, "KG"),
                (1000441, 100, "KG"),
                (1000441, 100, "KG"),
                (1000441, 100, "KG"),
                (1000441, 100, "KG"),
                ]
    create_json_for_so(materials)
