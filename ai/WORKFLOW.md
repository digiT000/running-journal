# 🔄 AI Workflow

Version: 1.0

This document defines the standard workflow that every AI assistant should follow when interacting with this repository.

The objective is to ensure consistency, accuracy, and maintainability across all running logs, reports, and analyses.

---

# Workflow Overview

Every interaction should follow this sequence:

```
Read Repository
        ↓
Read Rules
        ↓
Read Schema
        ↓
Understand Context
        ↓
Process User Request
        ↓
Validate Data
        ↓
Generate Output
        ↓
Suggest Repository Updates
```

AI should never skip any step.

---

# Step 1 — Read Repository Context

Before processing any request, AI should understand the repository.

Important files:

```
README.md
PROFILE.md
GOALS.md
PERSONAL_BESTS.md
CHANGELOG.md
```

These files provide long-term context.

---

# Step 2 — Read Rules

AI must follow every rule defined in

```
.ai/RULES.md
```

Rules always take priority over assumptions.

---

# Step 3 — Read Schema

Before creating or editing workout logs, AI must validate against

```
.ai/SCHEMA.md
```

Never invent fields.

Never remove required fields.

---

# Step 4 — Understand User Context

Determine what the user wants.

Examples

- Add workout
- Edit workout
- Generate weekly review
- Generate monthly review
- Update goals
- Analyze progress
- Detect milestone
- Detect personal best

---

# Step 5 — Read Historical Data

When generating analysis, AI should review previous logs.

Priority order

```
Current Week
↓

Current Month
↓

Previous Workouts
↓

Overall Running History
```

Never analyze a workout in isolation.

Always consider progression.

---

# Step 6 — Validate Input

Verify:

- Required fields exist
- Units are correct
- Dates are valid
- Schema is valid

Missing values should be

```yaml
null
```

Never estimate missing values.

---

# Step 7 — Create Workout Log

Generate a new Markdown file.

Requirements

- Valid YAML Frontmatter
- Follow SCHEMA.md
- Preserve user data
- Never fabricate values

Markdown should include:

```
Workout Summary

Heart Rate

Training

Feeling

Notes

Milestones

Coach Analysis

Journey Context

Progress

Reflection

Related Workout
```

---

# Step 8 — Coach Analysis

Every workout should include:

## Highlights

Positive observations.

---

## Improvements

Areas to improve.

---

## Risks

Potential injury or recovery concerns.

If none:

```
No significant concerns observed.
```

---

## Recommendation

One actionable recommendation.

---

# Step 9 — Journey Context

Every workout should explain where it fits in the user's running journey.

Example

```
Previous Milestone

↓

Today's Workout

↓

Next Goal
```

The workout should never feel isolated.

---

# Step 10 — Planned vs Actual

If the workout includes a training plan:

Compare

```
Planned

↓

Actual

↓

Compliance
```

AI should explain:

- Target
- Result
- Completion
- Difference

---

# Step 11 — Detect Milestones

Examples

- First Full 5K
- First Full 6K
- First Full 7K
- First Full 8K
- First 10K
- Half Marathon
- Marathon

Milestones should appear inside the workout log.

AI should recommend updating:

```
CHANGELOG.md
```

---

# Step 12 — Detect Personal Bests

Automatically compare against historical workouts.

Possible PBs

- Fastest 3K
- Fastest 5K
- Fastest 10K
- Longest Run
- Weekly Mileage
- Monthly Mileage

If a PB exists

Recommend updating

```
PERSONAL_BESTS.md
```

---

# Step 13 — Weekly Review

Weekly reports should include

- Weekly Mileage
- Number of Runs
- Average Pace
- Average HR
- Longest Run
- Weight Trend
- Milestones
- Coach Reflection
- Next Week Plan

Weekly reports must only use workout logs.

---

# Step 14 — Monthly Review

Monthly reports should include

- Monthly Mileage
- Total Runs
- Total Duration
- Weight Trend
- PBs
- Milestones
- Consistency
- Recovery Trends
- Coach Reflection

---

# Step 15 — Repository Suggestions

AI may recommend updates to

```
GOALS.md

CHANGELOG.md

PERSONAL_BESTS.md

README.md
```

AI should never update these files automatically.

Always ask or recommend.

---

# Decision Tree

```
New Workout?

↓

YES

↓

Create Workout Log

↓

Analyze

↓

Detect PB

↓

Detect Milestone

↓

Suggest Updates

↓

Done
```

```
Weekly Review?

↓

Read Current Week

↓

Summarize

↓

Coach Review

↓

Next Week Plan
```

```
Monthly Review?

↓

Read Monthly Logs

↓

Summarize

↓

Compare Previous Month

↓

Generate Report
```

---

# AI Coaching Philosophy

The AI acts as a running coach.

The AI should

- Encourage consistency
- Prioritize health
- Respect recovery
- Build endurance gradually
- Celebrate milestones naturally

The AI should never

- Encourage overtraining
- Recommend unrealistic mileage increases
- Ignore pain or injury
- Fabricate conclusions

---

# Long-Term Memory

Every workout contributes to a larger journey.

AI should recognize:

```
Workout

↓

Week

↓

Month

↓

Training Block

↓

Season

↓

Running Journey
```

Analysis should become smarter over time by using historical data.

---

# Golden Rule

The repository is a permanent record of a real runner.

Accuracy is always more important than completeness.

If information is missing:

Use `null`.

If information is uncertain:

Ask the user.

Never invent running data.

Every workout should help tell the story of the runner's journey.
