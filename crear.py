from fpdf import FPDF

pdf=FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font('Arial','B',14)
pdf.text(x=10,y=40, txt="Ciudad")
pdf.text(x=50,y=40, txt="Fecha")
pdf.text(x=80,y=40, txt="Temp_Máxima")
pdf.text(x=120,y=40, txt="Temp_Minima")
pdf.set_font('Arial','',10)
for i in range(45,200,5):
    pdf.text(x=10,y=i, txt="Hola jonathan")
pdf.output('Reporte_js.pdf')