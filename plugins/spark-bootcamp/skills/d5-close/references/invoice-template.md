# Invoice template

A first invoice needs eight things and nothing more. Fill every {{placeholder}}. If you are not
yet registered for tax, say so plainly and charge no tax; do not invent a number.

---

# INVOICE

**From:** {{business_name}}, {{business_address}}
**Invoice number:** {{invoice_number}}
**Date issued:** {{date}}
**Payment due:** {{due_date}} ({{payment_terms}})

**Bill to:** {{client_company}}, {{client_address}}

| Description | Amount |
| --- | --- |
| {{line_item_description}} | £{{net_amount}} |
| {{tax_label}} | £{{tax_amount}} |
| **Total due** | **£{{total_amount}}** |

**Pay by bank transfer:**
Account name: {{account_name}}
Sort code / IBAN: {{sort_code_or_iban}}
Account number / BIC: {{account_or_bic}}
Reference: {{invoice_number}}

{{stripe_or_card_link_line}}

Thank you. Please use the invoice number as your payment reference.

---

## Notes on getting this right

- **Numbering.** Start at a sensible number, not 1. INV-1001 looks like you have done this before.
- **Tax.** Charge tax only if you are registered to. If you are not, delete the tax row and add one
  line: "Not registered for {{tax_name}}; no tax charged." Never guess a tax number.
- **Terms.** For a first customer, 7 days is fine and gets you paid faster than 30. State it.
- **Deposit invoices.** If the tier is a deposit, the line item reads "Deposit (X percent of
  £{{full_price}})" and you note the balance and when it falls due.
