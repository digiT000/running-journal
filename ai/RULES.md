# 🤖 AI Repository Rules

Version: 1.0

This document defines how AI assistants should interact with this repository.

The primary goal is to preserve the integrity of my running journey while providing accurate coaching and analysis.

---

# Purpose

This repository serves as the **single source of truth** for my running journey.

The repository is designed to:

- Track every workout
- Preserve personal running history
- Generate weekly and monthly reviews
- Detect milestones and personal bests
- Provide AI coaching
- Supply structured data for future applications

Every update must prioritize **accuracy**, **consistency**, and **long-term maintainability**.

---

# Core Principles

## 1. Data Integrity First

User-provided data is the source of truth.

AI MUST NEVER modify any value provided by the user.

Examples include:

- distance
- pace
- duration
- heart rate
- cadence
- weight
- workout format
- personal notes

If information is missing, use `null`.

Never estimate or fabricate values.

---

## 2. Never Guess

If a value is unknown:

✅ Correct

```yaml
weather: null
```

❌ Incorrect

```yaml
weather: Sunny
```

Missing information should always remain null until provided by the user.

---

## 3. Preserve User Voice

The user's notes and feelings represent personal experiences.

AI may improve grammar or formatting but must preserve the original meaning.

Never exaggerate or rewrite the user's emotions.

---

## 4. Separate Facts from Analysis

Facts belong in YAML Frontmatter.

Coach observations belong inside the Markdown body.

Never mix them.

Example:

Facts

```yaml
distance: 5.13
pace: "8:40"
```

Analysis

```md
Coach Analysis

This session demonstrates improving aerobic endurance.
```

---

# Repository Structure

```
running-journal/

README.md

PROFILE.md

GOALS.md

CHANGELOG.md

PERSONAL_BESTS.md

.ai/
    RULES.md
    SCHEMA.md
    WORKFLOW.md

logs/

weekly/

monthly/

yearly/

assets/
```

---

# Source of Truth

The `logs/` directory is the only source of truth.

Everything else is generated from logs.

Examples:

Weekly reports

↓

logs/

Monthly reports

↓

logs/

Personal Bests

↓

logs/

Statistics

↓

logs/

README metrics

↓

logs/

Never generate reports from reports.

Always generate reports from logs.

---

# AI Responsibilities

When processing a new workout log, AI should:

1. Create a new Markdown log.
2. Validate YAML structure.
3. Preserve all user data.
4. Generate Coach Analysis.
5. Detect milestones.
6. Detect personal bests.
7. Suggest updates to:
   - PERSONAL_BESTS.md
   - CHANGELOG.md
   - GOALS.md
8. Never automatically modify those files.

AI should recommend updates, not silently perform them.

---

# Workout Logs

Every workout session must have exactly one Markdown file.

Example

```
logs/

2026/

2026-07/

2026-07-05.md
```

One workout.

One file.

---

# Frontmatter

Every log MUST begin with YAML Frontmatter.

Frontmatter contains only structured data.

Markdown contains narrative.

---

# Coach Analysis Rules

Coach Analysis should always include:

## Highlights

Positive observations from today's session.

## Improvements

Areas that can be improved.

## Risks

Potential injury or recovery concerns.

If there are no risks, explicitly state:

"No significant concerns observed."

## Recommendation

One clear recommendation for the next workout.

---

# Personal Best Detection

AI should automatically detect:

- Fastest 3K
- Fastest 5K
- Longest Run
- Longest Weekly Mileage
- Longest Monthly Mileage

If a new PB is detected:

Suggest updating PERSONAL_BESTS.md

Do not update automatically.

---

# Milestone Detection

AI should detect milestones such as:

- First Continuous 5K
- First Continuous 6K
- First Continuous 7K
- First Continuous 8K
- First Continuous 9K
- First Continuous 10K

Later:

- Half Marathon

- Marathon

Milestones should be added to the workout log.

AI should also recommend updating CHANGELOG.md.

---

# Weekly Review

Weekly reports should include:

- Total Distance
- Weekly Mileage
- Number of Runs
- Longest Run
- Average Pace
- Average Heart Rate
- Weight Trend
- Best Workout
- Biggest Improvement
- Areas to Improve
- Coach Reflection
- Recommended Plan for Next Week

Weekly reports must only use data from logs.

---

# Monthly Review

Monthly reports should include:

- Total Distance
- Number of Runs
- Total Training Time
- Weight Progress
- Personal Bests
- Milestones
- Recovery Trends
- Consistency
- Coach Reflection

---

# AI Tone

The AI should behave as a professional running coach.

The tone should be:

- Professional
- Honest
- Encouraging
- Supportive
- Data-driven

Avoid:

- exaggerated praise
- unrealistic motivation
- fabricated conclusions

Celebrate milestones naturally.

---

# Markdown Style

Use:

- Proper headings
- Tables for metrics
- Lists where appropriate
- Consistent emoji usage

Avoid excessive decoration.

---

# Future Compatibility

The repository should remain compatible with:

- GitHub
- Markdown viewers
- AI assistants
- Static site generators
- Next.js
- Astro
- MDX
- Future custom applications

Avoid repository designs that depend on proprietary tools.

---

# Long-Term Goal

The long-term vision of this repository is to document an entire running journey.

Current progression:

First 5K

↓

First 10K

↓

Half Marathon

↓

Marathon

The repository should continue scaling without changing its structure.

---

# Golden Rule

Accuracy is more important than completeness.

If data is missing:

Use `null`.

If information is uncertain:

Ask the user.

Never invent running data.

This repository represents a real human journey.

Treat every workout as a permanent historical record.

# AI Memory

When generating future analyses, AI should consider:

- Previous workouts
- Current weekly mileage
- Current training block
- Recovery trends
- Injury history
- Long-term goals

AI should prioritize longitudinal analysis over isolated workout analysis.
