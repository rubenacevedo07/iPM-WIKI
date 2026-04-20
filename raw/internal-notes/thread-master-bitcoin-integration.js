// ============================================================
// Thread Master — Bitcoin Integration
// IMP Wiki: wiki/themes/Bitcoin-Macro-Regime.md
// ============================================================

// 1. ADD TO CONFIG.strategies
{
  id: "michael-sailor-btc",
  label: "Michael Saylor BTC",
  asset: "BTC/USDT",
  direction: "LONG",
  summary: "Structural long Bitcoin. Active only in IMP liquidity-on or macro-hedge regime.",
  riskProfile: {
    baseRisk: "high",
    volatilitySensitivity: "high",
  },
  defaults: {
    copyType: "ratio",
    bulletCount: 20,
    leverage: 2,
    marginBehavior: "cross",
  },
  constraints: {
    minBulletCount: 10,
    maxBulletCount: 40,
    requiredLeverage: 2,
  },
  ui: {
    fitLabel: "Ciclo alcista de liquidez / BTC",
    contraindications: [
      "No mezclar con Anti-Vitalik en el mismo capital",
      "No usar en régimen IMP liquidity-off (Fed hawkish)",
      "Reducir leverage a 1x en Regime C (macro-hedge)",
    ],
    displayPriority: 3,
    impRegimeNote: "Ver wiki/themes/Bitcoin-Macro-Regime.md para señales de activación",
  },
},

// ============================================================
// 2. IMP CONTEXT BRIDGE
// Derive from wiki — update weekly via OP-5 refresh
// Source: wiki/narratives/Global-Macro-Regime-2026-04.md
//         wiki/themes/Bitcoin-Macro-Regime.md
// ============================================================

const IMP_CONTEXT = {
  // Updated: 2026-04-10
  // Source: FOMC March 2026 + Chokepoint scores April 2026
  macroRegime: "liquidity-off",       // Fed held 4.5-4.75%, higher-for-longer
  bitcoinBias: "underweight",         // Regime B active
  fedStance: "hawkish-hold",          // Powell: "no hurry to cut"
  realYieldTrend: "elevated",         // 10Y real yield high
  chokepointRisk: 8,                  // Bab el-Mandeb + Taiwan Strait at 8
  dsiBias: "stable",                  // No active dollar system stress
  nextRegimeChangeSignal: "Powell pivot or DSI deterioration",
  source: "wiki/themes/Bitcoin-Macro-Regime.md",
  updatedAt: "2026-04-10",
};

// ============================================================
// 3. ADD TO CONFIG.regimes
// ============================================================

// In regime "alcista" — add BTC strategy
{
  id: "alcista",
  // ... existing config ...
  allowedStrategies: ["michael-sailor", "michael-sailor-btc"],
  impContext: {
    requiredBitcoinBias: ["overweight"],
    helperNote: "IMP Regime A (liquidity-on): Fed dovish, real yields falling, M2 expanding. Ver wiki/themes/Bitcoin-Macro-Regime.md",
  },
},

// Add new regime for Regime C (macro stress)
{
  id: "macro-hedge",
  label: "Macro Hedge",
  description: "IMP Regime C: dollar system stress, sanctions escalation, capital controls",
  allowedStrategies: ["michael-sailor-btc"],  // lower leverage version
  impContext: {
    requiredBitcoinBias: ["macro-hedge"],
    helperNote: "IMP Regime C: DSI deteriorating, 3+ chokepoints critical, capital controls. BTC as censorship-resistant hedge.",
  },
},

// ============================================================
// 4. ADD TO compatibilityRules
// ============================================================

{
  id: "btc-regime-gate",
  description: "Block BTC strategy when IMP regime is liquidity-off",
  when: { field: "strategyId", equals: "michael-sailor-btc" },
  effect: "block",
  evaluate: (s, cfg) => {
    if (s.strategyId !== "michael-sailor-btc") return true;
    const allowed = ["overweight", "macro-hedge"];
    return allowed.includes(IMP_CONTEXT.bitcoinBias);
  },
  message: `Bitcoin strategy requires IMP regime: liquidity-on or macro-hedge. Current: ${IMP_CONTEXT.macroRegime} (${IMP_CONTEXT.fedStance}). Next signal: ${IMP_CONTEXT.nextRegimeChangeSignal}.`,
},

{
  id: "btc-leverage-cap-regime-c",
  description: "Cap leverage at 1x in Regime C macro-hedge",
  when: { field: "strategyId", equals: "michael-sailor-btc" },
  effect: "warn",
  evaluate: (s, cfg) => {
    if (s.strategyId !== "michael-sailor-btc") return true;
    if (IMP_CONTEXT.bitcoinBias === "macro-hedge" && s.leverage > 1) return false;
    return true;
  },
  message: "En régimen IMP macro-hedge, reducir leverage BTC a 1x (volatilidad extrema esperada).",
},

// ============================================================
// 5. UI HELPER COMPONENT (optional)
// Show IMP Bitcoin bias in strategy selector
// ============================================================

// In StrategyCard or BitcoinStrategyHelp component:
const BitcoinImpBadge = () => {
  const { bitcoinBias, macroRegime, fedStance, updatedAt } = IMP_CONTEXT;

  const colors = {
    overweight: "green",
    underweight: "red",
    "macro-hedge": "amber",
  };

  return (
    <div className={`imp-badge imp-badge--${colors[bitcoinBias]}`}>
      <span className="imp-badge__label">IMP BTC</span>
      <span className="imp-badge__value">{bitcoinBias.toUpperCase()}</span>
      <span className="imp-badge__note">
        {macroRegime} · {fedStance} · {updatedAt}
      </span>
    </div>
  );
};

// ============================================================
// WEEKLY UPDATE PROTOCOL
// Every Monday — OP-5 refresh updates IMP_CONTEXT:
//
// 1. Perplexity runs: Powell weekly + Lagarde weekly + Chokepoints weekly
// 2. Claude ingests → updates wiki/narratives/Global-Macro-Regime-[date].md
// 3. You update IMP_CONTEXT object above with new macroRegime + bitcoinBias
// 4. compatibilityRules auto-gate BTC strategy based on new context
//
// Regime change triggers:
// - Fed signals cut → macroRegime: "liquidity-on" → bitcoinBias: "overweight"
// - DSI deteriorates → bitcoinBias: "macro-hedge"
// - Sanctions escalation + capital controls → bitcoinBias: "macro-hedge"
// ============================================================
