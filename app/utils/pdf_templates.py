import os
from reportlab.lib.pagesizes import A4


def dibujar_encabezado(pdf, titulo=""):
    width, height = A4

    logo_path = os.path.join("app", "static", "img", "logo.png")

    if os.path.exists(logo_path):
        pdf.drawImage(
            logo_path,
            40,
            height - 90,
            width=70,
            height=55,
            preserveAspectRatio=True,
            mask="auto"
        )

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(
        width / 2,
        height - 45,
        "VIGILANCIA Y SEGURIDAD PRIVADA PACIFIC SECURITY FORCE CÍA. LTDA."
    )

    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(
        width / 2,
        height - 60,
        "Servicio de Guardianía en Condominios, Residenciales, Centros Comerciales,"
    )
    pdf.drawCentredString(
        width / 2,
        height - 72,
        "Instituciones Públicas y Privadas, etc. No. Registro S.C. 0481"
    )
    pdf.drawCentredString(width / 2, height - 84, "Quito - Ecuador")

    pdf.line(40, height - 100, width - 40, height - 100)

    if titulo:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(width / 2, height - 125, titulo)


def dibujar_pie(pdf):
    width, height = A4

    pdf.line(40, 65, width - 40, 65)

    pdf.setFont("Helvetica", 8)
    pdf.drawCentredString(
        width / 2,
        50,
        "Camilo Gallegos E14-16 y Av. Eloy Alfaro PB"
    )
    pdf.drawCentredString(
        width / 2,
        38,
        "Teléfonos: 022441237 / 0998583471"
    )
    pdf.drawCentredString(
        width / 2,
        26,
        "pacificsecurityforce@hotmail.com"
    )