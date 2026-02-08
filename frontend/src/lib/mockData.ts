import { Insight, Competitor, Product, ContextBlock } from '@/types';

// MOCK DATA REMAINING FOR FALLBACK / REFERENCE


export const MOCK_COMPETITORS: Competitor[] = [
    { id: 1, name: "Novo Nordisk", tier: "Tier 1", insight_count: 0, high_severity_count: 0, insights: { Theme: [], GTM: [], Positioning: [], Uncategorized: [] } },
    { id: 2, name: "Pfizer", tier: "Tier 1", insight_count: 0, high_severity_count: 0, insights: { Theme: [], GTM: [], Positioning: [], Uncategorized: [] } },
    { id: 3, name: "Novartis", tier: "Tier 1", insight_count: 0, high_severity_count: 0, insights: { Theme: [], GTM: [], Positioning: [], Uncategorized: [] } },
    { id: 4, name: "Roche", tier: "Tier 1", insight_count: 0, high_severity_count: 0, insights: { Theme: [], GTM: [], Positioning: [], Uncategorized: [] } },
    { id: 5, name: "AstraZeneca", tier: "Tier 1", insight_count: 0, high_severity_count: 0, insights: { Theme: [], GTM: [], Positioning: [], Uncategorized: [] } },
];

export const MOCK_PRODUCTS: Product[] = [
    { id: 1, name: "Mounjaro", therapeutic_area: "Metabolic", indication: "Type 2 Diabetes", phase: "Marketed", insight_count: 0, insights: { Direct: [], Adjacent: [] } },
    { id: 2, name: "Zepbound", therapeutic_area: "Metabolic", indication: "Obesity", phase: "Marketed", insight_count: 0, insights: { Direct: [], Adjacent: [] } },
    { id: 3, name: "Verzenio", therapeutic_area: "Oncology", indication: "Breast Cancer", phase: "Marketed", insight_count: 0, insights: { Direct: [], Adjacent: [] } },
    { id: 4, name: "Taltz", therapeutic_area: "Immunology", indication: "Psoriasis", phase: "Marketed", insight_count: 0, insights: { Direct: [], Adjacent: [] } },
    { id: 5, name: "Jardiance", therapeutic_area: "Metabolic", indication: "Diabetes/Heart Failure", phase: "Marketed", insight_count: 0, insights: { Direct: [], Adjacent: [] } },
];
