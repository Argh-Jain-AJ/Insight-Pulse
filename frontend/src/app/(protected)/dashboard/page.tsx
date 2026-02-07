'use client';

import React, { useState, useEffect } from 'react';
import ActivityItem from '@/components/ActivityItem';
import InsightCard from '@/components/InsightCard';
import PulseCard from '@/components/PulseCard';
import { fetchDashboardData } from '@/lib/api';
import { Insight } from '@/types';
import RunPipelineButton from '@/components/RunPipelineButton';

function formatTimestamp(isoString: string) {
    const date = new Date(isoString);
    const now = new Date();
    const diff = (now.getTime() - date.getTime()) / 1000 / 60 / 60; // hours
    if (diff < 24) return `${Math.floor(diff)} hours ago`;
    return date.toLocaleDateString();
}

function mapSeverity(sev: string): 'low' | 'medium' | 'high' | 'notable' {
    if (sev === 'critical') return 'high'; // Map critical to high
    if (sev === 'medium') return 'notable'; // Map medium to notable (orange)
    return sev as any;
}

export default function DashboardPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboardData().then(d => {
            setData(d);
            setLoading(false);
        });
    }, []);

    if (loading) {
        return (
            <div className="p-12 text-center">
                <p className="text-gray-500">Loading intelligence dashboard...</p>
            </div>
        );
    }

    const hasData = data && (data.recent_activity.length > 0 || Object.values(data.general_insights).flat().length > 0);

    if (!hasData) {
        return (
            <>
                <header className="top-bar">
                    <div>
                        <h1>Dashboard</h1>
                        <p className="subtitle">Real-time market and competitive intelligence</p>
                    </div>
                    <RunPipelineButton />
                </header>

                <div className="empty-state-container p-12 text-center flex flex-col items-center justify-center min-h-[400px]">
                    <div className="text-6xl mb-4">🔕</div>
                    <h2 className="text-2xl font-semibold text-gray-700">No significant changes in this period.</h2>
                    <p className="text-gray-500 mt-2 max-w-md">
                        Our intelligence agents are monitoring Eli Lilly's landscape.
                        We only surface insights when there is a clear change, escalation, or recurring pattern.
                    </p>
                    <button
                        onClick={() => window.location.reload()}
                        className="mt-6 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                    >
                        Refresh Pipeline Status
                    </button>
                </div>
            </>
        );
    }

    // REAL DATA RENDERING
    return (
        <>
            <header className="top-bar">
                <div>
                    <h1>Dashboard</h1>
                    <p className="subtitle">Real-time Intelligence (Connected to Backend)</p>
                </div>
                <RunPipelineButton />
            </header>

            <div className="content-grid">
                <section className="dashboard-section recent-activity">
                    <h2>Recent Market Activity</h2>
                    <div className="activity-list">
                        {data!.recent_activity.map((ins: any) => (
                            <ActivityItem
                                key={ins.id}
                                severity={mapSeverity(ins.severity)}
                                velocity={ins.velocity === 'increasing' ? 'increasing' : undefined}
                                timestamp={formatTimestamp(ins.created_at)}
                                title={`${ins.scope} Insight`}
                                description={ins.explanation}
                                type={ins.category || ins.scope}
                            />
                        ))}
                        {data!.recent_activity.length === 0 && <p className="p-4 text-gray-500">No recent activity.</p>}
                    </div>
                </section>

                <section className="dashboard-section general-insights">
                    <h2>General Insights</h2>
                    <div className="insights-grid">
                        {/* Theme */}
                        <div className="insight-column">
                            <div className="column-header"><h3>Theme Insights</h3><span className="icon">🌍</span></div>
                            {(data!.general_insights.Theme || []).map((ins: any) => (
                                <InsightCard key={ins.id} title="Theme Shift" description={ins.explanation} severity={mapSeverity(ins.severity)} />
                            ))}
                        </div>

                        {/* GTM */}
                        <div className="insight-column">
                            <div className="column-header"><h3>GTM Insights</h3><span className="icon">🚀</span></div>
                            {(data!.general_insights.GTM || []).map((ins: any) => (
                                <InsightCard key={ins.id} title="GTM Strategy" description={ins.explanation} severity={mapSeverity(ins.severity)} />
                            ))}
                        </div>

                        {/* Positioning */}
                        <div className="insight-column">
                            <div className="column-header"><h3>Positioning Insights</h3><span className="icon">🎯</span></div>
                            {(data!.general_insights.Positioning || []).map((ins: any) => (
                                <InsightCard key={ins.id} title="Positioning" description={ins.explanation} severity={mapSeverity(ins.severity)} />
                            ))}
                        </div>
                    </div>
                </section>

                <section className="dashboard-section rolling-pulse">
                    <h2>Rolling Pulse</h2>
                    <p className="section-desc">Accumulated insights</p>
                    <div className="pulse-grid">
                        {data!.rolling_pulse.map((ins: any) => (
                            <PulseCard
                                key={ins.id}
                                severity={mapSeverity(ins.severity)}
                                velocity={ins.velocity === 'increasing' ? 'increasing' : undefined}
                                timeWindow="Last 7 Days"
                                title={`${ins.scope} Trend`}
                                description={ins.explanation}
                            />
                        ))}
                    </div>
                </section>
            </div>
        </>
    );
}
