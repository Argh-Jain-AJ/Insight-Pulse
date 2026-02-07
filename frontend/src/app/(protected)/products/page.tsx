import React from 'react';
import TrackerCard from '@/components/TrackerCard';
import InsightGroup from '@/components/InsightGroup';
import { fetchProducts } from '@/lib/api';

export default async function ProductsPage() {
    const products = await fetchProducts();

    return (
        <>
            <header className="top-bar">
                <div>
                    <h1>Product Tracker</h1>
                    <p className="subtitle">Track direct competitive threats and adjacent market shifts impacting your portfolio.</p>
                </div>
            </header>

            <div className="content-grid" style={{ maxWidth: '1000px' }}>
                <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                    <button className="btn-filter">My Products</button>
                    <button className="btn-filter">Watchlist</button>
                </div>

                {products.map((prod) => (
                    <TrackerCard
                        key={prod.id}
                        title={prod.name}
                        subtitle={`${prod.therapeutic_area} • ${prod.indication} • ${prod.phase}`}
                        stats={[
                            { label: 'Total Insights', value: prod.insight_count },
                            { label: 'Last Update', value: "Recently" }
                        ]}
                    >
                        <div className="tracker-expanded-content">
                            <InsightGroup title="Direct Insights" blocks={prod.insights?.Direct || []} />
                            <InsightGroup title="Adjacent / Indirect Insights" blocks={prod.insights?.Adjacent || []} />
                            {prod.insight_count === 0 && (
                                <p style={{ color: '#888', fontStyle: 'italic', fontSize: '0.9rem' }}>No recent insights detected for this product.</p>
                            )}
                        </div>
                    </TrackerCard>
                ))}
            </div>
        </>
    );
}
