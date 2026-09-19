"use client";

import { useState } from "react";
import { fetchApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Play, ShieldAlert, ShieldCheck, FileWarning, EyeOff } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const SCENARIOS = [
  { id: "1", name: "Safe Customer Support", icon: ShieldCheck, color: "text-green-500", desc: "Lookup customer (ALLOW)" },
  { id: "2", name: "Financial Transaction", icon: FileWarning, color: "text-amber-500", desc: "₹18,500 refund (APPROVAL)" },
  { id: "3", name: "Destructive Attack", icon: ShieldAlert, color: "text-destructive", desc: "Delete all DB (BLOCK)" },
  { id: "4", name: "Secret Leakage", icon: EyeOff, color: "text-destructive", desc: "Email API Key (BLOCK)" }
];

export function DemoPanel() {
  const [running, setRunning] = useState<string | null>(null);
  const { toast } = useToast();

  const runScenario = async (id: string, name: string) => {
    setRunning(id);
    try {
      const result = await fetchApi(`/demo/scenarios/${id}`, { method: "POST" });
      toast({
        title: `Scenario: ${name}`,
        description: `Decision: ${result.evaluation?.decision || result.status}`,
        variant: result.evaluation?.decision === "BLOCK" ? "destructive" : "default"
      });
      // Optionally trigger a refresh event so other components update
      window.dispatchEvent(new Event('dashboard-refresh'));
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    } finally {
      setRunning(null);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2 rounded-lg border bg-background p-4 shadow-lg w-80">
      <div className="flex items-center gap-2 border-b pb-2 mb-2">
        <Play className="h-4 w-4" />
        <h3 className="font-semibold text-sm">Run Demo Scenarios</h3>
      </div>
      <div className="flex flex-col gap-2">
        {SCENARIOS.map((s) => (
          <Button 
            key={s.id} 
            variant="outline" 
            size="sm"
            className="justify-start gap-2 h-auto py-2"
            disabled={running !== null}
            onClick={() => runScenario(s.id, s.name)}
          >
            <s.icon className={`h-4 w-4 ${s.color}`} />
            <div className="flex flex-col items-start text-left">
              <span className="text-xs font-semibold">{s.name}</span>
              <span className="text-[10px] text-muted-foreground">{s.desc}</span>
            </div>
          </Button>
        ))}
      </div>
    </div>
  );
}
