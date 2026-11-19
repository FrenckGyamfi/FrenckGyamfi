"""Builds brand-kit/DataiTECH-invoice-template.xlsx (A4, auto-calculating VAT)."""
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.worksheet.page import PageMargins

GOLD, INK, GREY, LINE = 'B8893A', '23262B', '6B6B66', 'D9D6CC'
wb = Workbook(); ws = wb.active; ws.title = 'Invoice'
ws.sheet_view.showGridLines = False
for col, w in {'A': 2, 'B': 44, 'C': 9, 'D': 9, 'E': 14, 'F': 16}.items(): ws.column_dimensions[col].width = w

def f(size=10, bold=False, color=INK, italic=False): return Font(name='Calibri', size=size, bold=bold, color=color, italic=italic)
def put(ref, val, font=None, align=None, fmt=None):
    c = ws[ref]; c.value = val
    if font: c.font = font
    if align: c.alignment = align
    if fmt: c.number_format = fmt
    return c
R = Alignment(horizontal='right', vertical='center'); L = Alignment(horizontal='left', vertical='center', wrap_text=True)
thin = Side(style='thin', color=LINE); gold = Side(style='medium', color=GOLD)
PH = f(10, color=GOLD, italic=True)  # placeholder style: replace these

logo = XLImage('images/logo.png'); logo.width, logo.height = 210, 50
ws.add_image(logo, 'B2')
ws.row_dimensions[2].height = 22; ws.row_dimensions[3].height = 22
put('F2', 'INVOICE', f(22, True, GOLD), R)
put('F3', 'Factuur', f(10, color=GREY), R)

# sender
put('B6', 'DataiTECH', f(11, True))
put('B7', 'Data Informatics and Technologies', f(10, color=GREY))
put('B8', '[Street and number]', PH)
put('B9', '[Postcode] Zoetermeer, The Netherlands', PH)
put('B10', 'enquiries@dataitechbv.com', f(10))
put('B11', 'www.dataitechbv.com', f(10))

# invoice details
details = [('Invoice number', 'DT-2026-0001', None), ('Invoice date', '=TODAY()', 'DD-MM-YYYY'), ('Due date (30 days)', '=F7+30', 'DD-MM-YYYY'),
           ('Your reference / PO', '[PO number]', None), ('Service period', '[e.g. November 2026]', None)]
for i, (lab, val, fmt) in enumerate(details):
    r = 6 + i
    put(f'D{r}', lab, f(9, color=GREY), Alignment(horizontal='left', vertical='center'))
    ws.merge_cells(f'D{r}:E{r}')
    put(f'F{r}', val, PH if str(val).startswith('[') else f(10, True), R, fmt)
put('F6', 'DT-2026-0001', f(10, True), R)

# client
put('B13', 'BILL TO', f(9, True, GOLD))
for i, t in enumerate(['[Client organisation]', '[Attn.: name / department]', '[Street and number]', '[Postcode, City]', '[Client VAT number, if applicable]']):
    put(f'B{14 + i}', t, PH if i else f(11, True, GOLD, True))

# line items
hr = 20
for col, t in zip('BCDEF', ['Description', 'Qty', 'Unit', 'Rate (EUR)', 'Amount (EUR)']):
    c = put(f'{col}{hr}', t, f(9, True), R if col in 'CEF' else Alignment(horizontal='left', vertical='center', indent=1 if col == 'D' else 0))
    c.fill = PatternFill('solid', fgColor='F4EBD8'); c.border = Border(bottom=gold)
ws.row_dimensions[hr].height = 20
examples = [('[Description, e.g. Infrastructure assessment (fixed scope)]', 1, 'fixed'), ('[Description, e.g. Consultancy: storage design]', None, 'hours')]
for i in range(10):
    r = hr + 1 + i
    ws.row_dimensions[r].height = 18
    if i < len(examples):
        d, q, u = examples[i]
        put(f'B{r}', d, PH); put(f'C{r}', q, f(10), R); put(f'D{r}', u, f(10, color=GREY), Alignment(horizontal='left', indent=1))
    ws[f'B{r}'].alignment = L
    ws[f'C{r}'].number_format = '#,##0.##'; ws[f'C{r}'].alignment = R
    ws[f'E{r}'].number_format = '#,##0.00'; ws[f'E{r}'].alignment = R; ws[f'E{r}'].font = f(10)
    put(f'F{r}', f'=IF(OR(C{r}="",E{r}=""),"",ROUND(C{r}*E{r},2))', f(10), R, '#,##0.00')
    for col in 'BCDEF': ws[f'{col}{r}'].border = Border(bottom=thin)

last = hr + 10
t0 = last + 2
put(f'D{t0}', 'Subtotal', f(10, color=GREY)); put(f'F{t0}', f'=SUM(F{hr+1}:F{last})', f(10), R, '€ #,##0.00')
put(f'D{t0+1}', 'VAT rate', f(10, color=GREY)); put(f'E{t0+1}', 0.21, f(10), R, '0%')
put(f'D{t0+2}', 'VAT (BTW)', f(10, color=GREY)); put(f'F{t0+2}', f'=ROUND(F{t0}*E{t0+1},2)', f(10), R, '€ #,##0.00')
put(f'D{t0+3}', 'Total due', f(12, True)); put(f'F{t0+3}', f'=F{t0}+F{t0+2}', f(12, True, GOLD), R, '€ #,##0.00')
for col in 'DEF': ws[f'{col}{t0+3}'].border = Border(top=gold)
ws.row_dimensions[t0 + 3].height = 22

p0 = t0 + 6
put(f'B{p0}', 'PAYMENT', f(9, True, GOLD))
put(f'B{p0+1}', '="Please pay within 30 days, by "&TEXT(F8,"DD-MM-YYYY")&", quoting invoice number "&F6&"."', f(10))
put(f'B{p0+2}', 'IBAN  [NL00 BANK 0000 0000 00]   ·   BIC  [BANKNL2A]', PH)
put(f'B{p0+3}', 'Account name  DataiTECH', f(10))
put(f'B{p0+5}', 'For EU business clients outside the Netherlands: "VAT reverse-charged (BTW verlegd)", set the VAT rate to 0% and show the client VAT number. Delete this line otherwise.', f(8, color=GREY, italic=True))
ws[f'B{p0+5}'].alignment = L; ws.merge_cells(f'B{p0+5}:F{p0+5}'); ws.row_dimensions[p0 + 5].height = 26

fr = p0 + 8
put(f'B{fr}', 'DataiTECH · Zoetermeer, The Netherlands · KvK 62108158 · BTW NL854655475B02 · enquiries@dataitechbv.com', f(8, color=GREY))
ws.merge_cells(f'B{fr}:F{fr}'); ws[f'B{fr}'].alignment = Alignment(horizontal='center')
for col in 'BCDEF': ws[f'{col}{fr}'].border = Border(top=thin)

ws.print_area = f'A1:F{fr}'
ws.page_setup.paperSize = ws.PAPERSIZE_A4; ws.page_setup.orientation = 'portrait'
ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 1; ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_margins = PageMargins(left=0.5, right=0.5, top=0.6, bottom=0.6)
ws.print_options.horizontalCentered = True

wb.save('brand-kit/DataiTECH-invoice-template.xlsx'); print('saved')
