# palantir-wars-ice-programs.md
## Internal Research Note — Priority 7 Source
## Status: hypothesis pending corroboration by Priority 1-4 sources
## Compiled: 2026-04-22

---

## ICE / DHS Programs

### ICM — Investigative Case Management (2013–present)
- Original FALCON contract: 2014, awarded to ICE's Homeland Security Investigations (HSI) division
- Built on Palantir's proprietary platform "configured specifically for ICE's operational needs"
- Core function: gives every ICE agent access to a network of federal and private databases — cell location, air travel (APIS), SEVIS (student visas), field interview records
- Total ICM contract value (2011–2025): $287M in awards

### ImmigrationOS (2025–2027)
- **April 2025:** ICE awards Palantir a $30M sole-source (no-bid) contract
- ICE justification: "urgent and compelling need"; Palantir is "only source" capable of delivery in time; "deep institutional knowledge of ICE operations"
- Platform delivers a **prototype by September 25, 2025**; contract runs through September 2027
- Three functions:
  1. **Targeting/enforcement prioritization** — streamlines decisions on who gets removed first (violent criminals, visa overstays, gang affiliations)
  2. **Self-deportation tracking** — "near real-time visibility" on people voluntarily leaving
  3. **Logistics/lifecycle management** — streamlines process "from identification to removal"
- Pulls from IRS, Social Security, passport databases, license plates, and other federal systems
- Built on top of existing ICM — expansion of infrastructure Palantir has controlled since 2013
- ICM contract ballooned to $145M+ including ImmigrationOS funding
- **December 2025:** Palantir wins additional USCIS contract — now on both enforcement (ICE) and benefits (USCIS) sides of immigration system
- **February 2026:** DHS signs $1B contract with Palantir for software/services supporting immigration enforcement

**Total Palantir federal contracts since Trump inauguration (Jan 2025):** $1.3B+ across 14+ agencies

**Civil liberties concerns (ACLU, Amnesty, NYU Stern):**
- No public information on system accuracy
- No independent oversight or Congressional debate before deployment
- Errors can lead to detention, loss of status, wrongful deportation
- System could be expanded to target any American
- CNN: ImmigrationOS allows agents to "approve raids, book arrests, generate legal documents, and route individuals to deportation flights or detention — all from a single interface"

---

## Maven Smart System — DoD / War Programs

### Project Maven History
- Created 2017 using Google technology; Google withdrew 2018 after 4,000+ employee protests
- Palantir takes primary role in commercializing Maven capabilities

### Maven Smart System (MSS) — Current
- Palantir's commercialized Maven product: AI platform fusing imagery, video, drone feeds, satellite data, sensor arrays
- Machine learning for automatic detection, classification, and tracking of battlefield objects
- Reduces targeting data transmission: from 12 hours (2020) → under 1 minute (2024+)
- "20-50 soldiers can analyze data that previously required hundreds or thousands" (RUSI analyst)

**Contract milestones:**
- May 2024: Initial $480M, 5-year IDIQ contract with DoD (Army Aberdeen Proving Ground)
- September 2024: $99.8M Army Research Lab contract
- May 2025: DOD boosts contract ceiling by $795M → **total ceiling $1.275B through 2029**
- 20,000+ users across 35 military entities as of mid-2025
- Maven adoption eightfold increase since early 2024
- March 25, 2025: **NATO acquires Maven Smart System NATO (MSS NATO)** for Allied Command Operations — "one of the most expeditious contracts in NATO history" (six months from requirement to acquisition)
- June 2025: US Army creates "Detachment 201" — Palantir CTO Shyam Sankar among four Silicon Valley executives commissioned as Army Reserve lieutenant colonels

**Combatant commands using MSS:** CENTCOM, EUCOM, INDOPACOM, NORTHCOM/NORAD, TRANSCOM; deployed for Joint Staff

---

## Ukraine

- Palantir began providing services to Ukraine's military in 2022 (reported as initially free)
- March 2024: Agreement with Ukraine's Ministry of Economy
- Role: battlefield intelligence for targeting, war crimes evidence collection, landmine detection
- Karp (CEO): Palantir is "responsible for most of the targeting in Ukraine"
- From detection to target prosecution: "no more than two or three minutes" (Bruno Macaes, former Portuguese official, after Palantir London tour)
- NYT: MSS used in Ukraine showed Americans "how limited the technology is" — drove upgrades
- Palantir and Starlink turned Ukraine into "an AI war lab" (multiple analysts)
- Ukraine's MoD working on legal framework to formalize Palantir software use in military

---

## Gaza / Israel

### Timeline
- **January 2024:** Palantir announces "strategic partnership" with Israel's Ministry of Defense for "war-related missions"
- Board meeting held in Tel Aviv "in solidarity" with Israel (Bloomberg)
- Palantir did not disclose which specific technologies would be provided
- Palantir AIP (Artificial Intelligence Platform) previously introduced to help militaries "rapidly analyze and identify bombing targets"; executive described it as "optimizing the kill chain"
- Palantir draws heavily on recruits from Israel's Unit 8200 (cyber intelligence)

### Alleged involvement
- **Lavender/Gospel/Where's Daddy:** AI systems used by IDF to generate target lists. +972 Magazine/Local Call investigation identifies these systems; Palantir not mentioned by name but alleged to fit same category
- Palantir explicitly denies involvement with "Lavender" database
- Israeli military reportedly used Palantir tools during multiple Gaza raids (per CEO biography)
- **Lebanon, September 2024:** Israel relied on Palantir in the exploding pager/radio device attacks that killed dozens and wounded thousands
- **November 2025:** Palantir has permanent desk at US-led Civil-Military Coordination Center (CMCC) in Kiryat Gat, southern Israel — providing technological architecture for tracking Gaza aid delivery

### UN finding (June 2025)
- UN Special Rapporteur Francesca Albanese's report *From the Economy of Occupation to the Economy of Genocide*
- Found "reasonable grounds to believe Palantir has provided [Israel] automatic predictive policing technology, core defence infrastructure, and its AI Platform which allows real-time battlefield data integration for automated decision-making"
- Called on Palantir to prevent misuse or withdraw, warning of legal liability for complicity

### Palantir's official position
- "As a company, Palantir does support Israel. We've chosen to support them because of the appalling events of October 7th."
- Denies involvement with "Lavender," "Gospel," "Where's Daddy"
- States human rights due diligence is incorporated into all products

### Financial/institutional divestment pressure
- October 2024: Storebrand (Norway's largest asset manager) divests $24M in PLTR shares — IHL/human rights risk
- May 2025: University of San Francisco divests
- August 2024: San Francisco State University divests
- UK: Multiple MPs call for review; Liberal Democrats, opponents demand scrutiny

---

## Product Stack Reference

| Product | Function | Primary Customer |
|---|---|---|
| **Gotham** | Intelligence analysis; counterterrorism; target identification; launched 2008, originally for DoD/intel community | DoD, CIA, intelligence community |
| **Foundry** | Enterprise data integration; operational workflows; commercial and government | Enterprises, US government agencies |
| **AIP (Artificial Intelligence Platform)** | LLM + real-time operational data; military and commercial | DoD, commercial |
| **Maven Smart System (MSS)** | AI-enabled battlefield awareness; data fusion from drones, satellites, sensors; targeting | DoD, NATO, Ukraine |
| **ImmigrationOS** | Immigration enforcement lifecycle management; targeting, tracking, logistics | ICE/DHS |
| **ICM (FALCON)** | Investigative case management for ICE; multi-database access for agent field use | ICE (HSI and ERO) |
| **TITAN** | Next-gen ISR ground station (AI/ML); processes Space/High Altitude/Aerial/Terrestrial layer data; US Army deployment 2025 | US Army |
| **Gaia** | Battlefield visualization ("bring the battlefield into view") — confirmed deployed at CMCC in Israel Nov 2025 | IDF/CMCC |

**Confidence:** HIGH for ICE contracts (ACLU, American Immigration Council, Axios, FOIA documents). HIGH for Maven (DefenseScoop, NATO press release, DOD). MEDIUM for Gaza (disputed by Palantir; corroborated by UN Special Rapporteur, +972, Al Jazeera, multiple journalists but Palantir denies specific system involvement).
