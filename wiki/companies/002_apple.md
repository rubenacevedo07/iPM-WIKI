---
entity_id: 2
ticker: AAPL
archetype: HYBRID
composite_score: 83.00
last_updated: 2026-04-19
source: ipm_db_auto_generated
aliases: [Apple, AAPL]
tags: [ipm-entity, hybrid]
---

# Apple

> **Hybrid power — crosses multiple power dimensions simultaneously.** Composite power score: **83/100** (stable trend). Country: United States.

## Power Index

**Archetype:** `HYBRID`  
**Composite:** ████████░░ 83/100  
**Trend:** stable

| Dimension | Score | Bar |
|-----------|------:|-----|
| Financial | 94 | `█████████░` |
| Military | 28 | `██░░░░░░░░` |
| Political | 82 | `████████░░` |
| Technological | 92 | `█████████░` |
| Industrial | 62 | `██████░░░░` |
| Information | 90 | `█████████░` |

**Tiers:** Financial: Tier 1 (Dominant) · Political: Tier 1 (Dominant) · Military: Tier 3 (Minor)

## Leadership

- **Tim Cook** — CEO of Apple (🔴 Critical)

### Tim Cook — Vision

**Archetype:** `Conservative` · **Confidence:** 90/100  
**Horizon:** institutional

Cook's strategy centers on operational excellence, ecosystem lock-in, and services monetization. Not a product visionary — a value extractor who optimized Jobs-era platforms to maximum profitability. Privacy as competitive differentiation and regulatory shield. Deliberate about AI (Apple Intelligence) vs NVIDIA/Microsoft speed-to-market.

> *"Privacy is a fundamental human right"*
> — Apple WWDC 2022, 2022-06-06

> *"We are in the early innings of services"*
> — Apple Q4 2024 earnings call, 2024-10-31

**⚠ Divergence flags:**
- [High] Stated: *Privacy is a fundamental human right*
  Observed: Apple receives an estimated $18-20B/year from Google to be default search engine on iOS, directly facilitating Google's mass data collection from Apple devices
- [Medium] Stated: *Opening the platform would harm user security*
  Observed: DMA compliance revealed Apple could technically comply without security degradation, contradicting stated position

## Relations

### Outbound (this entity → others)

| Strength | Target | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[TSMC|TSMC]]** | `DependsOn` | Apple Silicon (A18, M4 series) manufactured exclusively by TSMC on 3nm process. ... |
| 🔴 Critical | **[[Ecuador|Ecuador]]** | `DependsOn` | All Apple Silicon from TSMC Taiwan. |
| 🟠 High | **[[../institutions/SAMSUNG|Samsung Electronics]]** | `DependsOn` | Samsung Display is primary OLED supplier for iPhone Pro/Pro Max (alongside LG an... |
| 🟠 High | **[[Hon Hai (Foxconn)|Hon Hai (Foxconn)]]** | `DependsOn` | Hon Hai (Foxconn) assembles ~70% of iPhone volume. Apple owns the manufacturing ... |
| 🟠 High | **[[Alphabet|Alphabet]]** | `Competes` | iOS vs Android is the dominant mobile OS duopoly. App Store vs Google Play. Siri... |
| 🟠 High | **[[../institutions/SAMSUNG|Samsung Electronics]]** | `Competes` | Apple and Samsung are the top-2 smartphone vendors globally (Apple ~18%, Samsung... |
| 🟡 Medium | **[[Microsoft|Microsoft]]** | `Competes` | Apple increasingly targets enterprise with iPhone+Mac+iPad combo vs Microsoft 36... |
| 🟡 Medium | **[[Microsoft|Microsoft]]** | `Partners` | Microsoft 365 (Word, Excel, Teams, Outlook) among top apps on iOS/macOS App Stor... |
| ⚪ Low | **[[NVIDIA|NVIDIA]]** | `Competes` | Apple M4 Ultra targets professional creative workflows previously dominated by N... |

### Inbound (others → this entity)

| Strength | Source | Type | Description |
|----------|--------|------|-------------|
| 🔴 Critical | **[[TSMC|TSMC]]** | `Partners` | Apple is TSMC single largest customer. First access to latest nodes. |
| 🔴 Critical | **[[TSMC|TSMC]]** | `Supplies` | Apple is TSMC's largest single customer at ~25% of revenue. A18, M4 series manuf... |
| 🔴 Critical | **[[Alphabet|Alphabet]]** | `Finances` | Google pays Apple an estimated $18-20B per year (revealed in DOJ v. Google trial... |
| 🔴 Critical | **[[Unknown|Unknown]]** | `Governs` | Apple Park is a HQ facility operated by Apple in Cupertino |
| 🔴 Critical | **[[Unknown|Unknown]]** | `Governs` | Foxconn Zhengzhou Contract is a HQ facility operated by Apple in Zhengzhou |
| 🔴 Critical | **[[Tim Cook|Tim Cook]]** | `Governs` | Tim Cook succeeded Steve Jobs in August 2011. |
| 🟠 High | **[[US Department of Justice|US Department of Justice]]** | `Regulates` | US DOJ and 16 state attorneys general filed antitrust lawsuit March 21, 2024 all... |
| 🟠 High | **[[European Commission|European Commission]]** | `Regulates` | EC designated Apple DMA gatekeeper Sep 2023 for iOS, App Store, Safari. Complian... |
| 🟠 High | **[[Vanguard Group|Vanguard Group]]** | `Owns` | Vanguard Group holds approximately 7.8% of Apple per SEC 13F Q4 2025. Largest in... |
| 🟠 High | **[[Unknown|Unknown]]** | `Governs` | Apple Cork Operations is a HQ facility operated by Apple in Cork |
| 🟠 High | **[[BlackRock|BlackRock]]** | `Owns` |  |
| 🟡 Medium | **[[Federal Trade Commission|Federal Trade Commission]]** | `Regulates` | FTC published mobile app stores report Dec 2023 criticizing Apple-Google duopoly... |
| 🟡 Medium | **[[US Department of Commerce|US Department of Commerce]]** | `Regulates` | BIS export controls on advanced semiconductors affect Apple indirectly via TSMC ... |
| 🟡 Medium | **[[State Street Corporation|State Street Corporation]]** | `Owns` | State Street Corporation holds approximately 3.7% of Apple per SEC 13F Q4 2025. |
| 🟡 Medium | **[[Microsoft|Microsoft]]** | `Partners` | Microsoft 365 and Teams are among top apps on iOS/macOS App Store. Structural co... |

## Recent Events

### 2024-10-28 — Apple launches Apple Intelligence with iOS 18.1 — on-device AI platform
`Critical` 📈 Positive · Source: Apple Newsroom ✓
[Source](https://www.apple.com/newsroom/2024/10/apple-intelligence-is-available-today-on-iphone-ipad-and-mac/)

iOS 18.1 released October 28, 2024 with first Apple Intelligence features: Writing Tools, Notification Summaries, Photo Clean Up, and ChatGPT integration via Siri. On-device first strategy differentiates from cloud-dependent competitors. Privacy Relay architecture for cloud processing. Apple enters consumer AI race formally.

### 2024-05-02 — Apple announces record $110B share buyback — largest in US corporate history
`High` 📈 Positive · Source: Apple Q2 FY2024 Earnings ✓
[Source](https://www.apple.com/newsroom/pdfs/fy2024-q2/FY24_Q2_Consolidated_Financial_Statements.pdf)

Apple authorized $110B share repurchase program on May 2, 2024 during Q2 FY2024 earnings — the largest single buyback authorization in US corporate history. Signals capital allocation prioritization over aggressive M&A. Demonstrates extreme cash generation ($25B+ FCF per quarter) and shareholder return commitment.

### 2024-03-21 — US Department of Justice sues Apple for illegal smartphone monopoly
`Critical` 📉 Negative · Source: US Department of Justice ✓
[Source](https://www.justice.gov/opa/pr/justice-department-sues-apple-monopolizing-smartphone-markets)

DOJ and 16 state AGs filed antitrust lawsuit March 21, 2024 alleging Apple maintains illegal monopoly over smartphone market. Targets iMessage green-bubble strategy, super-app restrictions, NFC access limits, and cloud streaming restrictions. Seeks structural remedies that could force platform openness.

### 2024-03-07 — Apple forced to open App Store to third-party stores in EU under DMA
`High` 📊 Mixed · Source: European Commission ✓
[Source](https://ec.europa.eu/commission/presscorner/detail/en/ip_23_4328)

EU Digital Markets Act compliance deadline March 7, 2024. Apple forced to allow alternative app stores, third-party payment processing, and NFC access in the EU. Apple introduced new fee structure critics called "malicious compliance." Marks structural change to App Store business model in Europe.

### 2024-02-02 — Apple Vision Pro goes on sale in the United States
`High` 📈 Positive · Source: Apple Newsroom ✓
[Source](https://www.apple.com/newsroom/2024/02/apple-vision-pro-available-in-the-us-on-friday-february-2/)

Apple Vision Pro launched at $3,499 on February 2, 2024 — first major new product category under Tim Cook. Spatial computing platform combining AR/VR. Initial units sold out quickly; analyst estimates of 200K-400K units in first year vs millions for iPhone. Establishes spatial computing platform strategy.

---
*Auto-generated from IPMDB on 2026-04-19. Edge count: 24.*
*Composite score: 83/100 | Archetype: HYBRID*