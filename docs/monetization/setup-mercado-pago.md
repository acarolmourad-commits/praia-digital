# Mercado Pago Setup — Praia Digital

**Gateway:** Mercado Pago Brazil  
**Products:** Checkout Pro, Subscriptions, Webhooks  
**Status:** READY FOR ACCOUNT CREATION

---

## Why Mercado Pago for Praia Digital

Praia Digital services with clear monetization potential:
- Consultations: R$197–R$497
- Course enrollment: R$497
- Subscription plans: R$97–R$297/mo
- Paid audits: R$150–R$350
- Photography packages: price TBD

Mercado Pago is the dominant Brazilian payment gateway with:
- Credit/debit card support
- PIX instant payment
- Installment options (1-12x)
- Subscriptions/recurring billing
- High trust among Brazilian buyers

---

## Account Creation

1. **Create account:** https://www.mercadopago.com.br
2. **Account type:** Business/Professional
3. **Required documents:**
   - CPF or CNPJ
   - Proof of address
   - Bank account details
4. **Verification:** Usually 1-2 business days
5. **Fee schedule:** ~3.99% + R$0.49 per transaction; varies by volume

---

## Integration Steps

### 1. Create Application
1. Go to https://www.mercadopago.com.br/developers
2. Sign in with business account
3. Create Application → Name: "Praia Digital"
4. Products to enable:
   - Checkout Pro
   - Subscriptions (if needed)
   - QR Code / Point (in-person)
5. Copy credentials:
   - `access_token` (keep secret)
   - `public_key`
   - `webhook_secret`

### 2. Configure Environment
Store credentials securely, NOT in repo:
```env
MP_ACCESS_TOKEN=APP_USR-...
MP_PUBLIC_KEY=APP_USR-...
MP_WEBHOOK_SECRET=...
APP_URL=https://praia.digital
```

### 3. Implement Checkout
**Option A: Redirect Checkout (simplest)**
- Generate preference via API
- Redirect buyer to Mercado Pago checkout
- Return to success/cancel URLs

**Option B: Checkout Pro on-page**
- Embed iframe or brick on service pages
- Buyer pays without leaving site
- More professional, slightly more complex

### 4. Webhook Receiver
Set up endpoint to receive payment notifications:
```
POST https://praia.digital/webhook/mercadopago
```
Events to handle:
- `payment.approved`
- `payment.rejected`
- `payment.cancelled`

### 5. Test in Sandbox
- Mercado Pago provides test credentials
- Test cards:
  - Approved: `4012 0000 0000 0000`
  - Rejected: `4012 0000 0000 0002`
  - Expired: `4012 0000 0000 0003`

### 6. Production Checklist
- [ ] Switch to production credentials
- [ ] Test with small real transaction
- [ ] Configure PIX if desired
- [ ] Set up email receipts
- [ ] Verify webhook signature validation

---

## Pages to Integrate

| Page | Product | Price |
|------|---------|-------|
| `planos-assinatura.html` | Monthly subscription | R$97–R$297/mo |
| `proposta-piloto-consultoria-*.html` | Consultation | R$197–R$497 |
| `curso-gratis-captar-leads-litoral-7-dias.html` | Course upgrade | R$497 |
| `checkout/` | Dedicated checkout | Create if needed |

---

## Security Notes

- Never expose `access_token` to browser
- Always validate webhook signatures
- Use HTTPS on all payment endpoints
- Store credentials in `.env` + `.gitignore`

---

*Guide generated: 2026-09-05*
