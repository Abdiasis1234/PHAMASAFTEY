"use client";

import { CopilotChat } from "@copilotkit/react-core/v2";
import { SiteNav } from "@/components/pdf-analyst/Brand";
import { SurfaceCanvas, CanvasEmptyState } from "@/components/pdf-analyst/SurfaceCanvas";
import { FilteredUserMessage } from "@/components/pdf-analyst/FilteredUserMessage";
import { FilteredAssistantMessage } from "@/components/pdf-analyst/FilteredAssistantMessage";
import { Split } from "@/components/pdf-analyst/Split";

const AGENT_ID = "fixed_agent";

const SAMPLE_PROMPTS = [
  "I've been taking ExampleMed 10mg for 3 days and feel dizzy and nauseous.",
  "A pharmacist reported a broken seal on a medicine pack — no symptoms yet.",
  "Patient had severe rash after antibiotic — needs urgent escalation guidance.",
];

export default function FixedPage() {
  return (
    <div className="h-screen flex flex-col bg-[var(--bg)]">
      <SiteNav active="fixed" />

      <div className="flex-1 min-h-0 flex">
        <Split
          persistKey="fixed.split"
          initialLeftFraction={0.36}
          left={
            <div className="h-full flex flex-col copilot-chat-wrapper">
              <div className="shrink-0 px-4 py-2 border-b border-[var(--line)] bg-[color-mix(in_oklab,var(--mint)_10%,var(--surface))]">
                <span className="mono text-[10.5px] uppercase tracking-[0.12em] text-[var(--muted)]">
                  Try a sample report
                </span>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {SAMPLE_PROMPTS.map((p) => (
                    <span
                      key={p}
                      className="text-[11px] px-2 py-1 rounded-md border border-[var(--line)] bg-[var(--surface)] text-[var(--muted)]"
                    >
                      {p.slice(0, 48)}…
                    </span>
                  ))}
                </div>
              </div>
              <div className="flex-1 min-h-0">
                <CopilotChat
                  agentId={AGENT_ID}
                  chatView={{
                    messageView: {
                      userMessage: FilteredUserMessage,
                      assistantMessage: FilteredAssistantMessage,
                    },
                  }}
                  labels={{
                    chatInputPlaceholder:
                      "Describe a safety concern, then ask to render the case dashboard…",
                    welcomeMessageText:
                      "Describe an adverse reaction, missing patient details, or medicine complaint. Then ask: “Render the safety case dashboard.”",
                  }}
                />
              </div>
            </div>
          }
          right={
            <SurfaceCanvas
              channel={AGENT_ID}
              emptyState={
                <CanvasEmptyState
                  title="No case dashboard yet"
                  subtitle="Describe a safety report in the chat and ask the agent to render the structured case dashboard. The A2UI surface will appear here."
                  hint={
                    <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--ink)]">
                      try: “Render the safety case dashboard.”
                    </span>
                  }
                />
              }
            />
          }
        />
      </div>
    </div>
  );
}
