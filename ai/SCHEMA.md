# 📄 Running Log Schema

Version: 3.1

This document defines the official schema for every workout log.

All workout logs inside this repository MUST follow this schema.

---

# File Naming

One workout = One Markdown file.

```
logs/
└── 2026/
    └── 2026-07/
        └── 2026-07-05.md
```

---

# File Structure

Each workout log contains two sections:

```
YAML Frontmatter
↓

Markdown Body
```

---

# YAML Frontmatter

Every field should always exist.

If data is unavailable:

```yaml
null
```

Do not remove fields.

---

# Complete Schema

```yaml
---
id: null
date: YYYY-MM-DD

activity:
  primary: null
  secondary: null

distance:
  value: null
  unit: km

duration:
  value: null
  unit: min

pace:
  value: null
  unit: min/km

weight:
  value: null
  unit: kg

heart_rate:
  average: null
  max: null
  unit: bpm

training:
  app: null
  completed: true

  planned:
    app: Runna
    workout: Easy Run 5K

  actual:
    workout: Full Continuous 5K

  compliance:
    completed: false
    percentage: 84

  workout:
    raw: null

    type: null

    warmup:
      type: null
      duration: null
      unit: minutes

    intervals:
      repeat: null

      run:
        duration: null
        unit: minutes

      recovery:
        type: walk
        duration: null
        unit: minutes

    cooldown:
      type: null
      duration: null
      unit: minutes

nutrition:
  pre_run: []

  post_run: []

  hydration:
    before: null

    during: null

    after: null

  caffeine: false

  electrolyte: null

recovery:
  sleep:
    duration: null

    unit: hours

    quality: null

  muscle_soreness: null

  fatigue: null

  stress: null

weather: null

environment: null

cadence:
  value: null

  unit: spm

effort:
  rpe: null

feeling:
  overall: null

  energy: null

  legs: null

  breathing: null

  mental: null

  enjoyment: null

notes: []

milestones: []

personal_bests: []

injury:
  pain: false

  location: null

  resolved: null

gear:
  watch: null

  shoes: null

tags: []
---
```

---

# Field Definitions

## date

Workout date.

Type

String

Format

```
YYYY-MM-DD
```

---

# activity

Defines the primary and optional secondary activity.

## Primary Enum

- easy-run
- recovery-run
- long-run
- interval-run
- tempo-run
- progression-run
- fartlek
- race
- walk
- strength
- mobility
- cross-training

Secondary may contain any activity above or `null`.

Example

```yaml
activity:
  primary: easy-run
  secondary: mobility
```

---

# distance

Total workout distance.

```yaml
distance:
  value: 5.13
  unit: km
```

---

# duration

Workout duration.

```yaml
duration:
  value: 44.67
  unit: min
```

Always store duration as decimal minutes.

Display formatting may convert it to HH:MM:SS.

---

# pace

Average pace.

```yaml
pace:
  value: 8.40
  unit: min/km
```

---

# weight

```yaml
weight:
  value: 92.5
  unit: kg
```

---

# heart_rate

```yaml
heart_rate:
  average: 151
  max: 173
  unit: bpm
```

---

# training

Contains workout metadata.

Workout type enum:

- easy-run
- recovery-run
- long-run
- interval-run
- tempo-run
- progression-run
- fartlek
- race
- walk
- strength
- mobility

Both `raw` and `structured` workout information should be stored.

Example

```yaml
training:
  planned:
    app: null

    workout:
      raw: null

      type: null

      warmup:
        type: null
        duration: null
        unit: minutes

      intervals:
        repeat: null

        run:
          duration: null
          unit: minutes

        recovery:
          type: walk
          duration: null
          unit: minutes

      cooldown:
        type: null
        duration: null
        unit: minutes

  actual:
    completed: true

    workout:
      raw: null

      type: null

      warmup:
        type: null
        duration: null
        unit: minutes

      intervals:
        repeat: null

        run:
          duration: null
          unit: minutes

        recovery:
          type: walk
          duration: null
          unit: minutes

      cooldown:
        type: null
        duration: null
        unit: minutes

  compliance:
    completed: true

    percentage: 100

    reason: null
```

---

## planned

Represents the workout that was originally scheduled.

Examples:

- Runna plan
- Garmin Coach
- Self-created training plan

If no plan existed:

```yaml
planned: null
```

## actual

Represents what was actually completed during the workout.

This section always reflects reality and must never be estimated.

Example

```yaml
actual:
  completed: true

  workout:
    raw: "Easy Run 5K"

    type: easy-run
```

---

---

## compliance

Measures how closely the completed workout matched the planned workout.

```yaml
compliance:
  completed: true

  percentage: 100

  reason: null
```

### Fields

| Field      | Type           | Description                               |
| ---------- | -------------- | ----------------------------------------- |
| completed  | boolean        | Whether the planned workout was completed |
| percentage | number         | Estimated completion percentage (0–100+)  |
| reason     | string \| null | Reason for incomplete or modified workout |

---

### Example 1 — Perfect Compliance

```yaml
planned:
  app: Runna

actual:
  completed: true

compliance:
  completed: true
  percentage: 100
  reason: null
```

---

### Example 2 — Stopped Early

```yaml
planned:
  app: Runna

actual:
  completed: false

compliance:
  completed: false
  percentage: 65
  reason: "Stopped due to rain."
```

---

### Example 3 — Exceeded Plan

```yaml
planned:
  app: Runna

actual:
  completed: true

compliance:
  completed: true
  percentage: 120
  reason: "Felt strong and continued running."
```

---

## AI Guidelines

AI should never invent compliance values.

Compliance must always be calculated using the planned workout and the actual workout.

If a percentage cannot be determined confidently:

```yaml
percentage: null
```

Never guess.

# nutrition

Nutrition before and after training.

```yaml
nutrition:
  pre_run:
    - Bread

  post_run:
    - Protein Shake

  hydration:
    before: 500ml

    during: null

    after: 500ml

  caffeine: false

  electrolyte: Pocari
```

---

# recovery

```yaml
recovery:
  sleep:
    duration: 7

    unit: hours

    quality: Good

  muscle_soreness: Low

  fatigue: Medium

  stress: Low
```

Enums

Muscle soreness

- None
- Low
- Medium
- High

Fatigue

- None
- Low
- Medium
- High

Stress

- Low
- Medium
- High

Sleep Quality

- Poor
- Fair
- Good
- Excellent

---

# environment

Enum

- Road
- Track
- Trail
- Treadmill
- Mixed

---

# effort

RPE Scale

1–10

```yaml
effort:
  rpe: 8
```

---

# feeling

Rating Scale

1–5

```yaml
energy: 5
legs: 4
breathing: 3
mental: 5
enjoyment: 5
```

---

# personal_bests

Structured format.

Example

```yaml
personal_bests:
  - category: 5K

    value: "40:00"

    previous: "40:45"

    improvement: "-00:45"
```

---

# injury

```yaml
injury:
  pain: true

  location: Left Knee

  resolved: true
```

---

# gear

```yaml
gear:
  watch: Huawei Band 11

  shoes: Nike Pegasus 41
```

---

# Markdown Body

Every log should follow this structure.

```
# Workout Summary

# Heart Rate

# Training

# Feeling

# Notes

# Milestones (optional)

# Coach Analysis

## Highlights

## Improvements

## Risks

## Recommendation

# Progress

# Related Workout
```

---

# Null Values

Always use

```yaml
null
```

Never use

- Unknown
- N/A
- "-"
- Empty String

---

# Design Principles

This schema should always remain

- Human-readable
- AI-friendly
- Git-friendly
- Type-safe
- Future-proof
- Backward compatible
- Easy to parse
- Easy to edit manually

New fields may be added.

Existing field meanings should never change.
