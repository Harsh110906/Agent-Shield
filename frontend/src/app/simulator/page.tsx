"use client";

import { useState } from "react";
import { fetchApi } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ShieldCheck, ShieldAlert, FileWarning, Play } from "lucide-react";

export default function SimulatorPage() {
  const [objective, setObjective] = useState("");
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState<any>(null);

  const runSimulation = async () => {
    setRunning(true);
    // In a real app we'd ask the LLM to generate proposals based on the objective,
    // but for the demo we'll use a hardcoded set of proposals to pass to the simulator API.
    const mockProposals = [
      {
        agent_id: "agent-finance",
        tool_name: "get_invoice",
        parameters: { invoice_id: "INV-999" }
      },
      {
        agent_id: "agent-finance",
        tool_name: "issue_refund",
        parameters: { amount: 12000, customer_id: "CUST-999" }
      },
      {
        agent_id: "agent-database",
        tool_name: "delete_customer",
        parameters: { id: "CUST-999" }
      }
    ];

    try {
      const res = await fetchApi("/simulate", {
        method: "POST",
        body: JSON.stringify(mockProposals)
      });
      setResults(res);
    } catch (e) {
      console.error(e);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Simulator (Dry-Run)</h1>
        <p className="text-muted-foreground">Test agent workflows against policies without executing real actions.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Simulation Input</CardTitle>
            <CardDescription>Provide a natural language objective for the agent.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Textarea 
              placeholder="e.g. Process all pending customer refunds." 
              className="min-h-[120px]"
              value={objective}
              onChange={e => setObjective(e.target.value)}
            />
            <Button onClick={runSimulation} disabled={running || !objective} className="w-full">
              <Play className="mr-2 h-4 w-4" /> {running ? "Simulating..." : "Run Simulation"}
            </Button>
          </CardContent>
        </Card>

        {results && (
          <Card className="bg-muted/30">
            <CardHeader>
              <CardTitle>Simulation Results</CardTitle>
              <CardDescription>Predicted actions and risk assessment.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col border rounded-md p-3 bg-background">
                  <span className="text-xs text-muted-foreground mb-1">Predicted Actions</span>
                  <span className="text-2xl font-bold">{results.stats.total}</span>
                </div>
                <div className="flex flex-col border rounded-md p-3 bg-background">
                  <span className="text-xs text-muted-foreground mb-1">Financial Exposure</span>
                  <span className="text-2xl font-bold">₹{results.stats.financial_exposure.toLocaleString()}</span>
                </div>
                <div className="flex flex-col border rounded-md p-3 bg-background">
                  <span className="text-xs text-muted-foreground mb-1">Policy Violations</span>
                  <span className="text-2xl font-bold text-destructive">{results.stats.policy_violations}</span>
                </div>
                <div className="flex flex-col border rounded-md p-3 bg-background">
                  <span className="text-xs text-muted-foreground mb-1">Highest Risk</span>
                  <span className="text-2xl font-bold text-amber-500">{results.stats.highest_risk}/100</span>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-semibold mb-3">Decisions Breakdown</h4>
                <div className="flex justify-between items-center bg-background border p-2 rounded">
                  <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4 text-green-500"/> ALLOW</div>
                  <span className="font-mono">{results.stats.ALLOW}</span>
                </div>
                <div className="flex justify-between items-center bg-background border p-2 rounded">
                  <div className="flex items-center gap-2"><FileWarning className="h-4 w-4 text-amber-500"/> APPROVAL</div>
                  <span className="font-mono">{results.stats.REQUIRE_APPROVAL}</span>
                </div>
                <div className="flex justify-between items-center bg-background border p-2 rounded">
                  <div className="flex items-center gap-2"><ShieldAlert className="h-4 w-4 text-destructive"/> BLOCK</div>
                  <span className="font-mono">{results.stats.BLOCK}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
