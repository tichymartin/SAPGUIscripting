from sap_create_po import main_po
from trx_inbound import inbound
from trx_confirm_to_inbound import main_confirm_to

bp = "5000000044"
materials = ["1000412", ]

indls = main_po(bp, materials)
# indls = "180000188"
pallets = inbound(indls)
# pallets = ["4961796259", "6595671840"]
main_confirm_to(pallets)
