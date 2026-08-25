"use client";

import React, { useState, useEffect } from "react";
import {
  ShieldCheck,
  Bus,
  Activity,
  Database,
  Cpu,
  Radio,
  Server,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Layers,
  Sparkles,
  ArrowRight,
} from "lucide-react";

interface HealthData {
  status: string;
  project: string;
  version: string;
  environment: string;
  timestamp: string;
  database: {
    status: string;
    latency_ms: number;
    database_name?: string;
    error?: string;
  };
  subsystems: Record<string, string>;
}

export default function Home() {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastChecked, setLastChecked] = useState<string>("");

  const backendUrl =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const fetchHealth = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${backendUrl}/api/v1/health`, {
        cache: "no-store",
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      setHealth(data);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err: any) {
      setError(
        err.message ||
          "Failed to connect to FastAPI backend. Ensure backend is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <main className="min-h-screen px-4 sm:px-6 lg:px-8 py-10 max-w-7xl mx-auto flex flex-col justify-between">
      {/* Header / Navbar */}
      <header className="flex flex-col sm:flex-row items-center justify-between gap-4 pb-8 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-amber-500 via-indigo-500 to-cyan-400 p-0.5 shadow-lg shadow-indigo-500/20">
            <div className="w-full h-full bg-surface rounded-[10px] flex items-center justify-center">
              <Bus className="w-6 h-6 text-amber-400" />
            </div>
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              Guardian Transit <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-indigo-400">AI</span>
            </h1>
            <p className="text-xs text-slate-400 font-mono">
              Smart School Bus Safety, Attendance & Telematics Platform
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <a
            href={`${backendUrl}/docs`}
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-surface hover:bg-slate-800 text-xs font-medium text-slate-200 border border-slate-700 transition"
          >
            <Server className="w-4 h-4 text-indigo-400" />
            FastAPI Swagger
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
          <button
            onClick={fetchHealth}
            disabled={loading}
            className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-xs font-medium text-white shadow-md shadow-indigo-600/30 transition disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            {loading ? "Testing..." : "Ping System"}
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-12 text-center relative">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-950/60 border border-indigo-500/30 text-indigo-300 text-xs mb-6 font-mono">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span>PHASE 1 FOUNDATION OPERATIONAL</span>
        </div>
        <h2 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
          AI-Driven School Transportation <br className="hidden sm:inline" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-cyan-400 to-amber-300">
            Safety & Attendance Engine
          </span>
        </h2>
        <p className="mt-4 text-base text-slate-300 max-w-2xl mx-auto">
          Modular Monolith architecture uniting Computer Vision face verification,
          GPS telemetry, instant parent notifications, and school fleet intelligence.
        </p>
      </section>

      {/* Live System Diagnostics Panel */}
      <section className="glass-panel rounded-2xl p-6 sm:p-8 mb-12 shadow-2xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 border-b border-white/5 gap-4">
          <div>
            <h3 className="text-lg font-semibold text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-cyan-400" />
              Live Infrastructure Connectivity Matrix
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Real-time handshake verification between Next.js frontend, FastAPI backend, and PostgreSQL.
            </p>
          </div>
          {lastChecked && (
            <div className="text-xs text-slate-400 font-mono">
              Last ping: <span className="text-slate-200">{lastChecked}</span>
            </div>
          )}
        </div>

        {/* Status Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          {/* Frontend Node */}
          <div className="glass-card rounded-xl p-5 border border-white/5 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Frontend App</span>
              <span className="flex h-2.5 w-2.5 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
            </div>
            <div className="mt-4">
              <div className="text-xl font-bold text-white">Next.js 14</div>
              <div className="text-xs text-emerald-400 flex items-center gap-1.5 mt-1 font-mono">
                <CheckCircle2 className="w-3.5 h-3.5" />
                App Router Active (:3000)
              </div>
            </div>
          </div>

          {/* Backend API Node */}
          <div className="glass-card rounded-xl p-5 border border-white/5 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">API Gateway</span>
              <span className="flex h-2.5 w-2.5 relative">
                <span
                  className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                    health ? "bg-emerald-400" : "bg-rose-400"
                  }`}
                ></span>
                <span
                  className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
                    health ? "bg-emerald-500" : "bg-rose-500"
                  }`}
                ></span>
              </span>
            </div>
            <div className="mt-4">
              <div className="text-xl font-bold text-white">FastAPI Async</div>
              <div
                className={`text-xs flex items-center gap-1.5 mt-1 font-mono ${
                  health ? "text-emerald-400" : "text-rose-400"
                }`}
              >
                {health ? (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    v{health.version} - Online (:8000)
                  </>
                ) : (
                  <>
                    <AlertTriangle className="w-3.5 h-3.5" />
                    {error ? "Offline / Unreachable" : "Connecting..."}
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Database Node */}
          <div className="glass-card rounded-xl p-5 border border-white/5 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Database Node</span>
              <Database className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="mt-4">
              <div className="text-xl font-bold text-white">PostgreSQL 16</div>
              <div
                className={`text-xs flex items-center gap-1.5 mt-1 font-mono ${
                  health?.database.status === "connected"
                    ? "text-emerald-400"
                    : "text-amber-400"
                }`}
              >
                {health?.database.status === "connected" ? (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Connected ({health.database.latency_ms}ms)
                  </>
                ) : (
                  <>
                    <AlertTriangle className="w-3.5 h-3.5" />
                    {health?.database.error ? "Connection Standby" : "Checking..."}
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Subsystems Architecture Grid */}
        <div className="mt-8 pt-6 border-t border-white/5">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            Subsystem Modular Readiness Status
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              {
                name: "Attendance Engine",
                phase: "Phase 6",
                desc: "Boarding & Offboarding events",
                icon: ShieldCheck,
              },
              {
                name: "Face Biometrics",
                phase: "Phase 7-8",
                desc: "InsightFace 512-dim embeddings",
                icon: Cpu,
              },
              {
                name: "GPS Telematics",
                phase: "Phase 10",
                desc: "Live coordinate stream",
                icon: Radio,
              },
              {
                name: "Live WebSockets",
                phase: "Phase 11",
                desc: "Real-time sync to Parent UI",
                icon: Activity,
              },
            ].map((sub, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-lg bg-surface/50 border border-white/5 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <sub.icon className="w-4 h-4 text-slate-400" />
                    <span className="text-[10px] font-mono text-indigo-300 bg-indigo-950/70 px-2 py-0.5 rounded border border-indigo-800/40">
                      {sub.phase}
                    </span>
                  </div>
                  <div className="font-semibold text-sm text-slate-200 mt-2">
                    {sub.name}
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">{sub.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Next Phase Notice */}
      <section className="glass-card rounded-xl p-5 border border-indigo-500/20 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0">
            <Database className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <div className="text-sm font-semibold text-white">
              Next Step: Phase 2 Database Implementation
            </div>
            <div className="text-xs text-slate-400">
              Defining SQLAlchemy ORM Models (User, Student, Parent, Bus, Route, FaceProfile, Attendance) & Alembic migrations.
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs font-medium text-indigo-400 shrink-0">
          <span>Ready for Phase 2</span>
          <ArrowRight className="w-4 h-4" />
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-12 pt-6 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <div>
          Guardian Transit AI &copy; {new Date().getFullYear()} — Lead Software Architect
        </div>
        <div className="flex items-center gap-4">
          <span className="font-mono text-slate-400">Modular Monolith Architecture</span>
        </div>
      </footer>
    </main>
  );
}
