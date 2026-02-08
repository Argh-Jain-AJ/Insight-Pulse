'use client';

import React, { useState, useEffect } from 'react';
import TrackerCard from '@/components/TrackerCard';
import InsightGroup from '@/components/InsightGroup';
import { fetchProducts } from '@/lib/api';
import RunPipelineButton from '@/components/RunPipelineButton';
import { Product } from '@/types';

export default function ProductsPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchProducts().then(data => {
            setProducts(data);
            setLoading(false);
        });
    }, []);

    if (loading) {
        return <div className="p-12 text-center text-gray-500">Loading products...</div>;
    }

    return (
        <>
            <header className="top-bar">
                <div>
                    <h1>Product Tracker</h1>
                    <p className="subtitle">Track direct competitive threats and adjacent market shifts impacting your portfolio.</p>
                </div>
                <RunPipelineButton />
            </header>

            <div className="content-grid" style={{ maxWidth: '1000px', marginTop: '2rem' }}>

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
                            {prod.insight_count > 0 ? (
                                <>
                                    <InsightGroup title="Direct Insights" blocks={prod.insights?.Direct || []} />
                                    <InsightGroup title="Adjacent / Indirect Insights" blocks={prod.insights?.Adjacent || []} />
                                </>
                            ) : (
                                <div className="tracker-empty-box">
                                    <span>No direct threats or shifts detected for {prod.name} yet.</span>
                                    <p className="text-sm">Run the intelligence pipeline to scan for new updates.</p>
                                </div>
                            )}
                        </div>
                    </TrackerCard>
                ))}
                {products.length === 0 && (
                    <div className="p-12 text-center text-gray-400 italic">
                        No products are currently being tracked.
                    </div>
                )}
            </div>
        </>
    );
}
