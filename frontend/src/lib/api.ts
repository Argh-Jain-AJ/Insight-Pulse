import { DashboardResponse, Competitor, Product, Insight } from '@/types';
import { MOCK_COMPETITORS, MOCK_PRODUCTS } from '@/lib/mockData';
import { DEMO_DATA } from '@/lib/demoData';

const API_BASE = 'http://127.0.0.1:8000/api';

const isDemoMode = () => {
    if (typeof window === 'undefined') return false;
    return localStorage.getItem('DEMO_MODE') === 'true';
};

export async function fetchDashboardData(): Promise<DashboardResponse | null> {
    if (isDemoMode()) {
        const insights = DEMO_DATA.insights as Insight[];
        const recent = insights.filter(i => i.severity === 'high' || i.velocity === 'increasing' || i.velocity === 'new');
        return {
            recent_activity: recent,
            general_insights: {
                Theme: insights.filter(i => i.category === 'Theme'),
                GTM: insights.filter(i => i.category === 'GTM'),
                Positioning: insights.filter(i => i.category === 'Positioning'),
                Other: insights.filter(i => !['Theme', 'GTM', 'Positioning'].includes(i.category || ''))
            },
            rolling_pulse: insights.slice(0, 5)
        };
    }

    try {
        const res = await fetch(`${API_BASE}/dashboard`, {
            cache: 'no-store',
            headers: { 'Cache-Control': 'no-cache' }
        });
        if (!res.ok) return null;
        return res.json();
    } catch (err) {
        console.error("API Fetch Error (Dashboard):", err);
        return null;
    }
}

export async function fetchCompetitors(): Promise<Competitor[]> {
    if (isDemoMode()) {
        const insights = DEMO_DATA.insights as Insight[];
        return DEMO_DATA.entities.competitors.map(c => {
            const focalInsights = insights.filter(i => i.subjects.includes(c.name));

            // Pre-calculate insights for demo mode visibility
            const blocks = DEMO_DATA.context_blocks.filter(b => b.focal_entity_name === c.name && b.focal_entity_type === 'competitor');
            const grouped: NonNullable<Competitor['insights']> = {
                Theme: [],
                GTM: [],
                Positioning: [],
                Uncategorized: []
            };

            blocks.forEach(b => {
                const insight = insights.find(i => i.id === b.insight_id);
                if (insight) {
                    const cat = insight.category as keyof typeof grouped | undefined;
                    const groupKey = (cat && grouped[cat]) ? cat : 'Uncategorized';
                    grouped[groupKey].push({
                        insight,
                        context_framing: b.framing_text
                    });
                }
            });

            return {
                ...c,
                tier: c.tier,
                insight_count: focalInsights.length,
                high_severity_count: focalInsights.filter(i => i.severity === 'high').length,
                insights: grouped
            };
        });
    }

    try {
        const res = await fetch(`${API_BASE}/competitors`, { cache: 'no-store' });
        if (!res.ok) {
            console.warn("Failed to fetch competitors, using fallback mock data.");
            return MOCK_COMPETITORS;
        }
        return res.json();
    } catch (err) {
        console.error("API Fetch Error (Competitors), using fallback:", err);
        return MOCK_COMPETITORS;
    }
}

export async function fetchCompetitorDetail(id: number): Promise<Competitor['insights'] | null> {
    if (isDemoMode()) {
        const comp = DEMO_DATA.entities.competitors.find(c => c.id === id);
        if (!comp) return null;

        const blocks = DEMO_DATA.context_blocks.filter(b => b.focal_entity_name === comp.name && b.focal_entity_type === 'competitor');
        const grouped: NonNullable<Competitor['insights']> = {
            Theme: [],
            GTM: [],
            Positioning: [],
            Uncategorized: []
        };

        blocks.forEach(b => {
            const insight = (DEMO_DATA.insights as Insight[]).find(i => i.id === b.insight_id);
            if (insight) {
                const cat = insight.category as keyof typeof grouped | undefined;
                const groupKey = (cat && grouped[cat]) ? cat : 'Uncategorized';
                grouped[groupKey].push({
                    insight,
                    context_framing: b.framing_text
                });
            }
        });
        return grouped;
    }

    try {
        const res = await fetch(`${API_BASE}/competitors/${id}`, { cache: 'no-store' });
        if (!res.ok) return null;
        return res.json();
    } catch (err) {
        console.error(`API Fetch Error (Competitor ${id} detail):`, err);
        return null;
    }
}

export async function fetchProducts(): Promise<Product[]> {
    if (isDemoMode()) {
        const insights = DEMO_DATA.insights as Insight[];
        return DEMO_DATA.entities.products.map(p => {
            const focalInsights = insights.filter(i => i.subjects.includes(p.name));

            // Pre-calculate insights for demo mode visibility
            const blocks = DEMO_DATA.context_blocks.filter(b => b.focal_entity_name === p.name && b.focal_entity_type === 'product');
            const grouped: NonNullable<Product['insights']> = {
                Direct: [],
                Adjacent: []
            };

            blocks.forEach(b => {
                const insight = insights.find(i => i.id === b.insight_id);
                if (insight) {
                    const cat: keyof typeof grouped = insight.subjects.includes(p.name) ? 'Direct' : 'Adjacent';
                    grouped[cat].push({
                        insight,
                        context_framing: b.framing_text
                    });
                }
            });

            return {
                ...p,
                insight_count: focalInsights.length,
                insights: grouped
            };
        });
    }

    try {
        const res = await fetch(`${API_BASE}/products`, { cache: 'no-store' });
        if (!res.ok) {
            console.warn("Failed to fetch products, using fallback mock data.");
            return MOCK_PRODUCTS;
        }
        return res.json();
    } catch (err) {
        console.error("API Fetch Error (Products), using fallback:", err);
        return MOCK_PRODUCTS;
    }
}

export async function fetchProductDetail(id: number): Promise<Product['insights'] | null> {
    if (isDemoMode()) {
        const prod = DEMO_DATA.entities.products.find(p => p.id === id);
        if (!prod) return null;

        const blocks = DEMO_DATA.context_blocks.filter(b => b.focal_entity_name === prod.name && b.focal_entity_type === 'product');
        const grouped: NonNullable<Product['insights']> = {
            Direct: [],
            Adjacent: []
        };

        blocks.forEach(b => {
            const insight = (DEMO_DATA.insights as Insight[]).find(i => i.id === b.insight_id);
            if (insight) {
                const cat: keyof typeof grouped = insight.subjects.includes(prod.name) ? 'Direct' : 'Adjacent';
                grouped[cat].push({
                    insight,
                    context_framing: b.framing_text
                });
            }
        });
        return grouped;
    }

    try {
        const res = await fetch(`${API_BASE}/products/${id}`, { cache: 'no-store' });
        if (!res.ok) return null;
        return res.json();
    } catch (err) {
        console.error(`API Fetch Error (Product ${id} detail):`, err);
        return null;
    }
}
