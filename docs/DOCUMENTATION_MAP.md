# Documentation Map - Visual Navigation Guide

```
ABB Online Simulation Platform - Documentation Structure
══════════════════════════════════════════════════════════

📍 START HERE
├─ README.md (root) ──────────────────────────┐
└─ docs/START_HERE.md ⭐ MAIN ENTRY POINT     │
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────┐
│  LEVEL 1: Project Foundation (Read These First)          │
└──────────────────────────────────────────────────────────┘
│
├─ 📄 PROJECT_SPECIFICATION.md ⭐ CRITICAL
│  └─ MVP requirements (FR-1 to FR-7)
│  └─ Success criteria
│  └─ Technical architecture overview
│
├─ 📄 CLAUDE.md
│  └─ Development commands (setup, run, test)
│  └─ Quick reference for coding
│
└─ 📄 README.md
   └─ Repository overview
   └─ Quick start guide


┌──────────────────────────────────────────────────────────┐
│  LEVEL 2: Architecture & Design (Technical Foundation)   │
└──────────────────────────────────────────────────────────┘
│
├─ 📂 architecture/
│  ├─ system-design.md ⭐ CRITICAL
│  │  └─ Full pipeline (RAPID → parse → simulate → render)
│  │  └─ Component interaction diagrams
│  │  └─ Data flow architecture
│  │
│  └─ api-specification.md
│     └─ All endpoint definitions
│     └─ Request/response schemas
│     └─ Error codes


┌──────────────────────────────────────────────────────────┐
│  LEVEL 3: Sprint Plans (Week-by-Week Execution)          │
└──────────────────────────────────────────────────────────┘
│
├─ 📂 roadmap/
│  │
│  ├─ 11-week-plan.md (High-level overview)
│  │  └─ Phase 1: Weeks 1-3 (Visualization)
│  │  └─ Phase 2: Weeks 4-6 (Logic & kinematics)
│  │  └─ Phase 3: Weeks 7-8 (MVP polish) ⭐
│  │  └─ Phase 4: Weeks 9-11 (Stretch + handoff)
│  │
│  ├─ implementation-timeline.md (Person-by-person)
│  │  └─ Dylane, Umaya, Jason, Noah tasks
│  │  └─ Dependencies
│  │
│  ├─ 📋 DETAILED 2-WEEK SPRINT PLANS:
│  │
│  ├─ week-1-2-sprint-plan.md
│  │  └─ Foundation: 3D scene, robot loading, API structure
│  │  └─ Deliverable: Robot visible, sliders working
│  │
│  ├─ week-3-4-sprint-plan.md
│  │  └─ Parser & kinematics: RAPID parser, FK/IK, gizmo
│  │  └─ Deliverable: Upload RAPID → AST, FK working
│  │
│  ├─ week-5-6-sprint-plan.md
│  │  └─ Simulation pipeline: Trajectory, collision
│  │  └─ Deliverable: Full simulation, collision highlighting
│  │
│  ├─ week-7-8-sprint-plan.md ⭐ MVP LAUNCH
│  │  └─ Timeline scrubber, playback, UAT, MVP sign-off
│  │  └─ Deliverable: STUDENT MVP COMPLETE
│  │
│  ├─ week-9-10-sprint-plan.md (Stretch goals)
│  │  └─ Control flow (IF/ELSE/FOR/WHILE), multi-robot
│  │  └─ Deliverable: Control flow working, all 3 robots
│  │
│  └─ week-11-finalization.md (Handoff)
│     └─ Docs, testing, deployment, demo, presentation
│     └─ Deliverable: Project handoff complete


┌──────────────────────────────────────────────────────────┐
│  LEVEL 4: Team Coordination (Who's Doing What)           │
└──────────────────────────────────────────────────────────┘
│
└─ 📂 team/
   └─ task-assignments.md
      └─ Current sprint tasks by person
      └─ Links to all sprint plans
      └─ Task status tracking


┌──────────────────────────────────────────────────────────┐
│  LEVEL 5: Development Guides (Future - Week 11)          │
└──────────────────────────────────────────────────────────┘
│
└─ 📂 guides/ (Created in Week 11)
   ├─ user-guide.md (Step-by-step tutorials)
   ├─ developer-guide.md (How to extend)
   ├─ deployment-guide.md (How to deploy)
   └─ testing-strategy.md (How to test)


┌──────────────────────────────────────────────────────────┐
│  QUICK NAVIGATION BY ROLE                                │
└──────────────────────────────────────────────────────────┘

👤 FRONTEND DEVELOPER (Dylane, Umaya)
├─ 1. Read: PROJECT_SPECIFICATION.md
├─ 2. Read: architecture/system-design.md (Frontend sections)
├─ 3. Find current sprint: roadmap/week-X-Y-sprint-plan.md
├─ 4. Check tasks: team/task-assignments.md
└─ 5. Setup: CLAUDE.md (Frontend commands)

👤 BACKEND DEVELOPER (Jason, Noah)
├─ 1. Read: PROJECT_SPECIFICATION.md
├─ 2. Read: architecture/system-design.md (Backend sections)
├─ 3. Read: architecture/api-specification.md
├─ 4. Find current sprint: roadmap/week-X-Y-sprint-plan.md
├─ 5. Check tasks: team/task-assignments.md
└─ 6. Setup: CLAUDE.md (Backend commands)

👤 QA/PM (Noah)
├─ 1. Read: PROJECT_SPECIFICATION.md (MVP criteria)
├─ 2. Read: roadmap/11-week-plan.md (Overall timeline)
├─ 3. Find current sprint: roadmap/week-X-Y-sprint-plan.md
├─ 4. Read: roadmap/implementation-timeline.md
└─ 5. Check: team/task-assignments.md

👤 NEW TEAM MEMBER
├─ 1. Start: docs/START_HERE.md ⭐
├─ 2. Read: PROJECT_SPECIFICATION.md
├─ 3. Read: architecture/system-design.md
├─ 4. Find your role in: team/task-assignments.md
└─ 5. Check current sprint plan


┌──────────────────────────────────────────────────────────┐
│  DOCUMENT DEPENDENCY TREE                                │
└──────────────────────────────────────────────────────────┘

START_HERE.md (Entry point)
│
├─ Links to PROJECT_SPECIFICATION.md (What we're building)
│  └─ References architecture/system-design.md
│     └─ References architecture/api-specification.md
│
├─ Links to roadmap/11-week-plan.md (When we're building)
│  ├─ References roadmap/implementation-timeline.md
│  │
│  └─ Breaks down into detailed sprint plans:
│     ├─ week-1-2-sprint-plan.md
│     ├─ week-3-4-sprint-plan.md
│     ├─ week-5-6-sprint-plan.md
│     ├─ week-7-8-sprint-plan.md ⭐ MVP
│     ├─ week-9-10-sprint-plan.md
│     └─ week-11-finalization.md
│
├─ Links to team/task-assignments.md (Who's building)
│  └─ References all sprint plans
│
└─ Links to CLAUDE.md (How to build)


┌──────────────────────────────────────────────────────────┐
│  SPRINT PLAN FORMAT (Hybrid Structure)                   │
└──────────────────────────────────────────────────────────┘

Each 2-week sprint plan contains:

├─ Sprint Overview
│  └─ Goals, milestones, deliverables
│
├─ Weekly Goals
│  ├─ Week X Overview (high-level per person)
│  └─ Week Y Overview (high-level per person)
│
├─ Critical Daily Tasks ⚠️ (Integration points only)
│  ├─ Blocking dependencies
│  └─ Cross-team integration points
│
├─ Weekly Task Breakdown (Grouped by week, NOT daily)
│  ├─ Frontend - Dylane
│  ├─ Frontend - Umaya
│  ├─ Backend - Jason
│  ├─ Backend - Noah
│  └─ PM/QA - Noah
│
├─ Risk Management
│  └─ Likelihood, Impact, Mitigation
│
├─ Testing Requirements
│  └─ Week-specific test cases
│
├─ Demo-Ready Acceptance Criteria
│  └─ Testable deliverables
│
└─ Definition of Done
   └─ Checklist for task completion


┌──────────────────────────────────────────────────────────┐
│  CRITICAL INTEGRATION POINTS ACROSS SPRINTS              │
└──────────────────────────────────────────────────────────┘

Week 1 Day 1:
├─ GLB file added (Noah) ────────┐
└─ FastAPI routers setup (Jason)─┤
                                 ▼
Week 1 Day 3:
└─ Robot GLB loading (Dylane) ◄──┘

Week 3 Day 1:
└─ Lark grammar created (Jason) ─┐
                                 ▼
Week 4:
└─ Parser implementation ◄────────┘

Week 5 Day 1:
└─ SimulateRequest/Response schema (Jason) ─┐
                                             ▼
Week 5 Day 3-4:
└─ Frontend wires /api/simulate (Dylane) ◄───┘

Week 6 Day 1:
└─ Obstacle mesh in PyBullet (Noah) ─┐
                                     ▼
Week 6 Day 2-3:
└─ Collision testing ◄────────────────┘

Week 8 Day 1-2:
└─ UAT with real RAPID (Noah) ──┐
                                ▼
Week 8 Day 4:
└─ MVP Demo Rehearsal ◄──────────┘

Week 8 Day 5:
└─ 🎯 MVP SIGN-OFF ⭐


┌──────────────────────────────────────────────────────────┐
│  FINDING YOUR CURRENT SPRINT                             │
└──────────────────────────────────────────────────────────┘

Project Start Date: [Insert date]

Calculate: (Today - Start Date) / 7 = Week Number

├─ Weeks 1-2:   roadmap/week-1-2-sprint-plan.md
├─ Weeks 3-4:   roadmap/week-3-4-sprint-plan.md
├─ Weeks 5-6:   roadmap/week-5-6-sprint-plan.md
├─ Weeks 7-8:   roadmap/week-7-8-sprint-plan.md ⭐ MVP
├─ Weeks 9-10:  roadmap/week-9-10-sprint-plan.md
└─ Week 11:     roadmap/week-11-finalization.md


┌──────────────────────────────────────────────────────────┐
│  COMMUNICATION CHANNELS                                  │
└──────────────────────────────────────────────────────────┘

Slack Channels:
├─ #abb-sim-dev       (General discussion)
├─ #abb-sim-frontend  (Dylane, Umaya)
├─ #abb-sim-backend   (Jason, Noah)
└─ #abb-sim-qa        (Noah, testing updates)

Meetings:
├─ Daily Standup: 9:00 AM (15 min)
└─ Sprint Review: End of each 2-week sprint (30 min)


══════════════════════════════════════════════════════════
Last Updated: 2026-02-05
Maintained By: Noah (PM/QA Lead)
```

---

## How to Use This Map

1. **Print this page** and keep it visible at your desk
2. **Bookmark** `docs/START_HERE.md` in your browser
3. **Start every work session** by checking your current sprint plan
4. **When blocked**, refer to the integration points in this map
5. **Lost?** Return to `docs/START_HERE.md`

---

## Legend

- ⭐ = Critical document or milestone
- 📄 = Single document
- 📂 = Directory containing multiple documents
- 📋 = Detailed task list
- 🎯 = Major project milestone
- ⚠️ = Critical integration point
- ◄─ = Dependency (requires completion of previous step)
