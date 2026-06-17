# DSW Ventures — Early-Stage Startup Screener

A Python-based deal origination tool that implements DSW Ventures' proprietary two-stage investment screening model. The tool ingests a structured dataset of early-stage UK startups, applies geographic and founder-profile filtering, scores each company across five weighted investment criteria, and produces a ranked shortlist with supporting visualisations — replicating the core analytical workflow used in early-stage VC origination.

---

## Methodology

### Stage 1 — Hard Filter: Geographic Mandate

The first stage enforces DSW's primary geographic mandate. DSW targets companies **outside** the Golden Triangle — the cluster of deep-tech activity centred on London, Oxford, and Cambridge, extended to include Guildford, Reading, and Hertford. The rationale is that startups in these markets are systematically overserved by capital; DSW's edge lies in identifying high-quality founding teams in underserved geographies before they attract mainstream VC attention.

A startup is eliminated if its registered postcode falls within the Golden Triangle (prefixes: EC, WC, W1, SW, SE, OX, CB, GU, RG, SG13/14, and others). Companies outside this geography pass to scoring automatically.

One exception applies: any Golden Triangle company with at least one female co-founder is granted an override and proceeds to scoring. This reflects DSW's commitment to portfolio diversity and recognition that founding talent should not be filtered on geography alone.

### Stage 2 — Weighted Scoring

Passing companies are scored across five factors, each rated 0–10, with weights applied to produce a final score out of 100:

| Factor | Weight | Rationale |
|---|---|---|
| IP Defensibility | 30% | Proprietary IP reduces replication risk; patents granted signal validated innovation |
| Founder Quality | 25% | University affiliation and team size used as proxies for technical depth and resilience |
| Funding Sweet Spot | 20% | DSW targets pre-Series A; companies with £50k–£750k raised sit in the optimal entry window |
| Proof of Concept | 15% | Composite signal from revenue, paying customers, pilots, and peer-reviewed research |
| Sector Fit | 10% | Preference weighting aligned to DSW's deep-tech and life sciences thesis |

**IP Defensibility** rewards granted patents most heavily, penalises hard-tech companies without IP protection, and applies a softer scoring floor to software and services sectors where patent filing is structurally less common.

**Founder Quality** maps university affiliation to prestige tiers (Tier 1: Oxford, Cambridge, Imperial, UCL, KCL, LSE, QMUL; Tier 2: 18 leading UK research universities) and adjusts for solo founders without institutional backing.

**Funding Sweet Spot** is non-linear: companies raising £50k–£750k score highest, reflecting DSW's pre-Series A mandate. Larger raises score lower because entry valuations are likely too high for early-stage ticket sizes.

**Proof of Concept** aggregates four binary signals — peer-reviewed research, revenue, paying customers, and completed pilots — into a composite score capped at 10.

**Sector Fit** assigns scores in four tiers aligned to DSW's investment thesis: deep-tech and AI at the top, climate tech and biotech in the second tier, software and agtech below that, and consumer/fintech/edtech at the floor.

---

## How to Run

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Run the screener**

```bash
python screener.py
```

This applies the two-stage model, prints a summary and top-10 table to the terminal, and writes `output/ranked_shortlist.csv`.

**3. Generate visualisations**

```bash
python visualise.py
```

This reads the ranked shortlist and writes four charts to `output/charts/`.

---

## Output

**`output/ranked_shortlist.csv`**

All companies that passed Stage 1, ranked by final score. Columns include all five factor scores, filter classification, and key company metadata.

**`output/charts/`**

| Chart | Description |
|---|---|
| score_distribution.png | Histogram of final scores across the shortlist |
| sector_breakdown.png | Count of shortlisted companies by sector |
| funding_vs_score.png | Scatter plot of funding raised vs DSW score, coloured by sector tier |
| top20_companies.png | Horizontal bar chart of the top 20 ranked companies |

---

## Tech Stack

- Python 3.8+
- pandas — data ingestion, filtering, and scoring pipeline
- matplotlib — chart generation

No external dependencies beyond the standard scientific Python stack.

---

*Company data is synthetic and generated for demonstration purposes.*
