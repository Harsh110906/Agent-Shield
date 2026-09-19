"use client";

import { useEffect, useState } from "react";
import { fetchApi } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ShieldAlert } from "lucide-react";

export default function SecurityPage() {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    fetchApi("/security-events").then(setEvents).catch(console.error);
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-3">
        <ShieldAlert className="h-8 w-8 text-destructive" />
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-destructive">Security Events</h1>
          <p className="text-muted-foreground">Critical security findings, prompt injections, and data leaks.</p>
        </div>
      </div>

      <div className="grid gap-4">
        {events.map((event) => (
          <Card key={event.id} className="border-destructive/30 bg-destructive/5">
            <CardHeader className="pb-3 flex flex-row items-start justify-between">
              <div>
                <CardTitle className="text-lg text-destructive">{event.event_type}</CardTitle>
                <CardDescription className="mt-1">
                  Agent: <span className="font-semibold text-foreground">{event.agent_id || "Unknown"}</span>
                </CardDescription>
              </div>
              <Badge variant="destructive">{event.severity}</Badge>
            </CardHeader>
            <CardContent>
              <p className="text-sm font-medium">{event.description}</p>
              <p className="text-xs text-muted-foreground mt-4">
                Detected at: {new Date(event.timestamp).toLocaleString()}
              </p>
            </CardContent>
          </Card>
        ))}
        {events.length === 0 && (
          <div className="text-center p-12 border rounded-lg bg-muted/20 text-muted-foreground">
            No security events detected yet.
          </div>
        )}
      </div>
    </div>
  );
}
