# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""HM Land Registry — Commercial and Corporate Ownership Data (CCOD).

Free, no key required. CCOD is published monthly as a single CSV.
Used for INS-063 (commercial voids as neighbourhood demand signal).

Service docs: https://use-land-property-data.service.gov.uk/datasets/ccod

The dataset page hosts a single canonical 'download all' link that resolves to
a snapshot CSV. We use the open service rather than the registered-user route.
"""
from __future__ import annotations

from .common import fetch_text, Fetched

# Canonical service page (HTML — used to discover the current CSV link).
SERVICE_PAGE = "https://use-land-property-data.service.gov.uk/datasets/ccod"

# Stable Land Registry SPARQL endpoint for queries against the open Price Paid
# linked-data graph (used for retail-postcode area health proxies if needed).
SPARQL = "https://landregistry.data.gov.uk/landregistry/query"


def service_page() -> Fetched:
    """Fetch the CCOD service page so we can discover the current download URL."""
    return fetch_text("land_registry", SERVICE_PAGE)


def sparql_query(query: str, accept: str = "text/csv") -> Fetched:
    """Run a SPARQL query against the Land Registry open data endpoint."""
    return fetch_text(
        "land_registry",
        SPARQL,
        params={"query": query},
        headers={"Accept": accept},
    )


# Example: count commercial-postcode price-paid transactions over time as a
# retail-area-health proxy. Restricting to category B (other / non-residential).
PRICE_PAID_BY_POSTCODE_DISTRICT = """
PREFIX ppd: <http://landregistry.data.gov.uk/def/ppi/>
PREFIX text: <http://jena.apache.org/text#>
SELECT ?year (COUNT(*) AS ?n)
WHERE {
  ?txn a ppd:TransactionRecord ;
       ppd:transactionDate ?date ;
       ppd:propertyAddress ?addr ;
       ppd:categoryType <http://landregistry.data.gov.uk/def/ppi/standardPriceCategoryB> .
  ?addr ppd:postcode ?pc .
  FILTER(STRSTARTS(?pc, "%(district)s "))
  BIND(YEAR(?date) AS ?year)
}
GROUP BY ?year
ORDER BY ?year
"""
