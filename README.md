# Spark Bootcamp

Five days from a raw idea to a first paying customer.

This is a Claude Code plugin. You install it, type one command a day, and it hand-holds you
through the whole journey: validating the problem with real interviews, mapping the market,
sizing it, building a brand and a pitch deck, defining and building an MVP, testing it with
real prospects, and closing your first sale. It works whether you are building software,
hardware or a service. Built by [Spark AI Agency](https://sparkconsulting.tech) for Digital
Jersey's cohort.

Everything you produce is saved to your own project and logged, so you finish the week with a
working product, a full set of documents, and an audit trail a regulator nods at rather than
flinches from.

## The week

| Day | Theme | What you walk away with |
|---|---|---|
| Mon | Discovery | 8 to 12 interviews synthesised, one validated problem, one named segment |
| Tue | Market and Proposition | A market map, TAM/SAM/SOM, a proposition and USP, a brand, a hand-out pitch deck |
| Wed | Product and Build | A working MVP live for a real prospect to act on, tracked in GitHub |
| Thu | Test and Go-to-Market | 5 usability tests, a sales deck, client processes, a funnel, a go-to-market plan |
| Fri | Tweaks and First Sale | Final fixes, pricing, and one committed yes with a date and an amount |

## Install

You need Claude Code, git and Node installed first. Digital Jersey runs a setup session before
the bootcamp to get you there.

```
/plugin marketplace add SebSparkCuriosity/5daybootcamp
/plugin install spark-bootcamp@spark
```

Then, once:

```
/spark-bootcamp:doctor
```

This checks your machine, lays out your project, and prints the pre-work you need before Monday
(accounts, a trading entity and bank account, a domain). Then start:

```
/spark-bootcamp:start
```

From there, `/spark-bootcamp:coach` always tells you where you are and the one command to run next.

## What is inside

One plugin, 60 skills, organised as a five-day journey plus a spine that holds it together (a
state machine, a running audit log, a shared brand, and a reusable interview engine). See
[`plugins/spark-bootcamp/README.md`](plugins/spark-bootcamp/README.md) for the full skill index.

## A note on the legal bits

Skills that produce legal or data-protection documents (privacy notices, engagement letters,
data-processing clauses) generate drafts to get you moving. They are drafts. Have a qualified
lawyer review anything before you rely on it. Spark does not warrant them.
