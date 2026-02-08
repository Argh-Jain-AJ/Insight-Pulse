'use client';

import React, { useState, useEffect } from 'react';
import TrackerCard from '@/components/TrackerCard';
import InsightGroup from '@/components/InsightGroup';
import { fetchCompetitors } from '@/lib/api';
import RunPipelineButton from '@/components/RunPipelineButton';
import { Competitor } from '@/types';

export default function CompetitorsPage() {
    const [competitors, setCompetitors] = useState<Competitor[]>([]);
    const [loading, setLoading] = useState(true);
    const [sortOption, setSortOption] = useState<'updates' | 'severity'>('updates');

    useEffect(() => {
        fetchCompetitors().then(data => {
            setCompetitors(data);
            setLoading(false);
        });
    }, []);

    const sortedCompetitors = [...competitors].sort((a, b) => {
        if (sortOption === 'updates') {
            return (b.insight_count || 0) - (a.insight_count || 0);
        } else {
            return (b.high_severity_count || 0) - (a.high_severity_count || 0);
        }
    });

    if (loading) {
        return <div className="p-12 text-center text-gray-500">Loading competitors...</div>;
    }

    return (
        <>
            <header className="top-bar">
                <div>
                    <h1>Competitor Tracker</h1>
                    <p className="subtitle">Monitor strategic shifts, GTM changes, and positioning moves across your competitive landscape.</p>
                </div>
                <RunPipelineButton />
            </header>

            <div className="content-grid" style={{ maxWidth: '1000px' }}>
                <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)', fontWeight: 500 }}>Sort by:</span>
                    <button
                        className={`btn-filter ${sortOption === 'updates' ? 'active' : ''}`}
                        onClick={() => setSortOption('updates')}
                        style={sortOption === 'updates' ? { borderColor: 'var(--color-primary)', color: 'var(--color-primary)', background: 'rgba(0, 78, 100, 0.05)' } : {}}
                    >
                        Updates
                    </button>
                    <button
                        className={`btn-filter ${sortOption === 'severity' ? 'active' : ''}`}
                        onClick={() => setSortOption('severity')}
                        style={sortOption === 'severity' ? { borderColor: 'var(--color-primary)', color: 'var(--color-primary)', background: 'rgba(0, 78, 100, 0.05)' } : {}}
                    >
                        Severity
                    </button>
                </div>

                {sortedCompetitors.map((comp) => (
                    <TrackerCard
                        key={comp.id}
                        title={comp.name}
                        subtitle="Competitor"
                        stats={[
                            { label: 'Updates', value: comp.insight_count },
                            { label: 'High Sev', value: comp.high_severity_count || 0, highlight: (comp.high_severity_count || 0) > 0 }
                        ]}
                    >
                        <div className="tracker-expanded-content">
                            {comp.insight_count > 0 ? (
                                <>
                                    <InsightGroup title="Theme Insights" blocks={comp.insights?.Theme || []} />
                                    <InsightGroup title="Go-to-Market (GTM)" blocks={comp.insights?.GTM || []} />
                                    <InsightGroup title="Positioning" blocks={comp.insights?.Positioning || []} />
                                    <InsightGroup title="Uncategorized" blocks={comp.insights?.Uncategorized || []} />
                                </>
                            ) : (
                                <div className="tracker-empty-box">
                                    <span>No strategic shifts detected for {comp.name} yet.</span>
                                    <p className="text-sm">Run the intelligence pipeline to scan for new updates.</p>
                                </div>
                            )}
                        </div>
                    </TrackerCard>
                ))}
                {competitors.length === 0 && (
                    <div className="p-12 text-center text-gray-400 italic">
                        No competitors are currently being tracked.
                    </div>
                )}
            </div>
        </>
    );
}
