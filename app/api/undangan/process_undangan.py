from app.models.undangan import Undangan
from app.dependencies.get_db_session import get_db_session
import sqlalchemy as sa
from fastapi import HTTPException, Response, Depends
from pydantic import BaseModel
a = """Assalamu'alaikum Wr. Wb.
Kepada Yth. 
Bapak/Ibu/Saudara/i
NAMA

Dengan memohon Rahmat dan Ridho Allah SWT, perkenankan kami mengundang Bapak/Ibu/Saudara untuk menghadiri acara pernikahan kami :

RAIHAN GHAZALI AMAJIDA, S.T.
Putra dari Bapak Eka Gunadi, S.E. & Ibu Weningtyas Trishandayani, S.E.

dengan 

ERVIRADISTYA SUMINARING TYAS, S.Tr.Par.
Putri dari Bapak Drs. Ery Juliarto & Ibu Irlina Pujiastuti

Berikut link undangan sebagai info lengkap dari acara kami :
https://ini-webku.com/raihan-ervira/?to=NAMA

Merupakan suatu kehormatan bagi kami apabila Bapak/Ibu/ Saudara/i berkenan hadir untuk memberikan doa restu kepada kami.

Undangan ini bersifat resmi. Mohon maaf karena ketidakmampuan jarak dan waktu undangan ini kami sampaikan melalui pesan ini.

Kehadiran serta doa dan restu Anda semua merupakan kado terindah bagi kami. Tiada yang dapat kami ungkapkan selain rasa terimakasih dari hati yang paling tulus.

Wassalamu’alaikum Wr.Wb.

Salam,
EKA GUNADI dan KELUARGA"""


def generate_kata(nama: str):
    nama_link = ""
    pecah_bama = nama.split(' ')
    ind = 0
    for na in pecah_bama:
        spasi = '%20'
        ind += 1
        if ind == len(pecah_bama):
            spasi = ""

        nama_link += na + spasi

    link = f"https://ini-webku.com/raihan-ervira/?to=Bapak/Ibu/%20{nama_link}"
    return f"""Assalamu’alaikum Wr. Wb.
Kepada Yth. 
Bapak/Ibu/Saudara/i
{nama}

Dengan memohon Rahmat dan Ridho Allah SWT, perkenankan kami mengundang Bapak/Ibu/Saudara untuk menghadiri acara pernikahan kami :

RAIHAN GHAZALI AMAJIDA, S.T.
Putra dari Bapak Eka Gunadi, S.E. & Ibu Weningtyas Trishandayani, S.E.

dengan 

ERVIRADISTYA SUMINARING TYAS, S.Tr.Par.
Putri dari Bapak Drs. Ery Juliarto & Ibu Irlina Pujiastuti

Berikut link undangan sebagai info lengkap dari acara kami :
https://ini-webku.com/raihan-ervira/?to=Bapak/Ibu/%20{nama_link}

Merupakan suatu kehormatan bagi kami apabila Bapak/Ibu/ Saudara/i berkenan hadir untuk memberikan doa restu kepada kami.

Undangan ini bersifat resmi. Mohon maaf karena ketidakmampuan jarak dan waktu undangan ini kami sampaikan melalui pesan ini.

Kehadiran serta doa dan restu Anda semua merupakan kado terindah bagi kami. Tiada yang dapat kami ungkapkan selain rasa terimakasih dari hati yang paling tulus.

Wassalamu’alaikum Wr.Wb.

Salam,
EKA GUNADI dan KELUARGA"""


async def progres_undangan(session=Depends(get_db_session)):

    b = """-"""

    response = session.execute(sa.select(Undangan.nama, Undangan.id)).all()

    for data_kontak in response:

        b = generate_kata(data_kontak.nama)

        values_to_update = {'kata': b}
        result = session.execute(
            sa.update(Undangan).values(
                **values_to_update).where(Undangan.id == data_kontak.id)
        )

        if result.rowcount == 0:
            raise HTTPException(400, detail='Dokumen not found')

    session.commit()
    return Response(status_code=204)
