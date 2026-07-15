---
name: Domain And Email
description: Registers a real domain (about GBP 10) and business email, so regulated buyers will enquire. Day 3, before the landing site goes live.
when_to_use: Day 3 product build, after d2-brand-foundations, before d3-landing-site. When still on a free subdomain and a gmail.
argument-hint: [domain]
---

# Domain And Email

**What this does.** Gets you a domain you own (harbourtrust.je), a business email on it (seb@harbourtrust.je), and points the domain at your host.
**Why it matters.** A trust officer or law-firm partner will not enquire through `something.vercel.app` from `harbourtrust123@gmail.com`, and GBP 10 a year is the cheapest credibility you will buy.
**You are ready for this when.** `02-market/brand/brand-foundations.md` exists (that is where your name was decided).

## Before you start
Read `02-market/brand/brand-foundations.md` (the name) and `.spark/state.json` (`founder`, `business_type`: the host depends on the path). You need a card; registering spends about GBP 10.

Guardrail (hard): do not buy until the founder says "yes" to the exact domain and exact price read back to them. Money does not move without sign-off.

## Steps
1. **Choose the domain** from the business name. Prefer `.je` for Jersey firms, `.com` second; avoid `.io`, `.co` and novelty endings. Keep it short and typo-proof; if taken, add the sector not a number (`harbourtrustco.je`, never `harbour99.je`).
2. **Pick a registrar, keep DNS in one place.** Recommend Cloudflare Registrar (at-cost, free fast DNS); a `.com` is about GBP 9/yr. A `.je` needs a Jersey-accredited registrar, then move DNS to Cloudflare if you want. Click-by-click: `${CLAUDE_SKILL_DIR}/references/domain-and-email-walkthrough.md`.
3. **Check it is free** before reaching for the card:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/check-domain-email.py --domain <yourdomain>
   ```
   "Does not resolve" means likely available. The registrar's search is the authority.
4. **Get sign-off, then register.** Read back the exact domain and annual price, wait for "yes", register. Keep free privacy; skip "SEO pack" and "email pro" upsells.
5. **Point the domain at your host** by adding the DNS records (values per path in the walkthrough). Propagation takes minutes to a couple of hours; that is normal.
6. **Set up the business email.** Launch today on free forwarding plus Gmail "send as" (receives and sends, GBP 0, fifteen minutes). Move to Google Workspace Business Starter (about GBP 5/user/month) once the first customer is in sight; that monthly spend needs its own sign-off. Note the choice in `DECISIONS.md`.
7. **Test end to end.** Send from the new address to another inbox and reply back; both must arrive. Then confirm records:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/check-domain-email.py --domain <yourdomain> --email you@<yourdomain>
   ```
8. **Wire the landing site to use it** so `d3-landing-site` publishes to the domain and Day 4 outreach sends from the business address. Write both into the artefact.

## The artefact
Writes `03-product/domain-email.md` in Markdown: the registered domain, registrar and annual cost; the DNS records added (type, name, value); the email route and address; a "verified" line with the date the send-and-receive test passed. Good: a stranger can rebuild the whole setup from it.

## Done when
Checker prints PASS on 1 and 2:
1. The domain resolves (reaches your host, not a parking page).
2. The domain has valid mail records (MX or forwarding).
3. A test email from `you@yourdomain` arrives elsewhere and a reply arrives back (confirmed by eye).

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d3-domain-email \
  --artefact 03-product/domain-email.md \
  --result "domain live at <yourdomain>, business email verified, GBP <N>/yr"
```
Record the money decision in DECISIONS.md:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Registered <yourdomain> and chose <email route>" \
  --rationale "Regulated buyers will not enquire via free subdomain; domain is GBP <N>/yr, email route fits current budget"
```
Set Day 3 progress:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"current_day":3,"days":{"3":{"outcome":"domain live and business email verified"}}}'
```

## If it goes wrong
- **DNS not live after two hours.** Edit DNS at whichever company answers for the domain; `--verbose` on the checker shows where it points.
- **The `.je` is taken or slow.** Register the matching `.com` today so nothing blocks, chase the `.je` in parallel, point both at one host later. Note in `DECISIONS.md`.
- **Gmail rejects "send as".** Use the SMTP relay or app password in the walkthrough; if it still fights, launch forwarding-only (you can receive) and fix sending before Day 4.
- **No card or spend not approved.** Do not register. Reserve the name in `DECISIONS.md`, stay on the free subdomain, return once sign-off lands.
