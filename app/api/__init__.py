from fastapi import APIRouter
from fastapi.responses import FileResponse


from app.api.auth.auth_login import LoginResponseModel, auth_login
from app.api.auth.auth_logout import auth_logout
from app.api.auth.auth_refresh_token import (RefreshTokenResponseMode,
                                             auth_refresh_token)
from app.api.auth.auth_register import auth_register
from app.api.auth.check_verivy import (CheckVerificationResponseModel,
                                       check_verifi)
from app.api.auth.edit_profile import edit_profile
from app.api.auth.get_poto_profile import get_foto_profile
from app.api.auth.get_profile import GetProfileResponseModel, get_profile
from app.api.auth.send_verify import SendVerifiResponseModel, sendWa
from app.api.auth.upload_pp import UploadPpResponseModel, upload_pp

from app.api.barang.add_barang import add_barang
from app.api.barang.update_barang import update_data_barang
from app.api.barang.get_barang import get_data_barang, GetBarangDataResponsemodel
from app.api.barang.get_barangs import get_data_barangs, GetBarangsDataResponsemodel

from app.api.suplier.add_suplier import add_suplier
from app.api.suplier.get_suplier import get_data_suplier, GetSuplierDataResponsemodel
from app.api.suplier.get_supliers import get_data_supliers, GetSupliersDataResponsemodel

from app.api.customer.add_customer import add_customer
from app.api.customer.get_customer import get_data_customer, GetCustomerDataResponsemodel
from app.api.customer.get_customers import get_data_customers, GetCustomersDataResponsemodel

from app.api.akun.add_akun import add_akun
from app.api.akun.get_akun import get_data_akun, GetAkunDataResponsemodel
from app.api.akun.get_akuns import get_data_akuns, GetAkunsDataResponsemodel

from app.api.purchase_order.add_po import add_purchase_order
from app.api.purchase_order.get_po import get_data_purchase_order, GetPurchaseOrderDataResponsemodel
from app.api.purchase_order.get_po_s import get_data_purchase_orders, GetPurchaseOrdersDataResponsemodel

from app.api.standar_doc.add_standar_doc import add_standar_doc
from app.api.standar_doc.get_standar_doc import get_data_standar_doc, GetStandarDocDataResponsemodel

api_router = APIRouter(prefix='/api')

# AUTHENTICATION

api_router.add_api_route('/api/v1/auth/register', auth_register,
                         methods=['POST'], tags=['Auth'], status_code=201)

api_router.add_api_route('/api/v1/auth/sendWa', sendWa,
                         methods=['POST'], tags=['Auth'], response_model=SendVerifiResponseModel)

api_router.add_api_route('/api/v1/auth/check_verifi', check_verifi,
                         methods=['POST'], tags=['Auth'], response_model=CheckVerificationResponseModel)

api_router.add_api_route('/api/v1/auth/login', auth_login,
                         methods=['POST'], tags=['Auth'], response_model=LoginResponseModel)

api_router.add_api_route('/api/v1/auth/logout', auth_logout,
                         methods=['POST'], tags=['Auth'], status_code=204)

api_router.add_api_route('/api/v1/auth/refresh_token', auth_refresh_token,
                         methods=['POST'], tags=['Auth'], response_model=RefreshTokenResponseMode)

api_router.add_api_route('/api/v1/auth/profile', get_profile,
                         methods=['GET'], tags=['Auth'], response_model=GetProfileResponseModel)

api_router.add_api_route('/api/v1/auth/profile', edit_profile,
                         methods=['PUT'], tags=['Auth'], status_code=204)

api_router.add_api_route('/api/v1/auth/upload_pp', upload_pp,
                         methods=['POST'], tags=['Auth'], response_model=UploadPpResponseModel)

api_router.add_api_route('/api/v1/auth/poto_profile', get_foto_profile,
                         methods=['GET'], tags=['Auth'])

# BARANG

api_router.add_api_route('/api/v1/barang/add_barang', add_barang,
                         methods=['POST'], tags=['barang'], status_code=204)

api_router.add_api_route('/api/v1/barang/update_barang', update_data_barang,
                         methods=['POST'], tags=['barang'], status_code=204)

api_router.add_api_route('/api/v1/barang/get_data_barang', get_data_barang,
                         methods=['POST'], tags=['barang'], response_model=GetBarangDataResponsemodel)

api_router.add_api_route('/api/v1/barang/get_data_barangs', get_data_barangs,
                         methods=['GET'], tags=['barang'], response_model=GetBarangsDataResponsemodel)

# SUPLIER

api_router.add_api_route('/api/v1/suplier/add_suplier', add_suplier,
                         methods=['POST'], tags=['suplier'], status_code=204)

api_router.add_api_route('/api/v1/suplier/get_suplier', get_data_suplier,
                         methods=['POST'], tags=['suplier'], response_model=GetSuplierDataResponsemodel)

api_router.add_api_route('/api/v1/suplier/get_supliers', get_data_supliers,
                         methods=['GET'], tags=['suplier'], response_model=GetSupliersDataResponsemodel)

#  CUSTOMER

api_router.add_api_route('/api/v1/customer/add_customer', add_customer,
                         methods=['POST'], tags=['customer'], status_code=204)

api_router.add_api_route('/api/v1/customer/get_customer', get_data_customer,
                         methods=['POST'], tags=['customer'], response_model=GetCustomerDataResponsemodel)

api_router.add_api_route('/api/v1/customer/get_customers', get_data_customers,
                         methods=['GET'], tags=['customer'], response_model=GetCustomersDataResponsemodel)

# AKUN

api_router.add_api_route('/api/v1/akun/add_akun', add_akun,
                         methods=["POST"], tags=['akun'], status_code=204)

api_router.add_api_route('/api/v1/akun/get_data_akun', get_data_akun,
                         methods=["POST"], tags=['akun'], response_model=GetAkunDataResponsemodel)

api_router.add_api_route('/api/v1/akun/get_data_akuns', get_data_akuns,
                         methods=["GET"], tags=['akun'], response_model=GetAkunsDataResponsemodel)

# PURCHASE ORDER

api_router.add_api_route('/api/v1/purchase_order/add_po', add_purchase_order,
                         methods=["POST"], tags=['purchase_order'], status_code=204)

api_router.add_api_route('/api/v1/purchase_order/get_po', get_data_purchase_order,
                         methods=["POST"], tags=['purchase_order'], response_model=GetPurchaseOrderDataResponsemodel)

api_router.add_api_route('/api/v1/purchase_order/get_po_s', get_data_purchase_orders,
                         methods=["GET"], tags=['purchase_order'], response_model=GetPurchaseOrdersDataResponsemodel)

# STANDAR DOC

api_router.add_api_route('/api/v1/standar_doc/add_po', add_standar_doc,
                         methods=["POST"], tags=['standar_doc'], status_code=204)

api_router.add_api_route('/api/v1/standar_doc/get_po', get_data_standar_doc,
                         methods=["POST"], tags=['standar_doc'], response_model=GetStandarDocDataResponsemodel)
