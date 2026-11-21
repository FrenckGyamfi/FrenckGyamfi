# DataiTECH brand kit

| File | What it is |
| --- | --- |
| `email-signature.html` | HTML email signature for Outlook, Gmail and Apple Mail |
| `email-signature.txt` | Plain-text signature, plus a short version for replies |
| `email-templates.md` | Seven client email templates, in English and Dutch |
| `DataiTECH-invoice-template.xlsx` | Invoice template (A4) that calculates amounts, VAT and total |
| `DataiTECH-invoice-example.pdf` | What the blank invoice looks like as a PDF |
| `logo.png` | Logo used in the signature |

## Before first use

Replace the remaining `[placeholders]`: street address, postcode and LinkedIn page.

The signature loads the logo from `https://dataitech.eu/images/logo.png`, so it shows once the website is live.
Until then, upload `logo.png` somewhere public (or insert it as an image in your mail program) and use that address.

## Email signature

1. Open `email-signature.html` in a browser and replace the placeholders (or ask for a version with your details filled in).
2. Select everything on the page (Ctrl/Cmd + A) and copy.
3. Paste it into the signature settings:
   - **Outlook:** Settings > Mail > Compose and reply > Email signature
   - **Gmail:** Settings > See all settings > General > Signature
   - **Apple Mail:** Settings > Signatures (untick "Always match my default message font")

## Invoice

1. Make a copy for each invoice, named after the invoice number (e.g. `DT-2026-0001.xlsx`).
2. Replace everything in gold italic `[brackets]`: your street address, client details, PO number and service period.
3. Fill in description, quantity, unit and rate per line. Amounts, subtotal, VAT (21%) and total calculate automatically.
4. The invoice date defaults to today (`=TODAY()`). Type the actual date before sending, so it doesn't change when reopened.
5. Save as PDF and send it with the "Sending an invoice" email template.
6. Number invoices in an unbroken sequence (DT-2026-0001, DT-2026-0002, ...), as the Dutch tax authority requires.

The invoice includes what a Dutch VAT invoice must show: sequential number, date, your name, address, KvK and VAT number,
the client's name and address, a description and period of the service, amounts excluding VAT, the VAT rate and amount, and the total.
For EU business clients outside the Netherlands, use reverse charge ("BTW verlegd"): VAT rate 0% and the client's VAT number.

**Dutch central government** (ministries and most agencies) only accepts e-invoices (UBL via Peppol or Digipoort), not PDF.
Most accounting packages, such as Exact, Moneybird or e-Boekhouden, can send these.
