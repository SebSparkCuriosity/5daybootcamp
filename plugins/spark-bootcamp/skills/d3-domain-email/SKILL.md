---
name: Domain And Email
description: Registers a real domain (about GBP 10) and stands up a working business email, so a trust or law firm will actually enquire. Use on Day 3, before the landing site goes live.
when_to_use: Day 3 product build, after d2-brand-foundations set the name and before d3-landing-site publishes the page. Whenever the founder is still on a free subdomain and a gmail.
argument-hint: [domain]
---

# Domain And Email

**What this does.** Gets you a real web address you own (like harbourtrust.je) and a real business email on it (like seb@harbourtrust.je), then points the domain at your host so the landing site can use it.
**Why it matters.** A regulated buyer, a trust officer, a partner at a law firm, will not enquire through a site on `something.vercel.app` from a sender at `harbourtrust123@gmail.com`. It reads as unserious, and in their world unserious means unsafe. A domain costs about GBP 10 a year. It is the cheapest credibility you will ever buy. Get it done before anyone sees the page.
**You are ready for this when.** `02-market/brand/brand-foundations.md` exists, because that is where your name was decided.

## Before you start
Read these:
- `02-market/brand/brand-foundations.md`: the business name. Your domain is built from it.
- `.spark/state.json`: `founder` and `business_type`. The host you point the domain at depends on the path.

You need a card, because registering a domain spends real money. It is small, about GBP 10 a year, but it is a spend.

Guardrail, and it is a hard one: **do not buy anything until the founder says yes to the exact domain and the exact price on screen.** Read the domain and the annual cost back to them, wait for a plain "yes", then proceed. This is the human-in-the-loop rule. Money does not move without a sign-off.

## Steps

1. **Choose the domain.** Take the business name from `brand-foundations.md` and turn it into a domain. Rules, in order of preference:
   - For a Jersey-facing business, prefer a `.je`. It signals local, and locals trust local. A `.com` is the safe second choice. Avoid `.io`, `.co` and novelty endings for regulated sectors; they read as tech-startup, not trust firm.
   - Keep it short and typo-proof. `harbourtrust.je` beats `harbour-trust-advisory-jersey.com`. If the exact name is taken, add the sector, not a number: `harbourtrustco.je`, never `harbour99.je`.
   - Check it is free. Run the checker (step 3) or look it up at your registrar.

2. **Pick the registrar, and keep DNS in one place.** Use one company for both the domain and its DNS. Recommendation: Cloudflare Registrar. It sells domains at cost (no markup, no first-year-cheap-then-triple trick) and its DNS is free, fast and the easiest to point at a host. A `.com` runs about GBP 9 a year there. For a `.je` you must use a Jersey-accredited registrar (Cloudflare does not sell `.je`); use one from the list in the walkthrough, then move DNS to Cloudflare afterwards if you want the simpler control panel. Full click-by-click steps are in `${CLAUDE_SKILL_DIR}/references/domain-and-email-walkthrough.md`.

3. **Check the domain is free before you reach for the card.** Run:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/check-domain-email.py --domain <yourdomain>
   ```
   If it reports "does not resolve", the domain is very likely unregistered and available. If it resolves to someone else's site, pick another. This is a quick sanity check, not a legal clearance; the registrar's own search is the authority on availability.

4. **Get the sign-off, then register.** Show the founder the exact domain and the exact annual price. Wait for "yes". Then register it at the chosen registrar. Do not turn on any paid add-ons (privacy is usually free and worth keeping; "SEO packs" and "email pro" upsells are not).

5. **Point the domain at your host.** This is DNS, and it is the step that scares people for no reason. You add one or two records at the registrar that say "when someone visits this domain, send them to this host". The exact records depend on the path (below). The walkthrough has the precise values to paste. DNS can take from a few minutes to a couple of hours to take effect; that is normal, not a fault.

6. **Set up the business email.** You need an address on the domain that can send and receive. Two routes:
   - **Fastest and free today:** email forwarding plus Gmail "send as". Forwarding catches anything to `you@yourdomain` and drops it in your existing inbox. Gmail's "send mail as" lets you reply from `you@yourdomain`. Receives and sends, GBP 0, live in fifteen minutes. Good enough to launch on.
   - **Proper, and what you will settle on:** Google Workspace Business Starter, about GBP 5 per user a month. A real mailbox, calendar and shared drive on your domain. Recommended once the first customer is in sight, not before. It is a monthly spend, so it needs its own sign-off.
   Start with forwarding today. Note the choice in `DECISIONS.md`. The walkthrough covers both.

7. **Test it end to end.** Send an email from the new address to a different inbox you control, and reply back to the new address. Both must arrive. Then run the checker to confirm the domain resolves and the mail records are in place:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/check-domain-email.py --domain <yourdomain> --email you@<yourdomain>
   ```

8. **Wire the landing site to use it.** Record the domain so `d3-landing-site` publishes to it instead of a raw host subdomain, and so every outreach message on Day 4 sends from the business address. Write both into the artefact below.

## The artefact
Writes `03-product/domain-email.md` in Markdown. It records:
- the registered domain, the registrar, and the annual cost paid;
- the DNS records added (type, name, value), so the setup is reproducible and auditable;
- the email setup chosen (forwarding-plus-Gmail, or Workspace) and the address;
- a one-line "verified" note: the date the send-and-receive test passed.

What good looks like: a stranger reads this file and can rebuild your entire domain and mail setup from it, and the "verified" line proves it worked, not just that it was configured.

## Done when
Three things are true, and the checker prints PASS on the first two:
1. The domain resolves (visiting it reaches your host, not a registrar parking page).
2. The domain has valid mail records (MX or a forwarding record).
3. A test email sent from `you@yourdomain` arrives in another inbox, and a reply to `you@yourdomain` arrives back. This one you confirm by eye; the checker cannot read your inbox.

## Log it
Append to CHANGELOG.md via the logbook helper, with the numeric result (the annual cost):
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
Set the Day 3 progress via the journey-state helper (the logbook call above already registered the artefact):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"current_day":3,"days":{"3":{"outcome":"domain live and business email verified"}}}'
```

## If it goes wrong
- **DNS has not taken effect after two hours.** Check you edited DNS at the same company that answers for the domain (if you moved DNS to Cloudflare, edit it at Cloudflare, not the original registrar). The checker's `--verbose` flag shows exactly what the domain currently points at.
- **The `.je` you want is taken or the registrar process is slow.** Register the matching `.com` today so nothing on Day 3 is blocked, and chase the `.je` in parallel. Point both at the same host later. Note it in `DECISIONS.md`.
- **Email will not send from the domain (Gmail rejects "send as").** Gmail needs an SMTP relay or an app password for that; the walkthrough has the exact settings. If it still fights you, launch on forwarding-only for now (you can receive, which is what matters for enquiries) and fix sending before Day 4 outreach.
- **No card, or spend not approved yet.** Do not register. Reserve the name by noting it in `DECISIONS.md`, keep the site on its free host subdomain for now, and come back the moment the spend is signed off. Everything downstream still works; it just looks less finished.
