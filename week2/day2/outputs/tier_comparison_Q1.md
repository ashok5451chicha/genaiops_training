# Tier comparison - Q1: Contract clause analysis (reasoning + arithmetic + careful reading)

## Prompt
```
You are helping a procurement analyst. Using ONLY the clauses below, answer:
1. In one month availability was 98.6%. What service credit is owed in money? Show the calculation.
2. The Customer terminates after 8 months. What is the early-termination charge in money?
3. Can the Supplier process customer data in India without asking? Quote the clause.
Keep the answer under 150 words.

<clauses>
SERVICES AGREEMENT - EXTRACT (fictional, for training use)

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

</clauses>
```

## Reference answer (for the human judge)
- Q1: 99.5 - 98.6 = 0.9 points -> 1 full 0.5-point step -> 5% of 12,400.00 = 620.00
- Q2: two months' fees = 24,800.00 (terminated within first 12 months)
- Q3: No - clause 11.4 requires prior written consent for processing outside the EEA

## opus

*18.9s, cost $1.3117, tokens in/out 2/426, served by claude-haiku-5-5, claude-opus-5-5*

**1. Service credit:** **620.00**
- Shortfall: 99.5% âˆ’ 98.6% = 0.9 percentage points
- Full 0.5-point steps: 1 (the remaining 0.4 is not a full step and earns nothing)
- Credit: 1 Ã— 5% = 5% Ã— 12,400.00 = **620.00** (below the 20% cap of 2,480.00)

**2. Early-termination charge:** **24,800.00**
- 8 months falls within the first 12 months, so the charge applies.
- 2 Ã— 12,400.00 = **24,800.00**. The 90 days' written notice in clause 9.2 is also still required.

**3. Processing in India:** **No.** India is outside the EEA, so the Supplier needs the Customer's prior written consent first. Clause 11.4: *"Customer personal data shall be processed only within the European Economic Area unless the Customer gives prior written consent."*

## sonnet

*5.9s, cost $0.6626, tokens in/out 2/292, served by claude-haiku-5-5, claude-sonnet-5-5*

**1. Service credit (cl. 7.1):** Shortfall = 99.5 âˆ’ 98.6 = 0.9 points â†’ 1 full 0.5-point band (0.9 < 1.0) â†’ 5% credit. 5% Ã— 12,400.00 = **620.00**.

**2. Early-termination charge (cl. 9.2):** Termination in month 8 falls within the first 12 months, so the charge is two months' fees: 2 Ã— 12,400.00 = **24,800.00**. (Clause 9.2 also requires 90 days' written notice; the charge applies regardless of that notice period.)

**3. Data in India (cl. 11.4):** No, not without asking. The clause states: *"Customer personal data shall be processed only within the European Economic Area unless the Customer gives prior written consent."* India is outside the EEA, so the Supplier needs the Customer's prior written consent.

## haiku

*4.3s, cost $0.1668, tokens in/out 2/369, served by claude-haiku-5-5*

**1. Service credit for 98.6% availability: â‚¬0 is not the answer; the credit is 15% of the monthly fee, which is 1,860.00.**

Clause 7.1 applies when availability falls below 99.5%. The shortfall is 99.5 âˆ’ 98.6 = 0.9 points. That is one full 0.5-point step plus a partial step, so only one full step counts: 1 Ã— 5% = 5% of 12,400.00 = **620.00**.

(Check: 0.9 Ã· 0.5 = 1.8, and only full steps count, so 1 step.)

**2. Early-termination charge after 8 months: 24,800.00.**

Clause 9.2 applies because termination falls in the first 12 months. The charge is two months' fees: 2 Ã— 12,400.00 = **24,800.00**.

**3. No. The Supplier cannot process customer data in India without asking.**

Clause 11.4: "Customer personal data shall be processed only within the European Economic Area unless the Customer gives prior written consent."

India is outside the EEA, so the Supplier needs the Customer's prior written consent first.

## Your scoring (fill in)

| Tier | Correct? (0-3) | Followed length limit? | Would you trust it unchecked? |
|---|---|---|---|
| opus |  |  |  |
| sonnet |  |  |  |
| haiku |  |  |  |
