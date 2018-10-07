from login import login, password

system = "k4t"
# k4q nebo k4d
user = login
password = password
headless_mode = False
url_trx = {"k4d": "kod.mgit.cz:8021/s2ap/trx?terminal_id=XHV&sap-language=CS",
           "k4q": "kod.mgit.cz:8011/s2ap/trx?terminal_id=XHV&sap-language=CS",
           "k4t": "kod.mgit.cz:8041/s2ap/trx?terminal_id=XHV&sap-language=CS",
           }

port_s = {"k4d": 32015,
          "k4q": 31015,
          "k4t": 34015,
          }

cart_id = "MT001"
cons_type = "02"
