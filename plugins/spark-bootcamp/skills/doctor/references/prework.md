# Pre-work: start this 2 to 4 weeks before your bootcamp Monday

This is not a Sunday-night checklist. Three things on it take weeks, not minutes:
booking your Day 1 interviews, a bank account that can receive money, and a
trading entity. Start all three the day you read this. You interview real people
on the Monday and take a real payment on the Friday, so the diary and the account
both have to work.

Tick each box in this file as you go. It lives at `.spark/prework.md` in your
project, so edit it and save.

## 1. Book your Day 1 interviews (start today, this is the long pole)

Nobody is free for an interview tomorrow. Day 1 of the bootcamp runs on 8 to 12
booked conversations, and the only way they exist is if the invitations went out
2 to 4 weeks earlier. `start` will ask for your actual bootcamp Monday and every
later skill reads it from there, so it is always the true date, never a guess.
If today is less than 2 weeks out from it, say so out loud: 8 to 12 booked is
still possible, but only if invitations go out today, not this evening.

The plugin walks you through each step; run `/spark-bootcamp:coach` and it will
point you at the next one.

- [ ] **Run `/spark-bootcamp:start`.** Your name, path, one-sentence idea, your
      bootcamp Monday, and the week's numeric target. 20 minutes of honest talking.
- [ ] **Triage who to interview** (`p0-interview-triage`). One segment, the exact
      role, 8 to 12 people, three screening questions. A conversation, not a form.
- [ ] **Build the invite list** (`p0-invite-list`). 20 or more named, reachable
      people, because roughly half will not reply.
- [ ] **Write and send the invitations** (`p0-invitations`). Email, WhatsApp or
      LinkedIn, whichever each person actually answers, inviting them to a 20 to
      25 minute slot on your bootcamp Monday. You approve every message before it goes.
- [ ] **Draft the data-protection pack** (`data-protection`). Ten minutes while
      replies come in: consent wording for the interviews, a privacy notice, and
      the data clause Friday's engagement letter embeds. Drafts only; a qualified
      lawyer reviews them before you rely on them.
- [ ] **Track replies to 8 booked** (`p0-schedule`). Run it whenever a reply lands.
      Pre-work is done when 8 or more interviews are in the Monday diary.

## 2. The other one that cannot wait: get paid on Friday

You need somewhere for a customer to send money on Day 5. Sort this now.

- [ ] **Trading entity decided.** Sole trader or a company. For the bootcamp, sole
      trader is fine and free to start in Jersey: you trade under your own name and
      declare the income. A company costs more and takes longer to register, so only
      form one now if you already know you need it (investors, liability, a partner).
      If in doubt, start as a sole trader and incorporate later. Write your choice in
      `DECISIONS.md` on the Monday.
- [ ] **Business bank account that can receive a transfer.** Jersey business
      accounts can take one to three weeks to open, so if you do not have one,
      apply today. A personal account you already control will do for the
      bootcamp if a business account will not arrive in time, but keep the bootcamp
      money separate and move to a proper business account straight after. Budget: 0
      to open, some banks charge a monthly fee of around GBP 5 to 15.
- [ ] **A way to actually take the payment.** A bank transfer (share your account
      name, sort code and account number) costs nothing and works for a first sale.
      Card and online payments (Stripe, GoCardless, SumUp) are nicer but need the
      entity and account above first, so treat them as a bonus, not a blocker.

## 3. Accounts (only the software path needs all three)

If you are building software, open all three now. They are free to start and each
takes about five minutes, but email confirmations and first logins are smoother done
in advance than mid-build on the Wednesday. Hardware and services founders need only
a GitHub account (handy, not essential) and can skip Supabase and Vercel.

- [ ] **GitHub** account, at github.com. Free. This is where your code lives and where
      the build day tracks every change. Then install the GitHub CLI from cli.github.com
      and run `gh auth login` so your machine is connected.
- [ ] **Supabase** account, at supabase.com. Free tier. Your database and login for the
      software slice. No card needed to start.
- [ ] **Vercel** account, at vercel.com. Free tier (Hobby). This is what puts your app on
      a public URL. No card needed to start.

## 4. A domain and a business email

- [ ] **A domain name**, around GBP 10 for the year. Buy the `.com` or the `.je` if it
      suits a Jersey audience. Namecheap, Cloudflare or Gandi are all fine. You do not
      need to point it anywhere yet; Day 2 handles that. Pick a name you can live with,
      not a perfect one. You can change it later.
- [ ] **A business email on that domain**, for example you@yourname.com. It makes your
      invitations and Friday outreach look like a business, not a hobby. Google
      Workspace and Zoho Mail both do this; Zoho has a free tier for one domain.
      Budget: 0 to around GBP 6 a month. Do this before the invitations go out if
      you can; a real domain in the from-line lifts reply rates.

## 5. The money budget for the week

Write down what you are willing to spend so Friday holds no surprises. A realistic
bootcamp week costs about GBP 10 to GBP 25 in total, because almost everything runs on
free tiers. Here is the honest picture.

| Item | Likely cost | Notes |
|---|---|---|
| Domain | ~GBP 10 / year | The one certain spend. |
| Business email | GBP 0 to ~6 / month | Free on Zoho's single-domain tier. |
| Hosting (Vercel) | GBP 0 | Free Hobby tier covers the bootcamp. |
| Database (Supabase) | GBP 0 | Free tier covers the bootcamp. |
| Bank account | GBP 0 to ~15 / month | Some Jersey business accounts charge a small fee. |
| A paid API, if your idea needs one | Name it and cap it | For example an AI model API. Set a hard spend cap (say GBP 5) before Wednesday so a runaway loop cannot surprise you. |

- [ ] **My total budget for the week is: GBP ______.** Write the number here. If your
      idea needs a paid API, name it and set its spend cap now, before the build day.

## When you are done

You are ready for your bootcamp Monday when every box above is ticked, or the
unticked ones are things you have consciously decided to skip (for example, a
hardware founder skipping Supabase). The one box that cannot be skipped is the
interviews: 8 or more booked, tracked in `00-prework/interview-schedule.md`.
Run `/spark-bootcamp:coach` any time to see your next step.
