import { Insight, Competitor, Product, ContextBlock } from '@/types';

// MOCK DATA REMAINING FOR FALLBACK / REFERENCE


export const MOCK_COMPETITORS: Competitor[] = [
    {
        id: 1,
        name: "Acme Corp",
        tier: "Tier 1",
        last_updated: "2 hours ago",
        insight_count: 5,
        high_severity_count: 2,
        insights: {
            Theme: [
                {
                    insight: {
                        id: 101,
                        tenant_id: 1,
                        scope: 'market',
                        severity: 'medium',
                        velocity: 'increasing',
                        explanation: 'Acme Corp is heavily investing in AI-driven drug discovery partnerships.',
                        category: 'Theme',
                        created_at: new Date().toISOString()
                    },
                    context_framing: 'Strategic shift observed over last 3 quarters.'
                }
            ],
            GTM: [
                {
                    insight: {
                        id: 102,
                        tenant_id: 1,
                        scope: 'competitor',
                        severity: 'high',
                        velocity: 'increasing',
                        explanation: 'Aggressive bundling of oncology portfolio in EU tenders.',
                        category: 'GTM',
                        created_at: new Date().toISOString()
                    },
                    context_framing: 'Directly impacts our Q3 tender strategy in Germany.'
                }
            ],
            Positioning: [],
            Uncategorized: []
        }
    },
    {
        id: 2,
        name: "BioGenX",
        tier: "Tier 2",
        last_updated: "1 day ago",
        insight_count: 2,
        high_severity_count: 0,
        insights: {
            Theme: [],
            GTM: [],
            Positioning: [
                {
                    insight: {
                        id: 201,
                        tenant_id: 1,
                        scope: 'competitor',
                        severity: 'low',
                        velocity: 'stable',
                        explanation: 'Re-branding of legacy assets to emphasize patient support programs.',
                        category: 'Positioning',
                        created_at: new Date().toISOString()
                    },
                    context_framing: 'Standard lifecycle management tactic.'
                }
            ],
            Uncategorized: []
        }
    },
    {
        id: 3,
        name: "Novus Pharma",
        tier: "Emerging",
        last_updated: "5 hours ago",
        insight_count: 3,
        high_severity_count: 1,
        insights: {
            Theme: [],
            GTM: [
                {
                    insight: {
                        id: 301,
                        tenant_id: 1,
                        scope: 'competitor',
                        severity: 'high',
                        velocity: 'new',
                        explanation: 'Launched direct-to-patient digital platform for rare disease awareness.',
                        category: 'GTM',
                        created_at: new Date().toISOString()
                    },
                    context_framing: 'New channel entry; monitor for patient acquisition rates.'
                }
            ],
            Positioning: [],
            Uncategorized: []
        }
    }
];

export const MOCK_PRODUCTS: Product[] = [
    {
        id: 1,
        name: "OncoSure",
        therapeutic_area: "Oncology",
        indication: "NSCLC",
        phase: "Marketed",
        last_updated: "3 hours ago",
        insight_count: 4,
        insights: {
            Direct: [
                {
                    insight: {
                        id: 401,
                        tenant_id: 1,
                        scope: 'product',
                        severity: 'high',
                        velocity: 'increasing',
                        explanation: 'Competitor X released superior OS data for same-line therapy.',
                        category: 'Clinical',
                        created_at: new Date().toISOString()
                    },
                    context_framing: 'Direct competitive threat to broad line usage.'
                }
            ],
            Adjacent: [
                {
                    insight: {
                        id: 402,
                        tenant_id: 1,
                        scope: 'market',
                        severity: 'medium',
                        velocity: 'stable',
                        explanation: 'Payer pushback on PD-1 inhibitors in second-line settings.',
                        category: 'Market Access',
                        created_at: new Date().toISOString()
                    },
                    context_framing: 'Adjacent: Affects broader class reimbursement dynamics.'
                }
            ]
        }
    },
    {
        id: 2,
        name: "CardioFix",
        therapeutic_area: "Cardiovascular",
        indication: "Heart Failure",
        phase: "Phase III",
        last_updated: "2 days ago",
        insight_count: 1,
        insights: {
            Direct: [],
            Adjacent: [
                {
                    insight: {
                        id: 501,
                        tenant_id: 1,
                        scope: 'competitor',
                        severity: 'low',
                        velocity: 'increasing',
                        explanation: 'Generic entrant filed ANDA for reference product.',
                        category: 'Generics',
                        created_at: new Date().toISOString()
                    },
                    context_framing: 'Adjacent: May impact pricing expectations at launch.'
                }
            ]
        }
    }
];
