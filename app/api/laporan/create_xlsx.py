from pydantic import BaseModel
import xlsxwriter
from datetime import datetime

from pydantic import BaseModel
from fastapi import Depends
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from typing import List, Optional


from app.dependencies.get_db_session import get_db_session


class GenerateLaporan_posisisData(BaseModel):
    mulai: Optional[str]
    ahir: Optional[str]


class GenerateLaporan_posisisResponseModel(BaseModel):
    data: List[object]


datalist = []


async def generate_xslx(data: GenerateLaporan_posisisData, session=Depends(get_db_session)):
    data_range = jsonable_encoder(data)
    sql = "SELECT * FROM baarang "

    tanggal_tag = " per - sampai -"

    if "mulai" in data_range and data_range["mulai"]:
        tanggal_tag = f" PER {data.mulai} SAMPAI {data.ahir} "

    response = session.execute(sa.text(sql))
    datalist = []

    for Custome in response:
        data_one = {
            "kode_barang": Custome.kode_barang,
            "nama_barang": Custome.nama_barang,
            "satuan": Custome.satuan,
        }

        datetime_str = '2023-01-01'

        x = 0
        pemasukan = 0
        pengeluaran = 0
        opname = 0
        penyesuaian = 0
        saldo_ahir = 0
        keterangan = ""

        tanggal_ahir = datetime.strptime(datetime_str, '%Y-%m-%d')
        tanggal_ahir = tanggal_ahir.date()

        # sql with range

        sql2 = f"SELECT jumlah, saldo_jml,tanggal FROM transaksi_in  WHERE kode_barang = '{Custome.kode_barang}' AND tanggal BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tanggal "
        sql3 = f"SELECT jumlah, saldo_jml, tanggal  FROM transaksi_out  WHERE kode_barang = '{Custome.kode_barang}' AND tanggal BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tanggal"
        sql4 = f"SELECT * FROM rijek  WHERE kode_barang = '{Custome.kode_barang}' AND tgl_rijek BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tgl_rijek"
        sql5 = f"SELECT * FROM opname  WHERE kode_barang = '{Custome.kode_barang}' AND tgl_opname BETWEEN '{data_range['mulai']}' AND'{data_range['ahir']}' ORDER by tgl_opname"

        # count pemasukan
        response2 = session.execute(sa.text(sql2))
        for Data_in in response2:
            pemasukan += Data_in.jumlah
            saldo_ahir = Data_in.saldo_jml
            tanggal_ini = Data_in.tanggal
            print(tanggal_ini)
            tanggal_ahir = tanggal_ini
            print(tanggal_ahir)

        # count pengeluaran
        response3 = session.execute(sa.text(sql3))
        for Data_in in response3:
            pengeluaran += Data_in.jumlah
            tanggal_ini = Data_in.tanggal
            if tanggal_ini >= tanggal_ahir:
                saldo_ahir = Data_in.saldo_jml
                tanggal_ahir = tanggal_ini

        # count penyesuaian
        response4 = session.execute(sa.text(sql4))
        for Data_in in response4:
            penyesuaian += Data_in.jumlah_rijek
            tanggal_ini = Data_in.tgl_rijek
            if tanggal_ini >= tanggal_ahir:
                saldo_ahir = Data_in.saldo_jml

        # count opname
        response5 = session.execute(sa.text(sql5))
        for Data_in in response5:
            print("OPNAMEEE")
            opname = Data_in.jml_opname
            keterangan = Data_in.keterangan

        data_one.update({'saldo_awal': 0,
                         "pemasukan": pemasukan,
                         "saldo_ahir": saldo_ahir,
                         "pengeluaran": pengeluaran,
                         "penyesuaian": penyesuaian,
                         "stok_opname": opname,
                         "selisih": pemasukan - pengeluaran - opname,
                         "ket": keterangan
                         })

        # print("tes")
        datalist.append(data_one)

    # type: ignore # type: ignore
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('laporan/laporan.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': '$#,##0'})
    # Adjust the column width.

    # Write some data headers.

    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 50)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:H', 15)
    worksheet.set_column('I:I', 25)

    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
    })

    # Merge 3 cells.
    worksheet.merge_range(
        'K2:O2', f'LAPORAN MUTASI BARANG {tanggal_tag}', merge_format)

    worksheet.merge_range(
        'K3:O3', f'LESTARI BERKAH SAE', merge_format)

    worksheet.write('A5', 'No', bold)
    worksheet.write('B5', 'Kode Barang', bold)
    worksheet.write('C5', 'Nama Barang', bold)
    worksheet.write('D5', 'Saldo Awal', bold)
    worksheet.write('E5', 'Pemasukan', bold)
    worksheet.write('F5', 'Pengeluaran', bold)
    worksheet.write('G5', 'Penyesuaian', bold)
    worksheet.write('H5', 'Stok Opname', bold)
    worksheet.write('I5', 'Saldo Akhir', bold)
    worksheet.write('J5', 'Selisih', bold)
    worksheet.write('K5', 'Ket', bold)

    # Some data we want to write to the worksheet.
    expenses = (
        ['9876097 D', 1000],
        ['',   100],
    )

    # Start from the first cell below the headers.
    row = 6
    col = 0

    # Iterate over the data and write it out row by row.
    # print(datalist)
    for data_barang in datalist:
        print(data_barang)
        worksheet.write(row, col,     1)
        worksheet.write(row, col + 1,     data_barang["kode_barang"])
        worksheet.write(row, col + 2, data_barang["nama_barang"])
        worksheet.write(row, col + 3, data_barang["saldo_awal"])
        worksheet.write(row, col + 4, data_barang["pemasukan"])
        worksheet.write(row, col + 5, data_barang["pengeluaran"])
        worksheet.write(row, col + 6, data_barang["penyesuaian"])
        worksheet.write(row, col + 7, data_barang["stok_opname"])
        worksheet.write(row, col + 8, data_barang["saldo_ahir"])
        worksheet.write(row, col + 9, data_barang["selisih"])
        worksheet.write(row, col + 10, data_barang["ket"])
        row += 1

    # Write a total using a formula.
    # worksheet.write(row, 0, 'Total',       bold)
    # worksheet.write(row, 1, '=SUM(B2:B5)', money)

    workbook.close()
