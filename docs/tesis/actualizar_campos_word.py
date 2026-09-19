"""Abre el Word integrado con Microsoft Word, actualiza todos los campos (indice,
indice de tablas, indice de figuras, numeracion SEQ) y exporta el PDF final.

Requiere Word instalado. Uso (desde backend/, con el venv):
    python ../docs/tesis/actualizar_campos_word.py
"""
import sys
import time
from pathlib import Path

import win32com.client as win32

DOCS = Path(__file__).resolve().parents[1]
ENTRADA = DOCS / "Trabajo de Graduacion - integrado.docx"
DOCX_FINAL = DOCS / "Trabajo de Graduacion.docx"
PDF_FINAL = DOCS / "Trabajo de Graduacion.pdf"

WD_FORMAT_PDF = 17
WD_FORMAT_DOCX = 16


def _exigir_cerrado(ruta: Path):
    """Word no puede sobrescribir un archivo que otro programa tiene abierto."""
    try:
        with open(ruta, "r+b"):
            pass
    except FileNotFoundError:
        pass
    except PermissionError:
        sys.exit(f"Cierra '{ruta.name}' (está abierto en Word u otro programa) y vuelve a ejecutar.")


def main():
    if not ENTRADA.exists():
        sys.exit(f"No existe {ENTRADA}")
    # Bloqueo huérfano de una corrida interrumpida.
    try:
        ENTRADA.with_name("~$" + ENTRADA.name[2:]).unlink(missing_ok=True)
    except OSError:
        pass
    _exigir_cerrado(DOCX_FINAL)
    _exigir_cerrado(PDF_FINAL)
    app = win32.DispatchEx("Word.Application")
    app.Visible = False
    app.DisplayAlerts = 0
    doc = None
    try:
        doc = app.Documents.Open(str(ENTRADA), ReadOnly=False, AddToRecentFiles=False)
        doc.Fields.Update()
        for i in range(1, doc.TablesOfContents.Count + 1):
            doc.TablesOfContents(i).Update()
        for i in range(1, doc.TablesOfFigures.Count + 1):
            doc.TablesOfFigures(i).Update()
        doc.Repaginate()
        # Segunda pasada: los indices cambian la paginacion de todo lo que sigue.
        for i in range(1, doc.TablesOfContents.Count + 1):
            doc.TablesOfContents(i).UpdatePageNumbers()
        for i in range(1, doc.TablesOfFigures.Count + 1):
            doc.TablesOfFigures(i).UpdatePageNumbers()
        doc.Repaginate()
        paginas = doc.ComputeStatistics(2)  # wdStatisticPages
        doc.SaveAs2(str(DOCX_FINAL), FileFormat=WD_FORMAT_DOCX)
        doc.ExportAsFixedFormat(OutputFileName=str(PDF_FINAL), ExportFormat=WD_FORMAT_PDF,
                                OpenAfterExport=False, OptimizeFor=0, CreateBookmarks=1)
        doc.Close(SaveChanges=0)
        doc = None
        print(f"paginas: {paginas}")
        print(f"docx: {DOCX_FINAL}")
        print(f"pdf:  {PDF_FINAL}")
    finally:
        # Si algo falla a medias, el documento modificado no debe dejar a Word
        # esperando una confirmación ni bloqueando el archivo.
        if doc is not None:
            try:
                doc.Close(SaveChanges=0)
            except Exception:
                pass
        app.Quit(SaveChanges=0)
        time.sleep(1)
    # El intermedio sin campos actualizados ya no hace falta.
    ENTRADA.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
