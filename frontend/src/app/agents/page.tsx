"use client";

import { useEffect, useState } from "react";
import { fetchApi } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

export default function AgentsPage() {
  const [agents, setAgents] = useState<any[]>([]);

  useEffect(() => {
    fetchApi("/agents").then(setAgents).catch(console.error);
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Agents</h1>
        <p className="text-muted-foreground">Manage and govern autonomous agents in your network.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {agents.map((agent) => (
          <Link href={`/agents/${agent.id}`} key={agent.id}>
            <Card className="hover:bg-muted/50 transition-colors h-full">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle className="text-xl">{agent.name}</CardTitle>
                  <Badge variant={agent.status === "ACTIVE" ? "default" : "secondary"}>
                    {agent.status}
                  </Badge>
                </div>
                <CardDescription>{agent.type} Operator</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">{agent.description}</p>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium">Risk Profile:</span>
                  <Badge variant={
                    agent.risk_level === "LOW" ? "default" :
                    agent.risk_level === "HIGH" ? "destructive" : "secondary"
                  }>
                    {agent.risk_level}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
