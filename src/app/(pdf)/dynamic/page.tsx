"use client";

import { z } from "zod";
import { CopilotChat, useRenderTool } from "@copilotkit/react-core/v2";
import { SiteNav } from "@/components/pdf-analyst/Brand";
import { SurfaceCanvas, CanvasEmptyState } from "@/components/pdf-analyst/SurfaceCanvas";
import { FilteredUserMessage } from "@/components/pdf-analyst/FilteredUserMessage";
import { FilteredAssistantMessage } from "@/components/pdf-analyst/FilteredAssistantMessage";
import { Split } from "@/components/pdf-analyst/Split";

const AGENT_ID = "dynamic_agent";

export default function DynamicPage() {
  useRenderTool({
    name: "generate_a2ui",
    parameters: z.any(),
    render: ({ status }) => {
      if (status === "complete") return <></>;
      return (
        <div className="surface-soft px-3 py-2 my-1 flex items-center gap-3 text-[13px] text-[var(--ink-2)]">
          <span className="relative inline-flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full rounded-full bg-[var(--lilac)] opacity-75 animate-ping" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[var(--lilac)]" />
          </span>
          <span>Composing analysis surface…</span>
        </div>
      );
    },
  });

  useRenderTool({
    name: "query_pdf",
    parameters: z.any(),
    render: () => <></>,
  });

  return (
    <div className="h-screen flex flex-col bg-[var(--bg)]">
      <SiteNav active="dynamic" />

      <div className="flex-1 min-h-0 flex">
        <Split
          persistKey="dynamic.split"
          initialLeftFraction={0.36}
          left={
            <div className="h-full flex flex-col copilot-chat-wrapper">
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
                      "First describe your case, then ask a follow-up…",
                    welcomeMessageText:
                      "Start by describing your safety concern (e.g. symptoms after ExampleMed). Then ask follow-ups like “What are the escalation criteria?” or “Show a symptom timeline chart.”",
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
                  title="No analysis surface yet"
                  subtitle="Describe a case and ask a follow-up question. The agent will compose charts, callouts, or tables from the A2UI catalog."
                  hint={
                    <span className="mono text-[11px] uppercase tracking-[0.14em] text-[var(--ink)]">
                      try: “What triggers regulatory escalation?”
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
