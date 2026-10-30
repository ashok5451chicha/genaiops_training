# Tier comparison - custom: Custom prompt

## Prompt
```
You are helping a card-servicing analyst. Using ONLY the terms below, answer:
1. A Platinum cardholder spent 8,400.00 on the card this year. Is the annual fee charged, and how much is it?
2. The cardholder withdraws 60.00 in cash. What cash-advance fee is charged? Show the calculation.
3. The cardholder makes a purchase of 400.00 in euros. What non-sterling fee applies?
Keep the answer under 120 words.

<terms>
CARD TERMS - EXTRACT (fictional, for training use)

3.1 Annual fee. The Platinum card has an annual fee of 180.00. The fee is waived for any card year in which
the cardholder spends at least 9,000.00 on purchases.

3.2 Non-sterling transactions. Purchases made in a currency other than GBP incur a non-sterling transaction
fee of 2.75% of the transaction value.

3.3 Late payment. If the minimum payment is not received by the due date, a late fee of 12.00 is charged.
No more than one late fee is charged per statement.

3.4 Cash advances. Cash withdrawals incur a fee of 3% of the amount withdrawn, subject to a minimum fee of
3.00. Interest is charged from the date of the withdrawal.

5.2 Disputes. A disputed transaction must be reported within 120 days of the transaction date.
</terms>
```

## opus

*4.8s, cost $0.0678, tokens in/out 2/320, served by claude-haiku-5-5, claude-opus-5-5*

1. **Annual fee:** Yes, the fee is charged: **180.00**. Under 3.1, it is only waived if purchases reach at least 9,000.00 in the card year, and 8,400.00 is 600.00 short.

2. **Cash-advance fee:** **3.00**. Under 3.4:
   - 3% Ã— 60.00 = 1.80
   - The minimum fee is 3.00, and 1.80 is below it, so 3.00 is charged.
   - Interest also runs from the date of the withdrawal.

3. **Non-sterling fee:** **11.00**. Under 3.2, a purchase in euros counts as non-GBP, so the fee is 2.75% Ã— 400.00 = 11.00.

## sonnet

*3.0s, cost $0.0331, tokens in/out 2/234, served by claude-haiku-5-5, claude-sonnet-5-5*

1. **Annual fee:** Yes, it is charged. Spend of 8,400.00 is below the 9,000.00 waiver threshold (3.1), so the fee is **180.00**.

2. **Cash advance fee:** 3% Ã— 60.00 = 1.80, which is below the 3.00 minimum (3.4), so the fee is **3.00**. Interest also accrues from the withdrawal date.

3. **Non-sterling fee:** 2.75% Ã— 400.00 = **11.00**, in the currency of the amount stated. The terms don't say whether the 400.00 is in euros or its GBP equivalent, so this assumes the fee is applied to the 400.00 figure as given (3.2).

## haiku

*3.6s, cost $0.0153, tokens in/out 2/520, served by claude-haiku-5-5*

**1. Annual fee:** Yes, charged at **180.00**. The waiver requires at least 9,000.00 in purchases, and the cardholder spent only 8,400.00.

**2. Cash-advance fee:** **3.00**. The fee is 3% of 60.00, which is 1.80, but the minimum fee is 3.00, so the minimum applies.

**3. Non-sterling fee:** **2.75%** of the transaction value. 2.75% Ã— 400.00 = **11.00**. The terms don't say how the fee is converted to sterling, so the 11.00 is in the transaction's currency.

## Your scoring (fill in)

| Tier | Correct? (0-3) | Followed length limit? | Would you trust it unchecked? |
|---|---|---|---|
| opus |  |  |  |
| sonnet |  |  |  |
| haiku |  |  |  |
