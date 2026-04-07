# ArmStudio — Frontend

Next.js 16 + React + Babylon.js frontend for ABB robot trajectory visualization.

## Setup

```bash
pnpm install
```

## Development

```bash
pnpm dev
# Runs at http://localhost:3000
```

API requests to `/api/*` are proxied to the backend at `http://localhost:8000` via Next.js rewrites (see `next.config.ts`).

## Production Build

```bash
pnpm build
pnpm start
```

## Stack

- **Next.js 16** — App Router, server/client components
- **React 19** — Functional components with hooks
- **Babylon.js 8** — WebGL 3D rendering (robot visualization, starfield)
- **Tailwind CSS 4** — Utility-first styling (CSS-based config)
- **openapi-fetch** — Type-safe API client generated from OpenAPI contract
- **Framer Motion** — UI animations
- **Lucide React** — Icons

## Project Structure

```
src/
  app/              — Next.js App Router (layout, page, globals.css)
  components/
    babylon/        — Viewport3D, createRobotScene (3D visualization)
    Header.tsx      — Robot selector, upload controls
    MainLayout.tsx  — 70/30 viewport/panel split
    SidePanel.tsx   — Tabbed panel (RAPID editor, joint jog)
    PlaybackControls.tsx — Play/pause/timeline controls
    BottomPanel.tsx — Status and log display
  types.ts          — Centralized type definitions
  assets/           — Static assets (SVGs, etc.)
```
