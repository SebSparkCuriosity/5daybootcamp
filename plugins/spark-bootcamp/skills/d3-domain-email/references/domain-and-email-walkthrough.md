# Domain and email: the click-by-click walkthrough

This is the long version of the steps in the skill. Do it once, in order. Total time is about thirty minutes, most of which is waiting for DNS. Have a card ready. The only required spend is the domain itself, about GBP 10 a year.

A quick plain-English glossary, because the jargon is the only hard part:
- **Domain.** The name you own, like harbourtrust.je. You rent it yearly from a registrar.
- **Registrar.** The company you buy the domain from and pay each year.
- **DNS.** The address book of the internet. It says "this domain lives at this host". You edit it at whoever controls the domain's DNS (usually the registrar).
- **A record.** A DNS line pointing a domain at a numeric server address.
- **CNAME record.** A DNS line pointing one name at another name (used to point at a host like Vercel).
- **MX record.** A DNS line saying "mail for this domain goes here".

## 1. Register the domain

### If you want a .com (recommended second choice, works everywhere)

Use Cloudflare Registrar. It sells at cost with no first-year discount trick, and its DNS is the simplest to work with.

1. Go to dash.cloudflare.com and create a free account.
2. Go to Domain Registration, then Register Domains.
3. Search your name. If it is free, add it. A .com is about GBP 9 a year.
4. Keep WHOIS privacy on (it is free). Skip every other add-on.
5. Pay. The domain and its DNS now live in one place, which is what you want.

### If you want a .je (recommended first choice for a Jersey business)

.je domains are managed locally and Cloudflare does not sell them. You must use an accredited registrar. Channel Isles domains are run through the CIDR registry; buy through one of its accredited registrars (search "accredited .je registrar"). Well-known general registrars that resell .je include some UK providers; check the current accredited list before you pay, because it changes.

1. Register the .je at the accredited registrar. Expect about GBP 40 a year for a .je, more than a .com, because the market is smaller. That is still cheap credibility for a Jersey firm.
2. After it is registered, you can optionally move DNS management to Cloudflare for the easier control panel: add the domain in Cloudflare as a "add a site" (free plan), then change the nameservers at the .je registrar to the two Cloudflare gives you. Wait for Cloudflare to say "active". Now you edit DNS at Cloudflare.

Whichever you choose, note the registrar and the annual cost. It goes in the artefact.

## 2. Point the domain at your host

Do this at whoever controls the DNS (Cloudflare if you moved it there, otherwise the registrar). The exact records depend on your business path.

### Software (site on Vercel, the default stack)

In Vercel, open the project, go to Settings, Domains, and type your domain. Vercel shows you the exact records to add. Usually:
- An A record: name `@`, value `76.76.21.21` (Vercel's address; use whatever Vercel shows you, not this from memory).
- A CNAME record: name `www`, value `cname.vercel-dns.com`.

Add those at your DNS provider, then go back to Vercel and click Refresh until the domain shows a green tick.

### Hardware or services (site on a simpler host, e.g. a page builder or Vercel-hosted single page)

Same idea. The host (Vercel, Netlify, a page builder) gives you the records. Paste them at your DNS provider. If your host only gives a "target" name, use a CNAME on `www` and a redirect from the bare domain, which the host explains in its own domain settings.

Record every line you add (type, name, value) so the artefact can list them.

## 3. Business email

You need an address on the domain that both receives and sends. Pick a route.

### Route A: forwarding plus Gmail send-as (free, live in fifteen minutes, launch on this)

**Receive**, via forwarding:
1. At Cloudflare, open Email, then Email Routing, and enable it (free). It adds the needed MX records for you automatically.
2. Add a route: `you@yourdomain` forwards to your existing personal or work inbox. Verify the destination address when it emails you.
3. Test: email `you@yourdomain` from your phone. It should land in your existing inbox.

If your DNS is not on Cloudflare, most registrars have their own "email forwarding" feature that does the same; turn it on and add the MX records they specify.

**Send as**, via Gmail:
1. In Gmail, Settings, Accounts and Import, "Send mail as", Add another email address.
2. Enter your name and `you@yourdomain`.
3. When asked for an SMTP server, use a relay. The simplest is to use your Gmail's own SMTP with an app password: server `smtp.gmail.com`, port `587`, TLS, username your full Gmail address, password an app password you create at myaccount.google.com, Security, App passwords. (App passwords need 2-step verification switched on first.)
4. Gmail sends a confirmation to `you@yourdomain`; because forwarding is on, it arrives in your inbox. Click the link.
5. Set `you@yourdomain` as the default "from" if you want every new mail to send from the business address.

Now you can receive at, and send from, `you@yourdomain` without paying a penny.

### Route B: Google Workspace (about GBP 5/user/month, the grown-up option)

Recommended once a first customer is in sight, not on Day 3. It gives a real mailbox, shared calendar and drive.
1. Go to workspace.google.com, start Business Starter, and enter your domain.
2. It walks you through verifying the domain (a TXT record you add at your DNS provider) and adding its MX records.
3. Create the mailbox `you@yourdomain`. Done.

Because this is a recurring monthly spend, it needs its own explicit sign-off before you subscribe.

## 4. Verify

Run the checker from the skill:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/check-domain-email.py --domain yourdomain --email you@yourdomain --verbose
```
It confirms the domain resolves and mail records exist. Then do the human test it prints: send from the new address, reply to it, confirm both arrive. Only then is the email "verified".

## Common snags

- **"It still shows the old parking page."** DNS caches. Give it up to two hours. Check you edited DNS at the right place (Cloudflare if you moved nameservers there).
- **"Gmail rejected my send-as."** You almost certainly skipped the app password, or 2-step verification is off. Turn 2-step on, create an app password, use that as the SMTP password.
- **"No MX records found by the checker but forwarding works."** Some forwarding setups still need MX records; if mail actually arrives in your test, trust the test over the checker and note it. If mail does not arrive, add the MX records your forwarding provider specifies.
- **".je is taking days to register."** Register the .com today so Day 3 is not blocked, and point both at the same host once the .je lands.
