export interface ContextBlock {
    insight: Insight;
    context_framing: string;
}

export interface Competitor {
    id: number;
    name: string;
    tier: string; // Changed from literal to string for API compatibility
    last_updated?: string; // Optional as backend might not always send
    insight_count: number;
    high_severity_count?: number;
    insights?: {
        Theme: ContextBlock[];
        GTM: ContextBlock[];
        Positioning: ContextBlock[];
        Uncategorized: ContextBlock[];
    };
}

export interface Product {
    id: number;
    name: string;
    therapeutic_area: string;
    indication: string;
    phase: string;
    last_updated?: string;
    insight_count: number;
    insights?: {
        Direct: ContextBlock[];
        Adjacent: ContextBlock[];
    };
}
export interface Insight {
    id: number;
    tenant_id: number;
    scope: 'market' | 'competitor' | 'product';
    severity: 'low' | 'medium' | 'high';
    velocity: 'decreasing' | 'stable' | 'increasing' | 'new';
    explanation: string;
    category?: string | null;
    created_at: string;
}

export interface DashboardResponse {
    recent_activity: Insight[];
    general_insights: {
        Theme: Insight[];
        GTM: Insight[];
        Positioning: Insight[];
        Other: Insight[];
    };
    rolling_pulse: Insight[];
}
