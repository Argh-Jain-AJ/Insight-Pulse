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

function capitalize(s: string) {
    if (!s) return s;
    return s.charAt(0).toUpperCase() + s.slice(1);
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

    // REAL DATA RENDERING
    return (
        <>
            <header className="top-bar">
                <div>
                    <h1>Dashboard</h1>
                    <p className="subtitle">Real-time market and competitive intelligence</p>
                </div>
                <RunPipelineButton />
            </header>

            <div className="content-grid">
                <section className="dashboard-section recent-activity">
                    <h2>Recent Market Activity</h2>
                    <div className="activity-list">
                        {data?.recent_activity?.map((ins: any) => (
                            <ActivityItem
                                key={ins.id}
                                severity={mapSeverity(ins.severity)}
                                velocity={ins.velocity === 'increasing' ? 'increasing' : undefined}
                                timestamp={formatTimestamp(ins.created_at)}
                                title={`${capitalize(ins.scope)} Insight`}
                                description={ins.explanation}
                                type={capitalize(ins.category || ins.scope)}
                            />
                        ))}
                        {(!data?.recent_activity || data.recent_activity.length === 0) && (
                            <div className="empty-container-subtle animate-pulse-soft">
                                <div className="empty-skeleton animate-shimmer w-full" />
                                <div className="empty-skeleton animate-shimmer w-3/4 self-start" />
                                <p className="empty-feedback-subtle">No changes detected. Activity will appear here after the next pipeline run.</p>
                            </div>
                        )}
                    </div>
                </section>

                <section className="dashboard-section general-insights">
                    <h2>General Insights</h2>
                    <div className="insights-grid">
                        {/* Theme */}
                        <div className="insight-column">
                            <div className="column-header"><h3>Theme Insights</h3><span className="icon">🌍</span></div>
                            {(data?.general_insights?.Theme || []).map((ins: any) => (
                                <InsightCard key={ins.id} title="Theme Shift" description={ins.explanation} severity={mapSeverity(ins.severity)} />
                            ))}
                            {(!data?.general_insights?.Theme || data.general_insights.Theme.length === 0) && (
                                <div className="p-4 border border-dashed border-gray-100 rounded-lg opacity-50">
                                    <div className="empty-skeleton-text animate-shimmer w-full" />
                                    <div className="empty-skeleton-text animate-shimmer w-2/3" />
                                </div>
                            )}
                        </div>

                        {/* GTM */}
                        <div className="insight-column">
                            <div className="column-header"><h3>GTM Insights</h3><span className="icon">🚀</span></div>
                            {(data?.general_insights?.GTM || []).map((ins: any) => (
                                <InsightCard key={ins.id} title="GTM Strategy" description={ins.explanation} severity={mapSeverity(ins.severity)} />
                            ))}
                            {(!data?.general_insights?.GTM || data.general_insights.GTM.length === 0) && (
                                <div className="p-4 border border-dashed border-gray-100 rounded-lg opacity-50">
                                    <div className="empty-skeleton-text animate-shimmer w-full" />
                                    <div className="empty-skeleton-text animate-shimmer w-2/3" />
                                </div>
                            )}
                        </div>

                        {/* Positioning */}
                        <div className="insight-column">
                            <div className="column-header"><h3>Positioning Insights</h3><span className="icon">🎯</span></div>
                            {(data?.general_insights?.Positioning || []).map((ins: any) => (
                                <InsightCard key={ins.id} title="Positioning" description={ins.explanation} severity={mapSeverity(ins.severity)} />
                            ))}
                            {(!data?.general_insights?.Positioning || data.general_insights.Positioning.length === 0) && (
                                <div className="p-4 border border-dashed border-gray-100 rounded-lg opacity-50">
                                    <div className="empty-skeleton-text animate-shimmer w-full" />
                                    <div className="empty-skeleton-text animate-shimmer w-2/3" />
                                </div>
                            )}
                        </div>
                    </div>
                    {(!data?.general_insights || Object.values(data.general_insights).flat().length === 0) && (
                        <p className="empty-feedback-subtle mt-2">Intelligence agents are monitoring for strategic shifts.</p>
                    )}
                </section>

                <section className="dashboard-section rolling-pulse">
                    <h2>Rolling Pulse</h2>
                    <p className="section-desc">Accumulated insights</p>
                    <div className="pulse-grid">
                        {data?.rolling_pulse?.map((ins: any) => (
                            <PulseCard
                                key={ins.id}
                                severity={mapSeverity(ins.severity)}
                                velocity={ins.velocity === 'increasing' ? 'increasing' : undefined}
                                timeWindow="Last 7 Days"
                                title={`${capitalize(ins.scope)} Trend`}
                                description={ins.explanation}
                            />
                        ))}
                    </div>
                    {(!data?.rolling_pulse || data.rolling_pulse.length === 0) && (
                        <div className="empty-container-subtle py-12">
                            <div className="flex gap-4 w-full justify-center">
                                <div className="empty-skeleton animate-shimmer w-64" />
                                <div className="empty-skeleton animate-shimmer w-64" />
                            </div>
                            <p className="empty-feedback-subtle">Patterns will normalize as more data is processed.</p>
                        </div>
                    )}
                </section>
            </div>
        </>
    );
}
