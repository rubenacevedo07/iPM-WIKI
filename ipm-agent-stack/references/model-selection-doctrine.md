# Model Selection Doctrine

## Principle

**The Calibration Moat is the product. Models are replaceable parts.** Use the right model for the right task. Optimize cost + quality per agent, not one-size-fits-all.

## Decision tree

### Question 1: Is this a critical call that affects moat data?

Critical calls write to:
- PredictionLog
- BrainLessonPromotion
- OracleWeightSnapshot
- ExecutiveBriefOutputs
- RiskApprovalStatus (approvals, not rejections)

→ Use **Claude Opus 4.7 API**. Quality premium justified.

### Question 2: Is this batch/volume work?

Batch work: entity extraction, Monte Carlo sampling, precedent retrieval, overnight parsing.

→ Use **Llama 3.3 70B local** (or DeepSeek R1 for reasoning-heavy batch).

### Question 3: Is this privacy-sensitive?

Sensitive: trade strategy, positions, proprietary signal logic.

→ **MUST be local** (Llama 3.3 70B or DeepSeek R1). No API.

### Question 4: Is this pure classification/extraction?

Simple tasks with high volume.

→ Use **small specialized models** (bge-large-en, custom fine-tuned classifiers). Zero marginal cost.

## Model inventory

### Claude Opus 4.7 (API)

**Strengths:**
- Best reasoning + instruction following
- Excellent calibration awareness (doesn't inflate confidence)
- Large context window (500K+)
- Consistent style across outputs
- Best at following strict schemas (PredictionLog fields)

**Weaknesses:**
- API dependency (rate limits, outages, pricing)
- Privacy concerns (sensitive data leaves network)
- Cost at scale (~$90/M tokens combined)

**Use for:**
- Atlas orchestration
- Nomos critical prediction sealing
- Helios geo-macro synthesis
- Cassandra final analog validation
- Janus doctrine promotion decisions
- Memo wiki curation

**Monthly budget target:** $600-1,500 at steady-state

### Llama 3.3 70B (local or rented)

**Strengths:**
- Quality ~85-90% of Opus on reasoning, ~70% on strict instruction following
- Runs locally on RTX 6000 Ada (48GB VRAM) or H100 rental ($2-4/hr)
- Privacy: data never leaves network
- Cost: hardware amortized, zero API fees

**Weaknesses:**
- Instruction following less strict (may deviate from required schemas)
- Less good at nuanced subtext interpretation
- Requires infra (Ollama or vLLM hosting)

**Use for:**
- Argus event classification batch
- Aegis risk rule evaluation
- Nomos Monte Carlo path sampling
- Janus batch resolution
- Argus central-bank tone scoring (batch)
- Overnight parsing workloads

**Monthly budget:** $100-200 (rental) OR $111/mo (RTX 6000 Ada amortized over 36 months)

### DeepSeek R1 (local)

**Strengths:**
- Excellent causal chain reasoning
- Strong counterfactual thinking
- Open weights, fine-tunable
- Transparent reasoning traces

**Weaknesses:**
- Less strong on instruction following
- Newer, less battle-tested

**Use for:**
- Cassandra precedent reasoning (causal chains)
- Hypothesis generation in GraphMind mode
- Scenario stress-testing

**Monthly budget:** zero marginal (same hardware as Llama 3.3)

### Embedding models

#### multilingual-e5-large (local)
- 1024 dims, 560M params
- 100+ languages (important for diverse sources)
- Use for: wiki + entities + speeches (heterogeneous)

#### bge-large-en-v1.5 (local)
- 1024 dims, 335M params
- English-focused, very fast
- Use for: news feeds, English documents

#### Nomic-embed-text-v1.5 (local)
- 768 dims, 137M params
- Matryoshka embeddings (can truncate without loss)
- Use for: applications needing embedding size flexibility

**All embedding models: zero API cost, runs on CPU or mini-GPU**

## Cost envelope per phase

### 2026 (Phase 5 frontend + early OpenClaw)

- Claude Opus: $100-250/mo (Atlas experimentation, limited Nomos sealing)
- Llama rental: $0 (not yet needed)
- Embeddings: $0 (not yet deployed)

**Total: $100-250/mo**

### 2027 (Hybrid graph layer + night loops active)

- Claude Opus: $300-800/mo (full agent stack running)
- Llama rental OR hardware: $150-200/mo (H100 spot) OR $111/mo (RTX 6000 amortized)
- Embeddings: $0 (local)

**Total: $450-1,000/mo**

### 2028-2030 (Scale + enterprise)

- Claude Opus: $800-2,000/mo (increased volume)
- Local hardware expanded: $300-500/mo amortized
- Fine-tuning experiments: $500-2,000 one-time per experiment

**Total: $1,200-2,500/mo recurring**

At enterprise revenue scale ($1M+ ARR), this is 1-3% of revenue. Acceptable.

## Fine-tuning roadmap

### 2026-2027: No fine-tuning
Focus: build Calibration Moat data, not model customization. Premature optimization to fine-tune before you have labeled data.

### 2028: First fine-tuning experiments
When Calibration Moat has 2+ years of data:
- IPM-Nomos: Llama 3.1 8B fine-tuned on resolved predictions
- IPM-CB-Tone: Llama 3.1 8B fine-tuned on speech → OfficialToneScore labels
- Cost per experiment: $200-500 compute

### 2029-2030: Deploy fine-tuned models in production
If experiments show >10% improvement on calibration metrics:
- Replace Llama 3.3 70B with IPM-specialized 8B fine-tunes for specific tasks
- Net cost: lower (smaller model = faster + cheaper to run)
- Net quality: higher on IPM-specific domain tasks

## Hard rules

1. **Never use hardcoded model names in agent logic** — abstract through a model service so models can be swapped without code changes
2. **Always measure model performance against moat metrics** — don't switch models based on vibes, use Brier score + output quality evaluations
3. **Never expose Claude API keys to OpenClaw directly** — API access goes through a backend service that founder controls
4. **Maintain ability to switch to 100% local** — if privacy concerns arise, system must function locally even with degraded quality
