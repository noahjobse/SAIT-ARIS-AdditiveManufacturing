# Week 7-8 Sprint Plan (MVP LAUNCH)

**Sprint Duration:** Weeks 7-8 (14 days)
**Sprint Goal:** Timeline scrubber, playback controls, error states, MVP sign-off
**Key Milestone:** **STUDENT MVP COMPLETE** - Upload RAPID → watch robot move with collision feedback

---

## Sprint Overview

By the end of Week 8, we should have:

✅ Timeline scrubber allows seeking through trajectory
✅ Speed controls adjust playback speed (0.25x, 0.5x, 1x, 2x)
✅ Step-through controls (next waypoint, previous waypoint)
✅ Error states with friendly messages (upload failed, IK failed, etc.)
✅ Loading indicators for all async operations
✅ Responsive layout (works on tablets, large monitors)
✅ Bug fixes from Weeks 1-6
✅ Full regression testing passed
✅ User acceptance testing with real RAPID programs
✅ **MVP SIGN-OFF COMPLETE**

---

## Weekly Goals

### Week 7 Overview

**Frontend - Dylane:**
- Implement timeline scrubber (seek to any waypoint)
- Add step-through controls (next/previous waypoint)
- Wire speed controls to animation playback rate
- Fix animation bugs from Week 5-6

**Frontend - Umaya:**
- Build speed control UI (dropdown or slider)
- Add loading indicators for all async operations
- Improve error state handling (network errors, validation errors)
- Test responsive layout on multiple screen sizes

**Backend - Jason:**
- Implement IK result caching (avoid redundant calculations)
- Add edge case handling (malformed targets, invalid syntax)
- Improve error messages (include line numbers, helpful suggestions)
- Optimize trajectory generation further

**Backend - Noah:**
- Add input validation hardening (sanitize file uploads)
- Implement timeout handling for IK solver
- Fix bugs found during testing
- Add detailed logging for debugging

**PM/QA - Noah:**
- Run full regression testing (all features from Weeks 1-6)
- Create test matrix (browsers, screen sizes, robot models)
- Document known issues and workarounds
- Prepare UAT test plan

### Week 8 Overview

**Frontend - Dylane:**
- Polish timeline scrubber (add tooltips, improve UX)
- Fix any remaining animation bugs
- Optimize rendering performance
- Add visual polish (animations, transitions)

**Frontend - Umaya:**
- Complete error state coverage (all endpoints)
- Add responsive layout fixes (mobile, tablet)
- Polish UI (spacing, alignment, colors)
- Test accessibility (keyboard navigation, screen reader)

**Backend - Jason:**
- Fix bugs from UAT
- Add validation for edge cases
- Improve API documentation in Swagger
- Performance optimization final pass

**Backend - Noah:**
- Fix bugs from UAT
- Add error logging and monitoring
- Validate all 3 robot models work correctly
- Final security review (input validation)

**PM/QA - Noah:**
- Conduct user acceptance testing with 10+ real RAPID programs
- Document test results and bugs
- Verify MVP acceptance criteria met
- **Conduct MVP sign-off demo with stakeholders**
- Write sprint retrospective

---

## Critical Daily Tasks

### Blocking Dependencies

**Week 7 Day 1 (Dylane):** Implement timeline scrubber
- **Blocks:** Seek functionality, step-through controls
- **Why:** Scrubber is foundation for all timeline-based playback features
- **Deliverable:** Scrubber component functional, can seek to any waypoint

**Week 7 Day 4-5 (All Team):** Integration - Wire speed controls to backend simulation
- **Integration:** Speed parameter must be added to `/api/simulate` request
- **Verification:** Changing speed dropdown updates simulation playback rate
- **Alternative:** If backend parameter not ready, speed controls work client-side only

### Cross-Team Integration Points

**Week 8 Day 1-2 (Noah QA):** Run UAT with 10+ real RAPID programs
- **Integration:** Tests full pipeline across all team members' work
- **Verification:** All programs execute without crashes, collisions detected correctly
- **Blockers:** Any critical bugs found must be fixed before MVP sign-off

**Week 8 Day 4 (All Team):** Final MVP demo rehearsal
- **Integration:** Entire team participates, stakeholders invited
- **Preparation:** Demo script, test data, backup plans for common issues
- **Verification:** Can demo all MVP features without errors

**Week 8 Day 5 (All Team):** MVP SIGN-OFF
- **Milestone:** Project meets all MVP acceptance criteria
- **Deliverable:** Document completion, demo presentation, handoff to stakeholders
- **Celebration:** Team completes 8-week MVP sprint!

---

## Weekly Task Breakdown

### Frontend - Dylane

**Week 7:**
- [ ] Create `TimelineScrubber.tsx` component in `src/components/controls/`
- [ ] Implement range slider for timeline (0 to max waypoint index)
- [ ] Wire scrubber to AnimationController (seek to waypoint function)
- [ ] Add current time display (MM:SS or waypoint index)
- [ ] Create step-through buttons (next, previous)
- [ ] Implement `seekToWaypoint(index: number)` in AnimationController
- [ ] Add speed control integration (0.25x, 0.5x, 1x, 2x multiplier)
- [ ] Fix animation bugs (jitter, incorrect joint angles)

**Week 8:**
- [ ] Add tooltip to scrubber (show waypoint details on hover)
- [ ] Improve scrubber UX (larger hit area, smooth dragging)
- [ ] Add keyboard shortcuts (space = play/pause, arrow keys = step)
- [ ] Optimize rendering performance (check FPS under load)
- [ ] Add smooth transitions for step-through (not instant jumps)
- [ ] Test timeline scrubber with long trajectories (500+ waypoints)
- [ ] Polish animations (fade in/out, smooth start/stop)
- [ ] Fix any remaining bugs from UAT

**Deliverable:** Timeline scrubber polished and functional, speed controls work, step-through smooth, no critical bugs

---

### Frontend - Umaya

**Week 7:**
- [ ] Create `SpeedControl.tsx` component (dropdown or radio buttons)
- [ ] Add speed options: 0.25x, 0.5x, 1x (default), 2x
- [ ] Wire speed control to AnimationController playback rate
- [ ] Create `LoadingIndicator.tsx` component (reusable spinner)
- [ ] Add loading states to all async operations (upload, simulate, load obstacles)
- [ ] Improve error handling in `api.ts` (network errors, timeouts)
- [ ] Create `ErrorMessage.tsx` component (reusable error display)
- [ ] Test responsive layout on tablet (768px width)

**Week 8:**
- [ ] Add error states for all endpoints (upload, simulate, robots, obstacles)
- [ ] Display friendly error messages (not raw API errors)
- [ ] Add retry buttons for failed operations
- [ ] Test responsive layout on mobile (320px, 375px, 414px widths)
- [ ] Fix layout issues (overlapping, clipped content)
- [ ] Polish UI spacing and alignment (use Tailwind spacing utilities)
- [ ] Test keyboard navigation (tab order, focus states)
- [ ] Add ARIA labels for accessibility (screen reader support)

**Deliverable:** All error states covered, loading indicators everywhere, responsive layout works on all screen sizes, accessible

---

### Backend - Jason

**Week 7:**
- [ ] Implement IK result caching in `kinematics/pybullet_ik.py`
- [ ] Cache key: (robot_id, target_position, target_orientation)
- [ ] Add LRU cache with max 1000 entries
- [ ] Add edge case handling for malformed RAPID targets
- [ ] Improve error messages (include line numbers, example syntax)
- [ ] Add validation for target positions (within robot reach sphere)
- [ ] Optimize trajectory generation (profile and identify bottlenecks)
- [ ] Add logging for slow operations (>1s)

**Week 8:**
- [ ] Fix bugs reported during UAT
- [ ] Add more detailed error messages for common mistakes
- [ ] Improve Swagger UI documentation (add examples, descriptions)
- [ ] Add input validation for `/api/simulate` (check robot_id, obstacles)
- [ ] Optimize collision detection (profile and optimize if >5s)
- [ ] Add performance metrics to response (simulation_time_ms)
- [ ] Write migration guide for future API changes
- [ ] Final code review and cleanup

**Deliverable:** IK caching improves performance, error messages helpful, bugs fixed, API documented

---

### Backend - Noah

**Week 7:**
- [ ] Add input validation for file uploads (sanitize filenames)
- [ ] Implement timeout handling for IK solver (max 2s per target)
- [ ] Add timeout handling for collision detection (max 5s total)
- [ ] Fix bugs found during Week 5-6 testing
- [ ] Add detailed logging with log levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Test edge case: upload very large RAPID file (>1MB, should reject)
- [ ] Test edge case: upload binary file as RAPID (should reject)
- [ ] Add health check improvements (check PyBullet status)

**Week 8:**
- [ ] Fix bugs reported during UAT
- [ ] Add error logging for all exceptions
- [ ] Validate all 3 robot models work with real RAPID programs
- [ ] Test with IRB 2600 and IRB 6700 (not just IRB 4600)
- [ ] Add security review checklist (input validation, file uploads)
- [ ] Test with malicious inputs (SQL injection attempts, path traversal)
- [ ] Add rate limiting for upload endpoints (prevent abuse)
- [ ] Final security and performance review

**Deliverable:** Input validation hardened, timeouts prevent hangs, security reviewed, all robots tested

---

### PM/QA - Noah

**Week 7:**
- [ ] Create `docs/testing/regression-test-plan.md`
- [ ] Document all features to test (Weeks 1-6)
- [ ] Create test matrix: 3 browsers × 3 screen sizes × 3 robot models
- [ ] Run regression tests on Chrome, Firefox, Safari (or Edge)
- [ ] Test all features: upload, parse, simulate, animate, collision, gizmo
- [ ] Document known issues in `docs/KNOWN_ISSUES.md`
- [ ] Create UAT test plan with 10+ real RAPID programs
- [ ] Prepare test data (RAPID files from RobotStudio or ABB examples)

**Week 8:**
- [ ] Conduct UAT Day 1-2: Run 10+ RAPID programs through full pipeline
- [ ] Document UAT results (pass/fail, issues found)
- [ ] Log bugs in GitHub Issues (critical, high, medium, low priority)
- [ ] Verify critical bugs fixed before sign-off
- [ ] Create MVP acceptance checklist (based on FR-1 to FR-7)
- [ ] Schedule MVP sign-off demo with stakeholders
- [ ] Prepare demo script and backup plan
- [ ] **Conduct MVP sign-off demo (Day 4-5)**
- [ ] Document demo outcome and feedback
- [ ] Write sprint retrospective (what went well, what to improve)

**Deliverable:** Regression tests pass, UAT complete, bugs documented/fixed, MVP sign-off successful

---

## Risk Management

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Critical bugs discovered in Week 8 (too late to fix) | Medium | Critical | Week 7 regression testing catches issues early; buffer time in Week 8 for fixes |
| MVP demo fails due to edge case | Low | Critical | Test with diverse RAPID programs (simple, complex, edge cases); have backup demo ready |
| Performance degrades on low-end hardware | Medium | Medium | Test on integrated GPU, optimize Babylon.js rendering; document minimum requirements |
| UAT reveals major usability issues | Medium | High | Conduct internal usability testing in Week 7; iterate on UI/UX before UAT |
| Timeline scrubber UX confusing for users | Low | Medium | User testing in Week 7, add tooltips and labels; simplify if needed |
| Collision detection still has false positives | Low | Medium | Document limitations in user guide; provide manual override if needed |

---

## Testing Requirements

**Week 7:**
- [ ] Test timeline scrubber with 50, 100, 500 waypoint trajectories (Dylane)
- [ ] Test speed controls (0.25x, 0.5x, 1x, 2x) (Dylane + Umaya)
- [ ] Test step-through controls (next, previous) (Dylane)
- [ ] Test IK caching improves performance (Jason + Noah)
- [ ] Test all error states (upload fail, parse fail, IK fail) (Umaya + Noah)
- [ ] Test responsive layout on 3 screen sizes (Umaya)
- [ ] Run full regression: all features from Weeks 1-6 (Noah)

**Week 8:**
- [ ] Conduct UAT with 10+ real RAPID programs (Noah + All)
- [ ] Test all 3 robot models (IRB 4600, 2600, 6700) (Noah)
- [ ] Test edge cases (empty RAPID, unreachable target, no obstacles) (Noah)
- [ ] Test accessibility (keyboard navigation, screen reader) (Umaya)
- [ ] Test performance on low-end hardware (integrated GPU) (Dylane)
- [ ] Verify all MVP acceptance criteria met (Noah)
- [ ] Final smoke test before demo (All)

---

## MVP Sign-Off Acceptance Criteria

By end of Week 8, team must demonstrate:

### FR-1: Triple-Model Support
- [ ] Can select IRB 4600, IRB 2600, or IRB 6700 from dropdown
- [ ] Each robot model loads correctly (visual + kinematics)
- [ ] Trajectory simulation works for all 3 robots

### FR-2: Environment Upload
- [ ] Can upload custom obstacle geometry (STL files)
- [ ] Obstacles appear in 3D scene
- [ ] Multiple obstacles supported (tested with 5+ obstacles)

### FR-3: Active Transform Gizmo
- [ ] 3D gizmo allows manual positioning of obstacles (X, Y, Z)
- [ ] Gizmo allows rotation of obstacles (R)
- [ ] Position changes persist (saved to backend)

### FR-4: RAPID Interpretation
- [ ] Parser handles MoveL, MoveJ, MoveC commands
- [ ] Parsed AST structure is correct
- [ ] Error messages for invalid syntax are helpful

### FR-5: Batch Processing
- [ ] Trajectory calculated server-side before playback
- [ ] Simulation completes in <5 seconds for 100-waypoint program
- [ ] Trajectory JSON returned to frontend

### FR-6: Playback Controls
- [ ] Timeline scrubber allows seeking to any waypoint
- [ ] Play, pause, stop buttons work correctly
- [ ] Speed controls adjust playback (0.25x, 0.5x, 1x, 2x)
- [ ] Step-through controls (next, previous waypoint)

### FR-7: Basic Collision
- [ ] Visual warning when collision detected (robot turns red)
- [ ] Collision warning appears in StatusPanel
- [ ] Collision detection works for robot vs obstacles (not self-collision)

### Additional MVP Criteria
- [ ] UI intuitive for non-programmers (tested with users)
- [ ] No crashes during 30+ minute sessions
- [ ] Error states provide helpful guidance
- [ ] Loading indicators show progress for all async operations
- [ ] Works on Chrome, Firefox, Safari/Edge (latest versions)
- [ ] Responsive layout works on desktop and tablet

**Sign-Off Status:** 🟢 MVP APPROVED if all criteria met, 🟡 MVP APPROVED WITH NOTES if minor issues, 🔴 MVP NOT READY if critical issues

---

## Definition of Done

A task is **DONE** when:

✅ Code written and committed to repo
✅ Code reviewed by at least one other team member (informal or PR)
✅ Tests written and passing (if applicable)
✅ No linting errors (ruff for backend, eslint for frontend)
✅ Documented in code comments (complex logic explained)
✅ Verified in browser/API (manual smoke test)
✅ **Tested in UAT (Week 8 only)**
✅ **Included in demo script (Week 8 only)**

---

## Team Assignments

| Person | Focus Area | Key Deliverable |
|--------|-----------|-----------------|
| **Dylane** | Timeline scrubber + performance | Scrubber polished, animations smooth |
| **Umaya** | Error states + responsive layout | All errors covered, works on all screens |
| **Jason** | IK caching + edge cases | Performance improved, errors helpful |
| **Noah (Backend)** | Validation + bug fixes | Security hardened, timeouts prevent hangs |
| **Noah (QA/PM)** | UAT + MVP sign-off | UAT complete, MVP approved |

---

## Communication

**Slack Channels:**
- `#abb-sim-dev` - General development discussion
- `#abb-sim-frontend` - Frontend-specific questions (Dylane, Umaya)
- `#abb-sim-backend` - Backend-specific questions (Jason, Noah)
- `#abb-sim-qa` - Testing and QA updates (Noah)

**Daily Standup:** 9:00 AM (15 minutes, async updates on weekends)

**Sprint Review:** End of Week 8 (1-hour MVP sign-off demo with stakeholders)

---

## Success Metrics

By end of Week 8, we should achieve:

- [ ] **Frontend:** Timeline scrubber, speed controls, step-through working
- [ ] **Frontend:** Error states and responsive layout complete
- [ ] **Backend:** Performance optimized, edge cases handled
- [ ] **Backend:** Security reviewed, all robots tested
- [ ] **QA:** Regression tests pass, UAT complete
- [ ] **QA:** **MVP SIGN-OFF APPROVED**

**Sprint Goal Achievement:** 🟢 Green if MVP APPROVED, 🟡 Yellow if APPROVED WITH NOTES, 🔴 Red if NOT APPROVED

---

## Demo Script for MVP Sign-Off

### Demo Flow (15-20 minutes)

**1. Introduction (2 min)**
- Introduce team and project goals
- Explain MVP scope (Student View for learning RAPID)

**2. Upload and Visualization (3 min)**
- Select IRB 4600 from robot dropdown
- Upload obstacle STL (show gizmo positioning)
- Demonstrate 3D scene navigation (orbit, zoom)

**3. RAPID Programming (4 min)**
- Upload sample RAPID program (`demo_program.mod`)
- Show parsed code in editor panel
- Explain move commands (MoveL, MoveJ, MoveC)

**4. Simulation and Playback (5 min)**
- Click Simulate button
- Show trajectory animation (play, pause, stop)
- Demonstrate timeline scrubber (seek to waypoint)
- Show speed controls (0.5x, 1x, 2x)
- Demonstrate step-through (next, previous)

**5. Collision Detection (3 min)**
- Position obstacle in robot path (use gizmo)
- Re-run simulation
- Show collision warning (red highlight on robot)
- Show collision details in StatusPanel

**6. Multi-Robot Support (2 min)**
- Switch to IRB 2600 from dropdown
- Re-run simulation on different robot model
- Show that kinematics work correctly

**7. Q&A and Next Steps (5 min)**
- Answer stakeholder questions
- Discuss Weeks 9-11 stretch goals
- Request feedback and approval

**Backup Plan:** If demo encounters issues, have pre-recorded video ready

---

## Next Sprint Planning

**Week 9-10 Preview (Stretch Goals):**
- Dylane: Multi-robot selector UI improvements
- Umaya: Control flow visualization, variable inspector
- Jason: Extend grammar for IF/ELSE/FOR/WHILE
- Noah (Backend): Control flow execution engine
- Noah (QA): Control flow test suite, multi-robot testing

**Week 9-10 Goal:** RAPID control flow (IF/ELSE/FOR/WHILE), all 3 robots fully supported

**Week 11 Preview (Finalization):**
- All: Documentation, final testing, deployment, demo video
- Noah: User guide, developer guide, final presentation

---

**Document Owner:** Noah (PM/QA Lead)
**Created:** 2026-02-05
**Last Updated:** 2026-02-05
**Next Update:** End of Week 8 (MVP Sign-Off Retrospective)

---

## Sprint Retrospective Template (Week 8)

**What Went Well:**
- [Team fills in after sprint]

**What Could Be Improved:**
- [Team fills in after sprint]

**Action Items for Weeks 9-11:**
- [Team fills in after sprint]

**MVP Approval Status:**
- [ ] APPROVED ✅
- [ ] APPROVED WITH NOTES ⚠️
- [ ] NOT APPROVED ❌

**Stakeholder Feedback:**
- [Record feedback from demo]
