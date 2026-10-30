# Tier comparison - Q2: Short summarisation

## Prompt
```
Summarise in two sentences for an executive: SERVICES AGREEMENT - EXTRACT (fictional, for training use)

4.1 Fees. The Customer shall pay the Supplier a fixed monthly fee of 12,400.00 for the
Managed Support Service, invoiced on the first business day of each month.

4.2 Late payment. Invoices unpaid after 30 days incur interest at 1.5% per month on the
overdue amount.

7.1 Service credits. If monthly availability falls below 99.5%, the Supplier shall credit
5% of that month's fee for each full 0.5 percentage points below 99.5%, up to a maximum
credit of 20% of the monthly fee.

9.2 Termination for convenience. Either party may terminate on 90 days' written notice.
If the Customer terminates in the first 12 months, an early-termination charge equal to
two months' fees applies.

11.4 Data location. Customer personal data shall be processed only within the European
Economic Area unless the Customer gives prior written consent.

```

## opus

*19.8s, cost $1.3222, tokens in/out 2/179, served by claude-haiku-5-5, claude-opus-5-5*

This fictional managed support agreement sets a fixed monthly fee of 12,400.00 (no currency is stated), with 1.5% monthly interest on invoices more than 30 days overdue, and service credits of up to 20% of the monthly fee if availability falls below 99.5%. Either party can exit on 90 days' notice, but the Customer pays two months' fees if it terminates in the first 12 months, and personal data must stay in the EEA unless the Customer gives written consent.

## sonnet

*2.8s, cost $0.0319, tokens in/out 2/153, served by claude-haiku-5-5, claude-sonnet-5-5*

The Customer pays a fixed 12,400 monthly fee for Managed Support, with 1.5% monthly interest on invoices unpaid after 30 days. The Supplier owes service credits of up to 20% of the monthly fee if availability drops below 99.5%. Either party may exit on 90 days' notice, though early termination by the Customer in the first year costs two months' fees, and personal data must stay within the European Economic Area unless the Customer consents otherwise.

## haiku

*4.1s, cost $0.2057, tokens in/out 2/165, served by claude-haiku-5-5*

**Summary:** The Customer pays a fixed fee of 12,400.00 per month for Managed Support, with overdue invoices accruing 1.5% monthly interest after 30 days. Service credits of 5% per 0.5-point availability shortfall (capped at 20%) apply below 99.5% uptime, either party may terminate on 90 days' notice (with a two-month early-termination charge if the Customer leaves in year one), and personal data stays in the EEA unless the Customer consents in writing.

## Your scoring (fill in)

| Tier | Correct? (0-3) | Followed length limit? | Would you trust it unchecked? |
|---|---|---|---|
| opus |  |  |  |
| sonnet |  |  |  |
| haiku |  |  |  |
