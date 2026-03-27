---
name: agent-debate
description: Multi-agent debate mechanism for complex decision making. Inspired by TradingAgents' bull/bear researcher pattern.
author: Sovereign (S.V.)
version: 0.1.0
triggers:
  - "debate"
  - "multi-agent discussion"
  - "complex decision"
  - "evaluate options"
metadata: {"clawdbot":{"emoji":"🎭","requires":{"bins":["node"]}}}
---

# Multi-Agent Debate Skill

**Inspired by**: TradingAgents' Bullish/Bearish Researcher pattern  
**Purpose**: Enable structured multi-agent debates for complex decisions

---

## Overview

This skill implements a structured debate mechanism where multiple sub-agents argue different perspectives on a complex topic before the main agent makes a final decision.

### Use Cases

- **Investment decisions**: Evaluate risks vs opportunities
- **Architecture choices**: Compare different technical approaches
- **Strategic planning**: Weigh pros/cons of different strategies
- **Risk assessment**: Identify potential failure modes

---

## Usage

### Basic Debate

```bash
# Start a 2-sided debate
sessions_spawn \
  --task "Debate: Should we implement Docker sandboxing for OpenClaw?" \
  --mode "session" \
  --label "debate-sandbox" \
  --context '{"debate_sides": ["pro", "con"], "rounds": 2}'
```

### Multi-Sided Debate

```bash
# 3-sided debate (e.g., build vs buy vs partner)
sessions_spawn \
  --task "Debate: How should we add MCP server support?" \
  --mode "session" \
  --label "debate-mcp" \
  --context '{"debate_sides": ["build_own", "integrate_existing", "partner"], "rounds": 3}'
```

---

## Debate Structure

```
┌─────────────────────────────────────────────────────────┐
│                  Debate Orchestrator                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Round 1: Initial Arguments                            │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Side A       │    │ Side B       │                 │
│  │ (Pro)        │    │ (Con)        │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
│  Round 2: Rebuttals                                    │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Side A       │    │ Side B       │                 │
│  │ (Rebuttal)   │    │ (Rebuttal)   │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
│  Round 3: Final Statements (Optional)                  │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Side A       │    │ Side B       │                 │
│  │ (Closing)    │    │ (Closing)    │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
│  → Synthesis & Decision                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Template

### Step 1: Create Debate Sub-Agents

```javascript
// scripts/debate-orchestrator.js

const debateConfig = {
  topic: "Should we implement Docker sandboxing?",
  sides: [
    {
      name: "pro",
      role: "Advocate",
      instructions: "Argue strongly FOR the proposal. Focus on benefits, opportunities, and competitive advantages."
    },
    {
      name: "con", 
      role: "Critic",
      instructions: "Argue strongly AGAINST the proposal. Focus on risks, costs, and potential failure modes."
    }
  ],
  rounds: 2,
  synthesis: true
};
```

### Step 2: Run Debate Rounds

```javascript
// Round 1: Initial Arguments
const round1Args = await Promise.all(
  debateConfig.sides.map(side =>
    sessions_spawn({
      task: `Argue ${side.name} side: ${debateConfig.topic}`,
      instructions: side.instructions,
      label: `debate-round1-${side.name}`
    })
  )
);

// Round 2: Rebuttals (with context from Round 1)
const round2Args = await Promise.all(
  debateConfig.sides.map((side, idx) =>
    sessions_spawn({
      task: `Rebuttal for ${side.name} side: ${debateConfig.topic}`,
      instructions: `${side.instructions}\n\nAddress these counter-arguments:\n${round1Args.filter((_, i) => i !== idx).map(a => a.result).join('\n')}`,
      label: `debate-round2-${side.name}`
    })
  )
);
```

### Step 3: Synthesize Decision

```javascript
// Final synthesis by main agent
const synthesis = await sessions_spawn({
  task: `Synthesize debate and make final decision: ${debateConfig.topic}`,
  instructions: `
    Review all arguments from both sides:
    
    Pro Arguments:
    ${round1Args[0].result}
    ${round2Args[0].result}
    
    Con Arguments:
    ${round1Args[1].result}
    ${round2Args[1].result}
    
    Make a final decision considering:
    1. Strength of arguments on both sides
    2. Evidence quality
    3. Risk/reward balance
    4. Implementation feasibility
    
    Output format:
    - Decision: [YES/NO/MORE_ANALYSIS_NEEDED]
    - Confidence: [1-5]
    - Rationale: [Detailed explanation]
    - Next Steps: [Action items]
  `,
  label: "debate-synthesis"
});
```

---

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `debate_sides` | string[] | ["pro", "con"] | Names of debate sides |
| `rounds` | number | 2 | Number of debate rounds |
| `synthesis` | boolean | true | Whether to synthesize final decision |
| `confidence_threshold` | number | 3 | Minimum confidence for decision (1-5) |
| `timeout_per_round` | number | 300 | Timeout per round in seconds |

---

## Example Output

```markdown
# Debate Results: Docker Sandboxing for OpenClaw

## Round 1: Initial Arguments

### Pro Side (Security & Isolation)
- **Security**: Docker provides process isolation, preventing malicious code from accessing host
- **Reproducibility**: Consistent environment across different hosts
- **Resource Limits**: Can enforce CPU/memory limits per agent
- **Industry Standard**: DeerFlow 2.0 uses Docker/K8s for sandboxing

### Con Side (Complexity & Overhead)
- **Complexity**: Adds Docker dependency, complicates setup
- **Performance**: Container overhead for simple tasks
- **Debugging**: Harder to debug issues inside containers
- **Current Safety**: exec already runs with user permissions (no sudo)

## Round 2: Rebuttals

### Pro Rebuttal
- Acknowledges complexity but notes `make docker-init` is one-time setup
- Performance overhead negligible for most tasks (<5%)
- Debugging tools exist (docker exec, logs)
- User permissions not sufficient for untrusted code

### Con Rebuttal
- Agrees security is important but notes 99% of tasks are trusted
- Proposes opt-in Docker for untrusted tasks only
- Suggests hybrid approach: local for trusted, Docker for untrusted

## Synthesis & Decision

**Decision**: YES (Hybrid Approach)

**Confidence**: 4/5

**Rationale**:
Both sides make valid points. Security is important but shouldn't complicate the common case.

**Recommended Approach**:
1. Keep current `exec` as default (trusted tasks)
2. Add optional Docker sandbox for untrusted code
3. Auto-detect based on task risk level
4. Make Docker setup optional (one-time `make setup-sandbox`)

**Next Steps**:
- [ ] Implement risk assessment for tasks
- [ ] Create Docker sandbox provider (optional)
- [ ] Update AGENTS.md with sandbox configuration
- [ ] Test with high-risk tasks (external code execution)
```

---

## Integration with OpenClaw

### Add to AGENTS.md

```markdown
## Multi-Agent Debate Protocol

For complex decisions (P0/P1 priority), use structured debate:

1. **Identify Decision Type**:
   - Technical architecture → 2+ sides (build/buy/partner)
   - Risk assessment → Pro/Con debate
   - Strategic planning → Multi-scenario analysis

2. **Spawn Debate Agents**:
   ```bash
   sessions_spawn --task "Debate: [topic]" --context '{"debate": true, "sides": [...]}'
   ```

3. **Synthesize Decision**:
   - Review all arguments
   - Assign confidence score (1-5)
   - Document rationale in memory/

4. **Threshold Rules**:
   - Confidence ≥ 4: Proceed immediately
   - Confidence 2-3: Board notification required
   - Confidence < 2: More analysis needed
```

### Add to session verification

```javascript
// scripts/verify-session.js
if (session.includesDebate) {
  verifyDebateQuality({
    rounds: session.debateRounds,
    sides: session.debateSides,
    synthesis: session.synthesis,
    confidence: session.confidence
  });
}
```

---

## Best Practices

### ✅ Do

- Use for high-stakes decisions (architecture, security, strategy)
- Set clear instructions for each side
- Allow sufficient time for each round (5-10 min)
- Document synthesis rationale in memory/
- Assign confidence scores honestly

### ❌ Don't

- Use for simple decisions (overhead not worth it)
- Stack debate with other complex tasks
- Skip synthesis step
- Ignore low confidence scores
- Use more than 3 rounds (diminishing returns)

---

## Metrics

Track debate effectiveness:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Debate completion rate | >90% | Debates that reach synthesis |
| Decision confidence | >3.5 | Average confidence score |
| Board override rate | <10% | Decisions overturned by board |
| Time to decision | <30 min | Average debate duration |

---

**Version**: 0.1.0 (Draft)  
**Status**: Pending Board Review  
**Next Steps**: Implement prototype, test with 2-3 real decisions
