---
name: agent-roles
description: Role-based sub-agent specialization system. Inspired by TradingAgents' analyst/researcher/trader roles.
author: Sovereign (S.V.)
version: 0.1.0
triggers:
  - "specialized agent"
  - "agent role"
  - "task assignment"
  - "sub-agent type"
metadata: {"clawdbot":{"emoji":"🎯","requires":{"bins":["node"]}}}
---

# Agent Role Specialization Skill

**Inspired by**: TradingAgents' specialized agent roles (Analyst/Researcher/Trader)  
**Purpose**: Enable role-based sub-agent assignment for better task matching

---

## Overview

This skill introduces role metadata to sub-agents, allowing the main agent to assign tasks based on specialized capabilities rather than generic "sub-agent" execution.

### Role Taxonomy

```
┌─────────────────────────────────────────────────────────┐
│                  Agent Role Hierarchy                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Orchestrator Roles                                    │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Lead Agent   │    │ Coordinator  │                 │
│  │ (Strategy)   │    │ (Task Mgmt)  │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
│  Execution Roles                                       │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Analyst      │    │ Researcher   │                 │
│  │ (Info Gather)│    │ (Deep Dive)  │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
│  Quality Roles                                         │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Critic       │    │ Reviewer     │                 │
│  │ (Risk Ident) │    │ (QA/Verify)  │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
│  Specialist Roles                                      │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Coder        │    │ Writer       │                 │
│  │ (Dev Tasks)  │    │ (Content)    │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Role Definitions

### Orchestrator Roles

| Role | Purpose | Skills | When to Use |
|------|---------|--------|-------------|
| **Lead Agent** | Strategic decision making | Planning, delegation, synthesis | Complex multi-step tasks |
| **Coordinator** | Task management & tracking | Organization, prioritization | Multiple parallel sub-tasks |

### Execution Roles

| Role | Purpose | Skills | When to Use |
|------|---------|--------|-------------|
| **Analyst** | Information gathering & summarization | Research, synthesis, pattern recognition | Market research, competitive analysis |
| **Researcher** | Deep technical investigation | Technical analysis, documentation review | Architecture research, API evaluation |

### Quality Roles

| Role | Purpose | Skills | When to Use |
|------|---------|--------|-------------|
| **Critic** | Risk identification & challenge | Critical thinking, scenario analysis | Pre-decision risk assessment |
| **Reviewer** | Quality assurance & verification | Attention to detail, testing | Code review, fact-checking |

### Specialist Roles

| Role | Purpose | Skills | When to Use |
|------|---------|--------|-------------|
| **Coder** | Software development | Programming, debugging, testing | Feature implementation, bug fixes |
| **Writer** | Content creation | Writing, editing, SEO | Documentation, blog posts, distribution |

---

## Usage

### Basic Role Assignment

```bash
# Assign analyst role for information gathering
sessions_spawn \
  --task "Analyze GitHub trending AI agent projects" \
  --role "analyst" \
  --label "prey-011-analysis" \
  --context '{"focus": ["architecture", "features", "adoption"], "output": "structured_report"}'

# Assign researcher role for deep technical dive
sessions_spawn \
  --task "Research MCP protocol integration options" \
  --role "researcher" \
  --label "mcp-research" \
  --context '{"depth": "technical", "compare": ["existing_implementations"], "deliverable": "integration_plan"}'

# Assign coder role for implementation
sessions_spawn \
  --task "Implement debate orchestration script" \
  --role "coder" \
  --label "debate-impl" \
  --context '{"language": "javascript", "test": true, "docs": true}'

# Assign writer role for content creation
sessions_spawn \
  --task "Write distribution post for prey_011 analysis" \
  --role "writer" \
  --label "prey-011-distribution" \
  --context '{"platform": "twitter", "tone": "technical", "length": "thread"}'
```

### Role-Based Task Routing

```javascript
// scripts/role-router.js

const roleCapabilities = {
  analyst: {
    strengths: ['information_gathering', 'summarization', 'pattern_recognition'],
    tools: ['web_search', 'web_fetch', 'read'],
    output_formats: ['report', 'summary', 'comparison_table']
  },
  researcher: {
    strengths: ['technical_analysis', 'deep_dive', 'documentation'],
    tools: ['web_fetch', 'read', 'exec', 'pdf'],
    output_formats: ['technical_report', 'architecture_diagram', 'integration_plan']
  },
  coder: {
    strengths: ['implementation', 'debugging', 'testing'],
    tools: ['exec', 'read', 'write', 'edit'],
    output_formats: ['code', 'tests', 'documentation']
  },
  writer: {
    strengths: ['content_creation', 'editing', 'seo'],
    tools: ['read', 'write', 'web_search'],
    output_formats: ['blog_post', 'social_thread', 'documentation']
  },
  critic: {
    strengths: ['risk_identification', 'challenge_assumptions', 'scenario_analysis'],
    tools: ['read', 'web_search'],
    output_formats: ['risk_report', 'challenge_document', 'alternative_scenarios']
  },
  reviewer: {
    strengths: ['quality_assurance', 'fact_checking', 'testing'],
    tools: ['read', 'exec'],
    output_formats: ['review_report', 'test_results', 'quality_score']
  }
};

function assignRole(task) {
  // Analyze task requirements
  const requirements = analyzeTask(task);
  
  // Match to best role
  const bestRole = Object.entries(roleCapabilities)
    .map(([role, caps]) => ({
      role,
      score: calculateMatchScore(requirements, caps)
    }))
    .sort((a, b) => b.score - a.score)[0];
  
  return bestRole.role;
}
```

---

## Role Metadata Schema

### sessions_spawn Extension

```yaml
# Enhanced sessions_spawn with role metadata
sessions_spawn:
  task: "String - Task description"
  role: "analyst|researcher|coder|writer|critic|reviewer|coordinator|lead"
  label: "String - Session label"
  context:
    focus: ["Array", "of", "focus", "areas"]
    depth: "shallow|medium|deep"
    output: "expected_output_format"
    constraints:
      - "Array of constraints"
    tools_allowed: ["read", "write", "exec", "web_search", ...]
    tools_forbidden: ["exec", ...]  # For safety
  timeout: 600  # seconds
  priority: "P0|P1|P2"
```

### Role-Specific Instructions

```yaml
# Role instruction templates
role_instructions:
  analyst: |
    You are an Analyst agent specializing in information gathering and synthesis.
    
    Your approach:
    1. Gather comprehensive information from multiple sources
    2. Identify patterns and key insights
    3. Summarize findings in structured format
    4. Highlight uncertainties and knowledge gaps
    
    Output format: Structured report with sections, tables, and key takeaways.

  researcher: |
    You are a Researcher agent specializing in deep technical investigation.
    
    Your approach:
    1. Read documentation and technical specifications
    2. Analyze architecture and implementation details
    3. Compare alternatives with pros/cons
    4. Provide actionable recommendations
    
    Output format: Technical report with diagrams, code examples, and integration steps.

  coder: |
    You are a Coder agent specializing in software implementation.
    
    Your approach:
    1. Understand requirements and constraints
    2. Design clean, maintainable solution
    3. Implement with tests and documentation
    4. Verify functionality
    
    Output format: Production-ready code with tests, docs, and usage examples.

  writer: |
    You are a Writer agent specializing in content creation.
    
    Your approach:
    1. Understand target audience and platform
    2. Craft compelling narrative
    3. Edit for clarity and impact
    4. Optimize for engagement
    
    Output format: Platform-optimized content (blog post, thread, etc.)

  critic: |
    You are a Critic agent specializing in risk identification.
    
    Your approach:
    1. Identify assumptions and potential failure modes
    2. Challenge conventional thinking
    3. Analyze worst-case scenarios
    4. Suggest mitigations
    
    Output format: Risk report with severity ratings and mitigation strategies.

  reviewer: |
    You are a Reviewer agent specializing in quality assurance.
    
    Your approach:
    1. Verify facts and claims
    2. Check code quality and best practices
    3. Test functionality
    4. Provide quality score and improvement suggestions
    
    Output format: Review report with issues, scores, and recommendations.
```

---

## Implementation Plan

### Phase 1: Role Metadata (Week 1)

```javascript
// Add role support to sessions_spawn wrapper
// File: scripts/sessions-spawn-role.js

const spawnWithRole = async (task, role, context = {}) => {
  const roleInstructions = getRoleInstructions(role);
  const roleTools = getRoleTools(role);
  
  return await sessions_spawn({
    task,
    instructions: `${roleInstructions}\n\nContext: ${JSON.stringify(context, null, 2)}`,
    label: `${role}-${task.slice(0, 20).replace(/\s+/g, '-')}`,
    tools: roleTools,
    ...context
  });
};
```

### Phase 2: Role-Based Routing (Week 2)

```javascript
// Auto-assign roles based on task analysis
// File: scripts/auto-role-router.js

const autoAssignRole = (task) => {
  const keywords = {
    analyst: ['analyze', 'research', 'compare', 'summarize', 'market', 'trending'],
    researcher: ['investigate', 'deep dive', 'technical', 'architecture', 'protocol'],
    coder: ['implement', 'code', 'build', 'feature', 'bug', 'fix'],
    writer: ['write', 'create content', 'blog', 'post', 'article', 'distribution'],
    critic: ['review', 'critique', 'risk', 'challenge', 'assess'],
    reviewer: ['verify', 'test', 'qa', 'quality', 'check']
  };
  
  const taskLower = task.toLowerCase();
  const scores = {};
  
  for (const [role, words] of Object.entries(keywords)) {
    scores[role] = words.filter(w => taskLower.includes(w)).length;
  }
  
  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])[0][0];
};
```

### Phase 3: Role Analytics (Week 3)

```javascript
// Track role performance metrics
// File: scripts/role-analytics.js

const roleMetrics = {
  analyst: {
    tasks_completed: 0,
    avg_quality_score: 0,
    avg_time_minutes: 0,
    board_satisfaction: 0
  },
  // ... other roles
};

function updateRoleMetrics(role, sessionResult) {
  roleMetrics[role].tasks_completed++;
  roleMetrics[role].avg_quality_score = 
    weightedAverage(roleMetrics[role].avg_quality_score, sessionResult.quality);
  // ... update other metrics
}
```

---

## Integration with AGENTS.md

### Update Sub-Agent Section

```markdown
## Sub-Agent Role System

OpenClaw now supports role-based sub-agent specialization:

### Available Roles

| Role | Purpose | Best For |
|------|---------|----------|
| `analyst` | Information gathering | Market research, competitive analysis |
| `researcher` | Technical deep dive | Architecture research, API evaluation |
| `coder` | Implementation | Feature development, bug fixes |
| `writer` | Content creation | Documentation, distribution content |
| `critic` | Risk identification | Pre-decision risk assessment |
| `reviewer` | Quality assurance | Code review, fact-checking |

### Usage

```bash
# Explicit role assignment
sessions_spawn --task "..." --role "analyst"

# Auto-assign (experimental)
sessions_spawn --task "..." --role "auto"
```

### Role Selection Guidelines

- **Information gathering** → `analyst`
- **Technical research** → `researcher`
- **Implementation** → `coder`
- **Content creation** → `writer`
- **Risk assessment** → `critic`
- **Quality check** → `reviewer`

For complex tasks, combine multiple roles:
1. `analyst` → Gather requirements
2. `researcher` → Research solutions
3. `coder` → Implement
4. `reviewer` → Quality check
```

---

## Example Workflows

### Prey Analysis Workflow

```
┌─────────────┐
│ Lead Agent  │ → Assign prey analysis task
└─────────────┘
       │
       ▼
┌─────────────┐
│ Analyst     │ → Search GitHub trending
│ (Sub-Agent) │ → Fetch project READMEs
└─────────────┘
       │
       ▼
┌─────────────┐
│ Researcher  │ → Deep technical analysis
│ (Sub-Agent) │ → Architecture diagrams
└─────────────┘
       │
       ▼
┌─────────────┐
│ Coder       │ → Create skill drafts
│ (Sub-Agent) │ → Implementation templates
└─────────────┘
       │
       ▼
┌─────────────┐
│ Writer      │ → Distribution content
│ (Sub-Agent) │ → Social media posts
└─────────────┘
       │
       ▼
┌─────────────┐
│ Lead Agent  │ → Synthesize & archive
└─────────────┘
```

### Feature Implementation Workflow

```
1. Analyst → Market research (what users want)
2. Researcher → Technical feasibility study
3. Critic → Risk assessment
4. Lead Agent → Go/no-go decision
5. Coder → Implementation
6. Reviewer → QA & testing
7. Writer → Documentation
```

---

## Best Practices

### ✅ Do

- Assign roles based on task requirements
- Use role-specific instructions
- Combine multiple roles for complex tasks
- Track role performance metrics
- Refine role definitions based on results

### ❌ Don't

- Use wrong role for task (e.g., writer for coding)
- Skip role assignment for complex tasks
- Ignore role performance metrics
- Over-constrain roles (allow flexibility)

---

## Metrics

Track role effectiveness:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Role assignment accuracy | >80% | Auto-assign vs manual match |
| Task completion rate | >90% | By role |
| Quality score | >4.0 | By role (1-5 scale) |
| Time efficiency | Baseline -20% | Compared to no-role |

---

**Version**: 0.1.0 (Draft)  
**Status**: Pending Board Review  
**Next Steps**: Implement role metadata, test with prey_011 workflow
