"""
ArmStudio — TCP Tracing Demo (SAIT ARIS)
=========================================
Playwright headed demo that loads sait_aris.mod on the dev server,
executes the simulation, and plays back the TCP trail drawing "SAIT ARIS".

Targets the local dev server (no Docker required).

Usage:
    backend/venv/bin/python e2e/tcp_trace_demo.py
"""

from playwright.sync_api import sync_playwright
import os
import time

FRONTEND_URL = "http://localhost:3000"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SAIT_ARIS_MOD = os.path.join(
    PROJECT_ROOT, "backend", "tests", "fixtures", "rapid", "sait_aris.mod"
)

# ---------------------------------------------------------------------------
# Subtitle overlay (same pattern as demo.py)
# ---------------------------------------------------------------------------

SUBTITLE_INJECT_JS = """
(text) => {
    let el = document.getElementById('demo-subtitle');
    if (!el) {
        el = document.createElement('div');
        el.id = 'demo-subtitle';
        Object.assign(el.style, {
            position: 'fixed',
            bottom: '24px',
            left: '50%',
            transform: 'translateX(-50%)',
            padding: '12px 32px',
            background: 'rgba(0,0,0,0.82)',
            color: 'white',
            borderRadius: '8px',
            fontSize: '18px',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            zIndex: '99999',
            transition: 'opacity 0.3s',
            textAlign: 'center',
            maxWidth: '80%',
            letterSpacing: '0.01em',
            lineHeight: '1.5',
            pointerEvents: 'none',
        });
        document.body.appendChild(el);
    }
    el.style.opacity = '1';
    el.textContent = text;
}
"""

CLEAR_SUBTITLE_JS = """
() => {
    const el = document.getElementById('demo-subtitle');
    if (el) el.style.opacity = '0';
}
"""


def subtitle(page, text):
    page.evaluate(SUBTITLE_INJECT_JS, text)


def clear_subtitle(page):
    page.evaluate(CLEAR_SUBTITLE_JS)


def pause(seconds=3.0):
    time.sleep(seconds)


# ---------------------------------------------------------------------------
# Demo scenes
# ---------------------------------------------------------------------------


def scene_intro(page):
    page.goto(FRONTEND_URL)
    page.wait_for_load_state("networkidle")
    pause(2)

    subtitle(page, "ArmStudio — TCP Tracing Demo")
    pause(3)

    subtitle(page, "The robot draws 'SAIT ARIS' — tracing letters with its tool center point")
    pause(3.5)

    page.locator("#robot-select").select_option(label="ABB IRB 4600")
    pause(2.5)

    subtitle(page, "ABB IRB 4600 — 6-axis industrial robot, 2050mm reach")
    pause(3)


def scene_load_program(page):
    subtitle(page, "Loading sait_aris.mod — a RAPID program that draws letters using MoveL commands")
    pause(2)

    page.get_by_role("button", name="RAPID Code").click()
    pause(1)

    file_input = page.locator('input[type="file"]')
    file_input.set_input_files(SAIT_ARIS_MOD)
    pause(2)

    subtitle(page, "RAPID parsed: 51 MoveL commands, tMarker tool with 150mm TCP offset")
    pause(3.5)

    subtitle(page, "Z=800mm = drawing surface  |  Z=900mm = pen lifted for transit moves")
    pause(3.5)


def scene_execute(page):
    subtitle(page, "Running simulation — PyBullet IK solves joint angles for every waypoint")
    pause(1)

    page.locator("button", has_text="Execute RAPID").click()

    try:
        page.wait_for_selector("text=Simulation complete", timeout=30000)
    except Exception:
        page.wait_for_timeout(15000)

    pause(1)
    subtitle(page, "Trajectory ready — each waypoint carries TCP position and joint angles")
    pause(3)


def scene_playback(page):
    subtitle(page, "Playing at 0.5x — watch the cyan trail build as the robot draws")
    pause(1.5)

    # Set 0.5x speed before playing
    page.locator("select").last.select_option("0.5")
    pause(0.5)

    play_btn = page.locator("button.rounded-full").first
    play_btn.click()
    pause(2)

    subtitle(page, "Pen-down strokes draw cyan lines  |  Pen-up transits are invisible")
    pause(6)

    subtitle(page, "S — A — I — T   ... drawing the word 'SAIT'")
    pause(8)

    subtitle(page, "Word gap — robot lifts the pen and moves to the next word")
    pause(5)

    subtitle(page, "A — R — I — S   ... completing 'ARIS'")
    pause(8)

    # Wait for playback to finish or stop it
    try:
        page.wait_for_selector("text=0:00", timeout=60000)
    except Exception:
        play_btn.click()  # stop if still playing
    pause(2)

    subtitle(page, "Scrubbing back — the trail rebuilds from the beginning")
    pause(1)
    scrubber = page.locator('input[type="range"]')
    if scrubber.count() > 0:
        scrubber.fill("5")
        pause(2)
        scrubber.fill("0")
        pause(1.5)


def scene_outro(page):
    subtitle(page, "RAPID code → AST → PyBullet IK → trajectory → 3D visualization")
    pause(4)

    subtitle(page, "SAIT Research Applications × ARIS Robotics")
    pause(4)

    clear_subtitle(page)
    pause(2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=80)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1,
        )
        page = context.new_page()

        scene_intro(page)
        print("Scene 1: Intro - done")

        scene_load_program(page)
        print("Scene 2: Load program - done")

        scene_execute(page)
        print("Scene 3: Execute - done")

        scene_playback(page)
        print("Scene 4: Playback - done")

        scene_outro(page)
        print("Scene 5: Outro - done")

        print("\nDemo complete! Browser will stay open.")
        input("Press Enter to close...")
        browser.close()


if __name__ == "__main__":
    run()
