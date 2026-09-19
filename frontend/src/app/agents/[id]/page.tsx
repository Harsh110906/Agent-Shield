"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { fetchApi } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Shield, ShieldAlert, CheckCircle } from "lucide-react";

export default function AgentDetail() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchApi(`/agents/${id}`).then(setData).catch(console.error);
  }, [id]);

  if (!data) return <div className="flex h-[50vh] items-center justify-center">Loading agent details...</div>;

  const { agent, tools } = data;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{agent.name}</h1>
        <p className="text-muted-foreground">{agent.description}</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Profile Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between">
              <span className="font-medium">Status</span>
              <Badge>{agent.status}</Badge>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Type</span>
              <span>{agent.type}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-medium">Risk Level</span>
              <Badge variant={agent.risk_level === "HIGH" ? "destructive" : "secondary"}>{agent.risk_level}</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Permitted Tools</CardTitle>
            <CardDescription>Tool access levels configured via gateway.</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Tool</TableHead>
                  <TableHead>Risk Score</TableHead>
                  <TableHead>Permission</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {tools.map((t: any) => (
                  <TableRow key={t.tool_id}>
                    <TableCell className="font-medium">{t.name}</TableCell>
                    <TableCell>{t.risk_base_score}</TableCell>
                    <TableCell>
                      {t.permission === "allowed" && <Badge variant="default" className="bg-green-500 hover:bg-green-600"><CheckCircle className="h-3 w-3 mr-1"/> ALLOWED</Badge>}
                      {t.permission === "approval" && <Badge variant="secondary" className="text-amber-500"><Shield className="h-3 w-3 mr-1"/> APPROVAL</Badge>}
                      {t.permission === "blocked" && <Badge variant="destructive"><ShieldAlert className="h-3 w-3 mr-1"/> BLOCKED</Badge>}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
