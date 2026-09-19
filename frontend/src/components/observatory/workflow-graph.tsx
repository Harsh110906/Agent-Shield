"use client";

import { useCallback } from "react";
import { ReactFlow, MiniMap, Controls, Background, useNodesState, useEdgesState, BackgroundVariant, MarkerType } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const initialNodes = [
  { id: "agent", position: { x: 50, y: 150 }, data: { label: "AI Agent" }, style: { background: '#1e293b', color: 'white', borderRadius: '8px' } },
  { id: "proposal", position: { x: 250, y: 150 }, data: { label: "Action Proposal" }, style: { background: '#334155', color: 'white', borderRadius: '8px' } },
  { id: "shield", position: { x: 450, y: 150 }, data: { label: "AgentShield Gateway" }, style: { background: '#2563eb', color: 'white', fontWeight: 'bold', borderRadius: '8px' } },
  { id: "permission", position: { x: 650, y: 50 }, data: { label: "Permission Check" }, style: { background: '#0f172a', color: 'white', borderRadius: '8px' } },
  { id: "security", position: { x: 650, y: 100 }, data: { label: "Security Scanner" }, style: { background: '#0f172a', color: 'white', borderRadius: '8px' } },
  { id: "policy", position: { x: 650, y: 150 }, data: { label: "Policy Engine" }, style: { background: '#0f172a', color: 'white', borderRadius: '8px' } },
  { id: "risk", position: { x: 650, y: 200 }, data: { label: "Risk Engine" }, style: { background: '#0f172a', color: 'white', borderRadius: '8px' } },
  { id: "decision", position: { x: 850, y: 150 }, data: { label: "Decision Engine" }, style: { background: '#3b82f6', color: 'white', borderRadius: '8px' } },
  { id: "allow", position: { x: 1050, y: 50 }, data: { label: "ALLOW" }, style: { background: '#22c55e', color: 'white', borderRadius: '8px' } },
  { id: "approval", position: { x: 1050, y: 150 }, data: { label: "APPROVAL" }, style: { background: '#f59e0b', color: 'white', borderRadius: '8px' } },
  { id: "block", position: { x: 1050, y: 250 }, data: { label: "BLOCK" }, style: { background: '#ef4444', color: 'white', borderRadius: '8px' } },
  { id: "tool", position: { x: 1250, y: 100 }, data: { label: "Tool Execution" }, style: { background: '#475569', color: 'white', borderRadius: '8px' } },
  { id: "audit", position: { x: 1250, y: 250 }, data: { label: "Audit Log" }, style: { background: '#0f172a', color: 'white', borderRadius: '8px' } }
];

const initialEdges = [
  { id: "e1", source: "agent", target: "proposal", animated: true },
  { id: "e2", source: "proposal", target: "shield", animated: true },
  { id: "e3", source: "shield", target: "permission" },
  { id: "e4", source: "shield", target: "security" },
  { id: "e5", source: "shield", target: "policy" },
  { id: "e6", source: "shield", target: "risk" },
  { id: "e7", source: "permission", target: "decision" },
  { id: "e8", source: "security", target: "decision" },
  { id: "e9", source: "policy", target: "decision" },
  { id: "e10", source: "risk", target: "decision" },
  { id: "e11", source: "decision", target: "allow", animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e12", source: "decision", target: "approval", animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e13", source: "decision", target: "block", animated: true, markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e14", source: "allow", target: "tool", markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e15", source: "approval", target: "tool", label: "if approved", markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e16", source: "block", target: "audit" },
  { id: "e17", source: "tool", target: "audit" }
];

export function WorkflowGraph() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div style={{ height: 500, width: "100%", border: "1px solid #1e293b", borderRadius: "8px" }} className="bg-background">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        colorMode="dark"
      >
        <Controls />
        <MiniMap />
        <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}
