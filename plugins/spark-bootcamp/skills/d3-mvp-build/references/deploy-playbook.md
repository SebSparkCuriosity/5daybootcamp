# Deploy playbook, Day 3

The goal is one thing: a public URL a stranger can reach. Not a perfect product. A reachable one. Free tiers get you there today with no spend and no sign-off.

## Software: deploy to Vercel

Default stack: Next.js, Supabase, Vercel. This is the fastest route from code to public URL that a non-technical founder can follow.

1. Push your repo to GitHub.
2. Import it into Vercel and deploy. The free (Hobby) tier is enough for Day 3, so no money changes hands and no sign-off is needed.
3. Add your Supabase environment variables in the Vercel project settings (the project URL and the anon key). Redeploy so they take effect.
4. You get a public `*.vercel.app` URL. That is your live URL. Smoke-check it.

Supabase note: keep the schema to the one or two tables the PRD action actually touches. A signup form needs one table. Do not model the whole business today.

## Hardware: prototype plus a capture page

You are proving demand, not manufacturing. Two artefacts.

1. The prototype: a CAD render, a rendered product shot, or a well-lit photo of a physical mock. One strong hero image does more work than a rough animation.
2. The page: a Next.js page on the Vercel free tier showing the render, the promise, and one action.

Money guardrail. A waitlist that captures an email needs no spend and no sign-off, build it freely. A refundable deposit through Stripe touches real money, so build it in Stripe test mode today, and pause for the founder to sign off before you swap in a live key. Test mode proves the flow works without charging anyone.

## Services: sample deliverable plus a bookable page

Prove the package is real by finishing one piece of it.

1. The sample: the actual artefact a client receives, done properly. A sample report, a worked audit, a completed template. This is your proof, so make it genuinely good.
2. The offer: one package, one fixed price, one turnaround. Not a menu.
3. The page: a Next.js page on the Vercel free tier with the offer, the sample as proof, and a booking or intake form. A form or an embedded scheduler both count as bookable.

Book a slot yourself through the live page before you call it done. If your own booking does not arrive, neither will a prospect's.

## The universal check

Whatever the path, do the one action yourself, on the public URL, on your phone. If you can complete it, it is shipped. If you cannot, that gap is your next issue.
