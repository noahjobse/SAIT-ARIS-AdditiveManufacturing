# Week 9-10 Sprint Plan

**Sprint Duration:** Weeks 9-10 (14 days)
**Sprint Goal:** RAPID control flow (IF/ELSE/FOR/WHILE), all 3 robots supported
**Key Milestone:** RAPID with control flow executes correctly, robot selector switches models

---

## Sprint Overview

By the end of Week 10, we should have:

✅ RAPID control flow supported (IF/ELSE, FOR loops, WHILE loops)
✅ AST interpreter executes conditional logic correctly
✅ All 3 robot models fully functional (IRB 4600, 2600, 6700)
✅ Robot selector switches between models (loads different kinematics)
✅ Control flow visualization in UI (optional)
✅ Variable inspector shows RAPID variables (optional)
✅ RAPID procedure calls supported (PROC/ENDPROC)
✅ Multi-robot test matrix complete (3 robots × 5 programs)
✅ Control flow test suite validates logic execution

**Note:** This sprint contains stretch goals. Core focus is IF/ELSE implementation; FOR/WHILE are lower priority.

---

## Weekly Goals

### Week 9 Overview

**Frontend - Dylane:**
- Improve multi-robot selector UI (thumbnails, robot info)
- Add robot metadata panel (payload, reach, DH parameters)
- Optimize 3D rendering for robot model switching
- Test all 3 robots load correctly

**Frontend - Umaya:**
- Design control flow visualization (show IF branches, loop iterations)
- Create variable inspector panel (show RAPID variables)
- Improve RAPID editor with better syntax highlighting
- Add line highlighting for current execution point (optional)

**Backend - Jason:**
- Extend Lark grammar for IF/ELSE statements
- Add support for boolean expressions (comparisons, AND/OR)
- Begin AST interpreter for control flow
- Handle conditional branches in trajectory generation

**Backend - Noah:**
- Create URDF configs for IRB 2600 and IRB 6700 (complete)
- Validate DH parameters against ABB datasheets
- Test FK/IK for all 3 robots with known configurations
- Implement robot config loader (switch between robots)

**PM/QA - Noah:**
- Create control flow test suite
- Write tests for IF/ELSE branching
- Create multi-robot test matrix (3 robots × 5 programs)
- Document control flow behavior

### Week 10 Overview

**Frontend - Dylane:**
- Polish robot selector (smooth transitions, loading states)
- Test robot switching during simulation
- Add robot comparison feature (side-by-side specs, optional)
- Performance testing with all 3 robots

**Frontend - Umaya:**
- Implement control flow visualization (highlight active branch)
- Complete variable inspector (display values, update in real-time)
- Add execution trace panel (show execution history, optional)
- Test UI with complex control flow programs

**Backend - Jason:**
- Extend grammar for FOR and WHILE loops
- Implement loop execution in AST interpreter
- Add support for RAPID procedures (PROC/ENDPROC)
- Handle nested control flow (IF within FOR, etc.)
- Optimize interpreter performance

**Backend - Noah:**
- Verify all 3 robots handle control flow correctly
- Test edge cases (infinite loops, deeply nested conditions)
- Add execution timeout for loops (prevent infinite execution)
- Optimize robot config switching (cache URDFs)

**PM/QA - Noah:**
- Write tests for FOR and WHILE loops
- Write tests for nested control flow
- Run multi-robot test matrix (3 × 5 = 15 test cases)
- Test procedure calls (PROC/ENDPROC)
- Prepare sprint review demo

---

## Critical Daily Tasks

### Blocking Dependencies

**Week 9 Day 1 (Jason):** Add IF/ELSE to Lark grammar
- **Blocks:** Week 10 interpreter implementation
- **Why:** Grammar must support control flow before interpreter can execute it
- **Deliverable:** Grammar file with IF/ELSE rules, boolean expressions

**Week 9 Day 3 (Noah Backend):** Add IRB 2600 and IRB 6700 configs
- **Blocks:** Multi-robot testing, robot selector functionality
- **Why:** All 3 robots must be available for testing and switching
- **Deliverable:** URDF files for IRB 2600 and 6700, configs validated

### Cross-Team Integration Points

**Week 10 Day 2-3 (Umaya):** Variable inspector displays RAPID variables
- **Integration:** Requires Jason's interpreter to expose variable state
- **Verification:** Run RAPID with variables → see values in inspector
- **Fallback:** If interpreter doesn't expose state, show static variable list

**Week 10 Day 4-5 (All Team):** Multi-robot + control flow demo
- **Integration:** Test IF/ELSE with all 3 robots
- **Verification:** Same program runs correctly on IRB 4600, 2600, 6700
- **Demo:** Show robot switching + control flow in sprint review

---

## Weekly Task Breakdown

### Frontend - Dylane

**Week 9:**
- [ ] Update `RobotSelector.tsx` with robot thumbnails (3D preview or images)
- [ ] Add robot metadata display (payload, reach, DOF, manufacturer)
- [ ] Create `RobotInfoPanel.tsx` component
- [ ] Display DH parameters table (optional, for advanced users)
- [ ] Implement robot switching logic (clear scene, load new robot)
- [ ] Add loading spinner during robot model switch
- [ ] Test IRB 4600, 2600, 6700 switching (verify kinematics update)

**Week 10:**
- [ ] Polish robot selector UI (hover states, smooth transitions)
- [ ] Test robot switching during active simulation (pause, switch, resume)
- [ ] Optimize 3D scene (dispose old robot mesh before loading new)
- [ ] Add robot comparison table (optional: side-by-side specs)
- [ ] Test performance with all 3 robots (FPS, memory usage)
- [ ] Fix any robot-specific rendering bugs
- [ ] Add robot model validation (verify skeleton structure)

**Deliverable:** Robot selector polished, all 3 robots switch smoothly, performance optimized

---

### Frontend - Umaya

**Week 9:**
- [ ] Design control flow visualization UI (sketch wireframe)
- [ ] Create `ControlFlowVisualizer.tsx` component (optional)
- [ ] Show IF branches (highlight active branch during execution)
- [ ] Create `VariableInspector.tsx` component
- [ ] Display RAPID variables in table (name, type, value)
- [ ] Research Monaco Editor integration for better syntax highlighting
- [ ] Add line numbers and syntax coloring to RAPID editor

**Week 10:**
- [ ] Implement control flow visualization (highlight current IF/ELSE/FOR)
- [ ] Wire variable inspector to backend interpreter state
- [ ] Add real-time variable updates during simulation
- [ ] Create `ExecutionTrace.tsx` panel (optional: show execution history)
- [ ] Test UI with complex programs (nested IFs, loops)
- [ ] Add toggle to show/hide advanced panels (inspector, trace)
- [ ] Polish UI (consistent styling, clear labels)

**Deliverable:** Control flow visualized, variable inspector functional, RAPID editor improved

---

### Backend - Jason

**Week 9:**
- [ ] Extend `grammar.lark` for IF/ELSE statements
- [ ] Add grammar rules for boolean expressions (==, !=, <, >, AND, OR)
- [ ] Define AST nodes: `IfStatement`, `BooleanExpr`, `Condition`
- [ ] Create `backend/app/interpreter/control_flow.py`
- [ ] Implement `execute_if(condition, true_branch, false_branch)`
- [ ] Handle conditional branches in trajectory generation
- [ ] Test IF/ELSE with simple conditions (x > 0, etc.)

**Week 10:**
- [ ] Extend grammar for FOR loops (FOR i FROM 1 TO 10 DO ... ENDFOR)
- [ ] Extend grammar for WHILE loops (WHILE condition DO ... ENDWHILE)
- [ ] Implement loop execution in interpreter
- [ ] Add loop counter tracking (prevent infinite loops)
- [ ] Add support for RAPID procedures (PROC main() ... ENDPROC)
- [ ] Handle nested control flow (IF within FOR, etc.)
- [ ] Optimize interpreter (avoid redundant IK calculations in loops)
- [ ] Add execution trace logging (for debugging)

**Deliverable:** IF/ELSE/FOR/WHILE supported, AST interpreter executes control flow, procedures work

---

### Backend - Noah

**Week 9:**
- [ ] Create `/models/robots/irb2600/robot.urdf`
- [ ] Define DH parameters for IRB 2600 (from ABB datasheet)
- [ ] Create `/models/robots/irb6700/robot.urdf`
- [ ] Define DH parameters for IRB 6700 (from ABB datasheet)
- [ ] Validate URDFs load into PyBullet without errors
- [ ] Test FK with known configurations for IRB 2600 and 6700
- [ ] Create `backend/app/kinematics/robot_config_loader.py`
- [ ] Implement `load_robot_config(robot_id: str)` function

**Week 10:**
- [ ] Test control flow execution with all 3 robots
- [ ] Verify IF/ELSE produces same logic for all robots (different trajectories)
- [ ] Add execution timeout for loops (max 10,000 iterations)
- [ ] Handle timeout gracefully (return error, not crash)
- [ ] Optimize robot config switching (cache loaded URDFs)
- [ ] Test edge cases (empty loop, condition always false)
- [ ] Add logging for control flow execution (track branches taken)
- [ ] Write unit tests for control flow interpreter

**Deliverable:** All 3 robot URDFs complete, control flow works for all robots, timeouts prevent hangs

---

### PM/QA - Noah

**Week 9:**
- [ ] Create `backend/tests/test_control_flow.py`
- [ ] Write test: IF condition true → execute true branch
- [ ] Write test: IF condition false → execute false branch
- [ ] Write test: nested IF statements (IF within IF)
- [ ] Create multi-robot test matrix document
- [ ] Define 5 test programs (simple move, IF, FOR, complex, edge case)
- [ ] Write test: IRB 4600 executes program X correctly
- [ ] Write test: IRB 2600 executes program X correctly (compare results)

**Week 10:**
- [ ] Write test: FOR loop executes correct number of iterations
- [ ] Write test: WHILE loop terminates when condition false
- [ ] Write test: infinite loop timeout (verify error response)
- [ ] Write test: procedure call (PROC main calls PROC helper)
- [ ] Run multi-robot test matrix (3 robots × 5 programs = 15 tests)
- [ ] Document test results in `docs/testing/multi-robot-results.md`
- [ ] Write test: nested control flow (IF in FOR in WHILE)
- [ ] Prepare demo script for sprint review

**Deliverable:** Control flow test suite complete, multi-robot tests pass, results documented

---

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Control flow interpreter too complex for 2-week sprint | High | Medium | Implement IF/ELSE first, defer FOR/WHILE if timeline tight; focus on core functionality |
| Multi-robot configs have errors (wrong DH parameters) | Medium | High | Validate against ABB datasheets early; test FK with known configs before IK |
| Infinite loops crash backend | Medium | High | Add iteration limit (max 10,000), timeout (max 30s); return error gracefully |
| Variable inspector state synchronization difficult | Medium | Low | If complex, show static variable list only; defer real-time updates to Week 11 |
| Control flow visualization UX unclear | Low | Low | User testing in Week 10; simplify or make optional if confusing |
| Robot switching breaks active simulation | Low | Medium | Pause simulation before switch, clear trajectory, restart from beginning |

---

## Testing Requirements

**Week 9:**
- [ ] Test IF/ELSE grammar parses correctly (Jason + Noah)
- [ ] Test IF condition true/false executes correct branch (Jason + Noah)
- [ ] Test IRB 2600 URDF loads and FK works (Noah)
- [ ] Test IRB 6700 URDF loads and FK works (Noah)
- [ ] Test robot selector switches between all 3 robots (Dylane)
- [ ] Test variable inspector component renders (Umaya)

**Week 10:**
- [ ] Test FOR loop executes 10 iterations (Jason + Noah)
- [ ] Test WHILE loop terminates correctly (Jason + Noah)
- [ ] Test nested control flow (IF in FOR) (Noah)
- [ ] Test procedure call (PROC main → PROC helper) (Noah)
- [ ] Test timeout for infinite loop (Noah)
- [ ] Test multi-robot matrix (3 robots × 5 programs) (Noah)
- [ ] Test control flow visualization updates correctly (Umaya)

---

## Demo-Ready Acceptance Criteria

By end of this sprint, team can demo:

### Week 9 Demo Criteria:
- [ ] Upload RAPID with IF statement → correct branch executes
- [ ] Switch between IRB 4600, 2600, 6700 → robot models load correctly
- [ ] Robot metadata panel shows specs for each robot
- [ ] Variable inspector component visible (may be empty or mock data)

### Week 10 Demo Criteria (Full Sprint):
- [ ] **Upload RAPID with IF statement → correct branch executes (verified in trajectory)**
- [ ] **Upload RAPID with FOR loop → robot repeats motion correct number of times**
- [ ] **Switch between IRB 4600/2600/6700 → simulation works for all models**
- [ ] Control flow visualization highlights active branch (optional)
- [ ] Variable inspector displays RAPID variables (optional)
- [ ] Procedure calls work (PROC main → PROC helper)
- [ ] Timeout prevents infinite loops (demo graceful error handling)

---

## Definition of Done

A task is **DONE** when:

✅ Code written and committed to repo
✅ Code reviewed by at least one other team member (informal or PR)
✅ Tests written and passing (if applicable)
✅ No linting errors (ruff for backend, eslint for frontend)
✅ Documented in code comments (complex logic explained)
✅ Verified in browser/API (manual smoke test)
✅ Tested with all 3 robot models (if robot-specific feature)

---

## Team Assignments

| Person | Focus Area | Key Deliverable |
|--------|-----------|-----------------|
| **Dylane** | Multi-robot selector UI | All 3 robots switch smoothly |
| **Umaya** | Control flow visualization + variable inspector | Advanced panels functional |
| **Jason** | Control flow grammar + interpreter | IF/ELSE/FOR/WHILE working |
| **Noah (Backend)** | Multi-robot configs + control flow execution | All robots tested with control flow |
| **Noah (QA/PM)** | Control flow tests + multi-robot matrix | Test suite comprehensive |

---

## Communication

**Slack Channels:**
- `#abb-sim-dev` - General development discussion
- `#abb-sim-frontend` - Frontend-specific questions (Dylane, Umaya)
- `#abb-sim-backend` - Backend-specific questions (Jason, Noah)
- `#abb-sim-qa` - Testing and QA updates (Noah)

**Daily Standup:** 9:00 AM (15 minutes, async updates on weekends)

**Sprint Review:** End of Week 10 (30-minute demo, retrospective)

---

## Success Metrics

By end of Week 10, we should achieve:

- [ ] **Frontend:** Robot selector switches all 3 models smoothly
- [ ] **Frontend:** Control flow visualization and variable inspector (optional)
- [ ] **Backend:** IF/ELSE working, FOR/WHILE implemented (stretch)
- [ ] **Backend:** All 3 robot URDFs validated
- [ ] **QA:** Control flow tests pass
- [ ] **QA:** Multi-robot test matrix complete (3 × 5 = 15 tests)

**Sprint Goal Achievement:** 🟢 Green if IF/ELSE + all 3 robots working, 🟡 Yellow if IF/ELSE only, 🔴 Red if IF/ELSE incomplete

**Note:** FOR/WHILE are stretch goals. IF/ELSE + multi-robot support is the core deliverable.

---

## Next Sprint Planning

**Week 11 Preview (Finalization):**
- Dylane: Final UI polish, demo mode, demo video recording
- Umaya: User guide screenshots, final UX improvements
- Jason: API docs auto-generation, deployment config
- Noah (Backend): Architecture docs, deployment scripts
- Noah (QA): User guide, developer guide, final test pass, presentation

**Week 11 Goal:** Documentation, testing, final delivery, demo presentation

---

**Document Owner:** Noah (PM/QA Lead)
**Created:** 2026-02-05
**Last Updated:** 2026-02-05
**Next Update:** End of Week 10 (Sprint Review)
