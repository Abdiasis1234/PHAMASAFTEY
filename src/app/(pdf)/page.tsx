import Link from "next/link";
import { PageHeader, SiteNav } from "@/components/pdf-analyst/Brand";

export default function Home() {
  return (
    <>
      <SiteNav active="home" />
      <PageHeader
        eyebrow="A2A Hackathon Track · Rho-Bank"
        meta={
          <span className="pill">
            <span className="dot" /> Track 1
          </span>
        }
        title={
          <>
            Two agents, one harness —{" "}
            <br className="hidden md:inline" />
            <span
              className="bg-clip-text text-transparent"
              style={{ backgroundImage: "var(--brand-gradient)" }}
            >
              personal + customer service over A2A.
            </span>
          </>
        }
        subtitle="Personal agent (:9001) acts for the user and talks to customer service (:9002) over the Agent-to-Agent protocol. CS searches a 698-document Redis knowledge base. Scored by the a2a-hack harness."
      />

      <main className="flex-1 max-w-[1320px] mx-auto px-6 py-12 w-full">
        <section className="surface p-6 mb-10">
          <h2 className="text-[18px] font-semibold tracking-tight">
            Primary dev loop (A2A track)
          </h2>
          <ol className="mt-4 space-y-2 text-[14px] text-[var(--muted)] list-decimal list-inside">
            <li>
              <code className="mono text-[12px]">copy .env.example .env</code> — set{" "}
              <code className="mono text-[12px]">GOOGLE_API_KEY</code>
            </li>
            <li>
              <code className="mono text-[12px]">docker compose up --build</code>
            </li>
            <li>
              Clone{" "}
              <a
                href="https://github.com/a2anet/a2a-hackathon"
                className="text-[var(--ink)] underline"
              >
                a2a-hackathon
              </a>{" "}
              and run{" "}
              <code className="mono text-[12px]">a2a-hack smoke</code>
            </li>
          </ol>
          <p className="mt-4 mono text-[12px] text-[var(--muted)]">
            Full guide: <strong>A2A.md</strong> in the repo root
          </p>
        </section>

        <div className="grid md:grid-cols-2 gap-5">
          <AgentCard
            name="Personal Agent"
            port=":9001"
            blurb="User's Rho-Bank assistant. Fetches user env tools, contacts CS via A2A with shared contextId."
          />
          <AgentCard
            name="CS Agent"
            port=":9002"
            blurb="Bank customer service. Policy + bank env tools + Redis KB (BM25 + vector search)."
          />
        </div>

        <section className="mt-14">
          <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--muted-2)]">
            Optional — Generative UI (Track 2)
          </span>
          <div className="grid md:grid-cols-2 gap-5 mt-4">
            <Link href="/fixed" className="surface p-5 hover:border-[var(--lilac)] transition">
              <span className="mono text-[11px] text-[var(--muted-2)]">/fixed</span>
              <p className="mt-1 text-[14px] text-[var(--muted)]">
                LangGraph + A2UI intake demo on :8123 (secondary)
              </p>
            </Link>
            <Link href="/dynamic" className="surface p-5 hover:border-[var(--lilac)] transition">
              <span className="mono text-[11px] text-[var(--muted-2)]">/dynamic</span>
              <p className="mt-1 text-[14px] text-[var(--muted)]">
                Dynamic A2UI follow-up surfaces (secondary)
              </p>
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-[var(--line)] py-6 mt-10">
        <div className="max-w-[1320px] mx-auto px-6 text-xs text-[var(--muted)] flex items-center justify-between">
          <span>
            Template:{" "}
            <a href="https://github.com/a2anet/a2a-hackathon-template" className="underline">
              a2a-hackathon-template
            </a>
          </span>
          <span className="mono">A2A Track 1</span>
        </div>
      </footer>
    </>
  );
}

function AgentCard({
  name,
  port,
  blurb,
}: {
  name: string;
  port: string;
  blurb: string;
}) {
  return (
    <div className="surface p-6">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-[var(--ink)]">{name}</h3>
        <span className="mono text-[11px] text-[var(--muted)]">{port}</span>
      </div>
      <p className="mt-2 text-[14px] text-[var(--muted)] leading-relaxed">{blurb}</p>
    </div>
  );
}
