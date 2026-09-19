"use client";

import { useEffect, useState } from "react";
import { fetchApi } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Check, X, ShieldAlert } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<any[]>([]);
  const { toast } = useToast();

  const loadApprovals = () => {
    fetchApi("/approvals").then(setApprovals).catch(console.error);
  };

  useEffect(() => {
    loadApprovals();
    
    // Listen for dashboard refresh events
    window.addEventListener('dashboard-refresh', loadApprovals);
    return () => window.removeEventListener('dashboard-refresh', loadApprovals);
  }, []);

  const handleApprove = async (id: string) => {
    try {
      await fetchApi(`/approvals/${id}/approve`, { method: "POST" });
      toast({ title: "Approved", description: "Action has been allowed to execute." });
      loadApprovals();
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    }
  };

  const handleReject = async (id: string) => {
    try {
      await fetchApi(`/approvals/${id}/reject`, { method: "POST" });
      toast({ title: "Rejected", description: "Action was blocked.", variant: "destructive" });
      loadApprovals();
    } catch (error: any) {
      toast({ title: "Error", description: error.message, variant: "destructive" });
    }
  };

  const pending = approvals.filter(a => a.status === "PENDING");
  const history = approvals.filter(a => a.status !== "PENDING");

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Approvals Inbox</h1>
        <p className="text-muted-foreground">Review high-risk actions requiring human authorization.</p>
      </div>

      <Tabs defaultValue="pending" className="w-full">
        <TabsList>
          <TabsTrigger value="pending">Pending ({pending.length})</TabsTrigger>
          <TabsTrigger value="history">History ({history.length})</TabsTrigger>
        </TabsList>
        
        <TabsContent value="pending" className="mt-6 space-y-4">
          {pending.length === 0 ? (
            <div className="text-center p-12 border rounded-lg bg-muted/20 text-muted-foreground">
              No pending approvals.
            </div>
          ) : (
            pending.map(approval => (
              <Card key={approval.id} className="border-amber-500/20">
                <CardHeader className="bg-amber-500/5 pb-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <ShieldAlert className="h-5 w-5 text-amber-500" />
                        {approval.tool_name}
                      </CardTitle>
                      <CardDescription className="mt-1">
                        Requested by: <span className="font-semibold text-foreground">{approval.agent_id}</span>
                      </CardDescription>
                    </div>
                    <Badge variant="secondary" className="text-amber-500">PENDING</Badge>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <h4 className="text-sm font-semibold mb-2">Action Parameters:</h4>
                  <pre className="bg-muted p-4 rounded-md text-sm mb-6 overflow-x-auto">
                    {JSON.stringify(approval.parameters, null, 2)}
                  </pre>
                  
                  <div className="flex justify-end gap-4">
                    <Button variant="outline" className="text-destructive" onClick={() => handleReject(approval.id)}>
                      <X className="mr-2 h-4 w-4" /> Reject & Block
                    </Button>
                    <Button className="bg-green-600 hover:bg-green-700 text-white" onClick={() => handleApprove(approval.id)}>
                      <Check className="mr-2 h-4 w-4" /> Approve Execution
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </TabsContent>

        <TabsContent value="history" className="mt-6 space-y-4">
          {history.map(approval => (
            <Card key={approval.id} className="opacity-80">
              <CardHeader className="py-4">
                <div className="flex justify-between items-center">
                  <div>
                    <CardTitle className="text-md">{approval.tool_name}</CardTitle>
                    <CardDescription>{approval.agent_id}</CardDescription>
                  </div>
                  <Badge variant={approval.status === "APPROVED" ? "default" : "destructive"}>
                    {approval.status}
                  </Badge>
                </div>
              </CardHeader>
            </Card>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}
