"use client";

import Image from "next/image";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Terminal,
  Cpu,
  ShieldAlert,
  Layers,
  ArrowRight,
  Github,
  FileCode2,
  Zap,
  Box,
} from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } },
};

const stagger = {
  hidden: {},
  show: { transition: { staggerChildren: 0.12 } },
};

const features = [
  {
    icon: FileCode2,
    title: "RAPID Parser",
    desc: "Upload ABB RAPID .mod files. Full lexer → parser → AST pipeline with control flow: IF/ELSE, FOR, WHILE.",
  },
  {
    icon: Cpu,
    title: "Inverse Kinematics",
    desc: "PyBullet-powered 6-DOF IK solver computes joint configurations for MoveJ and MoveL instructions in real time.",
  },
  {
    icon: ShieldAlert,
    title: "Collision Detection",
    desc: "Mesh-to-mesh collision checks between the robot arm and user-placed obstacles. Visualized in the 3D viewport.",
  },
  {
    icon: Layers,
    title: "FDM Print Simulation",
    desc: "STL → trimesh slice → RAPID AST → trajectory → extrusion visualization with speed/layer heatmaps.",
  },
];

const pipeline = [
  { step: "01", label: "Upload RAPID", sub: "Drop your .mod file" },
  { step: "02", label: "Parse AST", sub: "Lexer → Parser → Nodes" },
  { step: "03", label: "Simulate Trajectory", sub: "IK solver → waypoints" },
  { step: "04", label: "Visualize 3D", sub: "Babylon.js rendering" },
];

export default function MarketingPage() {
  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden" style={{ fontFamily: "var(--font-geist-sans)" }}>

      {/* ── Starfield + grid background ── */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {/* Stars */}
        <div style={{
          position: "absolute", inset: 0,
          backgroundImage: [
            "radial-gradient(1px 1px at 5% 8%, rgba(255,255,255,0.9), transparent)",
            "radial-gradient(1px 1px at 12% 42%, rgba(255,255,255,0.6), transparent)",
            "radial-gradient(1px 1px at 18% 75%, rgba(255,255,255,0.7), transparent)",
            "radial-gradient(1px 1px at 25% 22%, rgba(255,255,255,0.5), transparent)",
            "radial-gradient(1px 1px at 32% 88%, rgba(255,255,255,0.8), transparent)",
            "radial-gradient(1px 1px at 40% 55%, rgba(255,255,255,0.4), transparent)",
            "radial-gradient(1px 1px at 47% 15%, rgba(255,255,255,0.9), transparent)",
            "radial-gradient(1px 1px at 55% 68%, rgba(255,255,255,0.6), transparent)",
            "radial-gradient(1px 1px at 62% 33%, rgba(255,255,255,0.7), transparent)",
            "radial-gradient(1px 1px at 70% 92%, rgba(255,255,255,0.5), transparent)",
            "radial-gradient(1px 1px at 78% 18%, rgba(255,255,255,0.8), transparent)",
            "radial-gradient(1px 1px at 85% 60%, rgba(255,255,255,0.4), transparent)",
            "radial-gradient(1px 1px at 92% 40%, rgba(255,255,255,0.9), transparent)",
            "radial-gradient(1px 1px at 96% 78%, rgba(255,255,255,0.6), transparent)",
            "radial-gradient(1.5px 1.5px at 8% 30%, rgba(255,255,255,0.5), transparent)",
            "radial-gradient(1.5px 1.5px at 35% 65%, rgba(255,255,255,0.6), transparent)",
            "radial-gradient(1.5px 1.5px at 65% 48%, rgba(255,255,255,0.5), transparent)",
            "radial-gradient(1.5px 1.5px at 88% 25%, rgba(255,255,255,0.7), transparent)",
          ].join(","),
        }} />
        {/* Grid overlay */}
        <div style={{
          position: "absolute", inset: 0,
          backgroundImage: "linear-gradient(rgba(249,115,22,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(249,115,22,0.04) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }} />
        {/* Hero glow */}
        <div style={{
          position: "absolute", top: "-100px", left: "50%", transform: "translateX(-50%)",
          width: "600px", height: "400px",
          background: "radial-gradient(ellipse, rgba(249,115,22,0.08) 0%, rgba(147,51,234,0.06) 50%, transparent 70%)",
        }} />
      </div>

      {/* ── Nav ── */}
      <nav className="relative z-10 flex items-center justify-between px-8 py-5 border-b border-white/5">
        <div className="flex items-center gap-3">
          <Image src="/ArmStudio-Logo.png" alt="ArmStudio" width={32} height={32} style={{ height: "auto" }} />
          <span style={{ fontFamily: "var(--font-geist-mono)", fontSize: "16px", fontWeight: 700, letterSpacing: "-0.3px" }}>
            Arm<span style={{ background: "linear-gradient(135deg,#f97316,#9333ea)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>Studio</span>
          </span>
        </div>
        <Link
          href="/app"
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all"
          style={{ background: "linear-gradient(135deg,#f97316,#ea580c)", color: "white", fontFamily: "var(--font-geist-mono)" }}
        >
          Launch App <ArrowRight size={14} />
        </Link>
      </nav>

      {/* ── Hero ── */}
      <section className="relative z-10 flex flex-col items-center pt-[12vh] min-h-[92vh] px-6 text-center gap-8">
        <motion.div variants={stagger} initial="hidden" animate="show" className="flex flex-col items-center gap-6">

          <motion.div variants={fadeUp}>
            <Image src="/ArmStudio-Logo.png" alt="ArmStudio Logo" width={80} height={80} priority style={{ height: "auto" }} />
          </motion.div>

          <motion.div variants={fadeUp}>
            <h1 style={{ fontFamily: "var(--font-geist-mono)", fontSize: "clamp(42px, 8vw, 80px)", fontWeight: 800, letterSpacing: "-2px", lineHeight: 1.05 }}>
              Arm<span style={{ background: "linear-gradient(135deg,#f97316,#9333ea)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>Studio</span>
            </h1>
          </motion.div>

          <motion.p variants={fadeUp} className="text-gray-400 text-sm tracking-[4px] uppercase" style={{ fontFamily: "var(--font-geist-mono)" }}>
            RAPID &nbsp;→&nbsp; Simulate &nbsp;→&nbsp; Validate
          </motion.p>

          <motion.div variants={fadeUp} className="flex items-center gap-6 mt-2">
            {[
              { value: "6-DOF", label: "IK Solver" },
              { value: "3", label: "Robot Models" },
              { value: "FDM", label: "Print Sim" },
            ].map(({ value, label }) => (
              <div key={label} className="text-center">
                <div className="text-xl font-bold" style={{ color: "#f97316", fontFamily: "var(--font-geist-mono)" }}>{value}</div>
                <div className="text-xs text-gray-500 mt-0.5" style={{ fontFamily: "var(--font-geist-mono)" }}>{label}</div>
              </div>
            ))}
          </motion.div>

          <motion.div variants={fadeUp} className="flex items-center gap-4 mt-4">
            <Link
              href="/app"
              className="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold text-sm transition-all hover:opacity-90"
              style={{ background: "linear-gradient(135deg,#f97316,#ea580c)", color: "white", fontFamily: "var(--font-geist-mono)", boxShadow: "0 0 40px rgba(249,115,22,0.25)" }}
            >
              <Zap size={15} />
              $ armstudio --launch
            </Link>
            <a
              href="https://github.com"
              className="flex items-center gap-2 px-5 py-3 rounded-lg text-sm border transition-all hover:border-orange-500/50 hover:text-white text-gray-400"
              style={{ border: "1px solid rgba(255,255,255,0.1)", fontFamily: "var(--font-geist-mono)" }}
            >
              <Github size={15} />
              GitHub
            </a>
          </motion.div>

        </motion.div>
      </section>

      {/* ── App Screenshot ── */}
      <motion.section
        className="relative z-10 px-6 pb-32"
        variants={fadeUp} initial="hidden" animate="show"
      >
        <div className="max-w-5xl mx-auto">
          <div
            className="w-full rounded-xl overflow-hidden"
            style={{ border: "1px solid rgba(255,255,255,0.08)", boxShadow: "0 0 80px rgba(249,115,22,0.08), 0 0 40px rgba(147,51,234,0.06)" }}
          >
            {/* Fake browser chrome */}
            <div className="flex items-center gap-2 px-4 py-3 border-b" style={{ background: "rgba(255,255,255,0.03)", borderColor: "rgba(255,255,255,0.06)" }}>
              <div className="w-3 h-3 rounded-full bg-red-500/50" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
              <div className="w-3 h-3 rounded-full bg-green-500/50" />
              <div className="flex-1 mx-4 px-3 py-1 rounded text-xs text-gray-600 text-center" style={{ background: "rgba(255,255,255,0.04)", fontFamily: "var(--font-geist-mono)" }}>
                app.armstudio.com
              </div>
            </div>
            {/* Screenshot placeholder — swap with real screenshot */}
            <div
              className="w-full flex items-center justify-center"
              style={{
                aspectRatio: "16/9",
                background: "linear-gradient(135deg, rgba(249,115,22,0.04) 0%, rgba(0,0,0,0.8) 50%, rgba(147,51,234,0.04) 100%)",
                backgroundImage: "linear-gradient(rgba(249,115,22,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(249,115,22,0.03) 1px, transparent 1px)",
                backgroundSize: "40px 40px",
              }}
            >
              <div className="text-center" style={{ fontFamily: "var(--font-geist-mono)" }}>
                <div className="text-gray-600 text-sm mb-2">[ App Screenshot ]</div>
                <div className="text-gray-700 text-xs">Replace with real screenshot</div>
              </div>
            </div>
          </div>
          <p className="text-center text-gray-600 text-xs mt-4" style={{ fontFamily: "var(--font-geist-mono)" }}>
            Real-time 3D robot simulation in the browser
          </p>
        </div>
      </motion.section>

      {/* ── Features ── */}
      <motion.section
        className="relative z-10 px-6 pb-32"
        variants={stagger} initial="hidden" animate="show"
      >
        <div className="max-w-5xl mx-auto">
          <motion.div variants={fadeUp} className="text-center mb-16">
            <div className="text-xs text-orange-500 tracking-[4px] uppercase mb-3" style={{ fontFamily: "var(--font-geist-mono)" }}>Capabilities</div>
            <h2 className="text-3xl font-bold text-white" style={{ fontFamily: "var(--font-geist-mono)" }}>Built for engineers</h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {features.map(({ icon: Icon, title, desc }) => (
              <motion.div
                key={title}
                variants={fadeUp}
                className="p-6 rounded-xl transition-all hover:border-orange-500/20"
                style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)" }}
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className="p-2 rounded-lg" style={{ background: "rgba(249,115,22,0.1)" }}>
                    <Icon size={18} style={{ color: "#f97316" }} />
                  </div>
                  <h3 className="font-semibold text-white text-sm" style={{ fontFamily: "var(--font-geist-mono)" }}>{title}</h3>
                </div>
                <p className="text-gray-500 text-sm leading-relaxed">{desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* ── How it works ── */}
      <motion.section
        className="relative z-10 px-6 pb-32"
        variants={stagger} initial="hidden" animate="show"
      >
        <div className="max-w-4xl mx-auto">
          <motion.div variants={fadeUp} className="text-center mb-16">
            <div className="text-xs text-orange-500 tracking-[4px] uppercase mb-3" style={{ fontFamily: "var(--font-geist-mono)" }}>Pipeline</div>
            <h2 className="text-3xl font-bold text-white" style={{ fontFamily: "var(--font-geist-mono)" }}>How it works</h2>
          </motion.div>

          <div className="flex flex-col md:flex-row items-start md:items-center gap-4 md:gap-0">
            {pipeline.map(({ step, label, sub }, i) => (
              <div key={step} className="flex md:flex-col items-center md:flex-1 gap-4 md:gap-0">
                <motion.div variants={fadeUp} className="flex md:flex-col items-center md:items-center gap-4 md:gap-3 w-full md:text-center">
                  {/* Step circle */}
                  <div
                    className="flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm"
                    style={{
                      background: "linear-gradient(135deg,rgba(249,115,22,0.15),rgba(147,51,234,0.15))",
                      border: "1px solid rgba(249,115,22,0.3)",
                      color: "#f97316",
                      fontFamily: "var(--font-geist-mono)",
                    }}
                  >
                    {step}
                  </div>
                  <div>
                    <div className="text-white text-sm font-semibold" style={{ fontFamily: "var(--font-geist-mono)" }}>{label}</div>
                    <div className="text-gray-600 text-xs mt-0.5" style={{ fontFamily: "var(--font-geist-mono)" }}>{sub}</div>
                  </div>
                </motion.div>
                {/* Connector */}
                {i < pipeline.length - 1 && (
                  <div
                    className="hidden md:block flex-1 h-px mx-4"
                    style={{ background: "linear-gradient(90deg, rgba(249,115,22,0.3), rgba(147,51,234,0.3))", borderTop: "1px dashed rgba(249,115,22,0.2)" }}
                  />
                )}
              </div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* ── Team / SAIT × ARIS ── */}
      <motion.section
        className="relative z-10 px-6 pb-32"
        variants={fadeUp} initial="hidden" animate="show"
      >
        <div
          className="max-w-3xl mx-auto rounded-2xl px-10 py-14 text-center"
          style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)" }}
        >
          <div className="text-xs text-orange-500 tracking-[4px] uppercase mb-4" style={{ fontFamily: "var(--font-geist-mono)" }}>Partnership</div>
          <h2 className="text-2xl font-bold text-white mb-4" style={{ fontFamily: "var(--font-geist-mono)" }}>SAIT × ARIS Robotics</h2>
          <p className="text-gray-500 text-sm leading-relaxed max-w-xl mx-auto">
            ArmStudio is a SAIT Research Applications and ARIS Robotics collaboration. Built by students, grounded in research — making industrial robot simulation accessible without expensive proprietary tools.
          </p>
          <div className="flex items-center justify-center gap-8 mt-10">
            {["SAIT", "ARIS Robotics"].map((org) => (
              <div
                key={org}
                className="px-8 py-4 rounded-xl text-gray-600 text-sm font-semibold flex items-center justify-center"
                style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", fontFamily: "var(--font-geist-mono)", minWidth: "120px" }}
              >
                {org}
              </div>
            ))}
          </div>
        </div>
      </motion.section>

      {/* ── Footer ── */}
      <footer className="relative z-10 border-t px-8 py-8" style={{ borderColor: "rgba(255,255,255,0.06)" }}>
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Image src="/ArmStudio-Logo.png" alt="ArmStudio" width={20} height={20} />
            <span className="text-gray-600 text-xs" style={{ fontFamily: "var(--font-geist-mono)" }}>
              © 2026 ArmStudio — SAIT × ARIS Robotics
            </span>
          </div>
          <div className="flex items-center gap-6">
            <a href="https://github.com" className="text-gray-600 hover:text-gray-400 text-xs transition-colors flex items-center gap-1.5" style={{ fontFamily: "var(--font-geist-mono)" }}>
              <Github size={12} /> GitHub
            </a>
            <Link href="/app" className="text-gray-600 hover:text-orange-500 text-xs transition-colors" style={{ fontFamily: "var(--font-geist-mono)" }}>
              Launch App →
            </Link>
          </div>
        </div>
      </footer>

    </div>
  );
}
