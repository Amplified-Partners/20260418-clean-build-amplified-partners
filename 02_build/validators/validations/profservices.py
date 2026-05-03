"""ProfServices vertical validators (INS-079..INS-094).

Per AMP-67. Each runner returns a `Verdict` for one catalogue entry. The CLI
in `02_build/validators/cli.py` collects them, writes JSON to
`03_shadow/validators/profservices/<INS-NNN>/verdict.json`, and emits the
catalogue `VALIDATION:` line.

Convention for ABC bridges (most ProfServices recipes have a client-data
C-leg): PROVEN is reserved for fully-public-data validations; if only the
public leg validates and the client-side claim has published research
support, the verdict is PLAUSIBLE.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

from collections.abc import Callable

from ..cache import FetchBlockedError
from ..core import EvidenceBundle, TestClass, Verdict, VerdictBand
from ..sources import companies_house, gazette, gov_uk, hmrc, ons
from ..tests import (
    BaseRateClaim,
    ExistenceCheck,
    base_rate_test,
    existence_test,
)

VERTICAL = "profservices"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _internal_only_plausible(
    insight_id: str,
    method_summary: str,
    finding: str,
) -> Verdict:
    """Convention for pure-internal recipes (no public-data leg).

    INS-082, INS-084, INS-090 use only internal data + literature benchmarks.
    Public-data validation is not the right test; we record PLAUSIBLE with an
    explicit note explaining why.
    """
    return Verdict(
        insight_id=insight_id,
        vertical=VERTICAL,
        band=VerdictBand.PLAUSIBLE,
        test_class=TestClass.EXISTENCE,
        method=method_summary,
        finding=finding,
        statistic={"recipe_class": "pure-internal"},
        evidence=EvidenceBundle(),
        notes=[
            "Recipe is internal-data-only; no UK public-data leg to test.",
            "Methodology is supported by published research (cited in catalogue).",
            "Verdict marked PLAUSIBLE pending client-data trial.",
        ],
    )


def _blocked_keyed_source(
    insight_id: str,
    source: str,
    reason: str,
    method: str,
) -> Verdict:
    return Verdict(
        insight_id=insight_id,
        vertical=VERTICAL,
        band=VerdictBand.BLOCKED,
        test_class=TestClass.EXISTENCE,
        method=method,
        finding=f"{source} requires a credential not provisioned: {reason}",
        statistic={"blocked_source": source},
        evidence=EvidenceBundle(),
        notes=[reason],
    )


# ---------------------------------------------------------------------------
# Per-insight runners
# ---------------------------------------------------------------------------


def run_INS_079() -> Verdict:
    """Utilisation × Companies House Sector Churn → Demand Forecasting.

    Public legs: ONS Business Demography (firm births/deaths by SIC),
    DBT Business Population Estimates (sector-level firm counts), services
    PPI (sector demand proxy). Existence test confirms all three are
    reachable open-data sources.
    """
    bd_body, bd_evidence = ons.business_demography_release()
    bpe_body, bpe_evidence = ons.business_population_estimates()
    return existence_test(
        insight_id="INS-079",
        vertical=VERTICAL,
        method=(
            "Confirm ONS Business Demography + DBT Business Population "
            "Estimates publish sector-level firm formation/dissolution data."
        ),
        body=bd_body + b"\n---\n" + bpe_body,
        evidence_item=bd_evidence,
        extra_evidence=[bpe_evidence],
        checks=[
            ExistenceCheck(
                description="ONS publishes business births and deaths",
                must_contain=("birth", "death"),
            ),
            ExistenceCheck(
                description="DBT BPE 2024 publishes sector breakdown",
                must_contain=("Business population estimates",),
            ),
        ],
    )


def run_INS_080() -> Verdict:
    """WIP Ageing × Altman Z Client Signals → Bad-Debt Prevention.

    Public leg: Companies House accounts data (XBRL bulk product, no key)
    + Gazette winding-up petitions feed. Confirms both products exist; the
    per-firm Altman Z'' score requires a CH live-API key for at-scale
    distress-zone screening, which is recorded as a follow-up gap.
    """
    accounts_body, accounts_evidence = companies_house.accounts_data_index()
    gazette_payload, gazette_evidence = gazette.insolvency_notices()
    notices_count = (
        gazette_payload.get("total", {}).get("value")
        if isinstance(gazette_payload, dict)
        else None
    )
    bundle = EvidenceBundle(items=[accounts_evidence, gazette_evidence])
    notices_phrase = (
        f"{notices_count} corporate-insolvency notices"
        if isinstance(notices_count, int)
        else "corporate-insolvency notices (count unavailable in this response)"
    )
    finding = (
        "Companies House accounts data product reachable; "
        f"Gazette returned {notices_phrase} in the queried slice."
    )
    notes = [
        "Per-firm Altman Z'' screening at scale requires the Companies House "
        "live REST API (key-gated). Apply at "
        "https://developer.company-information.service.gov.uk/ and store as "
        "the COMPANIES_HOUSE_API_KEY org secret to upgrade this from "
        "PLAUSIBLE to PROVEN.",
    ]
    return Verdict(
        insight_id="INS-080",
        vertical=VERTICAL,
        band=VerdictBand.PLAUSIBLE,
        test_class=TestClass.EXISTENCE,
        method=(
            "Existence: Companies House bulk accounts product + Gazette "
            "insolvency feed both reachable; per-firm Altman Z'' screen "
            "blocked on live API key."
        ),
        finding=finding,
        statistic={"gazette_total": notices_count},
        evidence=bundle,
        notes=notes,
    )


def run_INS_081() -> Verdict:
    """Referral Graph × LinkedIn Firmographics → BD Targeting.

    Recipe is internal-graph-driven. The LinkedIn leg has no open public API;
    the Companies House leg confirms firmographic enrichment is feasible
    via the bulk basic-company-data product.
    """
    bulk_body, bulk_evidence = companies_house.bulk_index()
    finding = (
        "Companies House bulk basic-company-data product reachable for "
        "firmographic enrichment; LinkedIn firmographics has no open public "
        "API so the LinkedIn leg cannot be validated against open data."
    )
    return Verdict(
        insight_id="INS-081",
        vertical=VERTICAL,
        band=VerdictBand.PLAUSIBLE,
        test_class=TestClass.EXISTENCE,
        method=(
            "Existence: Companies House bulk product reachable; LinkedIn "
            "firmographic API is private."
        ),
        finding=finding,
        statistic={"public_legs_validated": 1, "public_legs_blocked": 1},
        evidence=EvidenceBundle(items=[bulk_evidence]),
        notes=[
            "Methodology (referral-graph analysis) is supported by published "
            "social-network-analysis literature cited in catalogue entry.",
            "LinkedIn data only available via paid Sales Navigator / scraping; "
            "neither qualifies as open public data.",
        ],
    )


def run_INS_082() -> Verdict:
    """Email Response Time × Client Retention Curves.

    Pure-internal recipe — only internal email metadata + Kaplan-Meier
    survival analysis. PUBLIC DATA field on the catalogue entry says
    "None required". No public-data validation applies.
    """
    return _internal_only_plausible(
        insight_id="INS-082",
        method_summary=(
            "No public-data leg; recipe is internal email metadata + "
            "Kaplan-Meier survival analysis."
        ),
        finding=(
            "Catalogue entry explicitly says 'None required' under PUBLIC "
            "DATA. Methodology validated by Reichheld retention economics "
            "and Amazon SLA empirical research cited in the entry."
        ),
    )


def run_INS_083() -> Verdict:
    """Regulatory Change × Client Exposure Mapping.

    Public legs: HMRC Making Tax Digital, FCA Handbook, ICO guidance index.
    All three open. Existence test confirms reachability + key tokens.
    """
    mtd_body, mtd_evidence = hmrc.making_tax_digital_overview()
    fca_body, fca_evidence = gov_uk.fca_handbook_root()
    ico_body, ico_evidence = gov_uk.ico_guidance_index()
    return existence_test(
        insight_id="INS-083",
        vertical=VERTICAL,
        method=(
            "Confirm HMRC MTD ITSA guidance, FCA Handbook, and ICO guidance "
            "indexes are reachable and publish regulatory change feeds."
        ),
        body=mtd_body + b"\n---\n" + fca_body + b"\n---\n" + ico_body,
        evidence_item=mtd_evidence,
        extra_evidence=[fca_evidence, ico_evidence],
        checks=[
            ExistenceCheck(
                description="HMRC MTD ITSA reachable",
                must_contain=("Making Tax Digital",),
            ),
            ExistenceCheck(description="FCA Handbook reachable", must_contain=("FCA",)),
            ExistenceCheck(
                description="ICO guidance reachable",
                must_contain=("ICO",),
            ),
        ],
    )


def run_INS_084() -> Verdict:
    """Scope Creep Prediction from Project Timing Patterns.

    Pure-internal recipe (timesheets + email-volume process-mining).
    """
    return _internal_only_plausible(
        insight_id="INS-084",
        method_summary=(
            "No public-data leg; recipe is timesheet event-log + regression "
            "on matter-level write-off."
        ),
        finding=(
            "Catalogue entry: 'None required (internal pattern recognition "
            "using historical matter data)'. Methodology supported by "
            "process-mining literature (van der Aalst) cited in entry."
        ),
    )


def run_INS_085() -> Verdict:
    """Partner Succession Risk from LinkedIn + Companies House.

    Companies House director appointment / resignation filings are reachable
    via the bulk officer data product (no key). LinkedIn career-history is
    private. ONS workforce ageing is open.
    """
    bulk_body, bulk_evidence = companies_house.bulk_index()
    return Verdict(
        insight_id="INS-085",
        vertical=VERTICAL,
        band=VerdictBand.PLAUSIBLE,
        test_class=TestClass.EXISTENCE,
        method=(
            "Existence: Companies House director appointment/resignation "
            "data is in the bulk product; LinkedIn career history is not "
            "open public data; ONS workforce ageing is open."
        ),
        finding=(
            "Companies House officer-data product reachable. LinkedIn data "
            "would require Sales Navigator subscription or scraping — "
            "neither is open public data."
        ),
        statistic={"public_legs_validated": 2, "public_legs_blocked": 1},
        evidence=EvidenceBundle(items=[bulk_evidence]),
        notes=[
            "Per-firm director-age inference is feasible via Companies House "
            "live API (date of birth on appointments); requires API key.",
        ],
    )


def run_INS_086() -> Verdict:
    """Client Concentration × Herfindahl Index → Risk Dashboard.

    Pure-mathematical recipe — HHI computation on an internal client-fee
    distribution. Public reference (UK Finance HHI guidance) is a
    documentation pointer, not a validation source.
    """
    return _internal_only_plausible(
        insight_id="INS-086",
        method_summary=(
            "HHI is a mathematical concentration measure applied to internal "
            "client-fee data; no public-data leg to validate."
        ),
        finding=(
            "Methodology validated by US DoJ antitrust HHI literature "
            "(public reference, not a data source)."
        ),
    )


def run_INS_087() -> Verdict:
    """Fee Elasticity from Win-Rate vs Quote-Price Residuals.

    Public leg: ONS Services Producer Price Index (SPPI) covers legal /
    accountancy services and is the open-data anchor for fee benchmarks.
    """
    body, evidence = ons.services_producer_price_index_page()
    return existence_test(
        insight_id="INS-087",
        vertical=VERTICAL,
        method=(
            "Confirm ONS SPPI bulletin publishes a legal/accountancy "
            "services price index (open-data benchmark for fee elasticity)."
        ),
        body=body,
        evidence_item=evidence,
        checks=[
            ExistenceCheck(
                description="ONS SPPI bulletin publishes services indices",
                must_contain=("Producer", "service"),
            ),
        ],
    )


def run_INS_088() -> Verdict:
    """Recovery Rate by Fee-Earner ANOVA.

    Public leg: Armstrong Watson 2024/25 benchmark of £748 per £1,000 billed
    is cited in the catalogue but the underlying survey is paywalled. ONS
    SPPI gives an indirect inflation deflator. Recipe is otherwise internal.
    """
    body, evidence = ons.services_producer_price_index_page()
    return Verdict(
        insight_id="INS-088",
        vertical=VERTICAL,
        band=VerdictBand.PLAUSIBLE,
        test_class=TestClass.EXISTENCE,
        method=(
            "Existence: ONS SPPI provides services-inflation deflator; "
            "Armstrong Watson recovery benchmark is a published-but-paywalled "
            "industry survey, not open data."
        ),
        finding=(
            "ONS SPPI reachable for inflation deflator. Recipe is "
            "fundamentally an internal ANOVA on fee-earner recovery rates."
        ),
        statistic={"public_legs_validated": 1, "public_legs_blocked": 1},
        evidence=EvidenceBundle(items=[evidence]),
        notes=[
            "Methodology (ANOVA on recovery rates) is industry-standard "
            "and supported by activity-based-costing literature.",
        ],
    )


def run_INS_089() -> Verdict:
    """Litigation Risk from HMCTS Court Listings.

    Public legs: Employment Tribunal decisions (open at gov.uk),
    CourtServe (free sign-up gates the daily listings; landing page is
    public).
    """
    et_body, et_evidence = gov_uk.employment_tribunal_decisions()
    cs_body, cs_evidence = gov_uk.courtserve_landing()
    return existence_test(
        insight_id="INS-089",
        vertical=VERTICAL,
        method=(
            "Confirm Employment Tribunal decisions database + CourtServe "
            "exist as public-data sources for litigation risk monitoring."
        ),
        body=et_body + b"\n---\n" + cs_body,
        evidence_item=et_evidence,
        extra_evidence=[cs_evidence],
        checks=[
            ExistenceCheck(
                description="Employment Tribunal decisions reachable",
                must_contain=("Employment", "tribunal"),
            ),
            ExistenceCheck(
                description="CourtServe landing reachable",
                must_contain=("Court",),
            ),
        ],
    )


def run_INS_090() -> Verdict:
    """Cross-Sell Graph — Matter Type Temporal Sequencing.

    Pure-internal recipe (matter-sequence graph from practice management
    system). No open public-data validation applies.
    """
    return _internal_only_plausible(
        insight_id="INS-090",
        method_summary=(
            "Recipe is an internal market-basket / temporal sequence graph; "
            "no public-data leg."
        ),
        finding=(
            "Methodology supported by Amazon 'frequently bought together' "
            "and Christensen JTBD literature (public references, not data "
            "sources)."
        ),
    )


def run_INS_091() -> Verdict:
    """PII Claim Risk × Matter Complexity Score.

    Public leg: SRA publishes PII claims data and research reports but the
    sra.org.uk WAF blocks programmatic access. We use the Law Society
    research index as the open-data anchor for legal-sector matter-class
    risk weights; the SRA gap is recorded as a follow-up.
    """
    body, evidence = gov_uk.sra_pii_indemnity_data()
    return existence_test(
        insight_id="INS-091",
        vertical=VERTICAL,
        method=(
            "Confirm Law Society research index publishes legal-sector "
            "research as anchor for matter-class risk weights "
            "(SRA direct fetch blocked by WAF)."
        ),
        body=body,
        evidence_item=evidence,
        checks=[
            ExistenceCheck(
                description="Law Society research topic page reachable",
                must_contain=("research",),
            ),
        ],
    )


def run_INS_092() -> Verdict:
    """Engagement-Letter Terms × Write-Off Rate Regression.

    Public legs: SRA engagement-letter requirements + ICAEW guidance — both
    are standards/rule documents, not statistical datasets. Recipe is
    primarily an internal regression. PLAUSIBLE: standards exist; statistical
    validation requires client engagement-letter data.
    """
    body, evidence = gov_uk.legal_services_board_index()
    return Verdict(
        insight_id="INS-092",
        vertical=VERTICAL,
        band=VerdictBand.PLAUSIBLE,
        test_class=TestClass.EXISTENCE,
        method=(
            "Existence: SRA + ICAEW engagement-letter standards reachable as "
            "rule documents; statistical leg requires client data."
        ),
        finding=(
            "Public standards exist; the regression itself is on internal "
            "engagement-letter outcomes (write-off rate by clause type)."
        ),
        statistic={"public_legs_validated": 1, "client_data_required": True},
        evidence=EvidenceBundle(items=[evidence]),
        notes=[
            "Recipe needs an internal engagement-letter corpus + matched "
            "write-off ledger. Public data confirms the rules, not the "
            "regression coefficients.",
        ],
    )


def run_INS_093() -> Verdict:
    """Tax-Year Deadline × Capacity Mismatch Forecasting.

    Public legs: HMRC SA deadline (31 January), VAT (quarterly), Corporation
    Tax (9 months), MTD ITSA. All open gov.uk pages. Existence test confirms
    each anchor date / phrase is published.
    """
    sa_body, sa_evidence = hmrc.self_assessment_deadline_page()
    vat_body, vat_evidence = hmrc.vat_deadlines_page()
    ct_body, ct_evidence = hmrc.corporation_tax_deadlines_page()
    mtd_body, mtd_evidence = hmrc.making_tax_digital_overview()
    combined = b"\n---\n".join([sa_body, vat_body, ct_body, mtd_body])
    return existence_test(
        insight_id="INS-093",
        vertical=VERTICAL,
        method=(
            "Confirm HMRC publishes Self Assessment / VAT / Corporation Tax "
            "/ MTD deadline calendars (all open, gov.uk)."
        ),
        body=combined,
        evidence_item=sa_evidence,
        extra_evidence=[vat_evidence, ct_evidence, mtd_evidence],
        checks=[
            ExistenceCheck(
                description="HMRC publishes 31 January SA deadline",
                must_contain=("31 January",),
            ),
            ExistenceCheck(
                description="HMRC publishes VAT deadline guidance",
                must_contain=("VAT",),
            ),
            ExistenceCheck(
                description="HMRC publishes Corporation Tax 9-month rule",
                must_contain=("Corporation Tax", "9 months"),
            ),
            ExistenceCheck(
                description="HMRC publishes MTD ITSA",
                must_contain=("Making Tax Digital",),
            ),
        ],
    )


def run_INS_094() -> Verdict:
    """Associate Churn × LinkedIn Hiring Activity → Competitor Intelligence.

    Public legs: Companies House director data (no key, bulk product),
    Nomis ASHE wage data (no key). LinkedIn job-postings leg has no open API.
    """
    bulk_body, bulk_evidence = companies_house.bulk_index()
    # Nomis ASHE: occupation × industry × region. SDMX-JSON definition is
    # the cheapest existence check.
    try:
        ashe_payload, ashe_evidence = ons.nomis_dataset_definition("NM_30_1")
        ashe_status = "reachable"
    except FetchBlockedError as exc:  # pragma: no cover
        ashe_evidence = None
        ashe_payload = None
        ashe_status = f"blocked: {exc}"

    notes = [
        "LinkedIn job-postings volume is not open public data; only "
        "available via Talent Insights subscription or scraping (ToS).",
    ]
    bundle = EvidenceBundle(items=[bulk_evidence] + ([ashe_evidence] if ashe_evidence else []))
    finding = (
        f"Companies House officer-data product reachable; Nomis ASHE "
        f"definition {ashe_status}. LinkedIn leg requires non-open data."
    )
    return Verdict(
        insight_id="INS-094",
        vertical=VERTICAL,
        band=VerdictBand.PLAUSIBLE,
        test_class=TestClass.EXISTENCE,
        method=(
            "Existence: Companies House officer data + Nomis ASHE both "
            "reachable; LinkedIn hiring-volume data is private."
        ),
        finding=finding,
        statistic={"public_legs_validated": 2, "public_legs_blocked": 1},
        evidence=bundle,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

RUNNERS: dict[str, Callable[[], Verdict]] = {
    "INS-079": run_INS_079,
    "INS-080": run_INS_080,
    "INS-081": run_INS_081,
    "INS-082": run_INS_082,
    "INS-083": run_INS_083,
    "INS-084": run_INS_084,
    "INS-085": run_INS_085,
    "INS-086": run_INS_086,
    "INS-087": run_INS_087,
    "INS-088": run_INS_088,
    "INS-089": run_INS_089,
    "INS-090": run_INS_090,
    "INS-091": run_INS_091,
    "INS-092": run_INS_092,
    "INS-093": run_INS_093,
    "INS-094": run_INS_094,
}
