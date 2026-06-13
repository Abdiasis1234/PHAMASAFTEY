import Link from "next/link";
import { AgentArchitecture, PageHeader, SiteNav } from "@/components/pdf-analyst/Brand";

export default function Home() {
  return (
    <>
      <SiteNav active="home" />
      <PageHeader
        eyebrow="PhamaSafety · London A2A Hackathon"
        meta={
          <span className="pill">
            <span className="dot" /> multi-agent demo
          </span>
        }
        title={
          <>
            From unstructured safety reports to{" "}
            <br className="hidden md:inline" />
            <span
              className="bg-clip-text text-transparent"
              style={{ backgroundImage: "var(--brand-gradient)" }}
            >
              structured cases & escalation.
            </span>
          </>
        }
        subtitle="Three cooperating agents transform patient, doctor, and pharmacist messages into structured pharmacovigilance cases — with generative UI for intake dashboards and follow-up analysis."
      />

      <main className="flex-1 max-w-[1320px] mx-auto px-6 py-12 w-full">
        <section>
          <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--muted-2)]">
            Agent architecture
          </span>
          <AgentArchitecture />
        </section>

        <div className="grid md:grid-cols-2 gap-5 mt-12">
          <ModeCard
            href="/fixed"
            badge="01 · CASE INTAKE"
            title="Structured safety dashboard"
            blurb="Describe an adverse reaction, missing patient details, or complaint. The intake agent extracts fields and paints a fixed-schema case dashboard."
            bullets={[
              "Extracts case type, medicine, symptoms, severity, urgency",
              "Highlights missing fields before escalation",
              "Works offline with OFFLINE=1 — no API key required for demo",
            ]}
            cta="Open case intake"
          />
          <ModeCard
            href="/dynamic"
            badge="02 · FOLLOW-UP Q&A"
            title="Dynamic analysis surfaces"
            blurb="Ask follow-up questions — escalation criteria, symptom timelines, regulatory paths — and the agent invents the UI from the catalog."
            bullets={[
              "Charts for symptom breakdown and timelines",
              "Callouts for regulatory escalation guidance",
              "Same 21-component A2UI catalog",
            ]}
            cta="Open follow-up Q&A"
          />
        </div>

        <section className="mt-14 surface p-6">
          <h2 className="text-[18px] font-semibold tracking-tight">
            Running the A2A agents locally
          </h2>
          <p className="mt-2 text-[14px] text-[var(--muted)] max-w-3xl">
            The UI runs on{" "}
            <code className="mono text-[12px]">pnpm dev</code> (Next.js + LangGraph
            on :8123). Start the Personal Agent (:9001) and CS Agent (:9002) with{" "}
            <code className="mono text-[12px]">docker compose up</code> or the scripts
            in <code className="mono text-[12px]">scripts/run-a2a-agents.ps1</code>.
            Add your <code className="mono text-[12px]">GEMINI_API_KEY</code> when
            ready for live LLM calls.
          </p>
        </section>

        <section className="mt-14 grid md:grid-cols-3 gap-3">
          <Spec k="Frontend" v="Next.js 16 · CopilotKit · A2UI v0.9 renderer" />
          <Spec k="A2A agents" v="Google ADK · Personal :9001 · CS :9002" />
          <Spec k="Research" v="Redis KB · BM25 + vector · internal to CS" />
        </section>
      </main>

      <footer className="border-t border-[var(--line)] py-6 mt-10">
        <div className="max-w-[1320px] mx-auto px-6 text-xs text-[var(--muted)] flex items-center justify-between">
          <span>PhamaSafety · pharmaceutical safety reporting demo</span>
          <span className="mono">Track 1 + 2</span>
        </div>
      </footer>
    </>
  );
}

function ModeCard({
  href,
  badge,
  title,
  blurb,
  bullets,
  cta,
}: {
  href: string;
  badge: string;
  title: string;
  blurb: string;
  bullets: string[];
  cta: string;
}) {
  return (
    <Link
      href={href}
      className="group surface p-7 hover:border-[var(--lilac)] transition relative overflow-hidden"
    >
      <div className="absolute -top-20 -right-20 w-[260px] h-[260px] rounded-full brand-gradient-soft opacity-0 group-hover:opacity-100 transition-opacity" />
      <div className="relative">
        <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--muted-2)]">
          {badge}
        </span>
        <h3 className="text-[24px] font-semibold tracking-tight mt-2">{title}</h3>
        <p className="mt-3 text-[var(--muted)] leading-relaxed text-[15px]">{blurb}</p>
        <ul className="mt-5 space-y-2">
          {bullets.map((b) => (
            <li
              key={b}
              className="flex items-start gap-2.5 text-[13.5px] text-[var(--ink-2)]"
            >
              <span className="mt-1.5 w-1 h-1 rounded-full bg-[var(--lilac)] shrink-0" />
              {b}
            </li>
          ))}
        </ul>
        <span className="inline-flex items-center gap-1 mt-6 text-[13px] font-medium text-[var(--lilac)]">
          {cta} →
        </span>
      </div>
    </Link>
  );
}

function Spec({ k, v }: { k: string; v: string }) {
  return (
    <div className="surface-soft px-4 py-3">
      <span className="mono text-[10px] uppercase tracking-[0.12em] text-[var(--muted-2)]">
        {k}
      </span>
      <p className="mt-1 text-[13px] text-[var(--muted)]">{v}</p>
    </div>
  );
}
