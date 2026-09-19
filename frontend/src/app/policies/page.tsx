"use client";

import { useEffect, useState } from "react";
import { fetchApi } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Shield } from "lucide-react";

export default function PoliciesPage() {
  const [policies, setPolicies] = useState<any[]>([]);

  useEffect(() => {
    fetchApi("/policies").then(setPolicies).catch(console.error);
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Security Policies</h1>
          <p className="text-muted-foreground">Configurable rules governing agent actions.</p>
        </div>
        <Button>
          <Shield className="mr-2 h-4 w-4" /> Create Policy
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {policies.map((policy) => (
          <Card key={policy.id} className="flex flex-col">
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle className="text-xl">{policy.name}</CardTitle>
                <Badge variant={policy.enabled ? "default" : "secondary"}>
                  {policy.enabled ? "ACTIVE" : "DISABLED"}
                </Badge>
              </div>
              <CardDescription>{policy.category}</CardDescription>
            </CardHeader>
            <CardContent className="flex-1">
              <p className="text-sm text-muted-foreground mb-4">{policy.description}</p>
              <div className="bg-muted p-4 rounded-md overflow-x-auto">
                <pre className="text-xs">
                  {JSON.stringify(policy.rules, null, 2)}
                </pre>
              </div>
            </CardContent>
            <CardFooter className="gap-2">
              <Button variant="outline" className="w-full">Edit</Button>
              <Button variant="outline" className="w-full text-destructive">Disable</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}
