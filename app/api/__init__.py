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

from app.api.purchase_order.add_po import add_purchase_order, AddPurchaseOrdersDataResponsemodel
from app.api.purchase_order.get_po import get_data_purchase_order, GetPurchaseOrderDataResponsemodel
from app.api.purchase_order.get_po_s import get_data_purchase_orders, GetPurchaseOrdersDataResponsemodel
from app.api.purchase_order.get_po_s_id import get_data_purchase_orders_id, GetPurchaseOrdersIdDataResponsemodel
from app.api.purchase_order.delete_po import delete_po

from app.api.standar_doc.add_standar_doc import add_standar_doc
from app.api.standar_doc.get_standar_doc import get_data_standar_doc, GetStandarDocDataResponsemodel
from app.api.standar_doc.get_standar_docs import get_data_standar_docs, GetStandarDocsDataResponsemodel
from app.api.standar_doc.get_standar_docs_id import get_data_standar_docs_id, GetStandarDocIdsDataResponsemodel


from app.api.transaksi_in.create_transaksi_in import create_transaksi_in
from app.api.transaksi_in.get_transaksi_in import get_data_transaksi_in, GetTransaksiInDataResponsemodel
from app.api.transaksi_in.get_transaksi_is_s import get_data_transaksi_ins, GetTransaksiinsDataResponsemodel
from app.api.transaksi_in.get_transaksi_ins_id import get_data_transaksi_in_id, GetTransaksi_in_IdDataResponsemodel
from app.api.transaksi_in.edit_transaksi_in import edit_transaksi_in
from app.api.transaksi_in.delete_transaksi_in import delete_T_in

from app.api.transaksi_out.create_transaksi_out import create_transaksi_out
from app.api.transaksi_out.get_transaksi_out_s import get_data_transaksi_outs, GetTransaksiOutsDataResponsemodel
from app.api.transaksi_out.get_transaksi_out import get_data_transaksi_out, GetTransaksiOutDataResponsemodel
from app.api.transaksi_out.edit_pengajuan import edit_Transaksi_out
from app.api.transaksi_out.edit_transaksi_out_acc import edit_Transaksi_out_acc
from app.api.transaksi_out.delete_transaksi_out import delete_T_out


from app.api.laporan.get_lap_posisi import get_data_lap_posisi, GetLaporan_posisisDataResponsemodel
from app.api.laporan.get_laporan_lpj_mutasi import get_data_lap_mutasi, GetLaporan_mutasiDataResponsemodel
from app.api.laporan.create_xlsx import generate_xslx
from app.api.laporan.create_xlsx_posisi import generate_xslx_posisi
from app.api.laporan.get_laoran import get_laporan
from app.api.laporan.get_laoran_posisi import get_laporan_posisi_xl

from app.api.opname.create_opname import create_opname

from app.api.rijek.create_rijek import create_rijek

from app.api.pengajuan_penyesuaian.add_pengajuan import add_penyesuaian
from app.api.pengajuan_penyesuaian.edit_penyesuaian import edit_penyesuaian

from app.api.pemberitahuan.pemberitahuan import get_pemberitahuans,  GetPemberitahuansDataResponsemodel

from app.api.user_log.create_user_log import create_user_log
from app.api.user_log.get_user_logs import get_user_logs, GetUserLogDataResponsemodel

# from app.api.undangan.process_undangan import progres_undangan

from app.api.akuntan.get_neraca import get_neraca, GetNeracaDataResponsemodel
from app.api.akuntan.get_laba_rugi import get_laba_rugi, GetLabaRugiDataResponsemodel
from app.api.akuntan.get_buku_besar import get_buku_besar, GetBukuBesarDataResponsemodel
from app.api.akuntan.create_jurnal import add_jurnal_umum
from app.api.akuntan.get_laba_berjalan import get_laba_berjalan, GetLabaBerjalanDataResponsemodel
from app.api.akuntan.get_laba_trans_ini import get_laba_trans_ini, GetLabaIniResponseModel
from app.api.akuntan.rebalancer import rebalancer


api_router = APIRouter(prefix='/api')

# AUTHENTICATION


# api_router.add_api_route('/api/v1/auth/progres_undangan', progres_undangan,
#                          methods=['POST'], tags=['Auth'], status_code=201)

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

#  USER LOG

api_router.add_api_route('/api/v1/user_log/create_user_log', create_user_log,
                         methods=['POST'], tags=['user_log'], status_code=204)

api_router.add_api_route('/api/v1/user_log/get_user_log', get_user_logs,
                         methods=['POST'], tags=['user_log'], response_model=GetUserLogDataResponsemodel)

# BARANG

api_router.add_api_route('/api/v1/barang/add_barang', add_barang,
                         methods=['POST'], tags=['barang'], status_code=204)

api_router.add_api_route('/api/v1/barang/update_barang', update_data_barang,
                         methods=['POST'], tags=['barang'], status_code=204)

api_router.add_api_route('/api/v1/barang/get_data_barang', get_data_barang,
                         methods=['GET'], tags=['barang'], response_model=GetBarangDataResponsemodel)

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
                         methods=["POST"], tags=['purchase_order'], response_model=AddPurchaseOrdersDataResponsemodel)

api_router.add_api_route('/api/v1/purchase_order/get_po', get_data_purchase_order,
                         methods=["POST"], tags=['purchase_order'], response_model=GetPurchaseOrderDataResponsemodel)

api_router.add_api_route('/api/v1/purchase_order/get_po_s', get_data_purchase_orders,
                         methods=["GET"], tags=['purchase_order'], response_model=GetPurchaseOrdersDataResponsemodel)

api_router.add_api_route('/api/v1/purchase_order/get_po_s_id', get_data_purchase_orders_id,
                         methods=["GET"], tags=['purchase_order'], response_model=GetPurchaseOrdersIdDataResponsemodel)

api_router.add_api_route('/api/v1/purchase_order/delete_po', delete_po,
                         methods=["POST"], tags=['purchase_order'], status_code=203)

# STANDAR DOC

api_router.add_api_route('/api/v1/standar_doc/add_doc', add_standar_doc,
                         methods=["POST"], tags=['standar_doc'], status_code=204)

api_router.add_api_route('/api/v1/standar_doc/get_doc', get_data_standar_doc,
                         methods=["POST"], tags=['standar_doc'], response_model=GetStandarDocDataResponsemodel)

api_router.add_api_route('/api/v1/standar_doc/get_docs', get_data_standar_docs,
                         methods=["GET"], tags=['standar_doc'], response_model=GetStandarDocsDataResponsemodel)

api_router.add_api_route('/api/v1/standar_doc/get_docs_id', get_data_standar_docs_id,
                         methods=["POST"], tags=['standar_doc'], response_model=GetStandarDocIdsDataResponsemodel)

# TRANSAKSI_IN

api_router.add_api_route('/api/v1/transaksi_in/create_transaksi_in',
                         create_transaksi_in, methods=['POST'], tags=['transaksi_in'], status_code=204)

api_router.add_api_route('/api/v1/transaksi_in/get_transaksi_in',
                         get_data_transaksi_in, methods=['POST'], tags=['transaksi_in'], response_model=GetTransaksiInDataResponsemodel)

api_router.add_api_route('/api/v1/transaksi_in/get_transaksi_in_s',
                         get_data_transaksi_ins, methods=['GET'], tags=['transaksi_in'], response_model=GetTransaksiinsDataResponsemodel)

api_router.add_api_route('/api/v1/transaksi_in/get_transaksi_ins_id',
                         get_data_transaksi_in_id, methods=['GET'], tags=['transaksi_in'], response_model=GetTransaksi_in_IdDataResponsemodel)

api_router.add_api_route('/api/v1/transaksi_in/edit_transaksi_in',
                         edit_transaksi_in, methods=["PUT"], tags=['transaksi_in'], status_code=204)

api_router.add_api_route('/api/v1/transaksi_in/delete_transaksi_in',
                         delete_T_in, methods=["PUT"], tags=['transaksi_in'], status_code=204)

# TRANSAKSI_out

api_router.add_api_route('/api/v1/transaksi_out/create_transaksi_out',
                         create_transaksi_out, methods=['POST'], tags=['transaksi_out'], status_code=204)

api_router.add_api_route('/api/v1/transaksi_out/get_transaksi_out_s',
                         get_data_transaksi_outs, methods=['GET'], tags=['transaksi_out'], response_model=GetTransaksiOutsDataResponsemodel)

api_router.add_api_route('/api/v1/transaksi_out/get_transaksi_out',
                         get_data_transaksi_out, methods=['POST'], tags=['transaksi_out'], response_model=GetTransaksiOutDataResponsemodel)

api_router.add_api_route('/api/v1/transaksi_out/edit_transaksi_out',
                         edit_Transaksi_out, methods=['POST'], tags=['transaksi_out'], status_code=204)

api_router.add_api_route('/api/v1/transaksi_out/edit_transaksi_out_acc',
                         edit_Transaksi_out_acc, methods=['PUT'], tags=['transaksi_out'], status_code=204)

api_router.add_api_route('/api/v1/transaksi_out/delete_transaksi_out',
                         delete_T_out, methods=["PUT"], tags=['transaksi_out'], status_code=204)


# LAPORAN
api_router.add_api_route('/api/v1/laporan/create_laporan_posisi', get_data_lap_posisi,
                         methods=["POST"],  tags=['laporan'], response_model=GetLaporan_posisisDataResponsemodel)

api_router.add_api_route('/api/v1/laporan/create_laporan_mutasi', get_data_lap_mutasi,
                         methods=["POST"],  tags=['laporan'], response_model=GetLaporan_mutasiDataResponsemodel)

api_router.add_api_route('/api/v1/laporan/generate_xlsx', generate_xslx,
                         methods=["POST"],  tags=['laporan'], status_code=204)

api_router.add_api_route('/api/v1/laporan/generate_xlsx_posisi', generate_xslx_posisi,
                         methods=["POST"],  tags=['laporan'], status_code=204)

api_router.add_api_route('/api/v1/laporan/get_laporan', get_laporan,
                         methods=["GET"],  tags=['laporan'], status_code=204)


api_router.add_api_route('/api/v1/laporan/get_laporan_posisi', get_laporan_posisi_xl,
                         methods=["GET"],  tags=['laporan'], status_code=204)

# OPNAME
api_router.add_api_route('/api/v1/opname/create_opname', create_opname,
                         methods=['POST'], tags=['opname'], status_code=204)

# RIJEK
api_router.add_api_route('/api/v1/rijek/create_rijek', create_rijek,
                         methods=['POST'], tags=['rijek'], status_code=204)

# PENYESUAIAN
api_router.add_api_route('/api/v1/penyesuaian/add_pengajuan', add_penyesuaian,
                         methods=['POST'], tags=['pengajuan'], status_code=204)

api_router.add_api_route('/api/v1/penyesuaian/edit_penyesuaian', edit_penyesuaian,
                         methods=['PUT'], tags=['Pemberitahuan'], status_code=204)

# PEMBERITAHUAN
api_router.add_api_route('/api/v1/auth/pemberitahuan', get_pemberitahuans,
                         methods=['GET'], tags=['Pemberitahuan'], response_model=GetPemberitahuansDataResponsemodel)

# AKUNTANSI
api_router.add_api_route('/api/v1/akuntansi/get_neraca', get_neraca,
                         methods=['POST'], tags=['akuntan'], response_model=GetNeracaDataResponsemodel)

api_router.add_api_route('/api/v1/akuntansi/get_laba_rugi', get_laba_rugi,
                         methods=['POST'], tags=['akuntan'], response_model=GetLabaRugiDataResponsemodel)


api_router.add_api_route('/api/v1/akuntansi/get_buku_besar', get_buku_besar,
                         methods=['POST'], tags=['akuntan'], response_model=GetBukuBesarDataResponsemodel)

api_router.add_api_route('/api/v1/akuntansi/add_jurnal_umum', add_jurnal_umum,
                         methods=['POST'], tags=['akuntan'], status_code=203)


api_router.add_api_route('/api/v1/akuntansi/get_laba_berjalan', get_laba_berjalan,
                         methods=['GET'], tags=['akuntan'], response_model=GetLabaBerjalanDataResponsemodel)


api_router.add_api_route('/api/v1/akuntansi/get_laba_trans_ini', get_laba_trans_ini,
                         methods=['GET'], tags=['akuntan'], response_model=GetLabaIniResponseModel)


api_router.add_api_route('/api/v1/akuntansi/rebalancer', rebalancer,
                         methods=['POST'], tags=['akuntan'], status_code=203)
