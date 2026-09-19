"use client";

import { useEffect, useState } from "react";
import { fetchApi } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Shield, ShieldAlert, Activity, CheckCircle, Clock } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    fetchApi("/metrics").then(setMetrics).catch(console.error);
  }, []);

  if (!metrics) {
    return <div className="flex h-[50vh] items-center justify-center">Loading dashboard...</div>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Command Center</h1>
        <p className="text-muted-foreground">Monitor and govern your autonomous AI agents.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.active_agents}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Actions Today</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.actions_today}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Approvals</CardTitle>
            <Clock className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.pending_approvals}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Blocked Actions</CardTitle>
            <ShieldAlert className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.blocked_actions}</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Live Activity Feed</CardTitle>
            <CardDescription>Real-time stream of agent actions and decisions.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {metrics.activity_feed.map((action: any) => (
                <div key={action.action_id} className="flex items-center justify-between rounded-lg border p-3">
                  <div className="flex flex-col gap-1">
                    <span className="text-sm font-semibold">{action.agent_name}</span>
                    <span className="text-xs text-muted-foreground">{action.tool_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs">Risk: {action.risk_score}</span>
                    <Badge variant={
                      action.decision === "ALLOW" ? "default" :
                      action.decision === "BLOCK" ? "destructive" : "secondary"
                    }>
                      {action.decision}
                    </Badge>
                  </div>
                </div>
              ))}
              {metrics.activity_feed.length === 0 && (
                <div className="text-sm text-muted-foreground">No recent activity.</div>
              )}
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Top Security Events</CardTitle>
            <CardDescription>Recent high-severity security findings.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {metrics.security_events.map((event: any) => (
                <div key={event.id} className="flex flex-col gap-2 rounded-lg border border-destructive/50 bg-destructive/10 p-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-semibold text-destructive">{event.event_type}</span>
                    <span className="text-xs opacity-70">{new Date(event.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <p className="text-xs">{event.description}</p>
                </div>
              ))}
              {metrics.security_events.length === 0 && (
                <div className="text-sm text-muted-foreground">No recent security events.</div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
