# The warmth model

Warmth is a single 0 to 100 score that answers one question: how close is this person to paying you? We built it so the top of the list is the fastest yes, not the loudest name.

Three parts add up to the score.

## 1. Intent (0 to 60 points)

What did they actually do? Actions beat words, and money beats everything. This is the largest weight because it predicts a sale better than anything else.

| Signal | Points |
|---|---|
| Left a deposit or pre-order, or paid anything | 60 |
| Booked a call or an intake slot | 45 |
| Asked a buying question ("how much", "when can I start", "can I buy") | 35 |
| Used the product slice and hit a limit (software) | 30 |
| Replied to the sample deliverable (services) | 30 |
| Joined a waitlist or mailing list | 15 |
| Opened or clicked an email only | 5 |

Take the single highest signal, do not stack them.

## 2. Segment match (0 to 25 points)

Are they exactly who you set out to serve in your Day 1 interview target? A perfect match scores 25. Right sector, wrong role scores 12. Adjacent but plausible scores 5. Off-target scores 0, and an off-target person should rarely make the top 10 however keen they are.

## 3. Engagement depth (0 to 15 points)

How many separate times have they shown up? One touch scores 5, two touches score 10, three or more score 15. Someone who filled the form, then replied to an email, then booked a call is warmer than a single big action with silence after.

## Reading the score

- 70 and above: hot. Day 5 opens here.
- 40 to 69: warm. Worth a direct, personal ask this week.
- Below 40: cool. Keep them in the plan but expect a longer path.

## Overruling the score

The number ranks the list. You pick #1. If a prospect scores slightly lower but is a faster yes (they hold the budget, they replied an hour ago, they already said "send me the price"), promote them and write the one-sentence reason in DECISIONS.md. The model serves the sale, not the other way round.
