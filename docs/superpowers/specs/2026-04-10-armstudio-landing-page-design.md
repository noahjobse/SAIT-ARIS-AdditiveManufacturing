# ArmStudio Marketing Landing Page — Design Spec

**Date:** 2026-04-10
**Purpose:** CapCon-ready marketing page with screenshots for poster. Also serves as the public-facing site for ArmStudio.

## Style Direction

Technical/Engineering aesthetic:
- Black starfield background with subtle orange grid overlay
- Hexagonal logo containing robotic arm wireframe (orange→purple gradient)
- Monospace typography for brand wordmark, sans-serif for body
- Stats-forward, engineering-audience tone
- Orange (`#f97316`) primary, purple (`#9333ea`) secondary — matches existing app palette

## Logo

Inline SVG component. Hexagonal border with stylized 3-joint robotic arm inside. Orange→purple gradient on strokes and joints. Reusable as:
- Hero logo (56-64px)
- Favicon (32px, simplified)
- Navbar brand mark (24px)

## Page Structure

### Route

New page at `frontend/src/app/marketing/page.tsx`. The existing `page.tsx` (simulator app) stays at `/`. The marketing page is accessed at `/marketing` for now — can be swapped to root later when auth/routing is set up.

### Section 1: Hero

- Full viewport height, starfield + grid background
- Centered layout:
  - Hex logo SVG (64px)
  - "ArmStudio" wordmark in monospace, "Studio" portion uses gradient
  - Subtitle: `RAPID → Simulate → Validate` in uppercase, letter-spaced, gray
  - Three stat badges in a row: `6-DOF` IK Solver | `3` Robot Models | `FDM` Print Sim
  - CTA button: monospace style `$ armstudio --launch` linking to `/`
- Framer Motion: fade-in + slight upward drift on load

### Section 2: App Screenshot

- Full-width container with rounded border (`white/10`), slight glow
- Placeholder gradient box (960×540 aspect) with "App Screenshot" text
- Caption below: "Real-time 3D robot simulation in the browser"
- Swap placeholder with actual screenshot when available
- Framer Motion: scroll-triggered fade-in

### Section 3: Features Grid

Four cards in a 2×2 grid (stacks to 1-col on mobile):

1. **RAPID Parser** — Upload ABB RAPID code, parsed into AST with full control flow support. Icon: code/terminal.
2. **Inverse Kinematics** — PyBullet-powered 6-DOF IK solver computes joint configurations in real time. Icon: cpu/settings.
3. **Collision Detection** — Mesh-to-mesh collision checks between robot and obstacles. Icon: shield/alert-triangle.
4. **FDM 3D Printing** — STL→slice→simulate pipeline with extrusion visualization and heatmaps. Icon: layers/printer.

Card style: dark card (`gray-900/50`) with `white/10` border, orange accent icon, monospace heading, gray body text.
Framer Motion: staggered fade-in on scroll.

### Section 4: How It Works

Horizontal 4-step pipeline with connecting lines:

1. **Upload RAPID** — Drop your `.mod` file
2. **Parse AST** — Lexer → Parser → AST nodes
3. **Simulate Trajectory** — IK solver generates waypoints
4. **Visualize 3D** — Watch the robot move in Babylon.js

Style: numbered circles with orange gradient, monospace labels, dashed connecting lines.
Framer Motion: sequential reveal left-to-right on scroll.

### Section 5: Team — SAIT × ARIS

- Brief paragraph: "A SAIT Research Applications × ARIS Robotics partnership. Built by students, powered by research."
- Placeholder spots for SAIT and ARIS logos (gray boxes if logos not available)
- Dark background section with subtle border-top

### Section 6: Footer

- "© 2026 ArmStudio — SAIT × ARIS Robotics"
- Links: GitHub (if public), Documentation (placeholder)
- Minimal, single row

## Technical Approach

- Single file: `frontend/src/app/marketing/page.tsx` (client component for Framer Motion)
- Logo extracted to `frontend/src/components/ArmStudioLogo.tsx` for reuse
- All styling via Tailwind classes — no additional CSS files
- Starfield effect: CSS radial-gradient (multiple small white dots) — same approach as in brainstorm mockups, lightweight, no canvas/JS needed
- Grid overlay: CSS linear-gradient with low-opacity orange lines
- Scroll animations: Framer Motion `motion.div` with `whileInView` trigger
- Responsive: mobile-first, grid switches from 2-col to 1-col at `md` breakpoint
- No external dependencies needed — everything is already installed

## Out of Scope

- Authentication / login flows
- Stripe integration
- Dynamic content / CMS
- SEO optimization beyond basic metadata
- Analytics
