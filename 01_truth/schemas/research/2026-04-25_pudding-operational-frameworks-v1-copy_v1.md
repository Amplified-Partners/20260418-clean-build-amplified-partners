---
title: "Pudding Operational Frameworks V1 Copy"
id: "pudding-operational-frameworks-v1-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "framework"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**PUDDING Operational Frameworks**

Lens Description, Rubric Scoring, and Kill Switch

*Prospecting, Not Expecting*

v1.0 --- 17 March 2026

Ewan Bramley (originator) + Claude (formaliser)

Theoretical foundation: Don Swanson (1986) ABC Model

**1. The Problem This Solves**

The PUDDING technique works. It\'s been mathematically validated (p \< 0.001 for 4/4 label matches). But its effectiveness depends entirely on three things that happen BEFORE you start mixing:

1.  **How well you describe the lens** --- a vague lens produces vague matches. A precise lens produces actionable candidates.

2.  **How consistently you score results** --- if scoring depends on who\'s having a good day, you can\'t compare across runs.

3.  **How quickly you kill dead ends** --- compute is money. A lens that produces no signal after the first batch is a lens to abandon, not to double down on.

These three frameworks make PUDDING repeatable, trustworthy, and economical.

**Key philosophy:** *\"Prospecting, not expecting.\"* You\'re panning for gold. You put your pan in the river, swirl it, and look. If there\'s nothing glinting after a few swirls, you move to a different spot. You don\'t dig a mine based on a hunch.

**2. The Lens Description Framework**

**What a Lens Is**

A lens is the specific problem, question, or goal you\'re looking through when you run a PUDDING session. It determines:

-   What domains you search

-   What counts as relevant

-   What \"success\" looks like

-   What the B-terms (bridges) need to connect

**A lens is NOT a topic.** \"Marketing\" is not a lens. \"How can we reduce the time from first contact to first sale for plumbers who currently take 14+ days?\" is a lens.

**The Lens Card**

Every PUDDING run starts by filling out a Lens Card. This is a single structured template:

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **LENS CARD --- \[short name\]**
  **GOAL:** *One sentence. What are you trying to discover or solve?*
  **DOMAIN A:** *The primary domain you know well*
  **DOMAIN B:** *The secondary domain you\'re looking into --- or \"OPEN\" if you want the technique to find it*
  **WHAT WOULD SUCCESS LOOK LIKE?** *Concrete description. Not \"find interesting connections.\" Example: \"A technique from Domain B that solves the 14-day lag in Domain A, backed by at least anecdotal evidence\"*
  **BOUNDARY:** *What is OUT of scope? Example: \"Not interested in enterprise solutions --- SMB only\"*
  **CLIENT TYPE:** *If applicable --- who is this for?*
  **DISC PROFILE:** *If known --- D/I/S/C*
  **CHANGE TOLERANCE:** *High / Medium / Low --- informs Kaizen split later*
  **COMPUTE BUDGET:** *How many pairs to screen before deciding? Default: top 50 pairs.*
  **EXPECTED OUTPUT FORMAT:** *□ Ranked candidate list □ Full recipe cards □ Implementation brief □ All*
  **CONFIDENCE THRESHOLD:** *Min Jaccard score to proceed. Default: J ≥ 0.75 (high), J ≥ 0.5 (investigation)*
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Good Lens vs. Bad Lens**

  -------------------- ---------------------------------------------------------------- ----------------------------------------
  **Quality**          **Good Lens**                                                    **Bad Lens**
  **Specificity**      \"Reduce invoice-to-payment time for sole traders using Sage\"   \"Improve finances\"
  **Testability**      Has a measurable outcome you could check                         \"Find interesting connections\"
  **Domain clarity**   Names at least one domain clearly                                \"Look at everything\"
  **Boundary**         States what\'s excluded                                          No exclusions (scope creep guaranteed)
  **Compute budget**   Sets a kill threshold                                            \"Keep going until we find something\"
  -------------------- ---------------------------------------------------------------- ----------------------------------------

**Why the Lens Must Be Set BEFORE Mixing**

**Ewan\'s critical rule:** *\"The pudding technique works very well, but only when you\'ve got a clear goal, a clear lens to put it through, and an objective framework. It needs to be decided before, so it\'s applied objectively across all the methodologies.\"*

If you set the lens after seeing the results, you\'re fitting the story to the data. That\'s confirmation bias, not discovery. The lens is your pre-registration.

**Lens Evolution**

A lens can evolve BETWEEN runs, not during them. If Run 1 produces unexpected but interesting signal in a direction you didn\'t anticipate, you don\'t retroactively change the lens --- you create a NEW lens card for a follow-up run. This preserves the audit trail.

**3. The Rubric Scoring Framework**

**The Problem with Existing Scoring**

The PUDDING skill already has two scoring approaches:

1.  **Simple:** (Shared Dimensions × 2) + Unique\_A + Unique\_B --- threshold ≥ 5

2.  **Advanced:** (Domain Distance × Pattern Alignment) + Gap Complement + Tension Bonus --- threshold ≥ 13

These work but they\'re subjective on some dimensions. The Anchored Rubric below replaces subjective descriptions with concrete anchor points that describe what each score looks like. No interpretation needed.

**The Anchored Rubric**

**1. DOMAIN DISTANCE (1--6)**

  ----------- ------------------------------------------------------------------
  **Score**   **Anchor**
  **1**       Same sub-domain (e.g., two marketing techniques)
  **2**       Same domain, different sub-domain (e.g., marketing + sales)
  **3**       Adjacent domains (e.g., finance + operations)
  **4**       Different domains, shared industry (e.g., HR + supply chain)
  **5**       Different industries (e.g., biology + software architecture)
  **6**       Completely unrelated fields (e.g., mycology + client onboarding)
  ----------- ------------------------------------------------------------------

**2. PATTERN ALIGNMENT (1--10)**

This is the PUDDING label Jaccard match --- NOT subjective. Formula: **Pattern Alignment = round(Jaccard\_slot × 10)**

  ----------- -------------------------------------------------
  **Score**   **Anchor**
  **10**      4/4 label match (identical WHAT.HOW.SCALE.TIME)
  **7--9**    3/4 label match
  **4--6**    2/4 label match
  **1--3**    1/4 or 0/4 label match
  ----------- -------------------------------------------------

**3. GAP COMPLEMENT (1--5)**

Test: Can you name the specific gap the combination fills? If yes, score 3+. If not, score 1--2.

  ----------- ------------------------------------------------------------------------------
  **Score**   **Anchor**
  **1**       Both concepts address the same gap --- no complement
  **2**       Slight complement --- one covers what the other mentions but doesn\'t solve
  **3**       Clear complement --- each solves a different part of the problem
  **4**       Strong complement --- combining fills a gap neither could fill alone
  **5**       Perfect complement --- two halves of a whole, each useless without the other
  ----------- ------------------------------------------------------------------------------

**4. TENSION BONUS (0--3)**

Test: Does combining them force you to resolve a contradiction? If yes, score 2+.

  ----------- --------------------------------------------------------------------------
  **Score**   **Anchor**
  **0**       No tension --- concepts agree on everything
  **1**       Mild tension --- different emphasis but compatible
  **2**       Productive tension --- disagreement creates insight when resolved
  **3**       Maximum tension --- apparent contradiction reveals something neither saw
  ----------- --------------------------------------------------------------------------

**The Combined Score**

**Pudding Candidate Score = (Domain Distance × Pattern Alignment) + Gap Complement + Tension Bonus**

  ---------------------- -----------------------
  **Threshold**          **Score**
  **Maximum possible**   (6 × 10) + 5 + 3 = 68
  **Minimum viable**     ≥ 13
  **High value**         ≥ 18
  **Exceptional**        ≥ 30
  ---------------------- -----------------------

Domain Distance and Pattern Alignment are the heavy hitters (up to 60 points). Gap Complement and Tension Bonus are tiebreakers (up to 8 points). Structural equivalence across distant domains is the strongest signal.

**Inter-Rater Reliability**

Because Pattern Alignment is deterministic (Jaccard calculation) and Domain Distance uses concrete anchors, only Gap Complement (1--5) and Tension Bonus (0--3) are subjective --- contributing at most 8 points out of 68 (\<12% of total score).

To validate: run 10 candidates through two independent scorers. Calculate ICC on the subjective dimensions. If ICC ≥ 0.7, the rubric is reliable. If not, tighten the anchors.

**4. The Kill Switch**

**The Philosophy**

*\"We should have data quite quickly from ones that just won\'t work. I don\'t want to waste a lot of time on this because we are prospecting, not expecting.\"*

A PUDDING run has three possible outcomes after the first batch:

1.  **GOLD** --- multiple candidates score ≥ 18. Proceed to full recipe development.

2.  **GRAVEL** --- some candidates score 13--17. Worth one more batch with refined taxonomy.

3.  **DIRT** --- nothing scores ≥ 13. Kill the lens. Move on.

**The 50-Pair Gate**

Default compute budget: screen the top 50 candidate pairs (after mathematical pre-screening with MinHash LSH / PMI). This is the \"first pan in the river.\"

After 50 pairs:

  ---------------------------------------- --------------------- --------------------------------------------------
  **Result**                               **Action**            **Next Step**
  ≥ 3 candidates scoring ≥ 18              **GREEN LIGHT**       Proceed to full recipe development
  1--2 scoring ≥ 18, or ≥ 5 scoring ≥ 13   **AMBER**             Refine taxonomy labels, run one more batch of 50
  Zero candidates scoring ≥ 13             **RED --- KILL IT**   Document null result, archive lens card, move on
  ---------------------------------------- --------------------- --------------------------------------------------

The kill is not a failure --- it\'s useful data. Archive it. It prevents someone running the same dead-end lens again.

**Time-Based Kill Switch**

If a single PUDDING run has consumed more than 2 hours of compute time (including LLM calls for labelling, scoring, and recipe development) without producing a GREEN LIGHT result, pause and reassess the lens. This prevents the \"just one more batch\" trap.

**The Null Result Template**

When a lens is killed, document it:

  ------------------------------------------------------------------------------------------------
  **LENS KILLED --- \[lens name\]**
  **Date:** *\[date\]*
  **Lens Card:** *\[reference\]*
  **Pairs Screened:** *\[number\]*
  **Best Candidate Score:** *\[number\]*
  **Reason for Kill:** *No structural signal / Scores below threshold / Time exceeded*
  **What We Learned:** *\[Any useful observation, even from a null result\]*
  **Do Not Re-run Unless:** *\[What would need to change to make this lens worth trying again\]*
  ------------------------------------------------------------------------------------------------

This feeds back into the Knowledge System / Graphiti --- null results are knowledge too.

**Escalation: When to Override**

The kill switch is a default, not a law. It can be overridden if:

1.  There\'s a specific hunch based on domain expertise that the taxonomy labels are wrong

2.  New data has entered the vault that wasn\'t available in the first run

3.  An adjacent lens DID produce signal, suggesting this lens would too with different domain pairings

Override must be documented: *\"Kill switch overridden because \[reason\]. Additional compute budget: \[number of pairs\].\"*

**5. How the Frameworks Interact**

The operational flow:

1.  **Fill out Lens Card** → defines the scope

2.  **Run PUDDING** with mathematical pre-screening → produces candidate pairs

3.  **Score each candidate** with the Anchored Rubric → produces ranked list

4.  **Apply Kill Switch gate** after first 50 pairs → GREEN / AMBER / RED

5.  **If GREEN →** develop full recipes, score with advanced formula, state 1+1=3

6.  **If AMBER →** refine and re-run once

7.  **If RED →** document null result, archive, move on

8.  **All results** (including nulls) feed back into Graphiti with full labels

+-------------------------------------------------+
| **The Lens Card** is the pre-registration.      |
|                                                 |
| **The Rubric** is the measurement tool.         |
|                                                 |
| **The Kill Switch** is the economic discipline. |
+-------------------------------------------------+

***Together: repeatable, objective, economical.***

**6. Quick Reference Card**

  -----------------------------------------------------------------------
  **LENS CARD TEMPLATE**
  **GOAL:** \[What are you trying to discover or solve?\]
  **DOMAIN A:** \[Primary domain\]
  **DOMAIN B:** \[Secondary domain or OPEN\]
  **SUCCESS:** \[Concrete measurable outcome\]
  **BOUNDARY:** \[What is out of scope?\]
  **CLIENT / DISC / CHANGE:** \[Type\] / \[D/I/S/C\] / \[High/Med/Low\]
  **COMPUTE BUDGET:** \[Default: 50 pairs\]
  **OUTPUT:** \[Ranked list / Recipe cards / Brief / All\]
  **CONFIDENCE:** \[J ≥ 0.75 high / J ≥ 0.5 investigation\]
  -----------------------------------------------------------------------

  ----------------------- ----------- ----------------------------------------------
  **Dimension**           **Range**   **Key Anchor**
  **Domain Distance**     1--6        1 = same sub-domain ... 6 = unrelated fields
  **Pattern Alignment**   1--10       round(Jaccard\_slot × 10) --- deterministic
  **Gap Complement**      1--5        Can you name the gap? Yes → 3+, No → 1--2
  **Tension Bonus**       0--3        Forces contradiction resolution? Yes → 2+
  ----------------------- ----------- ----------------------------------------------

**Score = (Domain Distance × Pattern Alignment) + Gap Complement + Tension Bonus**

  --------------------------- ------------ ----------------------------
  **Result after 50 pairs**   **Signal**   **Action**
  ≥ 3 candidates ≥ 18         **GREEN**    Proceed to recipes
  1--2 ≥ 18 or ≥ 5 ≥ 13       **AMBER**    Refine, run one more batch
  Zero ≥ 13                   **RED**      Kill, document, move on
  --------------------------- ------------ ----------------------------

  -------------------------------------------------------------
  **NULL RESULT TEMPLATE**
  **Date:** \[date\]
  **Lens Card:** \[reference\]
  **Pairs Screened:** \[number\]
  **Best Score:** \[number\]
  **Reason:** \[No signal / Below threshold / Time exceeded\]
  **Learned:** \[Observation from the null result\]
  **Re-run If:** \[What would need to change\]
  -------------------------------------------------------------

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Theoretical Foundation: Don R. Swanson (1986), Literature-Based Discovery

Adapted by: Ewan Bramley (originator) + Claude (formaliser)

Mathematical Validation: PMI, Jaccard, Information Theory --- see companion doc

Inter-rater reliability approach: Maki (2004), Stemler (2004)

*Status: Operational Framework v1.0 --- Hypothesis (untested in production)*
