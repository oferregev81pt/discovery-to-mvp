# Brief — Harvest Line restaurant ordering discovery

## Problem space
Harvest Line is a produce and dry-goods distributor. It supplies about 200 restaurants in the city: vegetables, herbs, fruit, dairy and pantry items, delivered every morning between 6 and 8 a.m.

Ordering is manual. Chefs send their order the night before to their sales rep, mostly as WhatsApp voice notes after service. The rep types each order into Stockwise, Harvest Line's warehouse system. The warehouse picks from 4:30 a.m. When something is out of stock, the warehouse substitutes, and the rep tries to tell the chef.

Leadership's question: "Restaurants keep complaining about wrong deliveries. Should we build an ordering app?"

## Who we talked to
- **Tamar Levi**, head chef and co-owner of Olive & Ash (60-seat bistro, customer for 2 years). Interviewed by Ofer Regev.
- **Avi Cohen**, sales rep at Harvest Line, handles about 35 restaurants. Interviewed by Ofer Regev.

Both calls were about 15-minute slots. Tamar's call was captured by two transcription tools (Zoom's transcript and an Otter recording). Avi's call has only the Zoom transcript.

## Glossary
Harvest Line (the distributor) · Olive & Ash (Tamar's restaurant) · Stockwise (Harvest Line's warehouse system) · WhatsApp · voice note · pick list (the warehouse's 5 a.m. list of what was picked) · substitution · delivery note (paper signed at the door) · credit / credit note · walk-in (the walk-in fridge) · mise en place · sous-chef · POS · flat-leaf parsley · fava beans · sesame-free bread · allergy table

## Constraints
- A team of 2 engineers and 1 designer for about 6 weeks.
- Stockwise has no API; anything that changes an order goes through a person or a CSV import.
- Delivery vans have no GPS tracking.
- Sales reps must stay in the loop; restaurants buy from people they trust.
