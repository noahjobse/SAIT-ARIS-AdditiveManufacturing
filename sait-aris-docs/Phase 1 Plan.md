# PHASE 1 — MASTER PLAN

> Related: [[ARIS Meeting Notes|ARIS Meeting Notes]], [[ARIS Plan Doc|ARIS Plan Doc]], [[Plan Timeline|Plan Timeline]]

**Phase:** Simulation & Digital Validation

**Duration:** Weeks 1–5

**Purpose:** Prove and understand the full digital pipeline (STL → toolpath → RAPID → multi-layer simulation) **before** any hardware work.

**Note:** This phase aligns with ARIS collaboration model: ~weekly meetings (30–60 min) for guidance and oversight. See [[ARIS Meeting Notes|ARIS Meeting Notes]] for full meeting context.

---

## 1) Phase 1 Objective (Locked)

Build a **robust, defensible simulation pipeline** in ABB RobotStudio + 3DP PowerPac that:

- Converts **STL → toolpath → RAPID**
- Successfully simulates **multi-layer prints**
- Covers:
    - **Two test geometries**
    - **Rocket v1 (baseline)**
    - **Rocket v2 (one deliberate iteration)**
- Uses **optimized-as-possible parameters** (for simulation)
- Documents:
    - **Blockers**
    - **Quality risks**
    - Root causes and mitigations
- Produces **annotated evidence** suitable for ARIS review

---

## 2) Phase 1 Success Gate (Exit Criteria)

Phase 1 is complete **only when**:

- ✅ No **blockers** remain
- ✅ All **quality risks** are **understood and documented**
- ❌ Quality risks do **not** need to be eliminated
- ❌ Hardware assumptions are **not** introduced

At completion, a **Phase 1 Freeze Package** is produced and handed to Phase 2.

---

## 3) Collaboration Model (Critical)

### What you are actually doing

You are **configuring simulations that generate robot code**, then **choosing and documenting the best outputs**.

### Rules

- ❌ No shared live editing of RobotStudio files
- ❌ No “master code file”
- ✅ Local experimentation
- ✅ Shared artifacts

### File reality

|   |   |
|---|---|
|Item|How it’s used|
|`.rsstation` (RobotStudio)|Local, disposable, never merged|
|RAPID `.mod` files|Generated outputs, shared|
|Docs / media|Shared, authoritative|
|Baseline station|Shared, **read-only**, versioned|  

---

## 4) Baseline RobotStudio Station (Locked)

**Owner:** You (only)

### Allowed contents

- Robot model
- Neutral cell layout
- **One example STL** (reference/learning only)

### Not allowed

- Final toolpaths
- Tuned/optimized parameters
- Authoritative test or rocket geometry

### Baseline update rule

- Updated **only** if a **foundational issue** is discovered
- (e.g., wrong robot model, coordinate convention)
- Versioned explicitly (e.g., `baseline_station_v1.rsstation`)

---

## 5) What Is Being “Edited” in Phase 1

- **Not code** in the traditional sense
- **Configuration inside RobotStudio**:
    - Speeds
    - Layer height
    - Path strategy
    - Orientation
    - Tool/workobject setup (virtual)

These configurations **generate RAPID**.

RAPID is selected, not merged.

---

## 6) Test Scope (Locked)

### Test Geometries

You will simulate **exactly two**:

1. **Test Geometry 1**
    - Flat pad / straight wall type
    - Purpose: layer stacking, starts/stops, baseline motion
2. **Test Geometry 2**
    - Curved or vertical geometry (e.g., cylinder/curved wall)
    - Purpose: curvature, orientation, reach, smoothness

### Rocket

- **Rocket v1:** baseline simulation
- **Rocket v2:** exactly **one deliberate change**
    - Orientation **or**
    - Layer/path strategy **or**
    - Toolpath parameter

---

## 7) Parameter Philosophy (Locked)

- Parameters are **optimized-as-possible** within simulation
- Values must be:
    - Deliberate
    - Justified
    - Expected to change in Phase 2
- “Placeholder only” values are **not acceptable**

---

## 8) Failure & Risk Classification (Locked)

### Blocker

- Simulation **cannot complete end-to-end**
- Examples:
    - Crash
    - Invalid motion
    - Hard stop
    - Simulation error

### Quality Risk

- Simulation completes
- Something looks questionable for print quality
    - Sharp turns
    - Awkward layer transitions
    - Suspicious orientation

**Rule:**

- Blockers must be resolved
- Quality risks must be understood and documented

---

## 9) Iteration Discipline (Locked)

- Iteration continues **until root cause is understood**
- Elimination of the issue is **attempted when feasible**
- No endless tuning once understanding is achieved

---

## 10) Evidence Minimum (Locked)

For **every** Phase 1 run

(TG1, TG2, Rocket v1, Rocket v2):

**Minimum required:**

- ≥ **3 annotated screenshots**
    - Overall toolpath
    - Close-up (layers / turns)
    - Frame/TCP visibility
- ≥ **1 short screen recording**
    - Shows multi-layer progression

If this minimum is not met → the run is **not complete**.

---

## 11) Naming & Versioning (Locked)

**Date-based naming only**

Examples:

- `2026-01-28_tg1_wall.mod`
- `2026-02-06_tg2_cylinder.mod`
- `2026-02-14_rocket_v1.mod`
- `2026-02-20_rocket_v2.mod`

Applies to:

- RAPID
- Screenshots
- Videos

---

## 12) Phase 1 Freeze Trigger (Locked)

Phase 1 freezes when:

- ✅ All planned runs exist (TG1, TG2, Rocket v1, Rocket v2)
- ✅ No blockers remain
- ✅ All quality risks are explained

At freeze:

- Phase 1 stops
- Outputs are curated
- Package is prepared for Phase 2

---

## 13) Phase 1 Timeline (Weeks 1–5)

### Week 1

- Repo scaffold
- Baseline station created
- Test geometries + rocket STL selected
- Evidence standard defined

### Week 2

- Test Geometry 1
- First end-to-end pipeline
- Initial parameter rationale
- **Jan monthly update**

### Week 3

- Test Geometry 2
- Comparison vs TG1
- Risk identification

### Week 4

- Rocket v1 baseline simulation
- Major constraints surfaced

### Week 5

- Rocket v2 (one deliberate change)
- Comparison v1 vs v2
- Phase 1 Freeze Package
- **Feb monthly update**

---

## 14) Phase 1 Outputs (Complete List)

### Technical

- RAPID for:
    - Test Geometry 1
    - Test Geometry 2
    - Rocket v1
    - Rocket v2
- RobotStudio baseline station (versioned)

### Evidence

- Annotated screenshots
- Screen recordings

### Documentation

- Parameter rationale
- Failure & risk log
- Geometry comparisons
- Rocket v1 vs v2 comparison
- Phase 1 freeze summary

---

## 15) Git Usage (Phase 1)

**Git is the system of record for:**

- RAPID
- Docs
- Evidence
- Baseline station (read-only)

**Git is NOT used for:**

- Co-editing RobotStudio
- Merging `.rsstation` files

> **Rule of thumb:**

> _We don’t co-edit simulations. We co-edit results._