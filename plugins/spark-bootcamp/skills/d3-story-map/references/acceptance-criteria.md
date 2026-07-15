# Acceptance criteria: how to write "done"

An acceptance criterion is a testable statement of when a feature is finished. It is the difference between "the signup works" (an opinion) and "given a visitor on the page, when they submit a valid email, then a row appears in the table and they see a confirmation message" (a fact anyone can check). Write them before you build, so the build has a finish line and you stop when the work is done, not when you run out of Friday.

## The one form that works: Given / When / Then

- **Given** the starting situation (who, and in what state).
- **When** the action they take.
- **Then** the observable result: something changed that you or anyone else can see.

Example, software: "Given a visitor on the landing page, when they enter an email and click Join, then their email is saved to the waitlist table and they see 'You're on the list'."

Example, hardware: "Given a prospect viewing the pre-order page, when they click Reserve and pay the deposit, then Stripe records the payment and their name appears in the orders list."

Example, services: "Given a prospect who has read the sample deliverable, when they pick a slot on the intake page, then the booking is saved and they receive a confirmation with the date."

## The test: could a stranger judge it?

Hand the criterion to someone who has never seen your product. If they can tell you pass or fail without asking you a single question, it is a real criterion. If they have to ask "well, how would I know?", it is not. Rewrite it until the result is something they can observe: a screen shown, a row written, a redirect happened, a payment recorded, a file produced.

## Words that mean you have not finished writing it

"Works", "is nice", "looks good", "is fast", "is easy", "is intuitive". None are observable. Replace each with the specific thing a user does and the specific thing they then see. "Fast" becomes "the result appears within 3 seconds". "Easy" becomes "a first-time visitor completes the flow without instructions".

## How many per Must

One to three. One is often enough for a small Must. If a Must needs more than three criteria to pin down, it is probably two Musts wearing one coat: split it. Every Must in `requirements-moscow.md` needs at least one before the story map is done.

## Why this is the auditable bit

Acceptance criteria are what turn "we built something" into "we built exactly this, and here is how we checked". When the week ends and `audit-pack` compiles the record, these lines are the evidence that each Must was delivered and verified, not just started. Write them as if a regulator or an investor will read them, because in a Spark build, they will.
