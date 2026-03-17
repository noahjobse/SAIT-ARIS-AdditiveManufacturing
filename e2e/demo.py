"""
ArmStudio — Cinematic Playwright Demo
======================================
Narrated walkthrough of the ABB Robot Simulation Platform.
Follows the same subtitle-overlay pattern used by Elliot and ManyBuildings demos.

Spins up docker-compose.demo.yml, runs the demo, tears down on exit.

Usage:
    cd /home/noah/projects/SAIT-ARIS-AdditiveManufacturing
    backend/venv/bin/python e2e/demo.py
"""

from playwright.sync_api import sync_playwright
import os
import subprocess
import time
import urllib.request

# Ports — offset from defaults to avoid conflicts with ManyBuildings (5173/8000)
FRONTEND_URL = "http://localhost:5174"
BACKEND_URL = "http://localhost:8001"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
COMPOSE_FILE = os.path.join(PROJECT_ROOT, "docker-compose.demo.yml")
SPINNY_DEMO_PATH = os.path.join(
    PROJECT_ROOT, "backend", "tests", "fixtures", "rapid", "spinny_demo.mod"
)

# ---------------------------------------------------------------------------
# Helpers (same overlay pattern as Elliot & ManyBuildings)
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

# Animate a joint by writing to the text input via React's internal setter.
ANIMATE_JOINT_JS = """
async ([jointIndex, targetValue, durationMs]) => {
    const inputs = document.querySelectorAll('input[type="text"]');
    const input = inputs[jointIndex];
    if (!input) return;

    const nativeSet = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value'
    ).set;

    const start = parseFloat(input.value) || 0;
    const steps = 30;
    const delay = durationMs / steps;

    for (let i = 1; i <= steps; i++) {
        const v = start + (targetValue - start) * (i / steps);
        nativeSet.call(input, String(Math.round(v)));
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(r => setTimeout(r, delay));
    }
}
"""


def subtitle(page, text):
    page.evaluate(SUBTITLE_INJECT_JS, text)


def clear_subtitle(page):
    page.evaluate(CLEAR_SUBTITLE_JS)


def pause(seconds=3.0):
    time.sleep(seconds)


def animate_joint(page, joint_index, target_value, duration_ms=1500):
    page.evaluate(ANIMATE_JOINT_JS, [joint_index, target_value, duration_ms])


# ---------------------------------------------------------------------------
# Docker lifecycle
# ---------------------------------------------------------------------------


def docker_up():
    """Build and start the demo containers, wait until both are ready."""
    print("Building and starting docker-compose.demo.yml ...")
    subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "up", "-d", "--build"],
        cwd=PROJECT_ROOT,
        check=True,
    )

    print("Waiting for backend ...", end="", flush=True)
    for _ in range(60):
        try:
            r = urllib.request.urlopen(f"{BACKEND_URL}/api/health", timeout=2)
            if r.status == 200:
                print(" ready!")
                break
        except Exception:
            pass
        print(".", end="", flush=True)
        time.sleep(2)
    else:
        print("\nWARNING: backend health check never passed")

    print("Waiting for frontend ...", end="", flush=True)
    for _ in range(30):
        try:
            r = urllib.request.urlopen(FRONTEND_URL, timeout=2)
            if r.status == 200:
                print(" ready!")
                return
        except Exception:
            pass
        print(".", end="", flush=True)
        time.sleep(2)
    print("\nWARNING: frontend never responded")


def docker_down():
    """Stop and remove the demo containers."""
    print("\nTearing down containers ...")
    subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "down"],
        cwd=PROJECT_ROOT,
    )


# ---------------------------------------------------------------------------
# Demo scenes
# ---------------------------------------------------------------------------


def scene_intro(page):
    """Scene 1: Load the platform, select robot, introduce the UI."""
    page.goto(FRONTEND_URL)
    page.wait_for_load_state("networkidle")
    pause(2)

    subtitle(page, "ArmStudio — ABB Robot Simulation Platform")
    pause(3)

    # Select the IRB 4600 robot model
    subtitle(page, "Selecting the ABB IRB 4600 — a 6-axis industrial robot")
    pause(1.5)
    page.locator("#robot-select").select_option(label="ABB IRB 4600")
    pause(3)

    subtitle(page, "Upload RAPID code, simulate trajectories, and visualize robot motion in 3D")
    pause(3.5)


def scene_joint_jog(page):
    """Scene 2: Demonstrate manual joint control with dramatic movements."""
    subtitle(page, "Joint Jog mode — manually control each of the robot's 6 axes")
    pause(3)
    clear_subtitle(page)

    # Ensure Joint Jog tab is active (it's the default, but be explicit)
    page.get_by_role("button", name="Joint Jog").click()
    pause(1)

    # Quick dramatic joint movements
    input_count = page.locator('input[type="text"]').count()
    if input_count >= 6:
        # J1: Base sweep
        subtitle(page, "Base rotation — real-time forward kinematics in the browser")
        animate_joint(page, 0, 70, 800)
        animate_joint(page, 0, -70, 1200)
        animate_joint(page, 0, 0, 600)

        # J2 + J5: Shoulder lift + wrist bend together
        subtitle(page, "Multiple axes moving — shoulder lift and wrist bend")
        animate_joint(page, 1, -60, 800)
        animate_joint(page, 4, 80, 800)
        pause(1)
        animate_joint(page, 1, 0, 600)
        animate_joint(page, 4, 0, 600)
    else:
        subtitle(page, "Joint sliders control each axis in real time")
        pause(3)

    # Reset all joints
    subtitle(page, "Resetting to home position")
    pause(1)
    reset_btn = page.locator("button", has_text="Reset Joints")
    if reset_btn.count() > 0:
        reset_btn.click()
    pause(2)


def scene_rapid_upload(page):
    """Scene 3: Switch to RAPID panel, upload spinny_demo.mod."""
    subtitle(page, "Now let's run a RAPID program — the language ABB robots speak")
    pause(3)

    # Switch to RAPID Code tab
    page.get_by_role("button", name="RAPID Code").click()
    pause(1.5)

    subtitle(page, "Uploading spinny_demo.mod — 8 high-speed joint movements across the workspace")
    pause(2)

    # Upload the actual spinny_demo.mod file
    file_input = page.locator('input[type="file"]')
    file_input.set_input_files(SPINNY_DEMO_PATH)
    pause(2)

    subtitle(page, "RAPID parsed: MoveAbsJ commands define joint-space waypoints at v5000 speed")
    pause(3)

    subtitle(page, "The backend converts RAPID → AST → trajectory via PyBullet inverse kinematics")
    pause(3)


def scene_execute(page):
    """Scene 4: Click Execute and watch the trajectory generate."""
    subtitle(page, "Executing — the parser analyzes the code and the simulator generates waypoints")
    pause(1)

    page.locator("button", has_text="Execute RAPID").click()

    # Wait for simulation to complete — look for success log message
    try:
        page.wait_for_selector("text=Simulation complete", timeout=20000)
    except Exception:
        page.wait_for_timeout(12000)

    pause(1)
    subtitle(page, "Trajectory generated — 1410 waypoints interpolated over 28 seconds of motion")
    pause(3.5)


def scene_playback(page):
    """Scene 5: Play the animation and demonstrate playback controls."""
    subtitle(page, "Playing the trajectory — watch the robot sweep through its workspace")
    pause(2)

    # The play button is the violet circle button (bg-violet-600 rounded-full)
    play_btn = page.locator("button.rounded-full").first
    play_btn.click()
    pause(1)

    subtitle(page, "Base spins, wrist flips — full joint-space choreography at v5000")
    pause(8)

    # Change speed to 2x
    subtitle(page, "Speed control: switching to 2x for a faster preview")
    pause(1)
    page.locator("select").last.select_option("2.0")
    pause(6)

    # Pause playback
    subtitle(page, "Pausing — the scrubber lets you inspect any moment in the trajectory")
    play_btn.click()
    pause(2)

    # Demonstrate scrubbing
    scrubber = page.locator('input[type="range"]')
    if scrubber.count() > 0:
        scrubber.fill("12")
        pause(2)
        subtitle(page, "Scrubbing to t=12s — inspect exact joint configuration at any moment")
        pause(3)
        scrubber.fill("5")
        pause(1.5)
        scrubber.fill("20")
        pause(1.5)
        scrubber.fill("0")
        pause(1)


def scene_outro(page):
    """Scene 6: Closing titles."""
    subtitle(page, "ArmStudio — from RAPID code to 3D simulation in seconds")
    pause(4)

    subtitle(page, "SAIT Research Applications x ARIS Robotics")
    pause(4)

    clear_subtitle(page)
    pause(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def run_demo():
    docker_up()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)
            context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                device_scale_factor=1,
            )
            page = context.new_page()

            scene_intro(page)
            print("Scene 1: Intro - done")

            scene_joint_jog(page)
            print("Scene 2: Joint Jog - done")

            scene_rapid_upload(page)
            print("Scene 3: RAPID Upload - done")

            scene_execute(page)
            print("Scene 4: Execute - done")

            scene_playback(page)
            print("Scene 5: Playback - done")

            scene_outro(page)
            print("Scene 6: Outro - done")

            browser.close()

        print("\nDemo complete!")
    finally:
        docker_down()


if __name__ == "__main__":
    run_demo()
