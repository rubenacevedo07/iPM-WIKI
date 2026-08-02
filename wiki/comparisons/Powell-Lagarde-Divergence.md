---
title: Powell vs Lagarde — IdeologyProfile Divergence (EUR/USD Signal)
slug: powell-lagarde-divergence
type: comparison
created: 2026-04-09
updated: 2026-04-09
confidence: high
sources:
  - raw/internal-notes/IPM_Project_State_2026_04_01.md
related_actors: [jerome-powell, christine-lagarde, donald-trump]
related_countries: [united-states, germany, france]
related_institutions: [federal-reserve, ecb]
related_commodities: []
related_themes: [dollar-dominance, de-dollarization]
---

# Powell vs Lagarde — IdeologyProfile Divergence

*IMP's first production signal model. Computed 2026-04-09 from live DB.*

---

## Raw Scores (4 key axes shown)

| Axis | Powell | Lagarde | Divergence |
|------|--------|---------|------------|
| **EconScore** | 4.0 | −2.0 | **6.0** ← largest |
| **AuthScore** | 0.0 | −3.0 | 3.0 |
| **GeoScore** | 1.0 | 4.0 | 3.0 |
| **EnvScore** | −1.0 | −5.0 | 4.0 |
| **Label** | Technocratic institutionalist | Liberal multilateralist | — |

## Signal Values

- **EUR/USD signal (EconScore + AuthScore / 2): 4.5** — strong
- **Average divergence all 4 axes: 4.0**

---

## Three-Way Comparison — Trump / Powell / Lagarde

| Axis | Trump | Powell | Lagarde |
|------|-------|--------|---------|
| EconScore | 5.0 | 4.0 | −2.0 |
| AuthScore | 7.5 | 0.0 | −3.0 |
| GeoScore | −4.0 | 1.0 | 4.0 |
| EnvScore | 8.5 | −1.0 | −5.0 |
| **Label** | Nationalist-populist authoritarian | Technocratic institutionalist | Liberal multilateralist |

### Pair divergences (avg across 4 axes)
- **Trump vs Lagarde: 9.75** — extreme, near maximum
- **Trump vs Powell: 5.75** — high
- **Powell vs Lagarde: 4.0** — moderate, stable signal range

---

## Axis-by-Axis Interpretation

**EconScore — divergence 6.0 (largest in Powell-Lagarde pair)**
Powell: 4.0 — economically conservative, aligned with US fiscal orthodoxy, low tolerance for inflation.
Lagarde: −2.0 — left of center economically, more tolerant of fiscal expansion, ECB mandate includes employment alongside price stability.
*Signal meaning:* When EconScore divergence is high, the two central banks are structurally biased toward different rate paths. Powell leans hawkish, Lagarde leans dovish. This is the primary EUR/USD rate differential driver.

**AuthScore — divergence 3.0**
Powell: 0.0 — genuinely apolitical, resistant to political pressure.
Lagarde: −3.0 — actively anti-authoritarian, strong European liberal democratic values.
*Signal meaning:* Both resist political interference in monetary policy, but from different ideological anchors. Lagarde's anti-authoritarian score means she reads Trump's pressure on Powell as a systemic threat to the global monetary order — this amplifies her policy independence posture.

**GeoScore — divergence 3.0**
Powell: 1.0 — mildly internationalist, BIS coordination, dollar system stability.
Lagarde: 4.0 — strongly multilateralist, EU project, international institutions.
*Signal meaning:* Lagarde is structurally more committed to international coordination. When the US turns isolationist (Trump GeoScore −4.0), Lagarde's multilateral bias means the ECB doubles down on EU autonomy — widening the monetary policy gap.

**EnvScore — divergence 4.0**
Powell: −1.0 — slightly interventionist (Fed climate risk in financial stability framework).
Lagarde: −5.0 — strongly interventionist (ECB green bond purchases, climate risk as core mandate).
*Signal meaning:* Lagarde's green mandate creates structural EUR headwinds in energy-shock environments (higher energy costs reduce EU competitiveness). When oil spikes, EUR/USD is caught between ECB climate commitment and US energy independence.

---

## EUR/USD Signal Logic

```
EUR/USD signal = f(EconScore divergence, AuthScore divergence)
              = (6.0 + 3.0) / 2
              = 4.5 / 10

Interpretation:
  0-2   → Low divergence, rate paths converging, EUR/USD range-bound
  2-4   → Moderate divergence, directional bias emerging
  4-6   → Strong divergence, structural rate differential, clear EUR/USD trend
  6-10  → Extreme divergence, regime-level policy gap
```

Current signal **4.5** = strong divergence zone. The structural bias is:
- Powell's economic conservatism (4.0) → Fed holds or hikes → USD strength
- Lagarde's economic left-of-center (−2.0) → ECB cuts faster → EUR weakness
- Net: **USD structural bid, EUR structural pressure**

This inverts when US growth disappoints or ECB inflation reignites — monitor EconScore trajectory as economic data changes.

---

## What Changes This Signal

The IdeologyProfile is **semi-static** — it reflects the structural framework each policymaker operates from, not their current stance. The signal changes when:

1. **Personnel change:** New Fed Chair or ECB President with different ideological profile
2. **Mandate change:** ECB climate mandate expansion (EnvScore more negative) or Fed dual mandate reweight
3. **IdeologyShiftLog entry:** Explicit documented shift in framework (hawkish pivot, regime change)

Monitor: `IdeologyShiftLog` table for any entries on EntityId 191 or 192.

---

## Related
- [[../comparisons/Trump-Powell-Divergence]] — political pressure signal (different instrument)
- [[../actors/POWELL-Jerome.md]]
- [[../actors/LAGARDE-Christine.md]]
- [[../indicators/DB-ID-Reference.md]]

## DB Sync Notes
- Both profiles confirmed in DB 2026-04-09
- IdeologyShiftLog: check for entries on EntityId 191, 192 — none documented yet
- DSI index feeds from EconScore divergence + other inputs (COFER, gold, SWIFT)

## Related Pages
- [[../actors/POWELL-Jerome]]
- [[../actors/LAGARDE-Christine]]
- [[../actors/TRUMP-Donald]]
- [[Trump-Powell-Divergence]]
- [[../institutions/FEDERAL-RESERVE]]
- [[../institutions/ECB]]
