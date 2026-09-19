"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Shield, LayoutDashboard, Users, FileText, CheckSquare, PlayCircle, Activity, ShieldAlert, Settings, FileSearch } from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Agents", href: "/agents", icon: Users },
  { name: "Policies", href: "/policies", icon: FileText },
  { name: "Approvals", href: "/approvals", icon: CheckSquare },
  { name: "Simulator", href: "/simulator", icon: PlayCircle },
  { name: "Observatory", href: "/observatory", icon: Activity },
  { name: "Audit Logs", href: "/audit", icon: FileSearch },
  { name: "Security", href: "/security", icon: ShieldAlert },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-screen w-64 flex-col border-r border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-6 border-b border-border/40">
        <Link href="/" className="flex items-center gap-2">
          <Shield className="h-6 w-6 text-primary" />
          <span className="text-lg font-semibold tracking-tight">AgentShield</span>
        </Link>
      </div>
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="grid gap-1 px-4">
          {navigation.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            // Exact match for dashboard to prevent highlighting everywhere
            const actuallyActive = item.href === "/" ? pathname === "/" : isActive;
            
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  actuallyActive 
                    ? "bg-primary/10 text-primary" 
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                <item.icon className="h-4 w-4" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
      <div className="p-4 border-t border-border/40">
        <div className="flex items-center gap-3 rounded-md bg-muted/50 p-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20 text-primary">
            <Shield className="h-4 w-4" />
          </div>
          <div className="flex flex-col">
            <span className="text-xs font-medium">Gateway Active</span>
            <span className="text-[10px] text-muted-foreground">Demo Mode</span>
          </div>
        </div>
      </div>
    </div>
  );
}
