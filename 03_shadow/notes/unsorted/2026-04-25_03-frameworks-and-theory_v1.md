---
title: "Analytical Framework Lineage Catalogue"
id: "03-frameworks-and-theory"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Analytical Framework Lineage Catalogue
## Amplified Partners — SMB Insights Engine: Workstream 03

**Purpose:** Academically grounded reference catalogue of analytical frameworks applicable to fused SMB data (internal + public). Each entry provides origin, mechanism, data requirements, enterprise use-case, SMB adaptation, concrete example insights, limitations, and productive pairings. Closes with a master mapping table and a Death Spiral Detection Rubric.

---

## FAMILY 1: CONSTRAINT & BOTTLENECK THEORY

### 1.1 Goldratt's Theory of Constraints (TOC)

**Origin:** Eliyahu M. Goldratt, 1984. Primary texts: *The Goal* (1984, North River Press), *The Theory of Constraints* (1990), *It's Not Luck* (1994). The five focusing steps are formally described in *The Goal* via the "Herbie" narrative and systematised in Goldratt's later works.

**Core mechanism:** TOC holds that any system's performance is limited at any given moment by exactly one binding constraint. Improvement anywhere else in the system produces no net throughput gain. The five focusing steps are: (1) **Identify** the constraint — locate the single choke-point limiting output; (2) **Exploit** it — get maximum output from the constraint without capital spending; (3) **Subordinate** everything else — the constraint is the drum; all other resources must serve and pace themselves to it; (4) **Elevate** the constraint — if still binding after exploitation, increase its capacity; (5) **Repeat** — once broken, the constraint moves; do not allow inertia to become the new constraint.

The **Herbie metaphor** from *The Goal*: a boy scout troop strung out on a hike because Herbie, the slowest boy, is somewhere in the middle. The system throughput (pace of the whole troop) is determined by Herbie, not by the fastest scouts. Moving Herbie to the front and lightening his pack (exploitation + subordination) is more effective than making the fast scouts run faster.

**Drum-Buffer-Rope (DBR):** The constraint (drum) sets the production cadence. A time buffer protects the drum from starvation. The rope limits work release into the system to match what the drum can process. Buffer Management uses green/amber/red zones to signal root-cause problems before they impact the drum.

**Thinking Processes:** For complex systemic problems, Goldratt's Thinking Processes provide structured logic trees: the **Current Reality Tree** (CRT) maps undesirable effects to a root cause via "if-then" causality; the **Evaporating Cloud** (EC) resolves chronic conflicts by exposing hidden assumptions; the **Future Reality Tree** (FRT) tests whether proposed injections will produce the desired effects without creating new problems.

**Throughput Accounting (TA) vs Cost Accounting:** Cost accounting allocates labour and overhead to products — it encourages local optimisation and may recommend cutting the very resources that protect throughput. TA uses three global measures: **Throughput (T)** = revenue minus totally variable costs (materials, sales commissions); **Inventory/Investment (I)** = money tied up in the system; **Operating Expense (OE)** = all other spending. The goal is to increase T while simultaneously reducing I and OE. TA correctly identifies that a product's contribution to profit is T/constraint-unit, not the traditional margin per unit.

**Data required:** Process logs (timestamps per stage), WIP counts by station, queue lengths, throughput rates, lead times, schedule adherence, product mix data, financial: T, I, OE.

**Typical enterprise use-case:** Manufacturing plant scheduling; hospital emergency department patient flow; software sprint planning.

**SMB adaptation:** Map the value stream manually in a 2-hour workshop. Constraint will almost always be one of: (a) the founder's own time, (b) a single skilled technician or role, (c) a slow approval process, (d) working capital (cash conversion cycle acting as a financial constraint). Use simple queue-length tracking from ERP/CRM/email timestamps to identify where jobs pile up. Drum-Buffer-Rope can be implemented on a whiteboard.

**Example insights for a UK SMB:**
1. A 12-person manufacturing firm finds that 80% of late deliveries trace to a single powder-coat finisher with a 3-day queue. Subordinating cutting and welding to the coater's pace (not running ahead) reduces WIP by 40% and improves on-time delivery from 68% to 91% within six weeks — no capital required.
2. A professional services firm discovers the constraint is proposal review by the managing director; by pre-approving proposal templates (exploitation) and delegating sign-off for sub-£25k projects (elevation), revenue per month increases 22%.
3. TA analysis reveals that the firm's lowest-margin product line uses 3× the constraint time per £1 of throughput; redirecting capacity to the top-throughput product adds £8k/month net contribution — invisible under cost accounting.

**Limitations:** TOC assumes a single binding constraint, which holds most of the time but breaks in highly networked systems with multiple simultaneous near-constraints. Thinking Processes require facilitation skill. TOC is weakest in pure knowledge work where constraint identification is ambiguous. Does not handle demand variability well without Advanced DBR. Assumes goal is throughput (may conflict with other objectives such as quality or sustainability).

**Pairs with:** Little's Law (queuing mathematics confirms DBR logic), Lean/TPS (waste reduction frees constraint capacity), Statistical Process Control (distinguishes signal from noise at the constraint), DuPont Analysis (maps T/I/OE to financial ratios), Deming SoPK (systems thinking underpins TOC philosophy).

---

## FAMILY 2: DEATH SPIRAL & DECLINE DYNAMICS

### 2.1 Jim Collins — How the Mighty Fall (Five Stages of Decline)

**Origin:** Jim Collins, 2009. *How the Mighty Fall: And Why Some Companies Never Give In* (HarperBusiness, 2009). Based on four years of comparative historical analysis of paired companies.

**Core mechanism:** Collins found decline moves through five sequential stages, and critically: **Stages 1–3 are invisible from outside**. The company looks and feels great while rotting internally. Only at Stage 4 does the fall become externally visible — by which point recovery requires heroic discipline.

- **Stage 1: Hubris Born of Success** — Arrogance replaces disciplined understanding of *why* success occurred. Leaders attribute results to their own genius rather than system, luck, or disciplined execution. Rhetoric of success replaces penetrating insight.
- **Stage 2: Undisciplined Pursuit of More** — Scale, scope, and growth acceleration beyond the company's ability to staff key seats with the right people. Overreaching, not complacency, drives decline.
- **Stage 3: Denial of Risk and Peril** — Internal warning signs mount; leaders discount negative data, amplify positive signals, blame external factors. Vigorous fact-based dialogue collapses.
- **Stage 4: Grasping for Salvation** — Sharp visible decline triggers lurching for silver bullets: charismatic leader, dramatic transformation, bolt-on acquisition, game-changing product. Each expensive failure accelerates the spiral.
- **Stage 5: Capitulation to Irrelevance or Death** — Accumulated setbacks erode financial strength and morale; leaders abandon hope, sell out, or simply allow the enterprise to atrophy.

**Data required:** Employee survey sentiment trends (engagement decline is a Stage 2–3 signal); hiring velocity relative to revenue (Stage 2); decision-making speed and consensus quality; executive tenure; press release tone (positive spin of negative data); capital allocation discipline.

**Typical enterprise use-case:** Strategic risk assessment during board reviews; M&A target evaluation; leadership team diagnostics.

**SMB adaptation:** SMBs show a compressed version of the stages — a 3-year lifecycle can traverse all five. Stage 1 signal: the founder stops measuring the drivers that built success (e.g., customer referrals, delivery quality) and focuses on headline revenue. Stage 2: new product launches, geographic expansion, headcount additions that outpace operational control. Stage 3: explanations that blame external factors (Brexit, supply chain, interest rates) for deterioration that is actually internal.

**Example insights for a UK SMB:**
1. A regional haulage firm shows Stage 2/3 transition: revenue grows 30% in 18 months via new depots, but gross margin compresses from 28% to 19%, driver vacancy rate doubles, and customer complaints are attributed to "driver shortage nationally" rather than scheduling failures.
2. A retail chain in Stage 3: management reports "record Q4 revenue" while working capital cycle lengthens from 45 to 72 days and the top three sales staff have departed.
3. A professional services firm in Stage 4: third new CRM in two years, rebrand, pivot to "AI-led delivery" — none of the interventions address the core constraint (partner billability).

**Limitations:** Stage identification is subjective without quantitative signals. Collins' research is based on large public companies; SMB dynamics differ (single-owner concentration risk; personal finance entanglement). Stages are not irreversible in 1–4 but the framework offers no algorithmic precision.

**Pairs with:** Goldratt TOC (constraint thinking identifies root causes masked by Stage 3 denial); Forrester System Dynamics (reinforcing loops explain the acceleration in Stages 4–5); Altman Z'' Score (Stage 4–5 financial deterioration is quantifiable); Bradford Factor (Stage 2–3 people-stress shows in absence data).

---

### 2.2 Jay Forrester — System Dynamics & Reinforcing Feedback Loops

**Origin:** Jay Wright Forrester, MIT. *Industrial Dynamics* (1961, MIT Press); *Urban Dynamics* (1969). Forrester is the founder of the field of System Dynamics. His key insight: "People discover that their own policies inevitably generate their troubles. They keep repeating more of the very policies that create the problem in the first place. This can produce a downward spiral toward failure." (*Strategy+Business*, 2005.)

**Core mechanism:** System Dynamics models organisations as networks of stocks (accumulations), flows (rates of change), and feedback loops. **Balancing loops** resist change and stabilise systems; **reinforcing loops** amplify change in one direction — either virtuous circles or death spirals. The **Boiled Frog** archetype: a slow-building reinforcing decline loop may not trigger alarm responses because no single period's change is large enough to register as a crisis. Senge's systems archetypes (Section 8) formalise common reinforcing patterns.

**Death Spiral mechanics:**
The classic accounting doom loop: Cost pressure → cut discretionary spend (training, maintenance, marketing) → quality/delivery degrades → customers defect → revenue drops → more cost pressure → repeat. The loop reinforces itself. The critical insight is that the *intervention* (cost cutting) is also the *cause* of the next cycle of decline — this is Forrester's "fixes that fail" archetype.

**Data required:** Time-series data on multiple interlinked variables (revenue, cost, headcount, quality KPIs, customer retention, product investment). The minimum viable dataset for loop identification is 12–24 months of monthly data across 5–8 variables.

**SMB adaptation:** Build a simple Causal Loop Diagram on a whiteboard. Identify 3–5 reinforcing loops operating in the business. Quantify one loop per quarter using available data. The goal is not a full simulation model — it is loop awareness that changes managerial decisions.

**Example insights for a UK SMB:**
1. A B2B services firm cuts business development spend when a major client departs; this reduces new client flow; 6 months later, revenue is further depressed, triggering another round of cuts — the reinforcing loop is identified retrospectively and broken by maintaining BD spend as a protected cost category.
2. A restaurant identifies a reinforcing virtuous loop: chef quality → food quality → reviews → bookings → revenue → ability to pay chef market rate → chef retention. Mapping this loop makes the chef retention budget non-negotiable.

**Limitations:** Qualitative loop diagrams risk becoming storytelling rather than analysis. Full SD modelling requires specialised skills and sufficient data. Causal attribution in messy real systems is difficult. Feedback loop models can always be re-drawn to support a preferred conclusion.

**Pairs with:** Collins Five Stages (provides the narrative; Forrester provides the mechanism); Senge Archetypes (formalise common loop structures); TOC (constraints are the reinforcing loops' leverage points); Monte Carlo (quantifies the speed and probability of loop outcomes).

---

### 2.3 Clayton Christensen — Disruption Theory / Innovator's Dilemma

**Origin:** Clayton M. Christensen, Harvard Business School. *The Innovator's Dilemma: When New Technologies Cause Great Firms to Fail* (1997, Harvard Business School Press). The term "disruptive technology" was coined in a 1995 HBR article; later revised to "disruptive innovation."

**Core mechanism:** Established companies fail not because they make mistakes but because they execute correct management practices — listening to customers, investing in higher-performance products, maximising margins — that render them structurally blind to low-end disruption. Disruptive innovations enter at the low end of the market (lower performance, lower cost, inferior to incumbents' offerings) and serve over-served or non-consuming customers. Incumbents cede the low end rationally (lower margins) while disruptors improve. Eventually the disruptor's performance crosses the threshold needed by mainstream customers — at which point the incumbent's entire market is taken. The theory connects to Schumpeter's "creative destruction" (1942).

**Data required:** Market share trends by segment; customer satisfaction scores by segment; product/service tier performance metrics; new entrant price points; technology adoption curves.

**SMB adaptation:** The SMB is more often the disrupted than the disruptor. Monitor whether new low-cost competitors (often digital-first) are winning the clients the SMB considers "not worth having." Those are the clients that were the incumbent's first to lose. Track reference pricing and new entrant customer reviews.

**Example insights for a UK SMB:**
1. A traditional bookkeeping firm loses small clients to software (Xero, FreeAgent, QuickBooks). These were the firm's least profitable clients — the "rational" response is to focus upstream. But this cedes the market entry point to a competitor that will eventually serve mid-market clients with AI-augmented advisory.
2. An established print company sees digital-first competitors win jobs under £500; over three years, the digital competitors upsell to £5,000 projects; by year four, the print firm's mid-market is contested.

**Limitations:** Christensen's original framework has been criticised for post-hoc classification (almost any successful new entrant can be called "disruptive" retrospectively). The Jobs-to-be-Done framework (Christensen, later work) is more operationally useful for diagnosis.

**Pairs with:** Wardley Mapping (evolution axis explicitly models the commoditisation dynamic Christensen describes); BCG Matrix (dogs/cash cows face disruption risk before stars); Blue Ocean (disruption is one path to new market creation); Porter Five Forces (disruption is the "new entrant" force materialising).

---

### 2.4 Nassim Taleb — Fragility, Antifragility, and the Barbell Strategy

**Origin:** Nassim Nicholas Taleb. *Antifragile: Things That Gain from Disorder* (2012, Random House). Preceded by *The Black Swan* (2007) and *Fooled by Randomness* (2001). The barbell strategy is described in both *The Black Swan* and *Antifragile*.

**Core mechanism:** Taleb distinguishes three responses to volatility and disorder: **Fragile** (breaks under stress; negative convexity; large downside, small upside); **Robust** (resists stress; neither gains nor loses); **Antifragile** (gains from stress; positive convexity; small downside, large upside). A fragile SMB has high fixed costs, concentrated revenue, correlated exposures, and debt — any shock is potentially fatal. An antifragile SMB has optionality (ability to act on opportunities created by disruption), minimal debt, diversified revenue, and structures that benefit from volatility (e.g., a competitor's distress creates acquisition opportunities).

The **Barbell Strategy**: avoid the middle of risk distribution. Allocate 90% of resources to extreme safety (robust core operations, cash reserves, debt-free balance sheet) and 10% to high-upside optionality (experiments, speculative bets with capped downside). Eliminate medium-risk exposures that carry hidden tail risk. Under Jensen's inequality, a convex payoff function has a higher expected value than the expected-value equivalent under linearity.

**Convexity heuristic for SMBs:** Favour strategies where "if I'm wrong, I lose a little; if I'm right, I gain a lot." Avoid strategies where "if I'm right, I gain a little; if I'm wrong, I lose everything." Long-term leases, single-supplier dependencies, and concentrated customer bases are concave (fragile) exposures.

**Data required:** Revenue concentration (Herfindahl-Hirschman Index applied to clients); supplier concentration; fixed-to-variable cost ratio; net debt position; cash runway; optionality inventory (pilot projects, partnerships in development).

**SMB adaptation:** Calculate the SMB's fragility score: what % of revenue would disappear if the top 3 clients simultaneously departed? What is fixed cost coverage at 70% of current revenue? What debt matures within 12 months? These are the barbell's "fragile middle."

**Example insights for a UK SMB:**
1. An SMB with 65% of revenue from two clients and a 12-month lease renewal due is deeply fragile. Barbell prescription: accelerate client diversification (new client acquisition investment as "option") while maintaining a 3-month cash buffer (safety).
2. A manufacturing SMB deliberately maintains one experimental product line at 5% of revenue — a small, capped experiment. In a recession, one of these options becomes the growth engine because competitors have cut all experimental activity.

**Limitations:** The barbell strategy may forgo significant near-term profitability. "Antifragile" can become a rationalisation for avoiding systematic risk management. Taleb's framework is philosophical rather than quantitative — it provides heuristics, not algorithms.

**Pairs with:** Monte Carlo cashflow stress testing (quantifies fragility); Altman Z'' (measures current fragility level); Collins Stages (antifragility is the structural answer to Stage 1 hubris); Forrester (reinforcing loops in fragile systems are especially dangerous).

---

## FAMILY 3: FINANCIAL HEALTH & DISTRESS MODELS

### 3.1 Altman Z-Score (1968) — Z', Z'' for Private/Non-Manufacturing Firms

**Origin:** Edward I. Altman, New York University. Published in *Journal of Finance*, 22(4), 1968: "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy." Z' (private firms) and Z'' (non-manufacturing/emerging markets) revised versions published in Altman, Hartzell & Peck (1995) and Altman (2000, 2013).

**Core mechanism:** Multiple discriminant analysis applied to five financial ratios, weighted by empirically derived coefficients, produces a single score predicting bankruptcy probability within two years. The original public-company formula: Z = 1.2X₁ + 1.4X₂ + 3.3X₃ + 0.6X₄ + 1.0X₅, where X₁=Working Capital/Total Assets; X₂=Retained Earnings/Total Assets; X₃=EBIT/Total Assets; X₄=Market Cap/Total Liabilities; X₅=Sales/Total Assets. Zones: Z > 2.99 (safe); 1.81–2.99 (grey); < 1.81 (distress).

**Z' Score (private UK firms):** Substitutes book value of equity for market cap in X₄. Formula: Z' = 0.717X₁ + 0.847X₂ + 3.107X₃ + 0.420X₄ + 0.998X₅. Safe zone: Z' > 2.9; grey: 1.23–2.9; distress: Z' < 1.23.

**Z'' Score (non-manufacturing/services — most relevant for UK SMBs):** Drops the sales/assets ratio (to avoid industry bias) and uses book equity. Z'' = 6.56X₁ + 3.26X₂ + 6.72X₃ + 1.05X₄. Safe: Z'' > 2.6; grey: 1.1–2.6; distress: Z'' < 1.1.

**UK-specific note:** UK SMBs are predominantly unlisted service businesses. The Z'' score is the correct variant. HMRC regained secondary preferential creditor status (December 2020, CIGA 2020) for VAT and PAYE ahead of floating charge holders — this changes the liquidation recovery calculus. UK insolvency routes: **CVL** (Creditors' Voluntary Liquidation, most common); **CVA** (Creditors' Voluntary Arrangement — repayment plan, requires 75% creditor approval); **Administration** (moratorium while an insolvency practitioner seeks going concern sale or CVA). HMRC's elevated status makes large tax liabilities particularly dangerous to Z'' scores.

**Data required:** Current assets, current liabilities, total assets, retained earnings, EBIT, total liabilities, book equity, net sales.

**SMB adaptation:** All inputs computable from Companies House filings or management accounts. Run quarterly. Track trend rather than absolute level — a score declining from 3.2 to 2.1 over 18 months is more alarming than a static 2.1.

**Example insights for a UK SMB:**
1. A construction subcontractor's Z'' declines from 2.8 to 0.9 over two years as retained earnings are distributed as dividends (reducing X₂) and a bad debt erodes working capital (reducing X₁). Early warning triggers a cash conversation six months before a banking covenant breach.
2. An e-commerce retailer sees Z'' spike to 4.1 in a strong trading year; the score is used to negotiate better trade credit terms with suppliers.
3. Peer-benchmarking five regional competitors from Companies House data reveals two are in Z'' grey zone — potential acquisition targets or capacity-to-take clients.

**Limitations:** Altman trained on US manufacturing data; UK service-sector SMBs may require recalibration. Sensitive to accounting policy choices (capitalised vs expensed items). Does not distinguish between cyclical distress and structural failure. The "grey zone" covers a wide range of outcomes — 30–50% of grey-zone firms fail within two years. Accuracy ≈70–75% for 2-year prediction.

**Pairs with:** Ohlson O-Score (logistic regression complement — different statistical approach); Piotroski F-Score (health improvement tracking); DuPont (decomposes the drivers of X₃); Cash Conversion Cycle (X₁ movements often trace to CCC deterioration).

---

### 3.2 Ohlson O-Score (1980)

**Origin:** James Ohlson, New York University Stern School of Business. Published in *Journal of Accounting Research*, 18(1), 1980: "Financial Ratios and the Probabilistic Prediction of Bankruptcy."

**Core mechanism:** Unlike Altman's discriminant analysis, Ohlson uses logistic regression on a dataset of >2,000 companies (vs Altman's 66). Produces a probability of bankruptcy within two years. Nine inputs including firm size (log total assets), leverage, working capital ratio, current ratio, a binary indicator for recent loss, EBITDA-to-liabilities. If O-score probability > 0.5, bankruptcy is predicted. Higher accuracy than original Z-score; lower Type I error rate (false non-distress predictions).

**Data required:** Balance sheet and income statement. Same inputs as Altman plus current ratio separately and an indicator for net loss in prior two years.

**SMB adaptation:** Run alongside Z'' as a cross-check. When Z'' and O-Score diverge, investigate the cause — divergence often reveals industry-specific ratio distortions.

**Limitations:** Trained on 1970 US data; requires recalibration for UK SMBs. The probability output implies precision that the underlying model accuracy (better than Z-score but not definitive) does not fully warrant.

**Pairs with:** Altman Z''; Zmijewski (1984) — three-variable probit model (net income/total assets, liabilities/total assets, current assets/current liabilities); Beaver (1966) univariate model (pioneered single-ratio analysis of failure, particularly cash flow/total debt).

---

### 3.3 Piotroski F-Score (2000)

**Origin:** Joseph Piotroski, University of Chicago. Published in *Journal of Accounting Research*, 38(Supplement), 2000: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers."

**Core mechanism:** A 0–9 integer score across three dimensions: **Profitability** (4 signals: ROA positive; operating cash flow positive; ROA improving YoY; cash flow > net income indicating earnings quality); **Financial Strength/Leverage** (3 signals: debt ratio declining; current ratio improving; no dilutive equity issuance); **Operating Efficiency** (2 signals: gross margin improving; asset turnover improving). Score 8–9: strong, improving fundamentals. Score 0–2: financial distress.

**Data required:** Two years of balance sheet and P&L. All inputs computable from Companies House filings.

**SMB adaptation:** Run annually as a simple internal health check. The nine binary signals are directionally unambiguous and require minimal financial sophistication. Use it as a board reporting scorecard.

**Example insights:** An SMB scores F=8 while its Altman Z'' is in the grey zone: the trajectory is improving — this business is recovering, not failing. Conversely, an F=3 score with Z''=3.5 suggests deterioration from a currently healthy position — early warning.

**Pairs with:** Altman Z''; DuPont Analysis (decomposes F-score profitability signals into drivers); Cash Conversion Cycle (efficiency signals trace to CCC components).

---

### 3.4 DuPont Analysis

**Origin:** DuPont Corporation internal management tool, 1920s. Formalised in finance literature. Three-factor model: ROE = Net Profit Margin × Asset Turnover × Equity Multiplier. Five-factor extension adds Tax Burden and Interest Burden.

**Core mechanism:** ROE = (Net Income/Revenue) × (Revenue/Average Total Assets) × (Average Total Assets/Average Shareholders' Equity). This decomposition reveals *how* ROE is generated: is it margin-driven (pricing power), efficiency-driven (asset utilisation), or leverage-driven (debt amplification)? High ROE powered by high leverage is structurally fragile; high ROE from margin and turnover is sustainable.

**SMB adaptation:** UK SMBs with negative equity (common after COVID bounce-back loans) cannot use the equity multiplier cleanly. Focus on the first two factors: gross margin trend and revenue/assets as a proxy for operational efficiency.

**Example insights:** A UK distributor with flat ROE is disguising margin compression (Net Margin declining from 4.2% to 2.9%) offset by higher leverage — the business is borrowing to maintain apparent returns while fundamental competitiveness is eroding.

**Pairs with:** Piotroski F-Score (asset turnover improvement is an F-Score signal); TOC (margin compression often traces to throughput constraint); Altman Z'' (leverage component feeds Z'' calculation).

---

### 3.5 Cash Conversion Cycle (CCC)

**Origin:** Lawrence J. Gitman, *Principles of Managerial Finance* (1974). CCC = Days Sales Outstanding (DSO) + Days Inventory Outstanding (DIO) − Days Payable Outstanding (DPO).

**Core mechanism:** The CCC measures the number of days cash is tied up in the operating cycle. A longer CCC = more working capital required = greater financing risk. Negative CCC (e.g., supermarkets: paid by customers before paying suppliers) is a cash generation advantage. Deteriorating CCC is an early warning of liquidity stress.

**SMB adaptation:** Compute monthly. DSO trend is the fastest signal: rising DSO means customers are paying slower (credit quality deteriorating, or collections processes failing). Pair with HMRC payment history data and CCJ filings for supplier-side validation.

**Pairs with:** Altman Z'' (X₁ working capital ratio is downstream of CCC); Little's Law (operational CCC is a queuing problem); TOC (CCC is the financial expression of inventory in the constraint).

---

## FAMILY 4: STRATEGIC FRAMEWORKS

### 4.1 Porter Five Forces (1979)

**Origin:** Michael E. Porter, Harvard Business School. Published in *Harvard Business Review*, March–April 1979: "How Competitive Forces Shape Strategy." Expanded in *Competitive Strategy* (1980, Free Press).

**Core mechanism:** Industry profitability is determined by the combined intensity of five structural forces: (1) **Rivalry among existing competitors**; (2) **Threat of new entrants** (entry barriers: scale economies, switching costs, capital requirements, incumbency advantages); (3) **Bargaining power of suppliers** (concentration, switching costs, substitute inputs); (4) **Bargaining power of buyers** (concentration, price sensitivity, switching costs); (5) **Threat of substitute products/services**. The five-forces model reveals where value is captured and lost — and therefore where competitive strategy must be positioned.

**SMB adaptation:** A Five Forces canvas is achievable in a half-day workshop. For fused data analysis: use Companies House data to map competitor entry/exit trends (rivalry + new entrants); use supplier invoicing data to calculate supplier HHI (concentration); use customer revenue concentration to measure buyer power.

**Example insights:** A UK IT services firm discovers that buyer power is extreme (top 5 clients = 78% of revenue; switching cost = zero) while rivalry is intensifying. The strategic prescription is clearly differentiation + stickiness investment, not price competition.

**Pairs with:** Porter Value Chain (identifies *where* in the chain each force exerts pressure); Blue Ocean (when all five forces are unattractive, create new market space); Wardley Mapping (evolution dynamics change force intensity over time).

---

### 4.2 Porter Value Chain & Generic Strategies

**Origin:** Michael E. Porter, *Competitive Advantage: Creating and Sustaining Superior Performance* (1985, Free Press).

**Core mechanism:** The Value Chain disaggregates primary activities (inbound logistics, operations, outbound logistics, marketing & sales, service) and support activities (firm infrastructure, HR, technology development, procurement). Competitive advantage is found in specific value chain activities where a firm can perform distinctively. **Generic Strategies**: Cost Leadership (lowest cost structure in the industry), Differentiation (unique value perceived by buyers), Focus (cost focus or differentiation focus within a narrow segment). Stuck in the middle — attempting both without commitment — is Porter's warning for most SMBs.

**SMB adaptation:** For UK SMBs, Cost Leadership is rarely viable (scale disadvantage vs large players). Differentiation Focus (deep niche expertise, relationship service model, sector-specific compliance knowledge) is the naturally defensible position.

**Pairs with:** Wardley Mapping (value chain activities are the anchors on the map); Kano Model (differentiation must be built on Attractive, not just Must-Be, features).

---

### 4.3 Blue Ocean Strategy

**Origin:** W. Chan Kim and Renée Mauborgne, INSEAD. *Blue Ocean Strategy* (2005, Harvard Business School Press). Built on Kim & Mauborgne's HBR research from the 1990s.

**Core mechanism:** Red Ocean = existing competitive space; Blue Ocean = uncontested market space created by redefining the value proposition. The Four Actions Framework: **Eliminate** (factors the industry takes for granted that add cost but no value); **Reduce** (factors below industry standard); **Raise** (above industry standard); **Create** (factors never offered). The Strategy Canvas visualises the current value curve vs the new offering. Blue Ocean is achieved when the new curve diverges significantly from incumbents' curves.

**SMB adaptation:** The Four Actions Framework applied to an SMB's service or product catalogue costs nothing to perform. It surfaces assumptions baked into "how we do things" that may be unnecessary — a common source of margin improvement.

**Example insight:** A UK accountancy practice applies Four Actions: Eliminate (monthly paper reporting); Reduce (face-to-face meetings); Raise (proactive tax planning alerts); Create (integrated payroll/HR advisory bundled with accounts). The new value curve attracts a different client segment at 40% higher fees.

---

### 4.4 BCG Growth-Share Matrix

**Origin:** Boston Consulting Group, c.1970. Developed by Bruce Henderson. Popularised in *The Product Portfolio* (BCG, 1970). Formalised in Henderson's articles through the 1970s.

**Core mechanism:** Two-axis portfolio matrix: market growth rate (vertical) vs relative market share (horizontal). Four quadrants: **Stars** (high share, high growth — require investment); **Cash Cows** (high share, low growth — generate cash); **Question Marks/Problem Children** (low share, high growth — require cash, uncertain future); **Dogs** (low share, low growth — candidates for divestment). The logic derives from the experience curve: high relative share → low relative cost → cash generation.

**SMB adaptation:** For a UK SMB with multiple service lines or client segments, map each segment as a "business unit." Replace "market share" with revenue rank vs identifiable competitors. Use as a strategic portfolio conversation tool.

**Limitations:** Market share data for SMBs is often unavailable. The matrix ignores competitive dynamics outside the share/growth dimensions. Industry boundaries are often ambiguous for SMBs.

**Pairs with:** Porter Five Forces (growth rate is influenced by force intensity); Ansoff Matrix (Question Marks may require market development or diversification).

---

### 4.5 Ansoff Matrix

**Origin:** Igor Ansoff, *Harvard Business Review*, 1957: "Strategies for Diversification."

**Core mechanism:** 2×2 matrix of product (existing/new) vs market (existing/new). **Market Penetration** (existing product, existing market — least risk); **Market Development** (existing product, new market); **Product Development** (new product, existing market); **Diversification** (new product, new market — highest risk). Risk increases as distance from current capabilities increases.

**SMB adaptation:** Use as a deliberate growth choice framing tool. Most SMBs default to Market Penetration by inertia; explicit discussion of Market Development or Product Development prevents strategic drift.

---

### 4.6 Wardley Mapping

**Origin:** Simon Wardley. Developed at Fotango, 2005; the evolution framing established 2004; further developed at Canonical UK, 2008–2010. First widely available via Wardley's blog and presentations (2016 onwards). Primary reference: Wardley, S. (2016). *Wardley Maps* (self-published, available via Medium/blog). **Highly underused at SMB scale.**

**Core mechanism:** A Wardley Map has two axes: the Y-axis represents the value chain (user-visible needs at top; invisible infrastructure at bottom); the X-axis represents the evolutionary stage of each component: **Genesis** (novel, unique, poorly understood) → **Custom Built** (emerging, scarce) → **Product** (competitive, well-understood) → **Commodity** (utility, standardised). The core insight: **everything evolves from left to right** under supply/demand competition. Competitive advantage decays as components commoditise. What was once a differentiator becomes expected infrastructure.

Strategic moves that follow from maps: **Pioneer-Settler-Town Planner** (different organisational modes for Genesis, Custom Built, and Commodity components); **Climatic Patterns** (predictable consequences of evolution, e.g., "everything commoditises eventually," "a component's commoditisation enables new higher-order Genesis opportunities"); **Inertia Identification** (practices that made sense for a component in Product stage become liabilities once it commoditises — the SMB equivalent of the Innovator's Dilemma).

**Data required:** Qualitative: understanding of what customers need, and what internal capabilities/dependencies exist. Can be enriched with supplier spend data, technology stack audit, and time-to-deliver metrics by capability.

**SMB adaptation:** A Wardley Map session for a UK SMB requires 3–4 hours and surfaces: (a) which capabilities the SMB is custom-building when commodity alternatives exist (cost efficiency opportunity); (b) which components are in early Genesis where the SMB could build a genuine differentiator; (c) which capabilities the SMB currently treats as differentiators but are in Product/Commodity stage (therefore: poor competitive defence).

**Example insights for a UK SMB:**
1. A professional services firm is custom-building its client onboarding workflow (8 custom forms, bespoke SharePoint) — this is Commodity territory; transition to a standard platform reduces admin cost by £18k/year while the freed capacity is redeployed to Genesis-stage client analytics.
2. A manufacturing SMB discovers that its ERP customisations (treating as Custom Built differentiators) are hampering system upgrades — they should be Product/Commodity; standardising enables scale.
3. A legal SMB maps precedent management as Genesis/Custom Built — a real source of expertise — but template production as Commodity; AI tooling for templates is the right Commodity play, freeing fee-earner time for high-value advisory.

**Limitations:** Wardley Mapping requires practitioner skill to avoid subjective component placement. Maps become outdated rapidly (evolution continues). No formal algorithmic output — insight depends on the quality of the mapping conversation.

**Pairs with:** TOC (the map identifies where constraints are likely to appear as components mature); Porter Five Forces (evolution changes force intensity — a Commodity component has high buyer power, low threat of new entrants from incumbents); Christensen Disruption (Genesis components of today are the disruptive threats of tomorrow).

---

## FAMILY 5: CUSTOMER & UNIT ECONOMICS

### 5.1 LTV:CAC Ratio & Cohort Retention

**Origin:** LTV:CAC as a business metric was popularised in the SaaS/VC ecosystem through the 2000s–2010s. The "3:1 ideal" is conventionally attributed to David Skok (*For Entrepreneurs* blog). **Fader & Hardie** (Peter Fader, Bruce Hardie, Wharton) formalised probabilistic CLV models: the **Pareto/NBD model** (Schmittlein, Morrison, Colombo, 1987, *Management Science*) for non-contractual settings; the **BG/NBD model** (Fader, Hardie, Lee, 2005, *Marketing Science*) for discrete-time contractual/subscription settings.

**Core mechanism:** LTV = ARPU × Gross Margin ÷ Churn Rate (simple approximation). More rigourously: LTV is the discounted expected gross margin from a customer over their predicted lifetime, estimated from cohort retention curves. The LTV:CAC ratio targets 3:1 as the threshold for sustainable growth economics. CAC Payback Period = CAC ÷ (Monthly Revenue × Gross Margin %); target under 12 months.

**Cohort analysis:** Group customers by acquisition period (e.g., monthly cohort). Track retention for each cohort over time. The key finding from Fader & Hardie's research: aggregate retention rates almost always *increase* over time due to heterogeneity (high-churn customers leave early; the surviving cohort is progressively selected for loyalty). This means naive "average churn rate" underestimates long-term retention of loyal customers and overestimates expected revenue.

**BG/NBD model significance for SMBs:** Decomposes customer-level transactions into a "buy" process and a "die" (defect) process, each following distinct distributions. Outputs: (a) predicted future purchase frequency per customer; (b) probability that each customer is still "alive" (i.e., not defected). With 12+ months of transaction history, a UK SMB can score every customer.

**Pareto principle note:** The classic "20% of customers = 80% of revenue" *overestimates* concentration. Ehrenberg-Bass research shows that in most consumer categories, the top 20% of buyers generates ~60% of sales — still substantial concentration, but less extreme than mythology suggests.

**Data required (for basic cohort analysis):** Transaction records with customer ID, date, value. Minimum 12 months; 24 months for meaningful LTV projection.

**SMB adaptation:** Run cohort retention tables monthly. Identify the "cliff cohort" — the acquisition period after which retention dramatically worsened (product quality change? pricing change? different channel?). Track LTV by acquisition channel to identify which channels generate loyal vs transactional customers.

**Example insights:**
1. A UK SaaS firm discovers that customers acquired via paid ads have 3× higher churn in month 6 than customers acquired via referral — the LTV:CAC ratio for paid ads is 1.4:1 (destroying value) vs 6:1 for referrals. Budget reallocation follows.
2. A B2B firm identifies that 12 customers acquired in 2021 have made 0 purchases in 18 months — BG/NBD scoring shows these customers have a 94% probability of having defected. Winback campaign targeting avoids wasted broad reactivation spend.

**Limitations:** LTV projections are sensitive to assumed churn rates and discount rates — small errors compound dramatically over a 3-year horizon. The 3:1 benchmark applies to SaaS; for low-margin retail, 1.5:1 may be viable. LTV:CAC ratio ignores payback period and cash flow timing.

**Pairs with:** Kaplan-Meier survival analysis (models customer lifetime duration directly); AARRR (funnel stages map to LTV drivers); Kano Model (feature prioritisation based on which features drive the highest-LTV customer retention).

---

### 5.2 Kano Model

**Origin:** Noriaki Kano, *Attractive Quality and Must-Be Quality* (1984, *Journal of the Japanese Society for Quality Control*). Published with Seraku, Takahashi, and Tsuji.

**Core mechanism:** Customer satisfaction is not a linear function of feature quality. Features fall into five categories: **Must-Be** (threshold requirements; absence causes dissatisfaction; presence causes neutrality — hygiene factors); **Performance** (one-directional; more = better satisfaction); **Attractive/Delighters** (unexpected; presence causes delight; absence causes no dissatisfaction but absence of delight); **Indifferent** (customers don't care); **Reverse** (presence causes dissatisfaction for some segments). Over time, Attractive features degrade to Performance and eventually Must-Be — a product's WOW factor today becomes tomorrow's baseline expectation.

**SMB adaptation:** A Kano survey on 20–30 customers can be conducted in under two weeks. Test 10–15 features with positive and negative question pairs. Cluster into quadrants. Prioritise Attractive features for investment; ensure Must-Be quality is non-negotiable; deprioritise Indifferent features.

**Pairs with:** Jobs-to-be-Done (JTBD discovers the underlying need; Kano classifies the feature response); LTV:CAC (Attractive features explain which cohorts retain at higher rates); Porter Generic Strategies (Attractive features are the substance of differentiation strategy).

---

### 5.3 Jobs-to-be-Done (JTBD)

**Origin:** Clayton Christensen, Tony Ulwick. Christensen popularised the concept in *The Innovator's Dilemma* context and later explicitly in *Competing Against Luck* (2016, HarperBusiness). Ulwick developed the *Outcome-Driven Innovation* framework.

**Core mechanism:** Customers don't buy products — they "hire" them to do a job. Understanding the functional, emotional, and social dimensions of that job reveals why customers switch, what causes dissatisfaction, and where new solutions can be designed. The famous milkshake example: milkshakes sold in the morning were "hired" to make a commute less boring — a completely different job than the milkshake sold to a family at lunchtime.

**SMB adaptation:** Conduct 5–10 "switch interviews" (customers who recently chose you or switched away). Ask: "What was going on in your life when you decided to look for a solution?" The "job" language redirects product/service design from feature lists to outcome delivery.

**Pairs with:** Kano Model (JTBD identifies the job; Kano classifies how well different features serve it); Blue Ocean (creating new market space requires understanding unarticulated jobs); Value Chain (align primary activities to JTBD execution).

---

## FAMILY 6: OPERATIONAL EXCELLENCE

### 6.1 Deming — PDCA, System of Profound Knowledge (SoPK), 14 Points

**Origin:** W. Edwards Deming. *Out of the Crisis* (1982/1986, MIT CAES). The SoPK is presented in *The New Economics for Industry, Government, Education* (1993, MIT CAES). The PDCA (Plan-Do-Check-Act) cycle is built on Shewhart's PDSA (Plan-Do-Study-Act). Deming's contribution to Japan's post-war industrial recovery is the foundation of modern quality management.

**Core mechanism:** The **System of Profound Knowledge** has four inter-related components: (1) **Appreciation for a System** (understanding how parts interact; sub-optimisation of parts destroys the whole); (2) **Knowledge of Variation** (distinguishing common cause from special cause variation — critical for correct managerial response); (3) **Theory of Knowledge** (prediction and learning); (4) **Psychology** (intrinsic motivation; management by objectives destroys systems). The **14 Points** include: create constancy of purpose; cease dependence on inspection; end price-tag-based supplier selection; break down departmental barriers; eliminate management by numerical objectives.

**SMB adaptation:** The most operationally powerful insight: **never react to common cause variation as if it were special cause**. Firing a salesperson for a bad month when the variation is within natural process limits (common cause) demoralises; only special cause variation (outside control limits) warrants specific investigation.

**Pairs with:** Statistical Process Control (operationalises variation knowledge); TOC (constraint exploitation requires understanding variation in the constraint); Kahneman System 1/2 (common-vs-special cause confusion is System 1 thinking applied to data).

---

### 6.2 Statistical Process Control (SPC) — Shewhart Control Charts, XmR

**Origin:** Walter A. Shewhart, Bell Telephone Laboratories. *Economic Control of Quality of Manufactured Product* (1931, Van Nostrand). The XmR (Individuals and Moving Range) chart for non-manufacturing use was substantially developed by Don Wheeler (*Understanding Variation*, 1993, SPC Press).

**Core mechanism:** Control charts plot a metric over time with three lines: the process mean; the Upper Control Limit (UCL = mean + 3σ); the Lower Control Limit (LCL = mean − 3σ). Points within control limits = **common cause variation** (inherent in the process; improvement requires changing the process, not reacting to individual data points). Points outside control limits or exhibiting non-random patterns = **special cause variation** (an assignable external cause; warrants specific investigation). The XmR chart is the default for business metrics (monthly revenue, customer complaints, delivery times) where subgroups are not applicable.

**SMB adaptation:** Apply XmR charts to 5–8 key business metrics on a rolling 24-month basis. Common business metrics suitable for XmR: monthly revenue, gross margin %, customer complaint rate, employee absenteeism rate, average invoice payment days, project delivery lead time.

**Example insights:**
1. A UK services firm's monthly revenue has UCL = £312k and LCL = £198k. A month at £189k is a special cause signal requiring investigation — not the normal "sales went quiet" explanation. A month at £285k within limits does not warrant a celebration or a management debrief.
2. Gross margin control chart detects an assignable special cause (a specific subcontractor causing consistent cost overruns) that would have been invisible in aggregate average analysis.

**Limitations:** Requires at least 20 data points for reliable control limit calculation. Monthly SMB data produces limits after ~2 years. Assumes approximate normality of the underlying process.

**Pairs with:** Deming SoPK (the philosophical foundation); TOC (control charts at the constraint are particularly valuable); Anomaly detection algorithms (SPC is the statistical underpinning of automated changepoint detection).

---

### 6.3 Lean / Toyota Production System (TPS)

**Origin:** Taiichi Ohno, Toyota Motor Corporation, 1950s–1970s. *Toyota Production System* (Ohno, 1978, translated 1988). Term "Lean" coined by Womack, Jones, Roos in *The Machine that Changed the World* (1990, Rawson Associates).

**Core mechanism:** The TPS rests on two pillars: **Just-in-Time** (JIT — produce what is needed, when needed, in the amount needed) and **Jidoka** (automation with human intelligence; stop the line when defects occur). The **7 Wastes (Muda)**: Overproduction, Waiting, Transportation, Over-processing, Inventory, Motion, Defects (TIMWOOD). **Mura** (unevenness in demand or process) and **Muri** (overburden of people and equipment) are the causes; Muda is the symptom. **A3 Thinking**: single-page structured problem-solving (context, current situation, root cause analysis, target condition, countermeasures, follow-up).

**Little's Law in Lean:** L = λW (average WIP = throughput rate × average cycle time). To reduce lead time (W) without increasing WIP (L), reduce batch sizes and WIP limits. This is the mathematical basis of Kanban.

**SMB adaptation:** The 7 Wastes audit takes 2 hours and surfaces typically 15–30% of time/cost that is non-value-adding. For a 10-person service firm, this is usually 3–4 FTEs of wasted capacity.

**Pairs with:** TOC (Lean reduces waste at all points; TOC ensures waste reduction is focused on the constraint first); SPC (Lean standardises processes; SPC monitors them for variation); Deming 14 Points (philosophical alignment).

---

### 6.4 Little's Law & Queueing Theory (Erlang C)

**Origin:** John D.C. Little (MIT). Proof published 1961: *Operations Research*, 9(3), "A Proof for the Queuing Formula: L = λW." **Erlang C**: A.K. Erlang, Danish mathematician, 1909–1917. Erlang C formula calculates the probability that an arriving call/customer must wait, given traffic intensity and number of servers.

**Core mechanism:** L = λW. In any stable queueing system: average number in system = average arrival rate × average time in system. Key implication: **the only way to reduce lead time without reducing throughput is to reduce WIP.** At utilisation rates approaching 100%, queue length and wait time grow exponentially — the classic "hockey stick" — which is why SMBs operating at 90%+ capacity are perpetually firefighting.

**Erlang C for SMB phone/contact centres:** Given call arrival rate (λ), average handling time, and number of agents, Erlang C calculates the probability of a caller waiting and expected wait time. Directly actionable for SMBs with inbound call handling.

**Pairs with:** TOC (Little's Law explains why exploiting the constraint is more effective than adding WIP before it); Lean (WIP reduction is the practical implementation); SPC (queue length control charts detect special cause overloads).

---

## FAMILY 7: DECISION SCIENCE & BEHAVIOURAL FRAMEWORKS

### 7.1 Dalio Believability-Weighted Decision-Making

**Origin:** Ray Dalio. *Principles: Life and Work* (2017, Simon & Schuster). Implemented at Bridgewater Associates through the "Dot Collector" system and operating procedures.

**Core mechanism:** Not all opinions are equal. A **believable person** on a given topic has a demonstrated track record of success and can explain the causal reasoning behind their views. For consequential decisions, weight opinions by believability rather than treating all views equally. Believability is domain-specific: the best salesperson is not necessarily the most believable voice on operations. In practice: identify the 2–3 most believable people on the specific decision; synthesise their views; if you disagree with their consensus, ask yourself whether you have sufficient demonstrated credibility to override. The "two-by-two" test: if you're not in the top 10–20% of people qualified to make this decision, you should default to the believable consensus.

**SMB adaptation:** Explicitly label decisions as "believability-weighted consultative" vs "single-decision-maker." For hiring decisions: the most believable voice is the person who has hired and managed the most similar roles successfully. For pricing decisions: the person with the most evidence of customer price elasticity understanding.

**Pairs with:** Tetlock Superforecasting (Brier scores provide empirical believability measurement over time); Bayesian Updating (the mechanism by which beliefs update); Kahneman System 1/2 (believability weighting counters in-group social conformity, a System 1 bias).

---

### 7.2 Kahneman — System 1/System 2, Prospect Theory

**Origin:** Daniel Kahneman & Amos Tversky. Prospect Theory published in *Econometrica*, 47(2), 1979. *Thinking, Fast and Slow* (2011, Farrar, Straus and Giroux). Nobel Prize in Economics (Kahneman, 2002).

**Core mechanism:** System 1 = fast, automatic, pattern-matching, heuristic-driven. System 2 = slow, effortful, analytical. Most business decisions are made by System 1. **Prospect Theory**: losses loom larger than equivalent gains (loss aversion ≈2:1 ratio). The **value function** is concave in gains (diminishing marginal value) and convex in losses (escalating marginal disutility). Key biases relevant to SMB decisions: **anchoring** (first price offered anchors all subsequent negotiation); **availability heuristic** (recent vivid examples distort probability assessment); **sunk cost fallacy** (continuing bad projects due to past investment).

**SMB adaptation:** Pre-mortem: before a major decision, assume it failed spectacularly. What went wrong? This activates System 2 thinking about downside scenarios. Reference class forecasting: replace inside-view ("our plan is unique") with base rates ("how often do similar SMBs in our sector succeed at this initiative?").

**Pairs with:** Dalio Believability (counters social confirmation bias); Tetlock Superforecasting (base rates are the cure for availability bias); Monte Carlo (quantifies what System 1 incorrectly estimates as negligible tail risk).

---

### 7.3 Tetlock Superforecasting & Brier Scores

**Origin:** Philip Tetlock. *Superforecasting: The Art and Science of Prediction* (2015, Crown Publishers). Based on the Good Judgment Project (IARPA), 2011–2015.

**Core mechanism:** Superforecasters achieve calibrated probabilistic predictions that dramatically outperform domain experts. Core practices: use base rates before adjusting for inside information; update Bayesian-style when new evidence arrives; express predictions as precise probabilities (not "likely" or "possible"); track accuracy using **Brier Scores** (mean squared error of probability predictions vs outcomes; 0 = perfect, 2 = perfectly wrong, 0.5 = equivalent to coin-flip). Superforecasters are intellectually humble, actively seek disconfirming evidence, and treat their beliefs as hypotheses.

**SMB adaptation:** Apply to high-stakes predictions: "What is the probability our largest client renews within 6 months?" "What is the probability the product expansion breaks even within 12 months?" Record and score quarterly. This creates an empirical believability database (who in the team is well-calibrated?) and improves future forecasting discipline.

**Pairs with:** Bayesian Updating (the formal mechanism underlying superforecasting); Dalio Believability (Brier scores provide objective believability measurement); Monte Carlo (superforecasting inputs feed probability distributions).

---

### 7.4 Bayesian Updating

**Origin:** Thomas Bayes (posthumous, 1763). Pierre-Simon Laplace formalised Bayesian inference in the early 19th century. Modern business application developed through the 20th century.

**Core mechanism:** P(H|E) = P(E|H) × P(H) / P(E). Prior belief × likelihood of evidence given hypothesis = posterior belief. In practice: start with a base rate (prior); when new evidence arrives, update the probability proportionally to how much more likely the evidence is under the hypothesis vs the base rate. Bayesian updating is the mathematically correct mechanism for rational belief revision.

**SMB adaptation:** Explicit Bayesian reasoning prevents two common errors: (a) "this evidence confirms what I believed" (insufficient update; confirmation bias); (b) "this single data point changes everything" (excessive update; failing to weight base rates). For example: one strong sales month should update the annual revenue forecast by the ratio of its informativeness, not be treated as a trend change.

**Pairs with:** Superforecasting (the conceptual framework); Granger causality / Bayesian Networks (formal analytical implementation); SPC (common-vs-special cause is a Bayesian question: does this data point change my estimate of the process mean?).

---

## FAMILY 8: ADVANCED PATTERN-FINDING

### 8.1 Don Swanson — Literature-Based Discovery (LBD) / ABC Model

**Origin:** Don R. Swanson, University of Chicago Graduate Library School. Published in *Perspectives in Biology and Medicine*, 30(1), 1986: "Fish oil, Raynaud's syndrome, and undiscovered public knowledge." The term "Swanson Linking" was proposed in 2003.

**Core mechanism:** The ABC model identifies knowledge that is implicit in existing published evidence but has never been connected. A → B (e.g., fish oil reduces blood viscosity) and B → C (abnormal blood viscosity is associated with Raynaud's syndrome) exist in separate, non-overlapping literatures. The A → C connection (fish oil might benefit Raynaud's patients) is therefore inferable but undiscovered. Key prerequisite: A and C must have no pre-existing published connection (the AC intersection test).

**Applied to SMB data fusion:** Replace "published literature" with data streams. If a pattern in internal operational data (A → B) has a known statistical relationship documented elsewhere (B → C), the A → C connection may be an undiscovered actionable insight. Example: internal data shows that clients whose onboarding takes >14 days have higher invoice query rates (A → B). Research shows that invoice query rates predict 6-month churn with 70% accuracy (B → C). Therefore: slow onboarding predicts 6-month churn (A → C) — a hypothesis that can be tested and actioned immediately.

**SMB adaptation:** The "Pudding technique" Ewan uses is exactly this: systematically mining for bridging variables (B factors) between observable internal signals and known outcomes. The discipline is to require that A-B and B-C relationships both have documented evidence (not assumed) before acting on the A-C hypothesis.

**Pairs with:** Bayesian Networks (provides the formal causal inference framework); Granger Causality (tests temporal precedence of A on C); Process Mining (identifies A patterns in event logs).

---

### 8.2 Process Mining

**Origin:** Wil van der Aalst, Eindhoven University of Technology (now RWTH Aachen). *Process Mining: Discovery, Conformance and Enhancement of Business Processes* (2011, Springer). The alpha algorithm published ~2004; the heuristics miner refined for noisy logs.

**Core mechanism:** Process mining extracts process models from **event logs** (records of timestamped activities for cases: customer IDs, job tickets, invoices). Three types: (1) **Process Discovery** — automatically learns the actual as-executed process model from event data, without prior model; (2) **Conformance Checking** — compares the discovered process against a normative process model; deviations (fitness, precision, generalisation metrics) reveal where the process drifts from intent; (3) **Performance Analysis** — measures time, frequency, and cost per activity; identifies bottlenecks and rework loops.

**SMB data requirements:** Any system that generates timestamped events per case. CRM (lead → opportunity → proposal → won/lost), ERP (purchase order → goods receipt → invoice → payment), support ticketing systems. Most UK SMBs using Xero, Salesforce, HubSpot, or Sage have event log data — it is rarely analysed at this level.

**Example insights:**
1. Process mining on a CRM reveals that proposals pending internal review (activity between "proposal drafted" and "sent to client") have a median lag of 6.2 days vs a target of 1 day; this lag correlates with a 35% win rate reduction (conformance deviation driving outcome).
2. Order-to-cash process mining shows that invoices to three specific clients consistently follow a variant path (additional approval steps inserted post-submission) that extends DSO by 18 days vs standard — targeted process intervention reduces DSO on those accounts.

**Pairs with:** TOC (process mining identifies the constraint with precision); Little's Law (queue lengths and cycle times are the outputs of process mining); SPC (apply control charts to process mining KPIs).

---

### 8.3 Anomaly Detection

**Core mechanisms:**
- **Isolation Forest** (Liu, Ting, Zhou, 2008): Tree-based algorithm that isolates anomalies by randomly selecting features and split values. Anomalies require fewer splits to isolate (shorter path length). No assumption of distributional shape. Efficient on high-dimensional data.
- **Local Outlier Factor (LOF)** (Breunig et al., 2000): Measures the local density deviation of a point vs its neighbours. A point in a region of low density relative to its neighbourhood is an outlier.
- **Seasonal-Trend Decomposition (STL)**: Decomposes time series into trend, seasonal, and remainder components. Anomalies surface in the remainder (residuals) after trend and seasonality are removed — essential for detecting signal in business data with clear seasonality.

**SMB applications:** Anomaly detection on financial time series (unusual expense patterns, invoice timing anomalies, supplier payment irregularities); customer behaviour (sudden drop in purchase frequency is an isolation forest outlier — early churn signal); employee data (absences clustering around specific days or in specific teams); web traffic anomalies (traffic spikes preceding sales vs bots).

**Pairs with:** SPC (SPC is a simple form of anomaly detection; isolation forest handles multivariate, non-linear relationships); Changepoint Detection (PELT/BOCPD for detecting when the statistical properties of a time series permanently shift — more than a point anomaly); Kaplan-Meier (anomalies in survival curves signal structural change in customer behaviour).

---

### 8.4 Survival Analysis — Kaplan-Meier & Cox Proportional Hazards

**Origin:** Edward Kaplan & Paul Meier. *Journal of the American Statistical Association*, 53(282), 1958. Cox Proportional Hazards model: David Cox, *Journal of the Royal Statistical Society*, Series B, 34(2), 1972.

**Core mechanism:** Survival analysis models **time to event** (customer churn, employee departure, supplier failure, equipment breakdown). The **Kaplan-Meier estimator** produces non-parametric survival curves — probability of survival beyond time t — handling censored observations (customers still active at the end of the observation window). The **Cox model** estimates the hazard ratio of each covariate: how much does each predictor (e.g., contract type, onboarding time, payment method) multiply the baseline hazard rate? Outputs directly actionable: "month-to-month customers have a 3.8× higher hazard than annual contract customers."

**SMB applications:** Customer churn prediction from CRM data; employee tenure analysis to identify which roles/departments have structurally high attrition hazard; supplier reliability modelling; equipment failure prediction (condition-based maintenance).

**Example insights:**
1. A UK staffing firm's Cox model shows that employees hired via one specific job board have a 2.1× higher hazard of departure within 6 months vs referral hires, and cost 40% more per hire — the channel is deleted.
2. A SaaS SMB's Kaplan-Meier curves show that the first 90 days are the highest-risk period; 61% of churn occurs before day 90. The activation workflow is redesigned around this cliff.

**Pairs with:** Cohort LTV Analysis (survival analysis underpins rigorous LTV estimation); BG/NBD model (Fader-Hardie formalise this probabilistically); Bradford Factor (employee survival analysis complements absence analytics).

---

### 8.5 Granger Causality & Bayesian Networks

**Origin:** Granger Causality: Clive Granger, *Econometrica*, 37(3), 1969. Nobel Prize in Economics, 2003. Bayesian Networks: Judea Pearl, *Probabilistic Reasoning in Intelligent Systems* (1988, Morgan Kaufmann); Causality (2000, Cambridge University Press).

**Core mechanism (Granger):** Variable X "Granger-causes" Y if past values of X improve the prediction of Y above and beyond past values of Y alone, in a vector autoregression framework. Important caveat: Granger causality is predictive, not necessarily structural/causal. Confounders, spurious correlations, and omitted variables can produce Granger-causal relationships that are not mechanistic.

**Core mechanism (Bayesian Networks):** A directed acyclic graph (DAG) where nodes are variables and edges represent conditional dependencies. The "do-calculus" (Pearl) enables computation of the effect of *interventions* (do(X = x)) rather than mere observations, distinguishing correlation from causal effect. At short time series lengths (<30 observations), Bayesian Networks outperform Granger causality (Zou & Feng, 2009, *BMC Bioinformatics*).

**SMB applications:** With monthly data for 3+ years, Granger causality tests can assess: does lead volume predict revenue 2 months ahead? Does employee satisfaction (from survey data) predict customer satisfaction 3 months ahead? Does marketing spend Granger-cause web traffic?

**Limitations:** Both methods require long, clean time series (Granger: 50+ observations preferred; Bayesian Networks: 30+). Granger causality does not handle non-stationarity well without differencing. Neither method proves causality — they inform hypotheses for experimental testing.

**Pairs with:** Swanson LBD (Granger/Bayesian Networks provide the formal statistical test for ABC connections); Monte Carlo (once causal relationships are estimated, Monte Carlo propagates uncertainty); Tetlock Superforecasting (Granger forecasts are inputs to calibrated probability estimates).

---

## FAMILY 9: SYSTEMS & COMPLEXITY

### 9.1 Stafford Beer — Viable System Model (VSM)

**Origin:** Stafford Beer. *Brain of the Firm* (1972, Allen Lane); *The Heart of Enterprise* (1979, Wiley); *Diagnosing the System for Organisations* (1985, Wiley). Grounded in Ross Ashby's **Law of Requisite Variety** (Ashby, *Design for a Brain*, 1952; *Introduction to Cybernetics*, 1956).

**Core mechanism:** Any viable system (one capable of independent existence) must have five systems: **S1 (Operations)** — the primary activities that produce output; **S2 (Coordination)** — dampens oscillations between S1 units, prevents cross-interference; **S3 (Control)** — optimises the here-and-now; the inside-and-now perspective; **S4 (Intelligence)** — scans the external environment; the outside-and-future perspective; **S5 (Policy)** — closes the S3/S4 loop; sets identity and norms. The VSM is **recursive**: each S1 unit is itself a viable system with its own S1–S5. Ashby's Law states: the variety of a controller must be at least as great as the variety of the system it controls. An SMB that tries to manage a complex market with inadequate information (insufficient variety) will fail to adapt.

**SMB adaptation:** Map the SMB's five systems. Common failure: S4 (Intelligence/Environmental Scanning) is absent or inadequate — the owner is too busy in S1/S3 operations to monitor external changes. Another common failure: S2 is purely informal (weekly meeting), creating oscillation between departments. The VSM diagnosis takes one day and typically surfaces 3–5 structural dysfunctions invisible to standard org chart analysis.

**Pairs with:** Senge Fifth Discipline (VSM provides the structural model; Senge provides the learning disciplines); Ashby's Law (foundation); Donella Meadows (leverage points map to VSM systems — S5/S4 are the highest-leverage interventions).

---

### 9.2 Peter Senge — Five Disciplines & Systems Archetypes

**Origin:** Peter Senge (MIT Sloan). *The Fifth Discipline: The Art and Practice of the Learning Organization* (1990, Currency/Doubleday). The archetypes are developed in Appendix 2 and Chapter 6.

**Core mechanism:** The five disciplines: **Systems Thinking** (the fifth discipline — integrates all others); **Personal Mastery** (individual commitment to learning); **Mental Models** (surfacing and challenging assumptions); **Building Shared Vision**; **Team Learning**. Senge's Systems Archetypes formalise recurring reinforcing/balancing loop patterns:
- **Fixes that Fail**: a short-term fix has delayed unintended consequences that worsen the original problem.
- **Shifting the Burden**: a symptomatic solution relieves pressure on the fundamental solution; the fundamental solution is never addressed; dependency on the symptomatic solution increases.
- **Limits to Growth**: a reinforcing growth loop runs into a balancing constraint; investing more in the growth engine makes things worse; the leverage is in the constraint.
- **Tragedy of the Commons**: shared resources deplete because individual incentives favour over-use.
- **Escalation**: two sides react to each other's actions in a mutually reinforcing arms race.

**Donella Meadows — 12 Leverage Points** (*Leverage Points: Places to Intervene in a System*, 1999, Sustainability Institute): ordered from weakest to strongest: (12) constants/sizes of flows → (11) sizes of stocks → (10) delays → (9) structure of material flows → (8) strength of negative feedback loops → (7) gain around driving positive loops → (6) structure of information flows → (5) rules of the system → (4) power to add/change/self-organise → (3) goals of the system → (2) mindset/paradigm → (1) power to transcend paradigms. Most management interventions target #12–#9 (weakest). The most powerful leverage is at the level of goals (#3) and paradigms (#2) — which is why TOC's Thinking Processes (which attack unexamined assumptions, a paradigm-level intervention) are so potent.

**Pairs with:** Forrester System Dynamics (mathematical underpinning of archetypes); VSM (the governance structure that sustains learning); Goldratt TOC (Limits to Growth archetype is the systems-thinking description of the constraint).

---

## FAMILY 10: MARKETING & GROWTH

### 10.1 Ehrenberg-Bass — Double Jeopardy & Mental/Physical Availability

**Origin:** Andrew Ehrenberg. "Double Jeopardy" first described by McPhee (1963); Ehrenberg applied it to marketing. Byron Sharp, Ehrenberg-Bass Institute for Marketing Science, University of South Australia. *How Brands Grow* (2010, Oxford University Press).

**Core mechanism:** The **Double Jeopardy Law**: smaller-share brands are penalised twice — they have far fewer buyers *and* those buyers purchase slightly less frequently. This pattern holds across hundreds of FMCG, B2B, and digital categories. The implication: brand growth comes overwhelmingly from **penetration** (new buyers), not loyalty. Sharpe's **mental availability** = the probability of a brand being recalled in a buying situation, across different Category Entry Points (CEPs). **Physical availability** = ease of purchase at any touchpoint. Both require continuous investment; neither sustains without ongoing support.

**SMB adaptation:** For UK SMBs: mental availability is built through consistent presence in the contexts where prospects consider the SMB's category. Physical availability for professional services = ease of finding, contacting, and engaging. The Double Jeopardy Law suggests that a UK SMB aiming to grow should invest primarily in reaching new buyers, not deepening loyalty programmes — loyalty is a symptom of size, not a cause.

**Pairs with:** AARRR (acquisition and activation are the primary growth levers consistent with Double Jeopardy); LTV:CAC (Ehrenberg-Bass is the theory; cohort analysis is the measurement tool).

---

### 10.2 AARRR (Pirate Metrics)

**Origin:** Dave McClure, 500 Startups. Introduced in "Startup Metrics for Pirates" presentation, 2007.

**Core mechanism:** Five sequential user behaviour metrics: **Acquisition** (how users are found); **Activation** (first valuable experience); **Retention** (users returning); **Revenue** (monetisation); **Referral** (users referring others). The framework forces prioritisation: which stage has the lowest conversion rate and therefore represents the highest leverage improvement opportunity?

**SMB adaptation:** AARRR maps to any business model, not just startups. For a UK B2B services firm: Acquisition = inbound enquiries by channel; Activation = proposal to first engagement; Retention = client renewal rate; Revenue = revenue per client; Referral = referral rate. Plotting conversion rates at each stage identifies the most broken link.

**Pairs with:** Cohort analysis (retention analytics); LTV:CAC (revenue and retention stages); Ehrenberg-Bass (acquisition-first growth philosophy).

---

### 10.3 Marketing Mix Modelling (MMM) at SMB Scale

**Origin:** Econometric marketing attribution originated in FMCG companies in the 1960s–1970s. Modern MMM uses regression analysis (Ordinary Least Squares or Bayesian Ridge Regression) to decompose observed sales into contributions from each marketing channel, controlling for seasonality, price, distribution, and external factors.

**SMB adaptation:** Lightweight MMM is feasible for UK SMBs with 2+ years of weekly data: monthly revenue as dependent variable; marketing spend by channel, price changes, promotional events, seasonality, and macro variables as regressors. Bayesian MMM (with informative priors from industry benchmarks) requires only 18–24 months of data vs 3+ years for frequentist approaches.

**Pairs with:** AARRR (MMM tests which acquisition channels actually drive revenue); Granger causality (preliminary test before full MMM build).

---

## FAMILY 11: HR & PEOPLE ANALYTICS

### 11.1 Bradford Factor

**Origin:** University of Bradford, c.1985. Adopted widely in UK HR practice. Formula: B = S² × D (B = Bradford Score; S = number of absence spells in 52 weeks; D = total absence days).

**Core mechanism:** Penalises frequent short absences more heavily than single long absences, reflecting their greater operational disruption. Ten single-day absences (B = 10² × 10 = 1,000) scores higher than one 10-day absence (B = 1² × 10 = 10). Typical trigger thresholds: informal review at 100–200; formal HR conversation at 400; disciplinary consideration at 600+.

**UK context:** Must be applied carefully in the context of the Equality Act 2010 (UK). Disability-related absences must be discounted; reasonable adjustments override Bradford Factor thresholds. ACAS guidance recommends Bradford Factor as a *tool*, not a *rule*.

**SMB adaptation:** Automate Bradford scoring in HR system. Run monthly. Overlay with SPC control charts to identify teams or departments with structurally elevated absence (systemic management issue) vs individual outliers.

**Pairs with:** Tenure Survival Analysis (Kaplan-Meier); Schein Cultural Levels (high Bradford scores in a team may signal cultural dysfunction at the artefacts level masking deeper assumptions); Senge Shifting the Burden (perverse absence management creates its own burden).

---

### 11.2 Schein — Organisational Culture Levels

**Origin:** Edgar H. Schein (MIT Sloan). *Organizational Culture and Leadership* (1985, Jossey-Bass; 5th ed. 2017).

**Core mechanism:** Culture exists at three levels: **Artefacts** (visible structures, processes, behaviour — what you see and hear); **Espoused Values** (stated strategies, goals, philosophies — what people say); **Basic Underlying Assumptions** (unconscious, taken-for-granted beliefs about human nature, time, relationships — what people actually do when nobody is watching). Most culture change efforts fail because they operate at the Artefacts level while underlying assumptions remain unchanged.

**SMB adaptation:** For a UK SMB undergoing growth, the critical tension is between the founder's basic assumptions (often embedded in the original culture) and the professional management systems needed at scale. The Dunbar Number (Robin Dunbar, 1992): ~150 people is the cognitive limit for stable social relationships. Beyond ~15 (a hunter-gatherer band), shared tacit culture requires explicit processes. Beyond ~50, management hierarchy becomes necessary. Beyond ~150, institutional culture requires formal codification.

**Pairs with:** VSM (S2/S5 functions are the formalisation of cultural norms); Collins Five Stages (Stage 2 overreach often breaks the Schein culture-scale contract); Bradford Factor (high absence rates may signal assumption-level cultural dysfunction).

---

## FAMILY 12: PRICING & VALUE CAPTURE

### 12.1 Van Westendorp Price Sensitivity Meter (PSM)

**Origin:** Peter van Westendorp, Dutch economist. Introduced in a Market Research Society conference paper, 1976.

**Core mechanism:** Four survey questions establish the psychologically acceptable price range: (1) "At what price would you consider this too cheap to be good quality?"; (2) "At what price would you consider this cheap/good value?"; (3) "At what price would you consider this expensive but worth it?"; (4) "At what price would you consider this too expensive to consider?" Plotting cumulative frequencies produces four intersecting curves. Key outputs: Point of Marginal Cheapness (PMC, lower acceptable bound); Point of Marginal Expensiveness (PME, upper acceptable bound); Acceptable Price Range (PMC to PME); Optimal Price Point (intersection of "too cheap" and "too expensive" curves). The Newton-Miller-Smith (1993) extension adds purchase likelihood questions to estimate demand elasticity.

**SMB adaptation:** 30–100 customer surveys sufficient for directional guidance. Most useful when repricing an established service or launching a new product line without competitive benchmarks.

**Limitations:** Stated preferences do not always match purchase behaviour; no competitive context; unreliable if respondents lack category familiarity.

**Pairs with:** Kano Model (features that drive Attractive satisfaction justify premium pricing); JTBD (pricing should reflect the value of the job done, not cost-plus); Conjoint Analysis (Van Westendorp for initial range; conjoint for trade-off precision).

---

### 12.2 Price Elasticity Estimation from Historical Data

**Core mechanism:** Elasticity ε = %ΔQ / %ΔP. For UK SMBs with sufficient historical data (price changes with recorded volume impacts), OLS regression or log-log models can estimate elasticity. A log-log model (ln(quantity) = α + ε × ln(price) + β × X) directly estimates the elasticity coefficient as ε. The challenge for most SMBs: insufficient variation in price history and insufficient data points for reliable estimation.

**Practical shortcut:** Van Westendorp PSM provides a qualitative directional estimate; A/B price testing (where ethically and operationally feasible) provides experimental evidence.

---

## FAMILY 13: RISK & RESILIENCE

### 13.1 Monte Carlo Simulation for Cashflow Stress Testing

**Core mechanism:** Rather than projecting a single "best estimate" cashflow, Monte Carlo draws thousands of samples from probability distributions assigned to each key input (revenue growth rate, gross margin, debtor days, capex timing). The output is a probability distribution of outcomes — revealing not just the expected scenario but the 10th and 90th percentile scenarios. For UK SMBs, the most critical inputs to vary: top-client revenue (particularly if concentrated), gross margin (input cost volatility), and debtor days (CCC risk).

**SMB adaptation:** A basic Monte Carlo model in Excel (using @RISK or Crystal Ball, or Python) with 5–8 uncertain inputs and 10,000 simulations runs in under a minute. Output: "probability of cashflow going negative in the next 12 months = 23%" — a precise risk statement that "we're probably fine" does not provide.

**Pairs with:** Altman Z'' (Monte Carlo scenarios can include Z'' calculations per simulation); Taleb Barbell (Monte Carlo quantifies the tail risk that the barbell strategy hedges); Forrester System Dynamics (feedback loops can be incorporated for higher-fidelity modelling).

---

### 13.2 FAIR (Factor Analysis of Information Risk)

**Origin:** Jack Jones. *Measuring and Managing Information Risk: A FAIR Approach* (Jones, 2014, Butterworth-Heinemann). FAIR is the only international standard quantitative model for cybersecurity and operational risk.

**Core mechanism:** Decomposes risk into Loss Event Frequency (LEF) × Loss Magnitude (LM). LEF = Threat Event Frequency × Vulnerability. LM = Primary Loss + Secondary Loss (reputational, regulatory, competitive). FAIR uses PERT distributions (minimum, most-likely, maximum) for each factor, enabling Monte Carlo aggregation of total annual loss exposure (ALE).

**UK SMB relevance:** UK GDPR under the UK Data Protection Act 2018 requires SMBs to demonstrate risk proportionality in data protection decisions. FAIR provides the quantitative basis for those decisions, avoiding both over-investment (£30k DLP system for a £5k/year risk) and under-investment.

**Pairs with:** Monte Carlo (the aggregation method); Taleb (FAIR quantifies the convexity of cyber risk — catastrophic tail events are not normally distributed).

---

## MASTER FRAMEWORK MAPPING TABLE

| Framework | Required Data | Time Horizon | SMB Applicability (1–5) | Pairs Well With |
|---|---|---|---|---|
| Goldratt TOC | Process logs, throughput, WIP, queue lengths | Immediate (days/weeks) | 5 | Lean, SPC, Little's Law, DuPont |
| Drum-Buffer-Rope | Constraint schedule, buffer levels | Operational | 5 | TOC, Lean, SPC |
| Throughput Accounting | Revenue, variable costs, OE, inventory | Monthly | 5 | DuPont, Altman Z'', TOC |
| Collins Five Stages | Engagement, margin trend, hiring data, decision quality | 12–36 months | 4 | Forrester, Altman, Bradford |
| Forrester System Dynamics | Multi-variable time series, 12–24 months | Medium-term | 3 | Senge, Goldratt, Monte Carlo |
| Christensen Disruption | Market share by segment, new entrant pricing | 18–60 months | 3 | Wardley, BCG, Porter Five Forces |
| Taleb Antifragility | Revenue concentration, fixed/variable costs, debt, cash | Strategic | 4 | Monte Carlo, Altman, Piotroski |
| Altman Z'' | Balance sheet, P&L (2 years) | 24-month forecast | 5 | Ohlson, Piotroski, DuPont, CCC |
| Ohlson O-Score | Balance sheet, P&L, net loss flag | 24-month forecast | 4 | Altman, Zmijewski |
| Piotroski F-Score | Two years' accounts | Annual | 5 | Altman, DuPont, CCC |
| DuPont Analysis | P&L, balance sheet | Annual/quarterly | 5 | Piotroski, Altman, TOC |
| Cash Conversion Cycle | AR, AP, inventory data | Monthly | 5 | Altman, Little's Law, TOC |
| Porter Five Forces | Industry data, competitor intel | Annual | 4 | Value Chain, Blue Ocean, Wardley |
| Blue Ocean (Four Actions) | Customer insight, competitor feature matrix | Strategic | 4 | JTBD, Kano, Porter |
| BCG Matrix | Revenue by segment, market growth data | Annual | 3 | Ansoff, Porter Five Forces |
| Wardley Mapping | Value chain audit, capability maturity | Strategic | 3 ⬆ | Porter, TOC, Christensen |
| LTV:CAC + Cohort Analysis | Transaction data (12–24 months), CAC by channel | Ongoing | 5 | AARRR, BG/NBD, Kaplan-Meier |
| Fader-Hardie BG/NBD | Transaction history, customer ID, dates | 12+ months | 3 | LTV:CAC, Kaplan-Meier |
| Kano Model | Customer surveys (30–100 respondents) | Strategic | 4 | JTBD, LTV:CAC, Porter |
| Jobs-to-be-Done | Customer interviews (5–10) | Strategic | 4 | Kano, Blue Ocean, JTBD |
| Deming SoPK/PDCA | Process data, variation metrics | Ongoing | 4 | SPC, TOC, Lean |
| Statistical Process Control (XmR) | 20+ observations of any metric | Ongoing | 5 | Deming, TOC, Anomaly Detection |
| Lean / TPS / 7 Wastes | Process observation, time studies | Immediate | 5 | TOC, SPC, Little's Law |
| Little's Law | WIP count, throughput rate, cycle time | Operational | 5 | TOC, Lean, Erlang C |
| Erlang C | Call arrival rate, handling time, agents | Operational | 3 | Little's Law, TOC |
| Dalio Believability Weighting | Track record data per decision-maker | Ongoing | 4 | Tetlock, Bayesian Updating |
| Kahneman System 1/2 | Decision audit logs | Ongoing | 4 | Dalio, Tetlock, Superforecasting |
| Tetlock Superforecasting / Brier | Probability forecasts + outcomes (logged) | Ongoing | 3 | Bayesian Updating, Dalio |
| Bayesian Updating | Prior data + new evidence (any form) | Ongoing | 4 | Tetlock, Granger, Swanson LBD |
| Swanson LBD / ABC Model | Two separate data streams with a bridging variable | Ad hoc | 4 ⬆ | Bayesian Networks, Granger, Process Mining |
| Process Mining | Event logs (CRM, ERP, ticketing) | Ongoing | 4 | TOC, Little's Law, SPC |
| Anomaly Detection (Isolation Forest) | Transaction / time-series data | Ongoing | 4 | SPC, Changepoint Detection |
| Kaplan-Meier / Cox Survival | Time-to-event data (customer IDs, dates) | 12+ months | 4 | LTV:CAC, Bradford Factor |
| Granger Causality | Monthly time series, 36+ months | Retrospective | 3 | Bayesian Networks, Swanson LBD |
| Bayesian Networks | Multi-variable dataset, DAG structure | Analytical | 3 | Granger, Swanson, Monte Carlo |
| Beer VSM | Org structure audit, info flow analysis | Strategic | 3 ⬆ | Senge, Ashby, Meadows |
| Senge Archetypes | Causal loop narrative data | Strategic | 4 | Forrester, Meadows, TOC |
| Meadows 12 Leverage Points | Systems analysis output | Strategic | 3 | Senge, VSM, Forrester |
| Ehrenberg-Bass Double Jeopardy | Sales/customer data by segment | Quarterly | 4 | AARRR, LTV:CAC, MMM |
| AARRR Pirate Metrics | Funnel analytics, cohort data | Monthly | 5 | LTV:CAC, Ehrenberg-Bass |
| Marketing Mix Modelling | 24 months weekly revenue + channel spend | Annual | 3 | AARRR, Granger |
| Bradford Factor | HR absence records (52 weeks rolling) | Monthly | 5 | Kaplan-Meier, SPC, Schein |
| Schein Culture Levels | Observation, interviews, surveys | Annual | 3 | Collins, VSM, Dunbar |
| Van Westendorp PSM | Customer surveys (30–100) | Strategic | 4 | Kano, JTBD, Conjoint |
| Price Elasticity | Historical price-volume data | Annual | 3 | MMM, Van Westendorp |
| Monte Carlo Cashflow | Financial model + uncertainty estimates | Monthly | 4 | Altman, Taleb, FAIR |
| FAIR Risk Quantification | Asset inventory, threat data, loss history | Annual | 3 | Monte Carlo, Taleb |

*SMB Applicability: 5 = immediately actionable with minimal data/resource; 1 = requires substantial data/expertise, rarely worth the effort for SMBs*

*⬆ indicates frameworks rated particularly high relative to their current SMB adoption rate (underused)*

---

## DEATH SPIRAL DETECTION RUBRIC

**Purpose:** A structured set of leading indicators computable from fused internal and public data that together constitute an early warning system for organisational decline. Organised by signal type. Each indicator notes the data source and approximate lead time before visible distress.

### Rubric Classification
Each indicator scores 0 (healthy) or 1 (warning) on a rolling 90-day basis. Total score 0–4: green; 5–9: amber (investigate); 10+: red (immediate review).

---

### TIER 1: FINANCIAL STRUCTURE SIGNALS (Altman / DuPont / CCC family)

**Indicator 1 — Altman Z'' Score Trend**
- Signal: Z'' decline >0.5 in any 12-month period, or Z'' < 1.23
- Data: Companies House filings or management accounts
- Lead time: 6–18 months ahead of visible distress
- Source mechanism: Working capital deterioration and earnings compression are early structural signals

**Indicator 2 — Piotroski F-Score Decline**
- Signal: F-Score ≤ 4 (especially if declining from ≥ 7 in prior year)
- Data: Annual accounts (two years)
- Lead time: 12–18 months

**Indicator 3 — Cash Conversion Cycle Lengthening**
- Signal: CCC extending >15% vs 12-month rolling average, or DSO increasing for 3+ consecutive months
- Data: AR ledger, AP ledger, inventory system
- Lead time: 3–9 months (DSO deterioration precedes cash crunch by one billing cycle)

**Indicator 4 — Gross Margin Compression**
- Signal: Gross margin declining >3 percentage points over 6 months, or below sector floor (estimated from Companies House peer benchmarking)
- Data: Management accounts, P&L
- Lead time: 3–12 months (precedes EBIT compression)

**Indicator 5 — Revenue Concentration Increase**
- Signal: Top-1 or top-3 client revenue concentration increasing above 40% / 65% respectively (Herfindahl-Hirschman Index applied to revenue)
- Data: Sales/CRM data
- Lead time: Variable; fragility indicator rather than direct spiral trigger

**Indicator 6 — HMRC / Tax Liability Ageing**
- Signal: PAYE/VAT accounts >30 days overdue, or HMRC Time To Pay arrangement entered
- Data: Internal accounts, HMRC correspondence
- Lead time: 3–6 months (HMRC secondary preferential creditor status makes tax debt structurally dangerous in UK insolvency)

---

### TIER 2: OPERATIONAL THROUGHPUT SIGNALS (TOC / Process Mining family)

**Indicator 7 — Constraint Utilisation Spike**
- Signal: Primary constraint resource operating at >90% utilisation for >8 weeks, with queue length growing
- Data: Operational logs, process mining on CRM/ERP events
- Lead time: 2–6 months (leads to customer experience deterioration and delivery failure)
- Goldratt link: The constraint is the system's weakest point; chronic over-utilisation with no elevation plan signals management inaction

**Indicator 8 — Order-to-Cash Lead Time Increase**
- Signal: Average days from order to invoice payment increasing >20% vs 6-month baseline, confirmed by SPC special cause signal
- Data: Accounting system timestamps
- Lead time: 2–6 months

**Indicator 9 — Delivery Performance / SLA Breach Rate**
- Signal: On-time/in-full delivery or SLA adherence declining below 85%, or control chart showing sustained deterioration (8+ consecutive points below mean)
- Data: Operations records, customer-facing logs
- Lead time: 1–4 months before customer defection begins

**Indicator 10 — Rework / Defect Rate Increase**
- Signal: Rework costs or defect rates increasing >15% on XmR control chart; confirmed special cause
- Data: Operations data, support ticket system
- Lead time: 1–3 months before customer visible quality complaints

---

### TIER 3: CUSTOMER HEALTH SIGNALS (LTV / Cohort / Survival family)

**Indicator 11 — Cohort Retention Cliff**
- Signal: Monthly cohort analysis shows current-period cohort 90-day retention >5 percentage points below the prior 4-quarter average
- Data: CRM/transaction data
- Lead time: 3–9 months ahead of revenue impact (customer defection precedes revenue decline)

**Indicator 12 — LTV:CAC Ratio Deterioration**
- Signal: Blended LTV:CAC falling below 2:1 or declining for 3+ consecutive months; or CAC payback period exceeding 18 months
- Data: Marketing spend, revenue per cohort, CRM
- Lead time: 6–18 months (slow-moving indicator; useful for trend not trigger)

**Indicator 13 — Customer Concentration + Churn Risk in Top Accounts**
- Signal: One or more of the top-5 clients shows BG/NBD probability of inactivity >60%, or reduces purchase frequency by >30%
- Data: CRM transaction data
- Lead time: 1–6 months (large account defection often has leading behavioural signals)

**Indicator 14 — Net Promoter Score Decline (or proxy)**
- Signal: Customer satisfaction proxy (e.g., review scores on Google/Trustpilot, survey NPS) declining >10 points over 6 months
- Data: Review data (public), customer surveys
- Lead time: 3–9 months ahead of defection acceleration

---

### TIER 4: PEOPLE & CULTURAL SIGNALS (HR family)

**Indicator 15 — Employee Tenure Survival Curve Shift**
- Signal: Kaplan-Meier survival curves show current-year cohort of employees has materially lower 6-month retention probability vs prior two cohorts (log-rank test p < 0.05)
- Data: HR records with hire and departure dates
- Lead time: 6–18 months (people deterioration precedes operational and customer deterioration)
- Collins Stage link: Stage 2–3 — talent exits when insiders see mismanagement before outsiders do

**Indicator 16 — Bradford Factor Team Spike**
- Signal: Mean Bradford Score in a critical team or function increasing >50% over rolling 12 weeks; or new entrant to >400 zone among key staff
- Data: HR attendance records
- Lead time: 1–4 months (high absence = team stress, management failure, or cultural dysfunction)

**Indicator 17 — Key Person Departure Velocity**
- Signal: >2 senior departures in a 90-day window from a team of <15; or departure of role-critical personnel without succession plan
- Data: HR records, LinkedIn monitoring (public data)
- Lead time: 1–6 months (knowledge loss and network disruption follow)

---

### TIER 5: STRATEGIC & EXTERNAL SIGNALS (Collins / Christensen / Wardley family)

**Indicator 18 — Revenue Mix Shift toward Lower-Margin Activities**
- Signal: Revenue from the SMB's highest-throughput product/service line declining as % of total for 3+ consecutive months; lower-margin or higher-constraint work filling the gap
- Data: Management accounts by product/service line
- Lead time: 6–24 months (reflects Stage 2 undisciplined pursuit of more, or Christensen-style ceding of core market)

**Indicator 19 — New Entrant Activity at Price Points 20%+ Below SMB**
- Signal: Identified via sector monitoring, lost bid analysis, or client exit interviews — a competitor consistently offering comparable service at significantly lower price
- Data: Lost deal data (CRM), public pricing, competitor tracking
- Lead time: 12–36 months (disruption precursor)

**Indicator 20 — Pipeline-to-Revenue Ratio Decline**
- Signal: Weighted sales pipeline value (CRM) declining as a multiple of monthly revenue below 2.5×, or conversion rate from proposal to win declining >5pp over 6 months
- Data: CRM pipeline data
- Lead time: 2–6 months

**Indicator 21 — Wardley Map Component Commoditisation (Innovation Stagnation)**
- Signal: No component in Genesis or early Custom Built stage in the past 24 months; all SMB capabilities are in Product or Commodity quadrant with no differentiation investment
- Data: Quarterly Wardley Map review
- Lead time: 24–60 months (slowest but deepest predictor)

---

### TIER 6: SYSTEMS-LEVEL SIGNALS (Forrester / VSM / Taleb family)

**Indicator 22 — Reinforcing Cost-Cutting Loop Activation**
- Signal: Three or more of the following co-occurring: training/CPD budget cut; BD/marketing spend cut; headcount freeze; deferred capex; deferred maintenance — while revenue is flat or declining
- Data: Budget/management accounts
- Lead time: 3–12 months (the Doom Loop entry point — cost cuts precede the quality deterioration that drives the next revenue decline cycle)
- Forrester "Fixes that Fail" archetype

**Indicator 23 — Decision Speed Slowdown / Escalation Increase**
- Signal: Average decision-making time (from proposal/request to approval) increasing >30% vs historical baseline; or an increase in decisions being escalated to the most senior person
- Data: CRM/ERP workflow timestamps, email/calendar analytics
- Lead time: 3–9 months (Stage 3 Collins signal — the leadership team is becoming defensive and information-bottlenecked)

**Indicator 24 — S4 Function Absence (VSM)**
- Signal: No structured competitor monitoring, market scanning, or strategic planning activity in the past 90 days at the leadership level
- Data: Calendar/meeting records, strategic documentation
- Lead time: 12–36 months (VSM S4 absence is a leading indicator of strategic surprise)

**Indicator 25 — Barbell Fragility Score**
- Signal: Fixed cost ratio >70% of total costs; top-3 client concentration >60%; net debt > 1.5× EBITDA; cash runway <3 months
- Data: Management accounts, balance sheet
- Lead time: 3–18 months (any single shock may be survivable; the combination is a Taleb "fragile middle" warning)

---

### Summary Rubric Scoring Table

| Tier | Indicators | Primary Analytical Family | Fastest Signal |
|---|---|---|---|
| 1: Financial Structure | 1–6 | Altman/DuPont/CCC | DSO (Ind. 3) — 30 days |
| 2: Operational Throughput | 7–10 | TOC/Process Mining/SPC | Constraint Queue (Ind. 7) — real time |
| 3: Customer Health | 11–14 | Cohort/Survival/BG/NBD | Retention Cliff (Ind. 11) — monthly |
| 4: People & Culture | 15–17 | Bradford/Survival/HR | Bradford Spike (Ind. 16) — weekly |
| 5: Strategic & External | 18–21 | Collins/Christensen/Wardley | Pipeline Ratio (Ind. 20) — monthly |
| 6: Systems-Level | 22–25 | Forrester/VSM/Taleb | Cost-Cut Loop (Ind. 22) — monthly |

**Score interpretation:**
- 0–4 warning indicators: Green — standard monitoring
- 5–9 warning indicators: Amber — convene diagnostic review within 30 days; apply TOC Thinking Processes (CRT) to identify root constraint
- 10–14 warning indicators: Red — immediate intervention; Altman Z'' and cashflow stress test (Monte Carlo) as first priorities; consider external advisory
- 15+ warning indicators: Critical — Stage 4 Collins dynamics likely active; survival strategy (barbell) and stakeholder communication are the immediate imperatives

---

## CITATIONS & KEY REFERENCES

1. Goldratt, E.M. & Cox, J. (1984). *The Goal*. North River Press.
2. Goldratt, E.M. (1990). *The Theory of Constraints*. North River Press.
3. Collins, J. (2009). *How the Mighty Fall*. HarperBusiness.
4. Christensen, C.M. (1997). *The Innovator's Dilemma*. Harvard Business School Press.
5. Forrester, J.W. (1961). *Industrial Dynamics*. MIT Press.
6. Taleb, N.N. (2012). *Antifragile*. Random House.
7. Altman, E.I. (1968). "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy." *Journal of Finance*, 22(4), 589–609.
8. Ohlson, J. (1980). "Financial Ratios and the Probabilistic Prediction of Bankruptcy." *Journal of Accounting Research*, 18(1), 109–131.
9. Piotroski, J. (2000). "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers." *Journal of Accounting Research*, 38(Supplement), 1–41.
10. Porter, M.E. (1979). "How Competitive Forces Shape Strategy." *Harvard Business Review*, March–April.
11. Porter, M.E. (1980). *Competitive Strategy*. Free Press.
12. Porter, M.E. (1985). *Competitive Advantage*. Free Press.
13. Kim, W.C. & Mauborgne, R. (2005). *Blue Ocean Strategy*. Harvard Business School Press.
14. Wardley, S. (2016). Wardley Maps [blog series]. https://medium.com/wardleymaps
15. Fader, P., Hardie, B. & Lee, K.L. (2005). "Counting Your Customers the Easy Way." *Marketing Science*, 24(2), 275–284.
16. Kano, N. et al. (1984). "Attractive Quality and Must-Be Quality." *Journal of the Japanese Society for Quality Control*, 14(2).
17. Christensen, C.M. & Raynor, M.E. (2016). *Competing Against Luck*. HarperBusiness.
18. Shewhart, W.A. (1931). *Economic Control of Quality of Manufactured Product*. Van Nostrand.
19. Deming, W.E. (1986). *Out of the Crisis*. MIT CAES.
20. Deming, W.E. (1993). *The New Economics for Industry, Government, Education*. MIT CAES.
21. Little, J.D.C. (1961). "A Proof for the Queuing Formula: L = λW." *Operations Research*, 9(3), 383–387.
22. Dalio, R. (2017). *Principles: Life and Work*. Simon & Schuster.
23. Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
24. Kahneman, D. & Tversky, A. (1979). "Prospect Theory." *Econometrica*, 47(2), 263–291.
25. Tetlock, P. & Gardner, D. (2015). *Superforecasting*. Crown Publishers.
26. Swanson, D.R. (1986). "Fish oil, Raynaud's syndrome, and undiscovered public knowledge." *Perspectives in Biology and Medicine*, 30(1), 7–18. DOI: 10.1353/pbm.1986.0087
27. van der Aalst, W. (2011). *Process Mining: Discovery, Conformance and Enhancement of Business Processes*. Springer.
28. Kaplan, E.L. & Meier, P. (1958). "Nonparametric Estimation from Incomplete Observations." *Journal of the American Statistical Association*, 53(282), 457–481.
29. Cox, D.R. (1972). "Regression Models and Life-Tables." *Journal of the Royal Statistical Society, Series B*, 34(2), 187–202.
30. Granger, C.W.J. (1969). "Investigating Causal Relations by Econometric Models and Cross-spectral Methods." *Econometrica*, 37(3), 424–438.
31. Pearl, J. (2000). *Causality: Models, Reasoning, and Inference*. Cambridge University Press.
32. Beer, S. (1972). *Brain of the Firm*. Allen Lane.
33. Senge, P.M. (1990). *The Fifth Discipline*. Currency/Doubleday.
34. Meadows, D. (1999). "Leverage Points: Places to Intervene in a System." Sustainability Institute.
35. Sharp, B. (2010). *How Brands Grow*. Oxford University Press.
36. McClure, D. (2007). "Startup Metrics for Pirates" [presentation]. 500 Startups.
37. Schein, E.H. (1985). *Organizational Culture and Leadership*. Jossey-Bass.
38. van Westendorp, P. (1976). "NSS-Price Sensitivity Meter." Market Research Society Annual Conference.
39. Ansoff, I. (1957). "Strategies for Diversification." *Harvard Business Review*, September–October.

---

*Document generated for Amplified Partners / Ewan Bramley — SMB AI Insights Engine, Workstream 03: Framework Lineage Research.*
*Part of a five-workstream master report on forensic data mining and public data fusion.*
