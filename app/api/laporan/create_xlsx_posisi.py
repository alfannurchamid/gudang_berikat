from pydantic import BaseModel
import xlsxwriter
from datetime import datetime
import json
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from typing import List, Optional


import xlsxwriter


class GenerateXlsx_posisisData(BaseModel):
    data: str
    mulai: Optional[str]
    ahir: Optional[str]


async def generate_xslx_posisi(data: GenerateXlsx_posisisData):

    data_in = jsonable_encoder(data)
    tanggal_tag = " per - sampai -"

    if "mulai" in data_in and data_in["mulai"]:
        tanggal_tag = f" PER {data.mulai} SAMPAI {data.ahir} "
    data_o = json.loads(data.data)
    data_p = data_o

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('laporan/laporan_posisi.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True, 'border': 2, 'align': 'center',
                                'valign': 'vcenter'})

    warp = workbook.add_format({'border': 1,
                                'align': 'center',
                                'valign': 'vcenter'})
    warp.set_text_wrap()

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': 'Rp #,##0', 'border': 1,
                                 'align': 'center',
                                 'valign': 'vcenter'})
    money_usd = workbook.add_format({'num_format': '$#,##0'})
    # Adjust the column width.

    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
    })

    cel_f = workbook.add_format({

        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })

    # Merge 3 cells.
    worksheet.merge_range(
        'K2:O2', f'LAPORAN POSISI BARANG {tanggal_tag}', merge_format)

    worksheet.merge_range(
        'K3:O3', f'LESTARI BERKAH SAE', merge_format)

    # type: ignore# type: ignore
    # Write some data headers.

    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:E', 10)
    worksheet.set_column('F:S', 15)

    worksheet.set_column('H:H', 20)
    worksheet.set_column('I:I', 5)
    worksheet.set_column('Q:Q', 20)

    worksheet.set_column('K:K', 20)
    worksheet.set_column('T:T', 20)
    worksheet.set_column('W:W', 20)

    worksheet.write('A5', 'No', bold)
    worksheet.write('B5', 'JENIS', bold)
    worksheet.write('C5', 'NO', bold)
    worksheet.write('D5', 'Tgl', bold)
    worksheet.write('E5', 'TGL_MASUK', bold)
    worksheet.write('F5', 'KODE BARANG', bold)
    worksheet.write('G5', 'SERI BARANG', bold)
    worksheet.write('H5', 'NAMA BARANG', bold)
    worksheet.write('I5', 'SAT', bold)
    worksheet.write('J5', 'JMLH', bold)
    worksheet.write('K5', 'NILAI PABEAN', bold)

    worksheet.write('L5', 'NO', bold)
    worksheet.write('M5', 'Tgl', bold)
    worksheet.write('N5', 'TGL_MASUK', bold)
    worksheet.write('O5', 'KODE BARANG', bold)
    worksheet.write('P5', 'SERI BARANG', bold)
    worksheet.write('Q5', 'NAMA BARANG', bold)
    worksheet.write('R5', 'SAT', bold)
    worksheet.write('S5', 'JMLH', bold)
    worksheet.write('T5', 'NILAI PABEAN', bold)

    worksheet.write('U5', 'JMLH', bold)
    worksheet.write('V5', 'SAT', bold)
    worksheet.write('W5', 'NILAI PABEAN', bold)

    # Start from the first cell below the headers.
    row = 5

    col = 0

    # Iterate over the data and write it out row by row.
    # print(datalist)
    for data_dok in data_p:
        print(data_dok["jenis_in"])
        worksheet.write(row, col,     row, cel_f)
        worksheet.write(row, col + 1,     data_dok["jenis_in"], cel_f)
        worksheet.write(row, col + 2, data_dok["no_daftar_in"], cel_f)
        worksheet.write(row, col + 3, data_dok["tanggal_daftar_in"], cel_f)
        worksheet.write(row, col + 4, data_dok["tanggal_in"], cel_f)
        worksheet.write(row, col + 5, data_dok["kode_barang_in"], cel_f)
        worksheet.write(row, col + 6, "-", cel_f)
        worksheet.write(row, col + 7, data_dok["nama_barang_in"], warp)
        worksheet.write(row, col + 8, data_dok["satuan"], cel_f)
        worksheet.write(row, col + 9, data_dok["jumlah_in"], cel_f)
        worksheet.write(
            row, col + 10, data_dok["nilai_pabean_in"], money)

        worksheet.write(row, col + 11, "", cel_f)
        worksheet.write(row, col + 12, "", cel_f)
        worksheet.write(row, col + 13, "", cel_f)
        worksheet.write(row, col + 14, "", cel_f)
        worksheet.write(row, col + 15, "", cel_f)
        worksheet.write(row, col + 16, "", cel_f)
        worksheet.write(row, col + 17, "", cel_f)
        worksheet.write(row, col + 18, "", cel_f)
        worksheet.write(row, col + 19, "", cel_f)

        worksheet.write(row, col + 20, data_dok["saldo_jml_in"], cel_f)
        worksheet.write(row, col + 21, data_dok["satuan"], cel_f)
        worksheet.write(
            row, col + 22,  data_dok["nilai_pabean_in"], money)

        # SISI KANAN---------------------
        row += 1
        if "no_daftar_out" in data_dok and data_dok["no_daftar_out"]:
            worksheet.write(row, col,     row, cel_f)
            worksheet.write(row, col + 1,   "", cel_f)
            worksheet.write(row, col + 2, "", cel_f)
            worksheet.write(row, col + 3, "", cel_f)
            worksheet.write(row, col + 4, "", cel_f)
            worksheet.write(row, col + 5, "", cel_f)
            worksheet.write(row, col + 6, "", cel_f)
            worksheet.write(row, col + 7, "", cel_f)
            worksheet.write(row, col + 8, "", cel_f)
            worksheet.write(row, col + 9, "", cel_f)
            worksheet.write(row, col + 10, "", cel_f)

            worksheet.write(row, col + 11, data_dok["no_daftar_out"], cel_f)
            worksheet.write(
                row, col + 12, data_dok["tanggal_daftar_out"], cel_f)
            worksheet.write(row, col + 13, data_dok["tanggal_out"], cel_f)
            worksheet.write(row, col + 14, data_dok["kode_barang_in"], cel_f)
            worksheet.write(row, col + 15, "-", cel_f)
            worksheet.write(
                row, col + 16, data_dok["nama_barang_in"], warp)
            worksheet.write(row, col + 17, data_dok["satuan"], cel_f)
            worksheet.write(row, col + 18, data_dok["jumlah_out"], cel_f)
            worksheet.write(
                row, col + 19, data_dok["nilai_pabean_out"], money)

            worksheet.write(row, col + 20, data_dok["saldo_jml_out"], cel_f)
            worksheet.write(row, col + 21, data_dok["satuan"], cel_f)
            worksheet.write(
                row, col + 22,  data_dok["nilai_pabean_out"], money)

            row += 1

    # Write a total using a formula.
    # worksheet.write(row, 0, 'Total',       bold)
    # worksheet.write(row, 1, '=SUM(B2:B5)', money)

    workbook.close()
