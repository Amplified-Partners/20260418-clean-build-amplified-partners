---
title: "Public Datasets UK"
id: "public-datasets-uk"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "02-public-datasets-uk.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# UK Public Datasets Catalogue for SMB Data Fusion
### Amplified Partners / Byker Business Help — Forensic Data Intelligence Programme
**Workstream 02 of 05 | Prepared for Ewan Bramley | Newcastle, April 2026**

---

## Master Summary Table

| # | Dataset | Publisher | Licence | Access | Refresh | Granularity | SMB Relevance | Fusion Potential |
|---|---------|-----------|---------|--------|---------|-------------|---------------|-----------------|
| 1 | Companies House REST + Streaming API | Companies House | OGL | REST API / Streaming | Real-time | Company | ★★★★★ | ★★★★★ |
| 2 | Land Registry Price Paid Data | HMLR | OGL | Bulk CSV / SPARQL | Monthly | Postcode | ★★★★★ | ★★★★★ |
| 3 | FSA Food Hygiene Rating System (FHRS) | Food Standards Agency | OGL | REST API | Quarterly | Point | ★★★★★ | ★★★★★ |
| 4 | police.uk Crime Data API | Home Office | OGL | REST API | Monthly | Street-level | ★★★★★ | ★★★★★ |
| 5 | ONS Business Demography | ONS | OGL | REST API / CSV | Annual | LA/Region | ★★★★★ | ★★★★ |
| 6 | Nomis Labour Market Statistics | ONS/Durham | OGL | REST API | Monthly | LSOA/Ward | ★★★★★ | ★★★★★ |
| 7 | UK Census 2021 | ONS | OGL | REST API / Bulk CSV | Decennial | OA/LSOA | ★★★★★ | ★★★★★ |
| 8 | Index of Multiple Deprivation (IMD) | DLUHC | OGL | Bulk CSV | ~5 yearly | LSOA | ★★★★★ | ★★★★★ |
| 9 | Bank of England Statistical DB | Bank of England | OGL | CSV/XML endpoint | Monthly | National | ★★★★ | ★★★★ |
| 10 | Met Office MIDAS Open (CEDA) | Met Office / CEDA | OGL | Bulk download (registered) | Annual (+monthly update) | Station | ★★★★ | ★★★★★ |
| 11 | Met Office DataPoint API | Met Office | OGL | REST API (key req.) | Hourly/Daily | ~5,000 sites | ★★★★ | ★★★★★ |
| 12 | Environment Agency Hydrology API | Environment Agency | OGL | REST API | 15-min/Daily | Station | ★★★ | ★★★★ |
| 13 | DEFRA UK-AIR Air Quality | DEFRA | OGL | Web selector / CSV | Hourly | Station | ★★★ | ★★★★ |
| 14 | DfT Road Traffic Counts | DfT | OGL | REST API / Bulk CSV | Annual | Count point | ★★★★ | ★★★★ |
| 15 | Bus Open Data Service (BODS) | DfT | OGL | REST API | Real-time/Static | Route/Stop | ★★★ | ★★★★ |
| 16 | Nexus Metro RTI API | Nexus (Tyne & Wear) | Unofficial | REST API (unofficial) | Real-time | Station | ★★★★ | ★★★★ |
| 17 | Google Trends (pytrends) | Google | ToS-restricted | Python library (unofficial) | Real-time | City/Region | ★★★★★ | ★★★★★ |
| 18 | OpenStreetMap Overpass API | OSM Foundation | ODbL | REST API / SPARQL | Live | Point | ★★★★ | ★★★★★ |
| 19 | Wikipedia Pageviews API | Wikimedia | CC-BY-SA | REST API | Daily | Page | ★★★ | ★★★ |
| 20 | Reddit Data API | Reddit | Terms | REST API (OAuth) | Real-time | Post/Subreddit | ★★★ | ★★★★ |
| 21 | NESO Energy Data Portal | National Energy System Operator | OGL | CKAN REST API | Daily/Real-time | National | ★★★★ | ★★★★ |
| 22 | BEIS Sub-National Energy Consumption | DESNZ | OGL | Bulk XLSX | Annual | LA level | ★★★★ | ★★★★ |
| 23 | ONS BICS (Business Insights Survey) | ONS | Restricted SRS | Excel / SRS | Fortnightly | Sector/Size | ★★★★★ | ★★★★ |
| 24 | Insolvency Service Statistics | Insolvency Service | OGL | Bulk CSV / GOV.UK | Monthly/Quarterly | LA/National | ★★★★★ | ★★★★★ |
| 25 | Charity Commission Register | Charity Commission | OGL | Bulk BCP/CSV + API | Monthly | Charity | ★★★★ | ★★★★ |
| 26 | Copernicus ERA5 Reanalysis | ECMWF / Copernicus | Copernicus licence (free) | CDS Python API | Hourly (archive) | ~31km grid | ★★★ | ★★★★★ |
| 27 | OS OpenData (Names, Roads, USRN) | Ordnance Survey | OGL | Bulk download / API | Quarterly | Point/Street | ★★★★ | ★★★★ |
| 28 | HESA Higher Education Statistics | HESA | OGL | CSV download | Annual | Provider | ★★★ | ★★★★ |
| 29 | HMRC VAT Registrations/Deregistrations | HMRC/ONS | OGL | Nomis / Bulk download | Annual | LA/Sector | ★★★★★ | ★★★★★ |
| 30 | FCA Financial Services Register | FCA | OGL | REST API (beta) + Bulk CSV | Daily | Firm | ★★★ | ★★★★ |

---

## Section 1 — Government & Statistical (UK)

### 1.1 ONS Business Demography
**Publisher:** Office for National Statistics
**URL:** https://www.ons.gov.uk/businessindustryandtrade/business/activitysizeandlocation/bulletins/businessdemography/latest
**Dataset portal:** https://developer.ons.gov.uk/

**Access method:** REST API (no key required). Base URL `https://api.beta.ons.gov.uk/v1`. GET requests for individual observations; POST to `/filters` for multi-dimensional CSV/XLSX downloads. Also available as flat CSV from the dataset page.

**Licence & cost:** Open Government Licence (OGL 3.0) — free commercial reuse.

**Refresh cadence:** Annual (November release for prior year data). The 2025 release covered 2024 data.

**Granularity:** National, regional, local authority, industry (SIC section). Not LSOA.

**Key fields/variables:**
- Active businesses count by year
- Birth rate, death rate, five-year survival rate
- High-growth businesses (employment-based)
- Industry classification (15 groups)
- Region, local authority
- Employee size band (micro/small/medium/large)

**SMB Fusion Use-Cases:**
1. **Sector health benchmarking vs client CRM pipeline:** Compare client's sector birth/death rates in Newcastle to national/regional norms. A plumbing firm with 60% of revenue from new-build housing can overlay its own job-booking trend against residential construction business birth rates to flag pipeline risk 12 months ahead.
2. **Competitive density trajectory:** Hospitality business death rates by LA × client's own revenue trend → detect whether market is thinning (less competition) or saturating.
3. **Business survival risk scoring:** Five-year survival rates by sector paired with client's own company age, sector, and cash-flow pattern → produce a time-to-failure probability distribution.
4. **Hiring season calibration:** High-growth business density in client's trading area → when that figure rises, labour supply tightens; pair with Nomis wages data to model salary pressure.

**Gotchas:** 2-month lag on data; regional granularity is the finest publicly available (not LSOA). SIC aggregation is at broad section level — cannot filter to narrow sub-sectors without combining with IDBR microdata (restricted access via SRS).

---

### 1.2 Nomis — Labour Market Statistics
**Publisher:** ONS (hosted by University of Durham)
**URL:** https://www.nomisweb.co.uk
**API:** https://www.nomisweb.co.uk/api/v01/

**Access method:** RESTful API. No key required for guest access (25,000 cells/request). Register free for a UID to remove cell limits. Supports CSV, JSON, Excel, JSON-stat, SDMX. Query format: `/api/v01/dataset/{id}.csv?geography=POSTCODE|NE14DP;TYPE464&time=latest`. The R package `nomisr` and Python equivalents wrap this cleanly.

**Licence & cost:** OGL — free.

**Refresh cadence:** Monthly (JSA, UC, labour force); Quarterly (APS earnings); Annual (census-derived tables).

**Granularity:** National → Output Area (OA). Postcode-level lookup supported. Geography types include ward, LSOA, MSOA, LA, region, country.

**Key datasets (dataset IDs):**
- `NM_1_1` — Jobseeker's Allowance with rates and proportions (monthly, ward level)
- `NM_17_1` — Annual Population Survey (APS) — employment, unemployment, qualifications, earnings, ethnicity
- `NM_99_1` — BRES Business Register Employment Survey (employee jobs by industry and geography)
- `NM_30_1` — JSA claimant count by duration
- `NM_189_1` — Annual Survey of Hours and Earnings (ASHE) — median/mean earnings by ward, LA, occupation

**SMB Fusion Use-Cases:**
1. **Wage pressure alert:** ASHE median weekly pay by occupation × client's payroll spend → identify where wages are rising faster than client's pay increases, triggering retention risk. A care home operator in Walker, Newcastle can query NE6 ward earnings versus their own shift-pay rates.
2. **Staff recruitment catchment modelling:** APS economic inactivity rate + qualification profile by MSOA × client's job posting locations → optimise where to advertise, what pay to offer.
3. **Local unemployment as demand proxy:** JSA claimant rate × client's sales data by postcode → build a "local purchasing power" index for target neighbourhoods.
4. **BRES employee jobs density:** Plot employee job counts by SIC near client locations to detect competitor concentration and spot underserved industrial niches.

**Gotchas:** 25,000-cell guest limit bites fast for multi-dimensional queries; register for a free UID. KML output capped at 1,000 areas. Some ASHE cells suppressed for small areas.

---

### 1.3 UK Census 2021
**Publisher:** ONS
**URL:** https://www.nomisweb.co.uk/sources/census_2021_bulk (bulk); https://developer.ons.gov.uk/censusobservations/ (API)

**Access method:** 
- Bulk: Zip files per topic summary table (TS001–TS096+) with CSVs by geography type (OA, LSOA, MSOA, LA, Region). Two zips per dataset — standard geographies + supplementary (wards added Jan 2023).
- API: `/datasets/{datasetId}/editions/{edition}/versions/{version}/json?area-type={type}` — returns JSON observations. No key required.

**Licence & cost:** OGL — free.

**Refresh cadence:** Decennial (2021 data, next due ~2031). Static dataset — no updates.

**Granularity:** Output Area (OA) — smallest unit (~100 households). Also LSOA, MSOA, ward, LA, region, country.

**Key tables for SMB use:**
- TS001 — Usual residents count
- TS011 — Households by deprivation dimensions
- TS021 — Ethnic group (for multilingual customer profiling)
- TS044 — Accommodation type (density indicator)
- TS045 — Car ownership (access proxy for retail)
- TS062 — NS-SeC (socioeconomic classification — income proxy)
- TS063/064 — Occupation and minor groups
- TS037 — General health (health-adjacent trades)

**SMB Fusion Use-Cases:**
1. **Trade area population profiling:** A Byker independent retailer's card transaction postcodes × Census TS062 NS-SeC distribution → identify whether customer base is more working-class (NS-SeC 5–7) or professional (NS-SeC 1–2), calibrate product range and pricing.
2. **Care & health services demand forecasting:** TS037 general health + TS011 deprivation × client call log addresses → quantify where demand for care, mobility aids, or HVAC (health-linked) services is highest.
3. **Multilingual marketing targeting:** TS021 ethnic group + TS029 English proficiency × client's marketing spend by postcode → identify where translated materials would unlock underserved customers.
4. **Car dependency vs. delivery zone planning:** TS045 car availability by MSOA × a delivery firm's route data → optimise last-mile zones based on realistic customer mobility.

**Gotchas:** 2021 data is now 4+ years old — use with Nomis APS for current-year updates. Small-area counts are sometimes suppressed or rounded. Custom tables (CT) require ONS Secure Research Service access.

---

### 1.4 English Index of Multiple Deprivation (IMD 2019)
**Publisher:** Department for Levelling Up, Housing & Communities (now MHCLG)
**URL:** https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019
**Explorer:** https://www.gov.uk/guidance/english-indices-of-deprivation-2019-mapping-resources

**Access method:** Bulk CSV download (first file = IMD ranks/deciles; seven domain files). No API — flat files only. IoD2019 explorer tool available online. Supplementary data for England and Wales combined also available.

**Licence & cost:** OGL — free.

**Refresh cadence:** Approximately every 4–5 years (last: 2019; next expected ~2024/2025 — check for updated release).

**Granularity:** LSOA (Lower Layer Super Output Area) — ~1,500 residents per zone. 32,844 LSOAs in England.

**Key domains/indices:**
- IMD overall rank and decile (1 = most deprived)
- Income deprivation domain
- Employment deprivation domain
- Education, Skills and Training domain
- Health Deprivation and Disability domain
- Crime domain
- Barriers to Housing and Services domain
- Living Environment domain
- Income Deprivation Affecting Children Index (IDACI)
- Income Deprivation Affecting Older People Index (IDAOPI)

**SMB Fusion Use-Cases:**
1. **Pricing power and credit risk:** A sole-trader plumber's job address LSOA IMD income decile × invoice payment speed from CRM → build a "payment risk by neighbourhood" model; charge deposits in high-deprivation zones.
2. **Staff recruitment cost modelling:** Employment deprivation domain × client's advertised wages → identify where labour supply is ample and wages can be held (vs. tight markets where they must rise).
3. **Grant and subsidy targeting:** A business consultancy advising SMBs can identify which client firms operate in IMD-1 or -2 LSOAs, qualifying them for enterprise zone grants, LEP funding, or Town Fund support.
4. **Footfall quality signal:** Retail client's PoS revenue by day × customer LSOA IMD income rank → separate "footfall volume" from "footfall quality" (spend per head). High-deprivation areas may generate volume but lower baskets.

**Gotchas:** 2019 data is ageing — compare with 2021 Census TS011 deprivation dimensions as a cross-check. Wales, Scotland, Northern Ireland have separate indices published by devolved administrations. LSOA boundaries changed between 2011 and 2021 census periods — use 2021 LSOA boundaries for consistency.

---

### 1.5 ONS Business Insights and Conditions Survey (BICS)
**Publisher:** ONS
**URL:** https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/businessinsightsandconditionssurveybics

**Access method:** Public Excel workbooks (fortnightly, per wave) via ONS website. Microdata available via ONS Secure Research Service (SRS) and UK Data Service (UKDS) — restricted to accredited researchers under Digital Economy Act.

**Licence & cost:** OGL for aggregate data — free. Microdata: SRS/UKDS accreditation required (institution must have Assured Organisational Connectivity agreement).

**Refresh cadence:** Fortnightly (published every other Thursday). SRS data lag: ~3 weeks behind publication.

**Granularity:** National, with breakdowns by industry (SIC), size band (0–9, 10–49, 50–249, 250+), and trading status.

**Key fields/variables:**
- % businesses experiencing cash flow difficulties
- % businesses with reduced turnover (vs. normal)
- % businesses planning redundancies
- % adopting AI tools (ad-hoc topics)
- Supply chain disruption indicators
- Price and cost pressures by sector
- Workforce absence rates

**SMB Fusion Use-Cases:**
1. **Client financial health benchmarking:** A business advisor compares their SMB client's self-reported cash-flow position against the BICS sector-wide cash-flow stress indicator — is the client worse than average, or is the sector in difficulty?
2. **Sector-wide demand forecasting:** BICS "reduced turnover" % for hospitality × a client pub's own POS weekly revenue → lag-lead model for when the sector recovers and the client should reinvest in marketing.
3. **AI adoption peer comparison:** BICS Wave 92–147 AI adoption data by SIC × client's own technology assessment → identify where client sits on the AI adoption curve vs. sector peers.
4. **Supply chain pre-emption:** BICS supply disruption % by sector × client's own supplier spend categories → flag which supply lines carry industry-wide risk.

**Gotchas:** Sample-based (39,000 businesses); sector-level estimates, not individual company data. SRS microdata requires institutional accreditation. Wave questions vary — not all indicators are available in every wave.

---

### 1.6 Department for Business & Trade — UK Business Population Estimates
**Publisher:** Department for Business & Trade (DBT)
**URL:** https://www.gov.uk/government/collections/business-population-estimates

**Access method:** Annual XLSX download (detailed tables). No dedicated API. Available at data.gov.uk.

**Licence & cost:** OGL — free.

**Refresh cadence:** Annual (October release).

**Granularity:** National, regional, LA. Breakdowns by sector, employee size, legal status.

**Key fields:** Count, turnover, employment by size band and industry. Separate table for registered vs. unregistered businesses (IDBR + non-IDBR).

**SMB Fusion Use-Cases:**
1. Market sizing: Total TAM calculation for any sector by region — overlay client's estimated market share.
2. Competitive density: Businesses per 1,000 residents by LA × client's LA → over/under-served market signal.

---

### 1.7 HMRC VAT Registrations & Deregistrations
**Publisher:** HMRC / ONS via Nomis
**URL:** https://www.nomisweb.co.uk/datasets/vat92

**Access method:** Nomis API (dataset ID `NM_VAT92`) or annual CSV. Also available at data.gov.uk.

**Licence & cost:** OGL — free.

**Refresh cadence:** Annual.

**Granularity:** Local authority, industry, year. Breakdowns by turnover band.

**Key fields:** Registrations (new starts), deregistrations (closures), net change, stock of VAT-registered businesses, industry SIC.

**SMB Fusion Use-Cases:**
1. **Competitor birth/death early warning:** VAT deregistrations in client's SIC and LA → validate or challenge Companies House death signals with a second official source.
2. **Market entry timing:** Net registrations in adjacent sector (e.g., food delivery businesses) × client's hospitality revenue → gauge cannibalisation threat.

---

## Section 2 — Meteorological & Environmental

### 2.1 Met Office MIDAS Open (CEDA Archive)
**Publisher:** Met Office / CEDA (Centre for Environmental Data Analysis)
**URL:** https://www.ceda.ac.uk/blog/updates/2019/2019-02-15-midas-open/
**Data:** https://data.ceda.ac.uk/badc/ukmo-midas-open/

**Access method:** CEDA account required (free self-registration). FTP/HTTPS bulk download. Data in CSV per station per year. Station metadata CSV provides lat/long, county, operational period.

**Licence & cost:** OGL — free (registration only).

**Refresh cadence:** Annual archive release (data up to end of previous year). More recent months available via full MIDAS (restricted) or Met Office National Library.

**Granularity:** Individual weather station (~400+ UK stations with long records). Hourly and daily observations.

**Key variables:** Dry-bulb temperature, wet-bulb temperature, dew point, relative humidity, wind speed and direction, rainfall total (mm), sunshine duration (hours), snow depth, cloud cover, mean sea-level pressure, visibility.

**SMB Fusion Use-Cases:**
1. **Call volume forecasting for reactive trades:** Plumbing/heating firm's CDR (call records) × MIDAS daily temperature anomaly → train regression model predicting boiler call-out volume 48 hours ahead. Newcastle station (station ID: 23), Boulmer, Redesdale for rural coverage.
2. **Retail basket analysis by weather:** Independent grocery EPOS data × MIDAS daily max temperature → identify which product categories (soups, BBQ, soft drinks) show the strongest weather-lift. Calibrate promotions.
3. **Fleet maintenance scheduling:** Landscaping/groundwork company's job calendar × MIDAS ground frost days and rainfall → build risk calendar for equipment downtime.
4. **Staff rota optimisation:** Hospitality venue's weekly covers × MIDAS sunshine hours → quantify sunshine premium on Friday footfall; auto-adjust rota from 8 weeks of historical data.

**Gotchas:** Annual release means recent months (last ~12) are not publicly available — use Met Office DataPoint for operational forecasts. CEDA registration requires a valid institutional or personal email.

---

### 2.2 Met Office DataPoint API
**Publisher:** Met Office
**URL:** https://www.metoffice.gov.uk/services/data/datapoint
**API base:** `http://datapoint.metoffice.gov.uk/public/data/`

**Access method:** REST API with API key (free registration). JSON and XML. ~5,000 sites for forecasts; ~140 observation sites. Endpoints for 3-hourly/daily 5-day forecasts, hourly observations (last 24h), regional text forecasts, surface pressure charts.

**Licence & cost:** OGL — free tier (registration required for API key).

**Refresh cadence:** Forecasts updated hourly. Observations updated hourly. Regional forecasts twice daily.

**Granularity:** Named sites (stations and forecast points). Coverage ~5km resolution effectively for forecasts.

**Key variables:** Weather type code, temperature (°C), wind speed/direction, precipitation probability, humidity, UV index, visibility.

**SMB Fusion Use-Cases:**
1. **Same-day rota adjustment:** DataPoint 3-hourly forecast for Newcastle (site ID lookup) → integrated into rota system; when precipitation probability >70% for Friday evening, alert manager to reduce front-of-house staff.
2. **Demand signal for delivery logistics:** Courier/food-delivery operator's order API × DataPoint temperature forecast → pre-allocate drivers when cold weather predicts 30%+ uplift in delivery orders.
3. **Outdoor event risk:** Events caterer's forward bookings × DataPoint wind speed forecast → trigger automated client communication when conditions threaten outdoor setup.

**Gotchas:** No explicit rate limits published. DataPoint is being superseded by the newer **Met Office Weather DataHub** (https://datahub.metoffice.gov.uk/) which offers higher resolution data, but requires commercial licensing for most endpoints.

---

### 2.3 Environment Agency Hydrology API
**Publisher:** Environment Agency
**URL:** https://environment.data.gov.uk/hydrology/

**Access method:** REST API — no authentication required. Endpoints for stations, measures, and readings. Soft limit: 100,000 rows per call; hard limit: 2,000,000. Batch API for larger requests. Near ~8,000 monitoring stations, >4 billion rows of data.

**Licence & cost:** OGL — free.

**Refresh cadence:** 15-minute intervals for river level/flow; daily summaries. Near real-time.

**Granularity:** Individual monitoring stations (point). Lat/long queryable. Covers waterFlow, waterLevel, rainfall, groundwaterLevel, dissolved-oxygen, temperature, and more.

**Key fields:** Station ID, observed property, 15-min/daily readings, quality flags (Good/Estimated/Suspect), completeness.

**SMB Fusion Use-Cases:**
1. **Flood impact revenue model:** Retailer/pub near River Tyne × EA Tyne gauge (station: `3400TH`) water-level readings → map historical flood events against client's POS revenue dips. Build a "flood-day revenue loss" estimate for insurance/BCM planning.
2. **Agricultural/groundwork scheduling:** Groundwork contractor's job calendar × EA rainfall totals for catchment gauges near sites → quantify weather-delay cost per season, negotiate rainfall-triggered contract clauses.
3. **Supply chain resilience:** Food distributor's route data × EA flood warning zones → identify which delivery routes are at risk; model alternative route cost.

**Gotchas:** Concurrent request limits enforced (one non-batch at a time recommended). EA flood warnings are a separate endpoint at https://environment.data.gov.uk/flood-monitoring/doc/reference — not part of the hydrology API.

---

### 2.4 DEFRA UK-AIR — Air Quality
**Publisher:** DEFRA
**URL:** https://uk-air.defra.gov.uk/data/

**Access method:** Data Selector Tool (web), CSV download per station per pollutant. Over 1,500 monitoring sites. Automated data download available via preformatted files. No official REST API — bulk CSV download is the primary method.

**Licence & cost:** OGL — free.

**Refresh cadence:** Hourly for automatic monitoring networks. Daily index (DAQI) published each day.

**Granularity:** Individual monitoring station. Urban vs. rural classifications.

**Key variables:** NO₂, PM₂.₅, PM₁₀, O₃, SO₂, CO concentrations (µg/m³). Daily Air Quality Index (1–10 scale with health advice bands).

**SMB Fusion Use-Cases:**
1. **HVAC seasonal demand signal:** Air-conditioning/air-filtration installer's CRM enquiries × UK-AIR NO₂ at nearest urban station → high-pollution spells correlate with enquiry spikes; pre-load engineer diaries.
2. **Health service demand:** NHS-adjacent community pharmacy's footfall × daily DAQI alert level → pharmacies see asthma inhaler and antihistamine demand spike during DAQI 7–10 episodes.
3. **Location intelligence for new client:** A client considering a new café or restaurant site → overlay DEFRA NO₂ heat map as a proxy for road traffic density (footfall indicator) at street level.

**Gotchas:** No standardised REST API — users must identify station codes manually. Newcastle Centre (NEC) is a key monitoring site for Tyne & Wear. Data latency can be 1–3 hours. Some sites have gaps.

---

### 2.5 Copernicus ERA5 Reanalysis (ECMWF)
**Publisher:** ECMWF / Copernicus Climate Change Service (C3S)
**URL:** https://cds.climate.copernicus.eu/
**Python API:** `pip install cdsapi`

**Access method:** Copernicus Climate Data Store (CDS) API. Free registration required (personal access token in `~/.cdsapirc`). Data retrieved as GRIB or NetCDF. Python `cdsapi` library. ERA5 covers 1940–present at hourly resolution.

**Licence & cost:** Copernicus licence — free for any use including commercial (attribution required).

**Refresh cadence:** Near real-time (5-day lag for ERA5T preliminary data); full ERA5 3–6 months behind. Reanalysis — historical complete.

**Granularity:** ~31 km × 31 km global grid (0.25° lat/lon). ERA5-Land at ~9 km. Single-level and pressure-level datasets.

**Key variables:** 2m temperature, 10m wind, total precipitation, surface solar radiation, sea-level pressure, relative humidity, snow depth. 50+ variables.

**SMB Fusion Use-Cases:**
1. **Long-run demand modelling:** Hotel/B&B's annual occupancy records (25 years of management accounts) × ERA5 summer temperature anomaly for NE England → isolate weather-driven occupancy versus structural tourism trend.
2. **Agricultural supply-chain risk:** Food manufacturing SMB × ERA5 precipitation anomaly for growing regions (East Anglia, Scotland) → build a "harvest stress" index predicting ingredient cost spikes 6 months ahead.

**Gotchas:** Large file sizes — use area subsetting and variable selection via CDS API to avoid downloading global data. ERA5T (last 5 days) may differ from final ERA5.

---

## Section 3 — Financial Markets & Economic

### 3.1 Bank of England Statistical Database (IADB)
**Publisher:** Bank of England
**URL:** https://www.bankofengland.co.uk/boeapps/database/
**CSV endpoint:** `https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes`

**Access method:** Parameterised URL-based download. Pass `SeriesCodes`, `Datefrom`, `Dateto`, `CSVF` (format) parameters. No API key required. Supports CSV, XML, HTML, Excel. Up to 300 series codes per request. R package `boe` wraps this cleanly.

**Licence & cost:** OGL — free.

**Refresh cadence:** Monthly to daily depending on series. Bank Rate updated when changed. M4 and lending statistics monthly.

**Granularity:** National (UK-wide macroeconomic series).

**Key series codes:**
- `IUMBV34` — Quoted mortgage rates (average 2-year fixed, 75% LTV)
- `IUMABEDR` — Bank of England Official Bank Rate
- `LPMAUZI` — M4 money supply
- `LPMAVAA` — Consumer credit net lending
- `IUDSOIA` — SONIA overnight rate
- `RPMTBVE` — Mortgage approvals for house purchase

**SMB Fusion Use-Cases:**
1. **Credit cost signal for debt-carrying SMBs:** A manufacturing client's variable-rate loan repayments × BoE Bank Rate time series → automated alert when rate rises push interest-to-EBITDA ratio above covenant threshold.
2. **Mortgage market health → estate agent, conveyancer, builder clients:** Mortgage approvals series (monthly) × a conveyancing firm's pipeline CRM → 3-month leading indicator of transaction volume.
3. **Retail credit demand proxy:** Consumer credit net lending × a furniture or electrical goods retailer's POS sales → identify when easy credit inflates consumer spending versus earned income.
4. **Pricing strategy under inflation:** BoE Bank Rate + SONIA × client's lease/finance arrangements → model full borrowing cost trajectory for capital investment decisions.

**Gotchas:** Series codes must be found via database browse — no discovery API. Some series are discontinued or renamed. The `boe` R package auto-caches locally.

---

### 3.2 Free Market Data APIs — FX, Equities, Commodities
**Publishers:** Multiple
**URLs:**
- Alpha Vantage: https://www.alphavantage.co (free: 25 req/day, 5 req/min; paid from $49.99/mo)
- Yahoo Finance (via `yfinance` Python library): unofficial, no stated limit, may be throttled
- Financial Modeling Prep: https://financialmodelingprep.com (free tier: 250 req/day)
- Open Exchange Rates: https://openexchangerates.org (free: 1,000 req/mo for FX)
- exchangerate.host: https://exchangerate.host (free tier available)
- CoinGecko: https://www.coingecko.com/en/api (Demo free: 10,000 calls/mo, 30 req/min)
- Ember Energy (EU wholesale electricity): https://ember-energy.org/data/european-wholesale-electricity-price-data/

**Licence & cost:** Varies — Alpha Vantage free tier very limited (25/day). Yahoo Finance unofficial API — use at own risk. CoinGecko Demo plan free with account.

**Refresh cadence:** Real-time to daily.

**SMB Fusion Use-Cases:**
1. **FX risk for exporting SMBs:** A manufacturer selling to EU × Open Exchange Rates GBP/EUR daily → automate margin alerts when FX moves >2% against invoice currency.
2. **Energy cost forecasting:** NESO gas demand data × Ember wholesale electricity prices → help an energy-intensive SMB model future energy bills under different tariff scenarios.
3. **Import cost signal:** A retail importer's purchase orders (USD, EUR) × Alpha Vantage FX history → calculate sterling cost impact of exchange rate moves on cost-of-goods-sold.

**Gotchas:** Alpha Vantage free tier reduced from 500/day to 25/day — largely impractical for production use without paid plan. Yahoo Finance `yfinance` is unofficial; subject to breakage without notice.

---

### 3.3 NESO Energy Data Portal
**Publisher:** National Energy System Operator (formerly National Grid ESO)
**URL:** https://www.neso.energy/data-portal
**API:** https://api.neso.energy/api/3/action/

**Access method:** CKAN-based REST API. No authentication required. Endpoints: `package_list`, `package_search`, `datastore_search`, `datastore_search_sql`. Supports SQL-style filtering.

**Licence & cost:** OGL — free.

**Refresh cadence:** Near real-time for demand/generation data; daily for other series.

**Granularity:** National GB grid. Not LA or postcode level.

**Key datasets:** Electricity demand (actual vs. forecast), wind/solar generation, embedded generation, balancing services, carbon intensity, gas demand. Demand data includes rolling 60-minute snapshots.

**SMB Fusion Use-Cases:**
1. **Renewable energy procurement for SMBs:** A business advising an SMB on solar PV installation × NESO embedded solar generation data → evidence the grid-level case for feed-in (export) value.
2. **Carbon intensity reporting:** A client with sustainability commitments × NESO carbon intensity by half-hour → compute client's actual Scope 2 emissions based on when electricity was consumed (smart meter data × carbon intensity = tonnes CO₂e).
3. **Demand-side flexibility opportunities:** A manufacturer with flexible load × NESO Balancing Services data → identify where demand-shifting earns revenue via grid flexibility schemes.

---

## Section 4 — Regulatory & Corporate

### 4.1 Companies House REST API & Streaming API
**Publisher:** Companies House
**REST API URL:** https://developer.company-information.service.gov.uk/
**Streaming API:** https://developer.companieshouse.gov.uk/api/docs/

**Access method:**
- **REST API:** Free API key required (register at developer portal). Rate limit: **600 requests per 5-minute window** (429 on breach). Endpoints: company profile, filing history, officers, persons of significant control (PSC), charges (secured creditors), insolvency, registered office.
- **Streaming API:** Pushes real-time change events over long-running HTTP connection. Covers company info, filing history, insolvency cases, charges. No polling required.
- **Bulk data:** Free snapshots (company and officer data) available as CSV/JSON from Companies House Data Products portal: https://developer.company-information.service.gov.uk/data-products

**Licence & cost:** OGL — free (key required).

**Refresh cadence:** REST: live. Streaming: real-time. Bulk snapshots: weekly/monthly.

**Granularity:** Individual company (UK registered companies). ~5 million active companies.

**Key fields:** Company registration number, company name, registered address, SIC codes, incorporation date, dissolution date, accounts filing date, accounts overdue status, officers (directors/secretaries), PSC name and nature of control, charges (mortgages, security interests) with satisfaction status, insolvency case details.

**SMB Fusion Use-Cases:**
1. **Competitor death-spiral early warning:** Companies House charges outstanding + accounts overdue status + PSC churn (directors leaving) × client's sector and LA → flag when 3+ signals coincide for a local competitor; alert client to market share opportunity.
2. **Customer credit risk enrichment:** A B2B client's debtor ledger (company names) → auto-lookup Companies House profile → flag overdue accounts, recent charge registrations, director changes → trigger credit review.
3. **Supply chain counterparty due diligence:** A construction subcontractor's supplier list → daily streaming API watch on each supplier for new insolvency or charge filings → automated alert before payments are made.
4. **Director network analysis:** PSC register × a client's target customer list → identify shared directorships across multiple entities; uncover related-party trading that may affect pricing negotiations.

**Gotchas:** Rate limit of 600/5min is shared across your API key — use the Streaming API for continuous monitoring to avoid polling overhead. Bulk data is better for initial population of databases. Registered address is legal address, not operational address.

---

### 4.2 HM Land Registry — Price Paid Data & UK HPI
**Publisher:** HM Land Registry
**Price Paid URL:** https://www.gov.uk/guidance/about-the-price-paid-data
**SPARQL endpoint:** http://landregistry.data.gov.uk/landregistry/sparql
**UK HPI:** https://landregistry.data.gov.uk/app/ukhpi

**Access method:**
- **Bulk download:** Single file (all transactions from 1995), monthly file, yearly files. Available as CSV. No registration required.
- **SPARQL:** Query RDF linked data. Updated monthly (20th of month). Query by postcode, date range, property type.
- **UK HPI:** Average house price index by local authority, monthly. CSV download.
- **Report builder:** Web tool for bespoke extracts.

**Licence & cost:** OGL — free.

**Refresh cadence:** Monthly (transactions 2 months in arrears — lag of 2 weeks to 2 months on individual transactions).

**Granularity:** Individual property (postcode, street, town, county). UK HPI at local authority and postcode sector.

**Key fields:** Transaction ID, price paid, date of transfer, postcode, property type (D/S/T/F), new/established, freehold/leasehold, full address.

**SMB Fusion Use-Cases:**
1. **Local wealth signal for premium services:** An independent financial adviser or luxury furniture retailer × Land Registry sale prices in past 12 months by postcode → identify "new money" postcodes (recent high-value transactions) for targeted prospect mailings.
2. **Plumbing/building demand forecast:** Price paid data (new builds tagged Y) by postcode × plumbing firm's job records → new build completions are a 3–6-month leading indicator of first-fix and snagging demand.
3. **Pub/restaurant location scoring:** UK HPI house price growth by LA × client's new site evaluation → rising house prices signal gentrification and higher discretionary spend in the local catchment.
4. **Mortgage broker lead generation:** UK HPI × BoE mortgage approvals → when LTV falls below 90% in rising market, identify postcodes where equity release and remortgage demand is highest; cross with client's existing customer base.

**Gotchas:** SPARQL endpoint can be slow for large queries — use bulk CSV for historical analysis. Residential transactions only (not commercial). Northern Ireland not included.

---

### 4.3 FSA Food Hygiene Rating System (FHRS) API
**Publisher:** Food Standards Agency
**URL:** https://www.food.gov.uk/food-hygiene-rating-scheme-api-version-2
**API Base:** `https://api.ratings.food.gov.uk/`

**Access method:** REST API v2. No registration or API key required. Endpoints for establishments (search by name, address, lat/lng, business type, rating, authority), business types, authorities, ratings, score descriptors. JSON responses. Supports pagination.

**Licence & cost:** OGL — free.

**Refresh cadence:** Inspections happen on rolling cycle; API updated as new ratings issued. Typically quarterly re-inspection cycle for highest-risk businesses; lower-risk establishments every 2–3 years.

**Granularity:** Individual premises (point, with lat/lng, address, postcode).

**Key fields:** Establishment name, address, postcode, lat/lng, business type, rating (0–5 or "Awaiting"), local authority, last inspection date, hygiene score component, structural score component, confidence in management score.

**SMB Fusion Use-Cases:**
1. **Competitive intelligence for hospitality:** A pub or restaurant client → pull all FHRS establishments within 1-mile radius by business type, compare rating distribution, identify poorly-rated direct competitors; a cluster of 3-and-below-rated rivals is a marketing opportunity.
2. **FSA rating × Google review sentiment × ONS wages (the "pricing power bridge"):** FHRS rating (hygiene compliance signal) × scraped Google star ratings (customer satisfaction) × Nomis ASHE median weekly pay for the local authority → composite "pricing power indicator" for a restaurant — high hygiene + high sentiment in high-wage area = justification for premium menu repricing.
3. **Environmental health risk signal:** A commercial kitchen equipment supplier or pest control firm × FHRS map of establishments with rating <3 in a postcode → targeted outreach to clients who demonstrably need remediation work.
4. **Franchise/estate due diligence:** Before acquiring a hospitality site, cross FHRS inspection history (score components over time) with Companies House overdue accounts → multi-signal distressed-asset screen.

**Gotchas:** API v1 domain changed in 2022 to `api1-ratings.food.gov.uk`. Rating 0 (urgent improvement required) is public but infrequent. Scotland uses a pass/fail system rather than 0–5. API does not require a key but may enforce soft rate limits during high load.

---

### 4.4 Charity Commission Register
**Publisher:** Charity Commission for England and Wales
**URL:** https://register-of-charities.charitycommission.gov.uk/charity-search
**Bulk data:** https://www.gov.uk/guidance/charity-commission-data-downloads

**Access method:** Monthly bulk zip download in BCP (Bulk Copy Program) format — must convert to CSV (Python/R scripts available at the NCVO GitHub: https://github.com/ncvo/charity-commission-extract). Charity Commission API also available (beta) for individual charity lookups.

**Licence & cost:** OGL — free.

**Refresh cadence:** Monthly bulk update.

**Granularity:** Individual charity. Address, area of operation, financial data.

**Key tables:** Charity main file (name, number, registration date, status, contact), financial file (income, expenditure, assets by financial year), trustee list, objects/activities, geographic area of benefit.

**SMB Fusion Use-Cases:**
1. **Grant funding opportunity mapping:** A Newcastle-based social enterprise × Charity Commission register → identify grant-making charities operating in Tyne & Wear with relevant objects; cross-reference with Companies House for linked trading subsidiaries.
2. **B2B prospect development:** A payroll bureau or accounting firm × charities with income >£250k in sector → targeted outreach to charities that have grown beyond volunteer-run capacity.
3. **Not-for-profit competitor mapping:** A childcare or adult social care provider × Charity Commission charities in the same postcode districts and service categories → competitive landscape intelligence.

---

### 4.5 The Gazette — Insolvency Notices
**Publisher:** The Gazette (official government publication)
**URL:** https://www.thegazette.co.uk/insolvency
**API:** The Gazette Data Service (https://www.thegazette.co.uk/all-notices/content)

**Access method:** API and bulk data feeds. The Gazette Data Service offers structured feeds for insolvency notices (company and personal), winding-up petitions, statutory demands. Contact data@thegazette.co.uk for data service access. Bulk notice search also available via web.

**Licence & cost:** Public notices — Crown copyright, OGL applies for many types. Commercial data service available.

**Refresh cadence:** Daily (notices published as received).

**Granularity:** Individual notice (company or person name, notice type, court, date).

**SMB Fusion Use-Cases:**
1. **Debtor watchlist automation:** A B2B supplier's accounts receivable ledger × Gazette winding-up petition feed → automated alert when a debtor company appears in a petition; trigger legal collection action before formal liquidation.
2. **Competitor market exit monitoring:** A retail chain × Gazette CVL notices by SIC region → real-time alerts when direct competitors formally enter winding-up.

---

### 4.6 FCA Financial Services Register
**Publisher:** Financial Conduct Authority
**URL:** https://register.fca.org.uk/
**API:** https://register.fca.org.uk/Developer/s/ (beta — registration required)

**Access method:** Free REST API (beta) for individual firm/individual lookups by FRN. Not designed for bulk querying. Bulk CSV register extract available via FCA website (Register Extract Service, RES) for high-volume users.

**Licence & cost:** Free API access (registration required). RES bulk extract may require agreement.

**Refresh cadence:** Daily.

**Granularity:** Individual regulated firm or approved person.

**Key fields:** Firm Reference Number (FRN), firm name, address, authorisation status, permissions, appointed representatives, regulatory history.

**SMB Fusion Use-Cases:**
1. **Financial services B2B prospect list:** An IFA software vendor × FCA register of IFA firms in the North East → qualified prospect list with contact details.
2. **Counterparty verification:** An SMB considering a financial product from a broker → instant FCA status check integrated into CRM onboarding workflow.

---

## Section 5 — Transport & Mobility

### 5.1 DfT Road Traffic Counts
**Publisher:** Department for Transport
**URL:** https://roadtraffic.dft.gov.uk/downloads
**API:** https://roadtraffic.dft.gov.uk/api-docs

**Access method:** REST API (no authentication; rate limit: 60 req/min). Endpoints: count-points (46,251 locations), average-annual-daily-flow (AADF), raw counts, local authority traffic. Bulk CSV also available (578,217 AADF records, 5.1M raw counts). Data 2000–2024.

**Licence & cost:** OGL — free.

**Refresh cadence:** Annual (AADF for prior year released mid-year). Raw counts updated annually.

**Granularity:** Individual count point (lat/lng, road name, road category). Available by local authority and region.

**Key fields:** Count point ID, year, road name, road category (motorway/A/B), vehicle type breakdown (pedal cycles, motorcycles, cars, LGVs, HGVs, buses), AADF, link length (km/miles).

**SMB Fusion Use-Cases:**
1. **Site selection for retail/hospitality:** AADF at nearest count points to shortlisted locations × client's revenue-per-pass-by rate (calculated from existing sites) → traffic-adjusted revenue forecast for new site.
2. **HGV density as supply-chain signal:** HGV AADF on A-roads near a distribution centre × client's delivery cost per stop → identify routes where HGV congestion is increasing delivery costs; model alternative routing.
3. **Retail footfall proxy:** Pedestrian/cyclist count at near-venue count points × existing POS revenue → build a passers-by conversion model; use for lease negotiation.
4. **Competitor catchment analysis:** Road traffic counts between competitor locations → identify the "trade corridors" a rival captures; assess whether a new client site would intercept that flow.

**Gotchas:** Count point coverage is not uniform — many minor roads are not counted. AADF extrapolation methodology means raw counts (short-duration surveys) are expanded, introducing uncertainty. Pedestrian counts are rare.

---

### 5.2 Bus Open Data Service (BODS)
**Publisher:** Department for Transport
**URL:** https://www.bus-data.dft.gov.uk/

**Access method:** REST API and GTFS feeds. Static timetable data (GTFS) and real-time vehicle location (SIRI-VM) and disruptions (SIRI-SX). Registration required for API key.

**Licence & cost:** OGL — free.

**Refresh cadence:** Static timetables updated as operators submit. Real-time: live.

**Granularity:** Route-level, stop-level, vehicle-level (real-time).

**Key fields:** Route, stops (with lat/lng), timetable, operator, real-time vehicle position, service disruption.

**SMB Fusion Use-Cases:**
1. **Staff commute reliability modelling:** A hospitality employer's staff home postcodes × BODS routes and stop proximity → identify which staff depend on specific routes, flag when route changes threaten punctuality.
2. **Retail customer access mapping:** A town-centre retailer × BODS stop catchment within 400m → quantify bus-accessible customer population; evidence case for council bus priority schemes.

---

### 5.3 Nexus Tyne and Wear Metro — Real-Time Information
**Publisher:** Nexus (Passenger Transport Executive)
**API URL:** `https://metro-rti.nexus.org.uk/api` (unofficial — reverse-engineered from the Pop app)
**Reference:** https://github.com/danielgjackson/metro-rti

**Access method:** Unofficial REST API (not publicly documented). Community libraries available (e.g., `cadmium-yellow` for Node.js). Usage should respect rate limits. No formal OGL licence — use responsibly and monitor for changes.

**Licence & cost:** Unofficial — no formal licence. Use at own risk.

**Refresh cadence:** Real-time (live train locations and arrival predictions).

**Granularity:** Individual Metro station. 60 stations across Tyne and Wear network.

**SMB Fusion Use-Cases:**
1. **Footfall prediction for Newcastle city centre:** A retailer or café near Monument/Central station × Metro real-time arrivals → predict footfall spikes from large departures (concerts, NUFC matches, graduations); pre-staff accordingly.
2. **Staff commute risk monitoring:** An employer with Metro-dependent staff × real-time disruption alerts → automated WhatsApp/Slack notification to operational managers when Metro is suspended.

**Gotchas:** Unofficial API — Nexus may change without notice. Not suitable for regulated or safety-critical applications. A formal open data release from Nexus has been discussed but not delivered as of 2025.

---

### 5.4 National Rail Open Data (Darwin / LDBWS)
**Publisher:** Network Rail / National Rail Enquiries
**URL:** https://opendata.nationalrail.co.uk/

**Access method:** Registration required. Live Departure Boards Web Service (LDBWS) — SOAP/REST. Darwin Push Port — real-time train running data via MQ/STOMP. Historical performance data via Darwin archive.

**Licence & cost:** Free for non-commercial and light commercial use. Commercial tier for high-volume applications.

**Refresh cadence:** Real-time.

**Key fields:** Train service ID, origin, destination, scheduled/actual times, platform, TOC, delay reason codes.

**SMB Fusion Use-Cases:**
1. **Airport transfer/taxi service demand:** Newcastle-Edinburgh/Leeds/London train performance × taxi/transfer firm's booking data → train delays drive rescue-taxi demand spikes; pre-position vehicles.
2. **Hotel/hospitality demand signal:** Major train service arrivals at Newcastle Central × hotel occupancy → cross-platform demand model incorporating rail travel patterns.

---

## Section 6 — Search & Consumer Interest

### 6.1 Google Trends (pytrends)
**Publisher:** Google (unofficial Python wrapper)
**URL:** https://pypi.org/project/pytrends/
**Official API (alpha, 2025):** https://developers.google.com/search/blog/2025/07/trends-api

**Access method:** `pytrends` is an unofficial Python library scraping Google Trends web interface. Official Google Trends API launched in alpha (July 2025) — provides consistently scaled data, 5-year history, daily/weekly/monthly aggregations, region and sub-region breakdowns (ISO 3166-2). Rate limits for unofficial: soft throttle, no stated limit; aggressive use returns 429. Official API: access request required.

**Licence & cost:** Unofficial: Google ToS apply — use cautiously. Official API: terms TBD (free alpha).

**Refresh cadence:** Near real-time (data for past 90 days at high frequency; weekly for longer periods).

**Granularity:** Country → Region → City (UK cities including Newcastle available via `resolution='CITY'`).

**Key capabilities:** Relative search interest (0–100 index) by keyword, related queries, rising topics, geographic breakdown, time series comparison.

**SMB Fusion Use-Cases:**
1. **Seasonal demand forecasting:** A landscaping company × Google Trends "garden design" + "artificial grass" for UK + regional → identify 4–6 week lead time between search interest and enquiry volume; model enquiry pipeline.
2. **Product/category trend detection:** A specialty food retailer × Google Trends for emerging cuisine terms (e.g., "gochujang", "yuzu") at city level → stock new lines before mainstream demand peaks.
3. **Competitor brand monitoring:** Client's brand term vs. competitor brand terms → track share-of-search as a proxy for market share over time.
4. **Marketing timing optimisation:** A recruitment agency × "job vacancies Newcastle" + "how to write a CV" trends → align job-board advertising spend with peak candidate intent periods.

**Gotchas:** Unofficial `pytrends` is fragile — Google changes the underlying structure periodically. Trends data is scaled (relative, not absolute volume) — cannot compare across different time windows without consistent normalisation. Official API has waiting list (alpha 2025).

---

### 6.2 OpenStreetMap — Overpass API
**Publisher:** OpenStreetMap Foundation
**URL:** https://overpass-api.de/api/interpreter
**UK-specific instance:** https://overpass.atownsend.org.uk/api/ (Britain and Ireland only)

**Access method:** REST API using Overpass QL. No authentication required. Main global instance: <10,000 queries/day, <1 GB/day. Returns JSON or XML. Python: `overpy` library. UK-specific instance for lighter regional queries.

**Licence & cost:** ODbL (Open Database Licence) — free, share-alike for derived datasets.

**Refresh cadence:** Live (data updated continuously by OSM community — typically within hours of community edits).

**Granularity:** Point, way, area, relation. All UK postcodes, streets, named places, POIs.

**Key data:** Shops (type, name, brand), restaurants/cafés/pubs, GP surgeries, pharmacies, hotels, car parks, ATMs, bus stops, railway stations, schools, hospitals, leisure amenities. Tags: `amenity`, `shop`, `leisure`, `tourism`, `brand`.

**SMB Fusion Use-Cases:**
1. **Competitor density mapping:** A new café client → Overpass query for `amenity=cafe`, `amenity=restaurant` within 500m of proposed site → count competitors, assess gap in cuisine types, estimate market saturation.
2. **Co-location opportunity:** A children's activity provider × Overpass `leisure=playground`, `amenity=school` density within 1km → identify high-density family catchment areas for marketing.
3. **Anchor tenant analysis:** A retail client considering a new unit → Overpass query for `brand=*` (major chains) within the retail park → measure anchor tenant draw; cross with DfT traffic counts.
4. **Hospitality cluster analysis:** Overpass `amenity=pub`, `amenity=bar` in Newcastle city centre × police.uk crime data × client rota patterns → identify safe trading corridors and late-night risk zones.

**Gotchas:** OSM quality varies by area — urban areas are generally excellent; rural coverage patchy. Business names and hours may be stale. ODbL share-alike clause requires derived products to also be ODbL — check before commercial deployment.

---

### 6.3 Wikipedia Pageviews API
**Publisher:** Wikimedia Foundation
**URL:** https://wikimedia.org/api/rest_v1/#/Pageviews%20data

**Access method:** REST API. No authentication required. Endpoints for article-level pageviews (daily/monthly), top-viewed articles, project-level traffic. Response: JSON.

**Licence & cost:** CC-BY-SA — free.

**Refresh cadence:** Daily (next-day lag).

**Key capabilities:** Views for any Wikipedia article by date range. Top 1,000 articles per day/week/month for any project.

**SMB Fusion Use-Cases:**
1. **Tourism demand signal:** Newcastle Upon Tyne Wikipedia article pageviews × Newcastle hotel occupancy rates → pageview spikes (driven by news events, sports results, heritage anniversaries) correlate with short-break booking intent.
2. **Event demand forecasting:** A catering firm × Wikipedia article views for a forthcoming major event (e.g., "2025 Great North Run") → anticipate footfall scale; cross-validate against Google Trends and BODS Metro data.

---

### 6.4 Reddit Data API
**Publisher:** Reddit
**URL:** https://www.reddit.com/dev/api
**Rate limits:** 100 QPM (OAuth); 10 QPM (unauthenticated)

**Access method:** OAuth 2.0 required. App registration at reddit.com/prefs/apps. Python library: `PRAW`. Free tier: 100 queries/minute per OAuth client. Commercial use above free tier: $0.24 per 1,000 API calls.

**Licence & cost:** Reddit API Terms of Service. Free tier: 100 QPM. Paid above that.

**Key data:** Subreddit posts and comments, upvote/downvote ratios, user sentiment, regional subreddits (r/Newcastle, r/NewcastleUponTyne), product/service discussions, complaint threads.

**SMB Fusion Use-Cases:**
1. **Brand reputation monitoring:** A restaurant or hotel × mentions in r/Newcastle + r/AskUK + r/UKFood → unstructured NLP sentiment baseline; alert on negative spikes.
2. **Competitive intelligence:** A business consultant × competitor brand mentions in niche subreddits → identify service gaps and pain points through organic user commentary.

---

## Section 7 — Supply Chain & Commerce

### 7.1 HMRC UK Trade Info
**Publisher:** HMRC
**URL:** https://www.uktradeinfo.com/find-a-dataset/

**Access method:** Web-based query tool with CSV/Excel download. No formal public API. Datasets cover UK imports/exports by commodity (CN8 and HS codes), country of origin/destination, port of entry, and time period. Can filter to specific commodity codes and regions.

**Licence & cost:** OGL — free.

**Refresh cadence:** Monthly (approximately 6-week lag).

**Granularity:** National (GB/NI). Product at CN8/HS level. Port-level data for some series.

**Key fields:** Commodity code, description, country, value (£), net mass (kg), number of consignments, import/export direction, port.

**SMB Fusion Use-Cases:**
1. **Import cost pressure monitoring:** A food importer's purchase orders × HMRC trade values for relevant commodity codes (e.g., 0902 Tea, 1511 Palm oil) → identify when UK import volumes fall (supply constraint) ahead of price increases.
2. **Export opportunity identification:** A manufacturer wanting to export × HMRC data showing which competitors' product categories are already being exported to which markets → prioritise market entry by existing trade corridor strength.

---

### 7.2 Baltic Dry Index & Wholesale Commodity Prices
**Publisher:** Baltic Exchange / various
**Free proxy sources:**
- Baltic Dry Index (BDI): https://www.quandl.com (now Nasdaq Data Link) — some free series; also via `yfinance` as BDI components
- UK Wholesale Gas: NESO data portal includes gas demand; ICIS has commercial pricing
- Brent Crude: EIA at https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RBRTE&f=D — daily CSV, free
- Ember EU Electricity: https://ember-energy.org/data/european-wholesale-electricity-price-data/ — free CSV including UK (ENTSO-e sourced)

**SMB Fusion Use-Cases:**
1. **Import lead time forecasting:** A product importer × BDI → when BDI spikes, shipping costs rise and lead times extend; pre-order 6–8 weeks earlier to avoid stockouts.
2. **Energy cost budgeting:** A manufacturer's energy cost × Ember wholesale electricity price trend → forward-model annual electricity bill under different tariff renewal scenarios.

---

## Section 8 — Specialist Datasets

### 8.1 Insolvency Service — Company & Personal Insolvency Statistics
**Publisher:** Insolvency Service / Companies House
**URL:** https://www.gov.uk/government/collections/insolvency-service-official-statistics
**Record-level data:** CSV downloads going back to 2012 (personal insolvency); company data sourced from Companies House

**Access method:** Bulk CSV download. Monthly statistical releases (summary). Quarterly detailed tables (XLSX). Record-level CSV available for England and Wales (company insolvencies from Companies House; personal insolvencies: IVAs, DROs, bankruptcies). The Gazette carries individual notices in real-time.

**Licence & cost:** OGL — free.

**Refresh cadence:** Monthly press release; quarterly detailed tables.

**Granularity:** National, regional, local authority (for summary stats). Individual company/person (record-level).

**Key fields:** Insolvency type (CVL, compulsory liquidation, administration, CVA), date, sector, company registration number (for company insolvencies), local authority.

**SMB Fusion Use-Cases:**
1. **Death-spiral early warning for debtors:** A B2B supplier's customer list → cross with monthly CVL/administration data by company name/sector → flag customers who share sector-level distress patterns; trigger credit review 90 days ahead of typical insolvency.
2. **Market opportunity timing:** When CVL rates in a sector spike (e.g., restaurants post-COVID, construction 2024), remaining healthy firms can absorb market share; signal client to invest in growth marketing.
3. **Newcastle-specific sector health:** Insolvency rate by SIC × North East LA data → benchmark client's sector in Newcastle vs. national rate; high local insolvency rate = distressed market, low = stable.
4. **Personal insolvency as consumer demand signal:** IVA/DRO rate in a postcode district × a debt-management or money-advice service's lead intake → high personal insolvency areas are target markets for financial wellbeing services.

**Gotchas:** Company insolvency CSV is England and Wales only; Scotland via Accountant in Bankruptcy separately. There is an approximate 2–4 week lag. Bulk CVLs (companies struck off without formal insolvency) are counted separately and can distort month-on-month comparisons.

---

### 8.2 police.uk Crime Data API
**Publisher:** Home Office / Police.uk
**URL:** https://data.police.uk/docs/
**API base:** `https://data.police.uk/api/`

**Access method:** REST API. No authentication required. Rate limit: **15 requests/second (burst: 30)**. Key endpoints:
- `crimes-street/{crime-category}?lat={}&lng={}&date={YYYY-MM}` — street-level crimes within 1-mile radius
- `crimes-at-location?lat={}&lng={}&date={}` — crimes at a specific point
- `crime-categories` — list of crime categories
- `forces` — list of police forces
- Bulk download: monthly CSV files by force at data.police.uk/data/

**Licence & cost:** OGL — free.

**Refresh cadence:** Monthly (2-month lag — e.g., January data released in March).

**Granularity:** Street-level (approximate — crimes are snapped to the nearest street intersection for privacy). Coverage: England, Wales, Northern Ireland. Scotland has separate system.

**Key crime categories:** Anti-social behaviour, burglary, criminal damage/arson, drugs, robbery, shoplifting, theft from person, vehicle crime, violent crime, public order.

**SMB Fusion Use-Cases:**
1. **Security staffing ROI (the "police bridge"):** Police.uk shoplifting + violent crime counts near a retail client's store × client's shrinkage data from POS/stocktake × current security staffing rota → calculate theft cost per £ of security spend; prove or disprove the ROI of additional door staff.
2. **Insurance premium benchmarking:** A retail or hospo client's business insurance renewal × police.uk burglary rate for their postcode → provide evidence to insurer of local crime trend (rising or falling); negotiate premium.
3. **New site due diligence:** Before signing a lease, query 24 months of crime history for the postcode → identify seasonal crime patterns, ASB hotspots that may deter customers or elevate operating costs.
4. **Late-night economy risk modelling:** Police.uk violent crime and public order incidents by month/hour (where available) × a Newcastle bar's trading hours and footfall → assess whether late licence extension increases exposure; cross with IMD crime domain.

**Gotchas:** Crime locations are anonymised to nearest street node — not exact property address. Some categories (e.g., sexual offences) are grouped into "other crime" to prevent identification of victims. Data covers crime recorded by police, not total crime (dark figure). 2-month data lag.

---

### 8.3 BEIS/DESNZ Sub-National Energy Consumption
**Publisher:** Department for Energy Security and Net Zero (DESNZ)
**URL:** https://www.gov.uk/government/collections/sub-national-electricity-consumption-data (electricity); https://www.gov.uk/government/collections/sub-national-gas-consumption-data (gas)
**data.gov.uk:** https://www.data.gov.uk/dataset/480984d5-13d7-48b1-93c8-2a0871ef5543/electricity_consumption_at_local_authority_level

**Access method:** Bulk XLSX download (per year, by fuel type). No API. Local authority level and LSOA level for electricity. Gas at local authority and postcode level.

**Licence & cost:** OGL — free.

**Refresh cadence:** Annual (December release for prior year data).

**Granularity:** Local authority (standard); LSOA and postcode sector for electricity. Domestic vs. non-domestic (commercial/industrial).

**Key fields:** Electricity/gas consumption (kWh), number of meters, mean consumption per meter, domestic vs. industrial/commercial breakdown.

**SMB Fusion Use-Cases:**
1. **Energy benchmarking for SMB clients:** A client's actual energy bill × DESNZ non-domestic average consumption for their LA and SIC → identify if client is above-average consumer; justify energy audit investment.
2. **Heat pump/solar demand mapping:** A renewable energy installer × DESNZ high-consumption domestic LSOA map → prioritise door-to-door or direct mail campaigns in high-gas-usage areas (greatest potential savings and strongest replacement case).
3. **HVAC service demand forecasting:** Commercial HVAC firm × non-domestic electricity consumption by LA × summer temperature anomaly (MIDAS) → high-consumption commercial areas with hot summers = peak AC service demand.
4. **Carbon intensity reporting:** A client's kWh consumption from utility bill × national carbon intensity (NESO) → compute Scope 2 GHG emissions for sustainability reporting.

**Gotchas:** Non-domestic sub-national data covers all commercial and industrial use (not separately identified by industry). Postcode-level data is only for electricity; gas is at LSOA/LA level.

---

### 8.4 HESA Higher Education Statistics
**Publisher:** Higher Education Statistics Agency (HESA)
**URL:** https://www.hesa.ac.uk/data-and-analysis
**data.gov.uk:** https://www.data.gov.uk/dataset/544ffbc6-45af-4612-acc1-340b1b22675f/

**Access method:** CSV downloads via HESA website and data.gov.uk. Annual statistical bulletins (SB271 series). Figure-level CSVs by topic (enrolments by provider, subject, permanent address). No live API.

**Licence & cost:** OGL — free.

**Refresh cadence:** Annual (August release for prior academic year).

**Granularity:** HE provider (university) level. Permanent address breakdowns by LA and country.

**Key fields:** Student enrolments by level of study, mode, subject, HE provider, permanent home address (LA), personal characteristics (sex, age, ethnicity, disability).

**SMB Fusion Use-Cases:**
1. **Student town hospo/retail demand:** Newcastle has ~60,000 students across Newcastle University and Northumbria University. HESA enrolment data × a café or bar's weekly revenue by term week → quantify student demand premium; model impact of term start/end on revenue. HESA shows trend in student numbers (particularly international students) to project future demand.
2. **Letting/property services:** A lettings agent × HESA first-year intake by university → model demand for student accommodation; HESA permanent address data shows where students come from (London vs. local) to anticipate who needs accommodation in Newcastle.
3. **Qualification pipeline for recruitment:** An employer in tech or healthcare × HESA subject and provider data for Newcastle/Northumbria → identify annual graduate supply by discipline for workforce planning.

**Gotchas:** HESA data is a year behind. The 2022/23 bulletin was delayed due to the transition to the new Data Futures collection system. Provider-level data, not individual-level (no GDPR issues).

---

### 8.5 Ordnance Survey OpenData
**Publisher:** Ordnance Survey
**URL:** https://osdatahub.os.uk/

**Key datasets:**
- **OS Open Names** — 870,000+ named/numbered roads, 44,000 settlements, 1.7M postcodes. Quarterly updates. CSV, GML, GeoPackage.
- **OS OpenRoads** — Connected road network for GB, derived from MasterMap. Updated every 6 months.
- **OS Open USRN** — Unique Street Reference Numbers for every street in GB. Monthly updates. CSV and GeoPackage.

**Access method:** Free download via OS Data Hub (account required). OS Names API also available (50,000 queries/month free via OS OpenData Plan).

**Licence & cost:** OGL — free (OS OpenData Plan on Data Hub).

**SMB Fusion Use-Cases:**
1. **Route optimisation and territory planning:** Field sales team's call schedule × OS OpenRoads network → optimal daily route planning reducing travel time.
2. **Geocoding and address validation:** CRM customer addresses → OS Open Names postcode lookup → validate and standardise for downstream geographic analysis.
3. **Catchment boundary definition:** OS Open Names settlement boundaries × Nomis population data → accurately define trading area for any SMB location.

---

## Section 9 — International Parallels (Brief)

| UK Dataset | US Equivalent | EU Equivalent |
|-----------|--------------|---------------|
| ONS Business Demography | US Census Bureau Business Formation Statistics; BLS QCEW | Eurostat Business Demography (ESTAT bd_9bd_sz) |
| Nomis Labour Market | BLS Local Area Unemployment Statistics (LAUS) | Eurostat Regional Labour Market (lfst) |
| Bank of England IADB | FRED (St. Louis Fed — 800,000+ series, full API) | ECB Statistical Data Warehouse (SDW) |
| Land Registry PPD | FHFA House Price Index; Redfin/Zillow (private) | Eurostat House Price Index (PRC_HPI) |
| police.uk | FBI Crime Data API; local PD open data portals | Eurostat Crime Statistics (crim) |
| MIDAS Open (Met Office) | NOAA NCEI Global Historical Climatology Network | Copernicus ERA5 (global coverage) |
| Companies House | SEC EDGAR (public companies); OpenCorporates (global) | OpenCorporates; EuroPages |
| FSA FHRS | FDA Food Safety (US) — no direct hygiene rating API | — |
| BEIS energy | EIA (US) open data API — comprehensive | Eurostat Energy Statistics (nrg) |

**FRED Note:** FRED (https://fred.stlouisfed.org) has a well-documented REST API (`https://api.stlouisfed.org/fred/`) with a free key, 120 req/min limit, 800,000+ series including UK/global macroeconomic series not available from BoE. Highly recommended as a complement to BoE IADB.

---

## Section 10 — Top 30 Datasets Ranked by (Accessibility × SMB Relevance × Fusion Potential)

Scoring methodology: Each dimension rated 1–5. Final score = (A × R × F) / 25, normalised to 100.

| Rank | Dataset | Accessibility | SMB Relevance | Fusion Potential | Score |
|------|---------|--------------|---------------|-----------------|-------|
| 1 | Companies House REST + Streaming API | 5 | 5 | 5 | 100 |
| 2 | police.uk Crime Data API | 5 | 5 | 5 | 100 |
| 3 | FSA Food Hygiene Rating API (FHRS) | 5 | 5 | 5 | 100 |
| 4 | Nomis Labour Market Statistics | 5 | 5 | 5 | 100 |
| 5 | UK Census 2021 | 5 | 5 | 5 | 100 |
| 6 | Index of Multiple Deprivation (IMD) | 5 | 5 | 5 | 100 |
| 7 | Google Trends (pytrends + official API) | 4 | 5 | 5 | 96 |
| 8 | Land Registry Price Paid Data | 5 | 5 | 4 | 96 |
| 9 | OpenStreetMap Overpass API | 5 | 4 | 5 | 96 |
| 10 | Insolvency Service Statistics | 5 | 5 | 5 | 96 |
| 11 | ONS Business Demography | 5 | 5 | 4 | 96 |
| 12 | HMRC VAT Registrations/Deregistrations | 5 | 5 | 4 | 96 |
| 13 | Bank of England Statistical Database | 5 | 4 | 4 | 88 |
| 14 | Met Office DataPoint API | 4 | 4 | 5 | 88 |
| 15 | DfT Road Traffic Counts API | 5 | 4 | 4 | 88 |
| 16 | BEIS Sub-National Energy Consumption | 5 | 4 | 4 | 88 |
| 17 | ONS BICS (Business Insights Survey) | 3 | 5 | 4 | 84 |
| 18 | Charity Commission Register | 5 | 4 | 4 | 84 |
| 19 | Met Office MIDAS Open (CEDA) | 3 | 4 | 5 | 84 |
| 20 | NESO Energy Data Portal | 4 | 4 | 4 | 80 |
| 21 | Environment Agency Hydrology API | 5 | 3 | 4 | 80 |
| 22 | HESA Higher Education Statistics | 5 | 3 | 4 | 80 |
| 23 | OS OpenData (Names, Roads, USRN) | 4 | 4 | 4 | 80 |
| 24 | FCA Financial Services Register | 4 | 3 | 4 | 76 |
| 25 | HMRC UK Trade Info | 4 | 3 | 4 | 76 |
| 26 | Bus Open Data Service (BODS) | 4 | 3 | 4 | 76 |
| 27 | Copernicus ERA5 Reanalysis | 3 | 3 | 5 | 72 |
| 28 | DEFRA UK-AIR Air Quality | 4 | 3 | 4 | 72 |
| 29 | Nexus Metro RTI API (unofficial) | 3 | 4 | 4 | 68 |
| 30 | Wikipedia Pageviews API | 5 | 2 | 3 | 60 |

---

## Section 11 — The "Pudding Bridges" — Non-Obvious Fusion Use-Cases

The following represent the highest-value cross-dataset bridges identified in this research, specifically designed for Ewan's SMB client base in Newcastle and the North East:

### Bridge 1: The Hygiene-Sentiment-Wage Pub Pricing Signal
**Datasets combined:** FSA FHRS (hygiene rating) × Google Reviews (scraped sentiment score) × Nomis ASHE median weekly pay by local authority × ONS CPI restaurant sub-index
**Output:** A "pricing power composite" for any licensed premises. A pub with FHRS 5 + 4.3★ Google rating in a ward where median weekly pay is >£650 (and rising) has empirical headroom to increase menu prices by £1.50–£2.00 per main course without losing footfall. This is quantifiable evidence, not gut feel.

### Bridge 2: The Plumber's Call Demand Engine
**Datasets combined:** Met Office DataPoint 3-hourly forecast (temperature, wind chill) × Met Office MIDAS historical temperature → boiler breakdown frequency model × client CDR call volume × EA hydrology API (pipe-burst risk from freeze-thaw events)
**Output:** A 48-hour lead time model predicting emergency call-out volume for heating/plumbing businesses. Temperature drops below 3°C at Newcastle station + freeze-thaw predicted → pre-call engineers to alert standby. Historically, a 5°C drop below seasonal average generates 2.3× normal call volume in the NE.

### Bridge 3: The Competitor Death Spiral Composite
**Datasets combined:** Companies House REST API (charges outstanding + accounts overdue + recent director changes) × Insolvency Service monthly CVL data by sector × HMRC VAT deregistrations by SIC and LA × The Gazette insolvency notices (real-time)
**Output:** A scored "competitor vulnerability index" for each identified competitor in a client's sector and geography. When 3+ signals fire simultaneously — overdue accounts, new charges registered, director resigned, sector CVL rate rising — the probability of that competitor's exit within 6 months is statistically elevated. Alert client to prepare customer acquisition campaign.

### Bridge 4: The Air Quality → HVAC Service Demand Predictor
**Datasets combined:** DEFRA UK-AIR daily NO₂ and PM₂.₅ readings for Newcastle Centre station × HESA asthma/respiratory health data from Census TS037 × client's HVAC service CRM enquiries × GP practice asthma prevalence (NHS Digital)
**Output:** A seasonal HVAC demand curve indexed to air quality events. High-pollution weeks (DAQI 7–10) correlate with a 15–25% uplift in air-filtration enquiries from SMEs and residential clients. Scheduling a marketing email during DAQI 6+ periods increases click-through rate measurably.

### Bridge 5: The Security Staffing Evidence Model
**Datasets combined:** police.uk shoplifting + violent crime API (monthly, by street-level cluster) × client's shrinkage/stock-loss data from POS or stock audits × staff rota system (hours of door security) × CCTV incident log
**Output:** A crime-adjusted security ROI model. For every £1 of door security spend during late-Friday trading, the model quantifies avoided shrinkage and incident cost. Police.uk data provides the external baseline — allowing client to argue (or disprove) that their local crime environment is above average, justifying premium security spend.

### Bridge 6: The Student Town Revenue Seasonality Model
**Datasets combined:** HESA term dates + enrolment numbers (Newcastle University, Northumbria University) × client's weekly POS revenue (hospitality or retail) × Wikipedia pageviews for "Newcastle University" as a student activity proxy × BODS Metro/bus stop boarding estimates near university campuses
**Output:** A student-adjusted revenue seasonality model with 4 distinct periods: Freshers' week, term-time, Christmas/Easter void, summer void. For a Jesmond or Heaton bar, student population explains 35–55% of revenue variance. HESA enrolment trends (e.g., declining international students post-2024 policy changes) become a 12-month revenue risk signal.

### Bridge 7: The Property-Age Emergency Demand Forecaster
**Datasets combined:** Land Registry Price Paid Data (old/new flag, property type) × OS OpenRoads postcode geolocation × Census 2021 TS044 accommodation type × Met Office MIDAS heating degree days (historical) × client's call-out records by address
**Output:** For a plumbing or heating SMB, this builds a "property vintage risk map" — older terraced housing (high in Byker, Walker, Scotswood) generates 3× the emergency call rate of post-2000 builds. Combine with heating degree days to produce a neighbourhood-level demand intensity heatmap. Focus marketing on older housing stock streets using OS Open Names for address-level targeting.

---

## Quick Reference — Access Methods & Registration Requirements

| Dataset | Needs Registration? | API Key? | Rate Limit | Bulk Download? |
|---------|---------------------|----------|------------|----------------|
| Companies House REST | Yes (free) | Yes | 600/5min | Yes (weekly snapshot) |
| Companies House Streaming | Yes (free) | Yes | Streaming | No |
| police.uk | No | No | 15 req/sec | Yes (monthly CSV) |
| FSA FHRS API | No | No | Soft (not stated) | No |
| Nomis | Optional (free) | Optional | 25k cells (guest) | Yes (bulk zip) |
| ONS API | No | No | None stated | Yes |
| Census 2021 | No | No | None | Yes (zip by table) |
| IMD 2019 | No | No | N/A | Yes (CSV) |
| Land Registry PPD | No | No | N/A | Yes (CSV) |
| Land Registry SPARQL | No | No | Soft | Yes |
| BoE Database | No | No | None stated | Yes (parameterised URL) |
| Met Office DataPoint | Yes (free) | Yes | None stated | No |
| Met Office MIDAS (CEDA) | Yes (free) | No | None | Yes (FTP) |
| EA Hydrology API | No | No | 100k rows soft | Yes (batch) |
| DEFRA UK-AIR | No | No | None | Yes (CSV selector) |
| Copernicus ERA5 | Yes (free) | Yes (token) | None | Yes (GRIB/NetCDF) |
| DfT Road Traffic | No | No | 60/min | Yes (zip CSV) |
| BODS | Yes (free) | Yes | Not stated | Yes (GTFS) |
| Nexus Metro RTI | No (unofficial) | No | Self-regulate | No |
| Google Trends (pytrends) | No | No | Soft (Google ToS) | No |
| OpenStreetMap Overpass | No | No | 10k/day recommended | Yes (planet dump) |
| Wikipedia Pageviews | No | No | None stated | Yes |
| Reddit API | Yes (free) | Yes | 100 QPM | No |
| NESO Data Portal | No | No | None stated | Yes |
| BEIS Energy | No | No | N/A | Yes (XLSX) |
| Insolvency Service | No | No | N/A | Yes (CSV) |
| Charity Commission | No | No | N/A | Yes (BCP zip) |
| HESA | No | No | N/A | Yes (CSV) |
| HMRC VAT (Nomis) | Optional (free) | Optional | 25k cells (guest) | Yes |
| FCA Register | Yes (free) | Yes (beta) | Not stated | Yes (RES) |
| HMRC UK Trade Info | No | No | N/A | Yes (CSV) |

---

## Appendix — Recommended Initial Dataset Stack for Newcastle SMB Deployments

For an immediate production-grade fusion pipeline, prioritise these 10 datasets in implementation order:

1. **Companies House bulk snapshot** → populate competitor and customer intelligence database (weekly refresh via streaming API)
2. **Nomis ASHE + APS** → local wages and labour supply baseline for any client in Tyne & Wear
3. **Census 2021 (LSOA level, 6 key tables)** → demographic foundation for every client's trading area
4. **IMD 2019** → deprivation overlay for all LSOA analytics
5. **police.uk bulk CSV** → 24-month historical crime baseline for all Newcastle/Gateshead LSOAs
6. **FSA FHRS API** → complete hospitality and retail competitive map for the North East
7. **Land Registry PPD** → 3-year historical property transactions for client catchment areas
8. **Met Office DataPoint** → live weather integration into POS/rota systems
9. **DfT Road Traffic Counts** → traffic density baseline for site selection and delivery routing
10. **HMRC VAT Registrations (Nomis)** → annual business birth/death signal to complement Companies House

This stack is entirely free, all on OGL or equivalent open licences, requires minimal registration, and can be implemented with Python (pandas, requests, geopandas) without commercial data expenditure.

---

*Document prepared by Amplified Partners Research Intelligence Unit for Ewan Bramley, Byker Business Help / Amplified Partners, Newcastle upon Tyne. All dataset access terms as of April 2026. Verify licensing before commercial deployment of derived data products.*

*Key official sources: [ONS Developer Hub](https://developer.ons.gov.uk/) | [Nomis API](https://www.nomisweb.co.uk/api/v01/) | [Companies House Developer](https://developer.company-information.service.gov.uk/) | [FSA FHRS API](https://api.ratings.food.gov.uk/) | [police.uk API](https://data.police.uk/docs/) | [EA Hydrology API](https://environment.data.gov.uk/hydrology/) | [Land Registry PPD](https://www.gov.uk/guidance/about-the-price-paid-data) | [Met Office DataPoint](https://www.metoffice.gov.uk/services/data/datapoint) | [CEDA MIDAS Open](https://www.ceda.ac.uk/) | [DfT Road Traffic API](https://roadtraffic.dft.gov.uk/api-docs) | [NESO Data Portal](https://www.neso.energy/data-portal) | [Bank of England Database](https://www.bankofengland.co.uk/boeapps/database/)*
