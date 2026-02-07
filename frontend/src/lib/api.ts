import { DashboardResponse, Competitor, Product } from '@/types';
import { MOCK_COMPETITORS, MOCK_PRODUCTS } from '@/lib/mockData'; // For fallback if needed

const API_BASE = 'http://127.0.0.1:8000/api';

export async function fetchDashboardData(): Promise<DashboardResponse | null> {
    try {
        const res = await fetch(`${API_BASE}/dashboard`, {
            cache: 'no-store',
        });

        if (!res.ok) {
            console.error('Failed to fetch dashboard data', res.status);
            return null;
        }

        return res.json();
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        return null;
    }
}

export async function fetchCompetitors(): Promise<Competitor[]> {
    try {
        const res = await fetch(`${API_BASE}/competitors`, { cache: 'no-store' });
        if (!res.ok) throw new Error("Failed to fetch competitors");
        const summaryList = await res.json();

        // Detailed fetch for each (inefficient but matches mock structure for now)
        // In real app, nested include is better.
        // For MVP, we'll fetch details for each to fully populate.
        // Actually, for list view, we just need summary + maybe pre-fetched details?
        // Let's implement lazy loading in UI? 
        // OR: Fetch detail for ALL? 
        // Let's do: Fetch list, and map to Comp structure. 
        // The endpoint /api/competitors only gives counts. 
        // We need details to show expandable rows.

        const detailedCompetitors = await Promise.all(summaryList.map(async (c: any) => {
            const detailRes = await fetch(`${API_BASE}/competitors/${c.id}`);
            const details = await detailRes.json();
            return {
                ...c,
                last_updated: "Recently", // Backend doesn't have this yet
                insights: details // Matches { Theme: [], ... }
            };
        }));

        return detailedCompetitors;

    } catch (err) {
        console.error("API Fetch Error:", err);
        return [];
    }
}

export async function fetchProducts(): Promise<Product[]> {
    try {
        const res = await fetch(`${API_BASE}/products`, { cache: 'no-store' });
        if (!res.ok) throw new Error("Failed to fetch products");
        const summaryList = await res.json();

        const detailedProducts = await Promise.all(summaryList.map(async (p: any) => {
            const detailRes = await fetch(`${API_BASE}/products/${p.id}`);
            const details = await detailRes.json();
            return {
                ...p,
                last_updated: "Recently",
                insights: details // Matches { Direct: [], Adjacent: [] }
            };
        }));

        return detailedProducts;
    } catch (err) {
        console.error("API Fetch Error:", err);
        return [];
    }
}
