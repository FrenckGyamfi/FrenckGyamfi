"""Content for the DataiTECH email signature and email templates (EN + NL)."""
LOGO_URL = 'https://dataitech.eu/images/logo.png'

def signature_html(logo_src=LOGO_URL):
    gold, ink, grey = '#B8893A', '#23262B', '#6B6B66'
    td = f'font-family:Arial,Helvetica,sans-serif;color:{ink};'
    return f'''<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse:collapse;{td}font-size:13px;line-height:1.45;">
  <tr>
    <td style="padding:0 0 10px 0;{td}">
      <div style="font-size:15px;font-weight:bold;color:{ink};">Frenck F.N Gyamfi</div>
      <div style="font-size:13px;color:{gold};">Data Informatics &amp; Technologies B.V.</div>
    </td>
  </tr>
  <tr>
    <td style="padding:0 0 10px 0;">
      <a href="https://dataitech.eu" style="text-decoration:none;"><img src="{logo_src}" width="168" height="40" alt="DataiTECH" style="display:block;border:0;width:168px;height:40px;"></a>
    </td>
  </tr>
  <tr>
    <td style="padding:8px 0 0 0;border-top:2px solid {gold};{td}font-size:12px;">
      <span style="color:{grey};">M</span>&nbsp;<a href="tel:+31614515145" style="color:{ink};text-decoration:none;">+31 6 1451 5145</a>&nbsp;·&nbsp;<a href="tel:+31620203034" style="color:{ink};text-decoration:none;">+31 6 2020 3034</a><br>
      <span style="color:{grey};">E</span>&nbsp;<a href="mailto:frenck@dataitech.eu" style="color:{ink};text-decoration:none;">frenck@dataitech.eu</a>
      &nbsp;&nbsp;<span style="color:{grey};">W</span>&nbsp;<a href="https://dataitech.eu" style="color:{ink};text-decoration:none;">dataitech.eu</a><br>
      <span style="color:{grey};">Zoetermeer, The Netherlands</span>
      &nbsp;·&nbsp;<a href="[https://www.linkedin.com/company/your-page]" style="color:{gold};text-decoration:none;">LinkedIn</a>
    </td>
  </tr>
  <tr>
    <td style="padding:8px 0 0 0;{td}font-size:12px;color:{gold};font-style:italic;">Data and AI. Now it makes sense.</td>
  </tr>
  <tr>
    <td style="padding:6px 0 0 0;font-family:Arial,Helvetica,sans-serif;font-size:10px;color:{grey};">Data Informatics &amp; Technologies B.V. · KvK 62198158 · BTW NL854655475B01</td>
  </tr>
</table>'''

SIGNATURE_TXT = '''Frenck F.N Gyamfi
Data Informatics & Technologies B.V. | DataiTECH

M +31 6 1451 5145 | +31 6 2020 3034
E frenck@dataitech.eu | W dataitech.eu
Zoetermeer, The Netherlands

Data and AI. Now it makes sense.
Data Informatics & Technologies B.V. · KvK 62198158 · BTW NL854655475B01'''

SIGNATURE_SHORT = '''Frenck F.N Gyamfi · DataiTECH
+31 6 1451 5145 · dataitech.eu'''

TEMPLATES = [
 ('enquiry', 'Reply to a new enquiry', 'Within one working day of a new enquiry.',
  ('Your enquiry about [topic]',
   '''Dear [Name],

Thank you for getting in touch about [topic]. Before we propose anything, we would like to understand why this matters to you now and what a good outcome looks like.

Could we schedule a 30-minute call? I am available on [day, time] or [day, time]. If neither suits you, just suggest a moment that does.

To make the call as useful as possible, it helps to know:
- your current environment (for example storage, backup and virtualisation platforms)
- the challenge or deadline you are facing
- who else should join

Kind regards,'''),
  ('Uw aanvraag over [onderwerp]',
   '''Beste [naam],

Dank voor uw bericht over [onderwerp]. Voordat we iets voorstellen, willen we graag begrijpen waarom dit nu speelt en wat voor u een goed resultaat is.

Kunnen we een kennismakingsgesprek van 30 minuten inplannen? Ik ben beschikbaar op [dag, tijd] of [dag, tijd]. Past dat niet, laat dan gerust weten wat wel uitkomt.

Om het gesprek zo nuttig mogelijk te maken, helpt het als we vooraf weten:
- uw huidige omgeving (bijvoorbeeld storage-, back-up- en virtualisatieplatforms)
- de uitdaging of deadline waar u voor staat
- wie er verder aansluit

Met vriendelijke groet,''')),
 ('proposal', 'Assessment proposal', 'After the intake call, with the proposal attached.',
  ('Proposal: [assessment] for [Client]',
   '''Dear [Name],

Thank you for the conversation on [date]. As agreed, here is our proposal for a fixed-scope assessment.

Why: [one sentence on the business goal]
What we review: [scope, e.g. storage, backup and recovery of production systems]
What you get: a written report with findings, risks and a prioritised plan, presented to your team
Timeline: [number] working days, starting [date]
Investment: EUR [amount] excl. VAT, fixed price

The full proposal is attached. Once you confirm, we will plan the kick-off. Let me know if anything needs adjusting.

Kind regards,'''),
  ('Voorstel: [assessment] voor [klant]',
   '''Beste [naam],

Dank voor het gesprek op [datum]. Zoals afgesproken ontvangt u hierbij ons voorstel voor een assessment met een vaste scope.

Waarom: [één zin over het doel]
Wat we onderzoeken: [scope, bijv. storage, back-up en herstel van productiesystemen]
Wat u krijgt: een rapport met bevindingen, risico's en een geprioriteerd plan, toegelicht aan uw team
Doorlooptijd: [aantal] werkdagen, start [datum]
Investering: EUR [bedrag] excl. btw, vaste prijs

Het volledige voorstel vindt u in de bijlage. Na uw akkoord plannen we de kick-off. Laat het gerust weten als er iets aangepast moet worden.

Met vriendelijke groet,''')),
 ('kickoff', 'Kick-off confirmation', 'Once the client has confirmed the work.',
  ('Kick-off confirmed: [project], [date]',
   '''Dear [Name],

Thank you for your confirmation. We are looking forward to getting started.

Kick-off: [date, time, location or Teams link]
Attendees: [names]

Agenda
1. Goals and the why behind them
2. Scope, planning and points of contact
3. Access, security requirements and documentation we need
4. Next steps

Before the kick-off, could you share [documents or access]?

Kind regards,'''),
  ('Kick-off bevestigd: [project], [datum]',
   '''Beste [naam],

Dank voor uw akkoord. We kijken ernaar uit om te beginnen.

Kick-off: [datum, tijd, locatie of Teams-link]
Deelnemers: [namen]

Agenda
1. Doelen en het waarom erachter
2. Scope, planning en aanspreekpunten
3. Toegang, beveiligingseisen en benodigde documentatie
4. Vervolgstappen

Kunt u voorafgaand aan de kick-off [documenten of toegang] met ons delen?

Met vriendelijke groet,''')),
 ('invoice', 'Sending an invoice', 'With the PDF invoice attached.',
  ('Invoice [DT-2026-0001] for [project or period]',
   '''Dear [Name],

Please find attached invoice [DT-2026-0001] for [description or period], for a total of EUR [amount] incl. VAT.

Payment is due on [due date], to IBAN NL34 ABNA 0136 6796 41 in the name of DataiTECH, quoting the invoice number. Your purchase order number [PO number] is stated on the invoice.

If anything needs to change for your accounts payable process, let me know and I will send a corrected version.

Kind regards,'''),
  ('Factuur [DT-2026-0001] voor [project of periode]',
   '''Beste [naam],

In de bijlage vindt u factuur [DT-2026-0001] voor [omschrijving of periode], voor een totaalbedrag van EUR [bedrag] incl. btw.

Wij verzoeken u het bedrag vóór [vervaldatum] over te maken naar IBAN NL34 ABNA 0136 6796 41 ten name van DataiTECH, onder vermelding van het factuurnummer. Uw inkoopordernummer [PO-nummer] staat op de factuur.

Moet er iets worden aangepast voor uw crediteurenadministratie? Laat het me weten, dan stuur ik een gecorrigeerde versie.

Met vriendelijke groet,''')),
 ('reminder', 'Friendly payment reminder', 'A few days after the due date.',
  ('Reminder: invoice [DT-2026-0001], due [due date]',
   '''Dear [Name],

According to our records, invoice [DT-2026-0001] of [invoice date] for EUR [amount] was due on [due date] and we have not yet received payment. If it has crossed with your payment, please disregard this message.

If not, could you arrange payment within 7 days to IBAN NL34 ABNA 0136 6796 41, quoting the invoice number? If there is a problem with the invoice, let me know so we can resolve it quickly. A copy of the invoice is attached.

Kind regards,'''),
  ('Herinnering: factuur [DT-2026-0001], vervallen op [vervaldatum]',
   '''Beste [naam],

Volgens onze administratie is factuur [DT-2026-0001] van [factuurdatum] voor EUR [bedrag] op [vervaldatum] vervallen en hebben wij de betaling nog niet ontvangen. Heeft uw betaling dit bericht gekruist, dan kunt u het als niet verzonden beschouwen.

Zo niet, wilt u het bedrag dan binnen 7 dagen overmaken naar IBAN NL34 ABNA 0136 6796 41, onder vermelding van het factuurnummer? Is er iets mis met de factuur, laat het me dan weten zodat we het snel oplossen. Een kopie van de factuur vindt u in de bijlage.

Met vriendelijke groet,''')),
 ('final', 'Final payment notice', 'If the reminder has not led to payment.',
  ('Final notice: invoice [DT-2026-0001]',
   '''Dear [Name],

Despite our reminder of [date], we have not yet received payment of invoice [DT-2026-0001] for EUR [amount], which was due on [due date].

We ask you to pay the outstanding amount within 14 days of this message, by [date], to IBAN NL34 ABNA 0136 6796 41, quoting the invoice number. If payment has not been received by then, we will charge the statutory commercial interest (wettelijke handelsrente) from the due date.

We would much rather avoid that. If there is an issue, please contact me today.

Kind regards,'''),
  ('Laatste herinnering: factuur [DT-2026-0001]',
   '''Beste [naam],

Ondanks onze herinnering van [datum] hebben wij de betaling van factuur [DT-2026-0001] voor EUR [bedrag], vervallen op [vervaldatum], nog niet ontvangen.

Wij verzoeken u het openstaande bedrag binnen 14 dagen na dagtekening van dit bericht, uiterlijk [datum], over te maken naar IBAN NL34 ABNA 0136 6796 41, onder vermelding van het factuurnummer. Is de betaling dan niet ontvangen, dan brengen wij vanaf de vervaldatum de wettelijke handelsrente in rekening.

Dat voorkomen we liever. Is er een probleem, neem dan vandaag nog contact met mij op.

Met vriendelijke groet,''')),
 ('handover', 'Project handover and feedback', 'At the end of a project. Also helps you collect testimonials for the website.',
  ('Handover of [project] and a short question',
   '''Dear [Name],

With [deliverable] delivered on [date], we have completed [project]. Thank you for the pleasant cooperation with your team.

Attached you will find the final documentation (HLD/LLD) and [test or recovery evidence]. As agreed, [support arrangement].

One short question: would you be willing to share two or three sentences about working with us? With your permission we would use them on our website, anonymised if you prefer. A reply to this email is enough.

Kind regards,'''),
  ('Oplevering van [project] en een korte vraag',
   '''Beste [naam],

Met de oplevering van [resultaat] op [datum] hebben we [project] afgerond. Dank voor de prettige samenwerking met uw team.

In de bijlage vindt u de definitieve documentatie (HLD/LLD) en [test- of herstelbewijs]. Zoals afgesproken [ondersteuningsafspraak].

Nog één korte vraag: wilt u in twee of drie zinnen delen hoe u de samenwerking heeft ervaren? Met uw toestemming plaatsen we die op onze website, desgewenst anoniem. Een reactie op deze e-mail is voldoende.

Met vriendelijke groet,''')),
]
