# Homework comparison - Q1: Contract clause analysis (reasoning + arithmetic + careful reading)

## Fair-test rules
- New chat for each tool; identical pasted text; synthetic data only.
- Record the model name and plan each app shows.

## Prompt used
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

## Reference answer (check yours against this)
- Q1: 99.5 - 98.6 = 0.9 points -> 1 full 0.5-point step -> 5% of 12,400.00 = 620.00
- Q2: two months' fees = 24,800.00 (terminated within first 12 months)
- Q3: No - clause 11.4 requires prior written consent for processing outside the EEA

## Results

How this was run: the identical Q1 prompt, as a fresh conversation with no system prompt and no earlier messages.
**Claude** was run through the Anthropic API on the same models the Claude.ai app offers (Sonnet 5.5, the default, and
Opus 5.5); this is the API, not the app UI. **ChatGPT and Gemini were not run**: no access from this machine (no
browser session or API key for either).

| Question | ChatGPT | Claude.ai (Sonnet 5.5 via API) | Claude.ai (Opus 5.5 via API) | Gemini |
|---|---|---|---|---|
| Model / plan shown in the app | not run | claude-sonnet-5-5 (API, organisation key) | claude-opus-5-5 (API, organisation key) | not run |
| Credit amount correct (620.00)? | – | Yes, with working, 20% cap checked | Yes, with working, cap shown (2,480.00) | – |
| Termination charge correct (24,800)? | – | Yes | Yes | – |
| Quoted clause 11.4 for the data question? | – | Yes, verbatim | Yes, verbatim | – |
| Stayed under 150 words? | – | Yes, 142 (close to the limit) | Yes, 126 | – |
| Time to answer (seconds, roughly) | – | 3.7 | 5.4 | – |
| Did it add anything NOT in the clauses? | – | Two cautious caveats, both labelled as such: whether notice-period fees are payable on top of the charge, and that 11.4 covers personal data only. No invented facts | Same notice-period caveat; noted no currency is stated. No invented facts | – |

Raw answers: `outputs/day2_runs/partB_claude_api_Q1.json`.

## Privacy settings check (do this once per tool)

Locations below are from each vendor's help pages (checked 29 Oct 2026). **Confirm each one in your own account** and
tick the last column.

| Tool | Where the setting is | Default on personal accounts | Business / enterprise | Seen in my account? |
|---|---|---|---|---|
| ChatGPT | Profile → Settings → Data controls → **Improve the model for everyone** (mobile: sidebar → profile → Data controls). Temporary chats are never used for training | **On** for Free, Plus and Pro | Business / Enterprise / Edu / API: not used for training by default | ☐ |
| Claude.ai | Settings → Privacy → Privacy settings → **Help improve Claude**. Incognito chats are never used for training | **On** unless switched off at sign-up or in the Sept-2025 terms pop-up; retention 5 years if on, 30 days if off | Claude for Work / Team / Enterprise / API: consumer training terms do not apply | ☐ |
| Gemini | gemini.google.com → Settings & help → **Activity** → *Keep Activity* (Gemini Apps Activity). Temporary chats are not used to improve Google AI | **On** for users 18+; a subset of chats is read by human reviewers and kept up to 3 years; chats are kept 72 h even when off | Qualifying Google Workspace editions: enterprise terms; work accounts without one are treated like consumer accounts | ☐ |

- Account type for this homework: **personal / free on all three** (assumed; change it if yours differ). That means
  public or synthetic text only. Never customer, employee or bank data, whatever the toggle says.

## Reflection

Both Claude models answered all three parts correctly, showed the step logic, and quoted clause 11.4 word for word, so
on this prompt I would accept either as a first draft. I would still check the credit calculation first, because the
"full steps only" rule is where the CLI run's Haiku answer went wrong. What the extra sentences added is useful: both
models flagged what the clauses do *not* say, instead of filling the gap. A fair comparison with ChatGPT and Gemini
still needs those apps run under the same rules.
