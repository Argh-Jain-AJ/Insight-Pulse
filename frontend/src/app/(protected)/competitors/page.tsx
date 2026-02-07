import React from 'react';
import TrackerCard from '@/components/TrackerCard';
import InsightGroup from '@/components/InsightGroup';
import { fetchCompetitors } from '@/lib/api';

export default async function CompetitorsPage() {
    const competitors = await fetchCompetitors();

    return (
        <>
            <header className="top-bar">
                <div>
                    <h1>Competitor Tracker</h1>
                    <p className="subtitle">Monitor strategic shifts, GTM changes, and positioning moves across your competitive landscape.</p>
                </div>
            </header>

            <div className="content-grid" style={{ maxWidth: '1000px' }}>
                <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                    <button className="btn-filter">All Tiers</button>
                    <button className="btn-filter">High Severity Only</button>
                </div>

                {competitors.map((comp) => (
                    <TrackerCard
                        key={comp.id}
                        title={comp.name}
                        subtitle={comp.tier}
                        stats={[
                            { label: 'Updates', value: comp.insight_count },
                            { label: 'High Sev', value: comp.high_severity_count || 0, highlight: (comp.high_severity_count || 0) > 0 }
                        ]}
                    >
                        <div className="tracker-expanded-content">
                            <InsightGroup title="Theme Insights" blocks={comp.insights?.Theme || []} />
                            <InsightGroup title="Go-to-Market (GTM)" blocks={comp.insights?.GTM || []} />
                            <InsightGroup title="Positioning" blocks={comp.insights?.Positioning || []} />
                            <InsightGroup title="Uncategorized" blocks={comp.insights?.Uncategorized || []} />

                            {comp.insight_count === 0 && (
                                <p style={{ color: '#888', fontStyle: 'italic', fontSize: '0.9rem' }}>No recent insights detected for this competitor.</p>
                            )}
                        </div>
                    </TrackerCard>
                ))}
            </div>
        </>
    );
}
