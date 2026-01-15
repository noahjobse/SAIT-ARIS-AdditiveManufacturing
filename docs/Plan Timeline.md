## 14-week top-down schedule (Jan 19 → Apr 24)

> Related: [[ARIS Plan Doc|ARIS Plan Doc]], [[Phase 1 Plan|Phase 1 Plan]]

### Phase 1 — Simulation and Digital Validation (Weeks 1–5)

> See [[Phase 1 Plan|Phase 1 Plan]] for complete Phase 1 details.

**Goal:** STL → slice → simulate → RAPID, with test geometry **and** the impressive rocket.

**Week 1 (Jan 19–25)** — Kickoff + constraints + RobotStudio setup

- Lab tour / access expectations + safety rules (you lead)
  - **Note:** Requires formal ARIS lab tour, student name list submission, and approvals (Majid coordinating) (see [[ARIS Meeting Notes|ARIS Meeting Notes]])
- RobotStudio installed, project repo/structure ready
- Pick rocket STL + define "test geometry" pieces
- Provide skills/experience summary to ARIS (per meeting notes)

**Week 2 (Jan 26–Feb 1)** — Test geometry slicing + first RAPID

- Slice simple shapes (wall/pad/cylinder)
- Generate RAPID + run full simulation
- Start monthly report #1 draft (end of week)

**Week 3 (Feb 2–8)** — Tool/WorkObject virtual setup + iteration

- Define virtual TCP + WorkObject frame
- Fix collisions / reachability issues
- Version toolpaths (v1 → v2)

**Week 4 (Feb 9–15)** — Rocket slicing + simulation v1

- Slice the “impressive” rocket
- Simulate full multi-layer path
- Capture clean screenshots/video for ARIS

**Week 5 (Feb 16–22)** — Phase 1 freeze + handoff package

- Finalize Phase 1 artifacts: RAPID + station + parameters sheet
- “Hardware readiness checklist” prepared (mounting, wiring assumptions)
- Monthly report #1 submitted (if ARIS cadence aligns to late Feb)

---

### Phase 2 — Hardware Integration and Calibration (Weeks 6–10)

> See [[ARIS Plan Doc|ARIS Plan Doc]] for Phase 2 objectives.

**Goal:** Mount tool + bed, control temps/extrusion, calibrate TCP/WObj, stable multi-layer test print.

**Week 6 (Feb 23–Mar 1)** — Hardware onboarding + mounting plan locked

- Confirm what you’re allowed to attach/modify
- Finalize extruder mount concept + cable routing plan
- Monthly report #2 (Feb) submitted

**Week 7 (Mar 2–8)** — Extruder integration (tool) + basic control verification

- Mount hotend extruder
- Verify temperature monitoring/control
- Verify extrusion control interface (rate on/off)

**Week 8 (Mar 9–15)** — Heated bed integration (WorkObject)

- Mount bed / define WorkObject physically
- Verify bed temperature stability
- Dry runs: motion only, no extrusion

**Week 9 (Mar 16–22)** — Calibration week (TCP + WorkObject)

- TCP calibration for nozzle tip
- WorkObject calibration for bed frame
- First extrusion passes on simple geometry

**Week 10 (Mar 23–29)** — Multi-layer simple geometry print + baseline tuning

- Achieve a repeatable multi-layer test print
- Lock baseline: temp range, speed range, extrusion rate
- Monthly report #3 (March) submitted

---

### Phase 3 — Final Print and Results (Weeks 11–14)

> See [[ARIS Plan Doc|ARIS Plan Doc]] for Phase 3 objectives.

**Goal:** Print the rocket, evaluate results vs simulation, final demo/report.

**Week 11 (Mar 30–Apr 5)** — Rocket “pre-flight” + partial / first attempt

- Re-verify calibration
- Rocket dry run (no extrusion)
- First real rocket attempt (or partial height test)

**Week 12 (Apr 6–12)** — Fix the top 1–2 failure modes

- Focused iteration (adhesion OR extrusion stability OR path artifacts)
- Second rocket attempt (if needed)

**Week 13 (Apr 13–19)** — Final rocket print + evidence capture

- Best-effort final print run
- Full photo/video documentation
- Start final report + slide/demo outline

**Week 14 (Apr 20–26)** — Final report + ARIS demo (Apr 24 week)

- Final results write-up + lessons learned
- Deliver: strengths/weaknesses + what you’d improve
- Monthly/final report #4 submitted + presentation/demo

---

## Monthly reporting checkpoints (aligned to your requirement)

- **End of Feb:** Phase 1 progress package (simulation/RAPID heavy)
- **End of Mar:** Hardware integration + calibration + test prints
- **Apr 24 week:** Final results + demo + full lessons learned
- (If ARIS wants “true monthly,” you can also send a short update end of Jan, but the above matches the real work milestones.)