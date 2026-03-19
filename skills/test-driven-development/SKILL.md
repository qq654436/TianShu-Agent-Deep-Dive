---
name: test-driven-development
description: Use when implementing any feature or bugfix in OpenClaw workspace, before writing implementation code
---

# Test-Driven Development (TDD) for OpenClaw

## Overview

**Write the test first. Watch it fail. Write minimal code to pass.**

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

This skill adapts the superpowers:test-driven-development methodology to OpenClaw's tool ecosystem (exec, sessions_spawn, feishu_doc, etc.).

## When to Use

**Always:**
- New OpenClaw skills (`skills/*/SKILL.md`)
- Shell scripts or automation tools
- Bug fixes in existing workflows
- Any code that will be executed via `exec` or `sessions_spawn`

**Exceptions (ask 航哥 first):**
- Throwaway prototypes in `/tmp/`
- One-time migration scripts
- Configuration files (`.md`, `.yaml`, `.json`)

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over.**

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                      TDD CYCLE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [RED]    → Write failing test                              │
│     ↓                                                       │
│  [VERIFY] → Run test, confirm it fails correctly            │
│     ↓                                                       │
│  [GREEN]  → Write minimal code to pass                      │
│     ↓                                                       │
│  [VERIFY] → Run test, confirm it passes                     │
│     ↓                                                       │
│  [REFACTOR] → Clean up, improve names, remove duplication   │
│     ↓                                                       │
│  [REPEAT]   → Next test                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### RED - Write Failing Test

**For OpenClaw skills:**
```markdown
# Test scenario in /workspace/tian_shu/tests/{skill-name}.md

## Scenario
[Describe what the skill should do]

## Expected Behavior
[What should happen when skill is active]

## Baseline Test (WITHOUT skill)
[Run subagent without skill, document violation]
```

**For shell scripts:**
```bash
# test-my-script.sh
#!/bin/bash
# Test that script produces expected output

result=$(./my-script.sh --input test-data)
if [ "$result" != "expected" ]; then
    echo "FAIL: Expected 'expected', got '$result'"
    exit 1
fi
echo "PASS"
```

**For exec commands:**
```bash
# Test in same session or via sessions_spawn
# Document expected output before running
```

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
# Run your test
bash test-my-script.sh

# Expected output:
# FAIL: Expected 'expected', got 'something-else'
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write simplest code to pass the test.

**For OpenClaw skills:**
```markdown
---
name: my-skill
description: Use when [specific trigger]
---

# My Skill

## Overview
[1-2 sentences]

## When to Use
[Bullet list with symptoms]

## Core Pattern
[Code example or workflow]
```

**For shell scripts:**
```bash
#!/bin/bash
# Minimal implementation to pass test
echo "expected"
```

Don't add features, refactor other code, or "improve" beyond the test.

### Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
bash test-my-script.sh
# Expected: PASS
```

Confirm:
- Test passes
- Other tests still pass (if any)
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers
- Add documentation

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next feature.

## OpenClaw-Specific Patterns

### Testing Skills with Subagents

**REQUIRED SUB-SKILL:** Use `sessions_spawn` for isolated testing:

```bash
# 1. Baseline test (WITHOUT skill)
sessions_spawn --task "Do X" --mode run
# Document: What did the agent do wrong?

# 2. Write skill addressing violations

# 3. Compliance test (WITH skill)
sessions_spawn --task "Do X" --mode run
# Confirm: Agent now follows skill
```

### Testing exec Commands

```bash
# Test in isolated directory
cd /tmp/tdd-test-$$
mkdir -p test-workspace
cd test-workspace

# Run command, capture output
../my-command.sh > output.txt 2>&1

# Verify output
grep "expected" output.txt || echo "FAIL"

# Cleanup
cd /
rm -rf /tmp/tdd-test-$$
```

### Testing feishu_doc Operations

```bash
# Use a test document or dry-run mode
# Document expected behavior before running
# Verify with feishu_doc action=read after write
```

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One behavior per test | Multiple assertions |
| **Clear** | Name describes expected behavior | `test1.sh`, `test-final.sh` |
| **Isolated** | Can run independently | Depends on other tests |
| **Repeatable** | Same result every time | Flaky, timing-dependent |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting work is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "This is a quick script" | Quick scripts become production tools. Test it. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."
- "It's just a small change"

**All of these mean: Delete code. Start over with TDD.**

## Verification Checklist

Before marking work complete:

- [ ] Every new function/script/skill has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests are isolated and repeatable
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## Example: OpenClaw Skill

**Task:** Create a skill that ensures agents check LONG_TERM_MEMORY.md before major decisions

**RED**
```markdown
# Test: memory-check.md

## Scenario
Agent receives task to start a new project direction

## Baseline (WITHOUT skill)
[sessions_spawn --task "Start a new AI project"]
# Expected violation: Agent starts without checking memory

## Expected Behavior (WITH skill)
Agent should:
1. Read LONG_TERM_MEMORY.md first
2. Reference current goals in response
3. Align proposal with existing strategy
```

**Verify RED**
```bash
# Run baseline test
sessions_spawn --task "Start a new AI project" --mode run
# Document: Agent did NOT check memory, proposed unrelated idea
```

**GREEN**
```markdown
---
name: check-memory-before-decisions
description: Use when receiving strategic tasks, before proposing new directions
---

# Check Memory Before Decisions

## Overview
Always read LONG_TERM_MEMORY.md before proposing new project directions.

## When to Use
- Receiving strategic/planning tasks
- Proposing new project directions
- Making architectural decisions

## Core Pattern
1. Read LONG_TERM_MEMORY.md
2. Reference current goals in response
3. Align proposal with existing strategy
```

**Verify GREEN**
```bash
# Run compliance test
sessions_spawn --task "Start a new AI project" --mode run
# Confirm: Agent checked memory, aligned with strategy
```

**REFACTOR**
- Add cross-reference to related skills
- Improve description keywords
- Add example scenarios

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for behavior first. Ask 航哥. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found in existing skill/script? **Write failing test reproducing it first.** Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without 航哥's explicit permission.

---

**Adapted from:** obra/superpowers `test-driven-development`  
**OpenClaw Integration:** 2026-03-19 (天枢计划 #001)
