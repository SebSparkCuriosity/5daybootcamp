# MoSCoW: the strict definitions

MoSCoW comes from Dai Clegg at Oracle in 1994. The capital letters are the four buckets; the lowercase o's just make it sayable. It works because it forces a decision on every requirement instead of letting a wish-list masquerade as a plan.

Sort honestly. The whole value is in the discipline, and the discipline is easy to cheat.

## Must
The promise, made real. Without this the product does not deliver the proposition and the customer will not pay. Test it: if you shipped without this line, would you still be keeping the promise in `proposition.md`? If yes, it is not a Must. Cap: 7.

## Should
Important and painful to leave out, but the promise survives without it. This is your version-two list, and version two is next week, not this week. Should items are real work you have consciously deferred, not junk.

## Could
Desirable, low cost, low effort. You will get to these only if time remains, and in a five-day build it will not. Keeping the list is fine. Expecting to build it is not.

## Won't
Explicitly out of scope for this cycle. This is the most valuable bucket and the one founders skip. Naming what you will not build stops scope creep dead and tells anyone reading (including a regulator or investor) that you made a deliberate choice, not an accidental omission. Write at least 3.

## The two traps

1. **Everything is a Must.** If more than 7 lines are Musts, you have relabelled your wish-list. Demote until 7 remain.
2. **The empty Won't.** No Won'ts means no decisions were made. A serious scope has a serious Won't list.

## The MVP boundary

The MVP is the line a customer crosses with a card. Not the impressive version, not the safe version: the smallest version someone will pay for. Every Must sits on the customer's side of that line. Everything else sits past it, in Should, Could or Won't.
