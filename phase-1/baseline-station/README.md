# Baseline RobotStudio Station

## Owner
**You (only)** - This directory is locked to prevent accidental commits of working stations.

## Purpose
This directory contains the **versioned baseline RobotStudio station** - a minimal, foundational setup that serves as the starting point for all Phase 1 simulations.

## Allowed Contents

- Robot model (ABB IRB 140 or similar)
- Neutral cell layout
- **One example STL** (reference/learning only)

## NOT Allowed

- Final toolpaths
- Tuned/optimized parameters
- Authoritative test or rocket geometry
- Working/experimental stations

## Baseline Update Rule

The baseline station is updated **only** if a **foundational issue** is discovered, such as:
- Wrong robot model
- Incorrect coordinate convention
- Fundamental setup error

When updated, it must be **versioned explicitly**:
- `baseline_station_v1.rsstation`
- `baseline_station_v2.rsstation`
- etc.

## File Reality

Per Phase 1 Master Plan:
- ❌ No shared live editing of RobotStudio files
- ❌ No "master code file"
- ✅ Local experimentation (outside this directory)
- ✅ Shared artifacts (RAPID, docs, evidence)

**Rule of thumb:** We don't co-edit simulations. We co-edit results.

## Usage

1. Copy the baseline station to a local working directory
2. Perform your simulation work locally
3. Generate RAPID and evidence from your local station
4. Commit only the outputs (RAPID `.mod` files, screenshots, videos) to the repository
5. **Do NOT commit your working `.rsstation` files**
