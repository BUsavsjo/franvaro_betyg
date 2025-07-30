import os
import xlrd
import xlwt


def busavsjo_samla_franvarorapporter():
    """
    Slår ihop alla .xls-filer i data/import data franvaro till en fil (data/franvaro.xls),
    behåller bara rubriken från första filen och hoppar över de fyra första raderna i resten.
    """
    rotmapp = os.path.dirname(os.path.dirname(__file__))
    indata_mapp = os.path.join(rotmapp, "data", "import data franvaro")
    output_fil = os.path.join(rotmapp, "data", "franvaro.xls")

    wb_out = xlwt.Workbook()
    ws_out = wb_out.add_sheet("Data")

    rad_index = 0
    antal_filer = 0

    for filnamn in sorted(os.listdir(indata_mapp)):
        if filnamn.endswith(".xls") and filnamn != "franvaro.xls":
            filvag = os.path.join(indata_mapp, filnamn)
            try:
                wb_in = xlrd.open_workbook(filvag)
                sheet = wb_in.sheet_by_index(0)

                start_row = 0 if antal_filer == 0 else 4  # behåll rubrik bara från första filen

                # Infoga filnamn som kommentarrad (om inte första filen)
                if antal_filer > 0:
                    ws_out.write(rad_index, 0, f"Från fil: {filnamn}")
                    rad_index += 1

                for row_idx in range(start_row, sheet.nrows):
                    for col_idx, cell in enumerate(sheet.row_values(row_idx)):
                        ws_out.write(rad_index, col_idx, str(cell))
                    rad_index += 1

                antal_filer += 1

            except Exception as e:
                print(f"⚠️ Kunde inte läsa {filnamn}: {e}")

    wb_out.save(output_fil)
    print(f"✔️ Skapade '{output_fil}' med {antal_filer} rapporter")


if __name__ == "__main__":
    busavsjo_samla_franvarorapporter()
