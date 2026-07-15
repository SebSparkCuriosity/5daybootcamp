# MCP setup for the chosen stack

MCP servers let me act inside your tools directly, so the Day 3 build skills
create the repo, run the database migrations, and read the deployment logs for
you, rather than handing you steps to copy. Connect the ones your path needs,
then move on. This takes about five minutes.

## Software: GitHub and Supabase

**GitHub.** Holds your code and triggers the Vercel deploy on every push.
1. In Claude Code, run `/mcp` and choose to add a server, or add GitHub in your
   MCP settings.
2. Authenticate with your GitHub account when prompted. Grant repo access.
3. Confirm it is live: I should be able to list your repositories.

**Supabase.** Your database, auth and file storage.
1. Create a free Supabase account first at supabase.com if you have not.
2. Add the Supabase MCP server in Claude Code the same way.
3. Authenticate, then pick or create the project for this build.
4. Confirm it is live: I should be able to list your tables.

A card is not needed on either free tier. You only add a card if you upgrade
later, which you will not need before a first paying customer.

## Hardware: none required for CAD

The CAD render (Onshape) and the pre-order page (Carrd plus a Stripe payment
link) are done in the browser and do not need an MCP server. If your pre-order
page later becomes a coded site, add the GitHub MCP then, following the software
steps above.

Stripe onboarding is separate from MCP. Start it early: it needs your bank
details and identity verification, which can take a day to clear.

## Services: none required

Google Docs, Carrd and Cal.com are all direct document and page work. No MCP
server is needed. If you standardise on Microsoft 365, the same is true for Word
and Bookings.

## If a connection fails

Check you are signed in to the provider in your browser, then retry the connect
step. If it still fails, skip the MCP for now and tell me: I can fall back to
giving you exact steps to run yourself so the build is not blocked. A missing
MCP slows me down, it does not stop the week.
