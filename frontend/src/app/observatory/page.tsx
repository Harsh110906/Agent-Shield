"use client";

import { WorkflowGraph } from "@/components/observatory/workflow-graph";

export default function ObservatoryPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Agent Observatory</h1>
        <p className="text-muted-foreground">Visualize and monitor the AgentShield execution workflow.</p>
      </div>

      <div className="w-full">
        <WorkflowGraph />
      </div>
    </div>
  );
}
