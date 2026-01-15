## ARIS Micro-Project Executive Plan (One Page)

> Related: [[ARIS Meeting Notes|ARIS Meeting Notes]], [[Phase 1 Plan|Phase 1 Plan]], [[Plan Timeline|Plan Timeline]]

**Project Title:** Additive Manufacturing Employing Articulated Robot Arms

**Sponsor/Stakeholder:** ARIS Robotics  
**Status:** Confirmed & Aligned (see [[ARIS Meeting Notes|ARIS Meeting Notes]] for details)
**Key Contacts:** Craig, Ryan, Majid (ARIS); Prof. Omar (Instructor); Noah (Student Lead)

**Core Goal:** Build and validate an additive manufacturing workflow using a conventional industrial robot arm (ABB IRB 140 or similar), from STL input through simulation and RAPID execution to a physical multi-layer print (target artifact: a 3D printed model rocket).

---

### 1) Project Purpose

This project focuses on employing an industrial articulated robot arm as an additive manufacturing system capable of receiving an STL file, generating a toolpath, validating it in simulation, and executing a multi-layer print using a hotend extruder and temperature-stabilized print bed.

---

### 2) Required Objectives (Project Commitments)

1. Generate a toolpath and RAPID code from an STL (sample rocket) using RobotStudio 3DP PowerPac or RoboDK.
2. Integrate a PLA or PETG hotend extruder as a robot tool, including:
    - Monitor hotend temperature
    - Control extrusion rate
3. Integrate a temperature-stabilized print bed as a workobject, including:
    - Control and monitor hot-bed temperature
4. Perform TCP and WorkObject calibration with fixed extruder tool and attached workobject (hotbed).
5. Perform a multi-layer print using the integrated hardware.
6. Report progress and final results to ARIS monthly with:
    - Project management breakdown
    - Technical documentation
    - Obstacles and solutions
    - Final results

---

### 3) Approach and Work Phases (Top-Down)

**Phase 1 — Simulation & Digital Validation** (see [[Phase 1 Plan|Phase 1 Plan]])

- RobotStudio + 3DP PowerPac workflow: STL → slicing/toolpath → RAPID → simulation validation
- Run **simple test geometry first**, then the **rocket** simulation
- Define virtual TCP and WorkObject frames to prepare for physical calibration

**Phase 2 — Hardware Integration & Calibration**

- Integrate extruder tool (temperature monitoring + extrusion control)
- Integrate heated bed as WorkObject (temperature monitoring + control)
- Perform TCP + WorkObject calibration
- Produce stable multi-layer test prints on simple geometry

**Phase 3 — Final Print & Evaluation**

- Execute multi-layer rocket print (best achievable quality)
- Document results, compare expected vs actual behavior, record lessons learned
- Deliver final demo + final report package

---

### 4) Timeline (14 Weeks)

**Project window:** Week 3 of January → week of April 24 (14 weeks)

- **Weeks 1–5:** Phase 1 (Simulation & Digital Validation) (see [[Phase 1 Plan|Phase 1 Plan]])
- **Weeks 6–10:** Phase 2 (Hardware Integration & Calibration)
- **Weeks 11–14:** Phase 3 (Final Print, Results, Demo)

See [[Plan Timeline|Plan Timeline]] for detailed week-by-week schedule.

---

### 5) Team Structure and Accountability

**Execution model:** “Lead + team support” per domain (everyone contributes across phases; leads ensure closure).

- **Project Integration & Documentation Lead:** Noah (also owns monthly ARIS reporting)
- **Safety & Lab Compliance Lead:** Noah
- **Simulation & Toolpath (RobotStudio) — Co-Leads:** (assigned by team)
- **Extruder & Material System — Lead:** (assigned by team)
- **Print Bed & WorkObject — Lead:** (assigned by team)
- **Calibration & Accuracy — Lead:** (assigned by team)

---

### 6) Risks and Mitigations (TBD items called out explicitly)

**Key risks (to be managed):**

- Toolpath/simulation validity vs real-world execution
- Calibration accuracy (TCP/WorkObject) impacting print quality
- Hardware integration complexity (extruder/bed control and safe mounting)
- Lab access constraints (time windows, safety approvals)

**Mitigation strategy:**

- Simulation-first gating (test geometry → rocket)
- Calibration procedure documented and repeatable
- Early safety/compliance alignment and checklists
- Maintain an obstacle log with fixes for monthly reporting

**Confirmed with ARIS (see [[ARIS Meeting Notes|Meeting Notes]]):**

- Lab access requires formal tour, student name list, and internal approvals (Majid coordinating, returning mid-next week)
- Collaboration model: ~weekly meetings (30–60 min) for guidance/oversight, not day-to-day supervision
- No hard deliverable date or success threshold; research-focused progress demonstration valued
- Technical approach confirmed: RobotStudio + 3DP PowerPac, RAPID, G-code → RAPID conversion, simulation-first

**Still to be confirmed:**

- Exact lab access start date and frequency (pending Majid return)
- Tooling/mounting constraints and approval process
- Available extruder/bed hardware and interface requirements

---

### 7) Reporting Deliverable (Monthly)

Each monthly update to ARIS will include:

1. Project management breakdown
2. Technical documentation (evidence: screenshots/photos/videos/logs)
3. Obstacles and solutions (root cause + fix + outcome)
4. Current results / final results (as applicable)

**Note:** ARIS values demonstrated progress, working/partially working systems, clear documentation, demonstrations, and lessons learned. This is research-focused, not a production deliverable with hard success thresholds.