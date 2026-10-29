# Tier comparison - Q3: Judgement

## Prompt
```
A colleague pastes a customer's full name, phone number and order history into a free personal chatbot account to 'save time'. List three risks and one safer alternative. Max 80 words.
```

## opus

*5.8s, cost $0.0622, tokens in/out 2/208, served by claude-haiku-5-5, claude-opus-5-5*

**Risks:**
1. **Privacy/legal breach:** Sharing personal data with an unapproved third party may violate GDPR/CCPA and company policy, and can bring fines and notification duties.
2. **Data retention/training:** Free consumer accounts may store prompts or use them for training, and you can't control deletion.
3. **Security exposure:** If the account is compromised or chats are shared, customer data could leak and be used for fraud or phishing.

**Safer alternative:** Use a company-approved enterprise AI tool with a data protection agreement, and anonymise the data (remove names and phone numbers) before pasting it.

## sonnet

*4.2s, cost $0.0311, tokens in/out 2/199, served by claude-haiku-5-5, claude-sonnet-5-5*

**Risks**
1. **Privacy/legal breach:** Sharing personal data (name, phone, orders) without consent or a lawful basis likely violates GDPR/data-protection rules.
2. **Data retention/training:** Free personal accounts may store the data or use it to train models, outside company control.
3. **No governance:** No audit trail, access controls, or deletion guarantees if it leaks.

**Safer alternative:** Use a company-approved, enterprise AI tool with a data-processing agreement, or anonymize/pseudonymize the data first (e.g., "Customer A", no phone number).

## haiku

*4.4s, cost $0.1252, tokens in/out 2/414, served by claude-haiku-5-5*

**Three risks:**
1. **Customer data exposure:** The free chatbot may store, log, or train on the data, and the company loses control of it.
2. **Compliance breach:** Sharing personal data this way can violate GDPR, CCPA, or company policy, and may trigger breach-reporting duties.
3. **No accountability:** Personal accounts have no access controls, audit trail, or deletion guarantee if the data leaks.

**Safer alternative:** Use a company-approved AI tool under a data processing agreement, or remove names, phone numbers, and order details and paste only the anonymized task.

## Your scoring (fill in)

| Tier | Correct? (0-3) | Followed length limit? | Would you trust it unchecked? |
|---|---|---|---|
| opus |  |  |  |
| sonnet |  |  |  |
| haiku |  |  |  |
