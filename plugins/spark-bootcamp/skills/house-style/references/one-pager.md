<!--
Spark branded one-page template (markdown).
The brochure and proposal skills copy this file, then replace every {{token}}.
Never leave a raw {{token}} in a saved artefact. Where brand.json has no value
for a token, use the fallback given in the comment beside it.

Tokens pulled from .spark/brand/brand.json:
  {{brand.name}}          -> brand.name           (fallback: the founder's business name from state.json)
  {{brand.tagline}}       -> brand.tagline        (fallback: "Idea into system.")
  {{brand.primary}}       -> brand.colours.primary (fallback: #0B5FEF)
  {{brand.accent}}        -> brand.colours.accent  (fallback: #00C2A8)
  {{brand.contact_email}} -> brand.contact.email   (fallback: leave the line out)
  {{brand.contact_url}}   -> brand.contact.url      (fallback: leave the line out)
Content tokens the calling skill fills from its own inputs:
  {{headline}} {{problem}} {{what_it_is}} {{proof_point}} {{how_it_works_1..3}}
  {{price}} {{target_outcome}} {{call_to_action}}
-->

# {{brand.name}}

**{{headline}}**

{{brand.tagline}}

---

## The problem

{{problem}}

## What it is

{{what_it_is}}

One line of proof: {{proof_point}}

## How it works

1. {{how_it_works_1}}
2. {{how_it_works_2}}
3. {{how_it_works_3}}

## What you get, and by when

{{target_outcome}}

Price: {{price}}. Fixed. Agreed before we start.

## Next step

{{call_to_action}}

Talk to us: {{brand.contact_email}} · {{brand.contact_url}}
