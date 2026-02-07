'use client';

import React, { useState } from 'react';
import { ChevronDown, ChevronRight } from './Icons';

interface TrackerCardProps {
    title: string;
    subtitle: string; // e.g., "Tier 1" or "Oncology - Phase III"
    stats: {
        label: string;
        value: string | number;
        highlight?: boolean;
    }[];
    children: React.ReactNode; // The expanded content (Insights)
}

const TrackerCard: React.FC<TrackerCardProps> = ({ title, subtitle, stats, children }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <div className={`tracker-card ${isExpanded ? 'active' : ''}`} style={{
            background: 'white',
            border: '1px solid var(--color-border)',
            borderRadius: '8px',
            marginBottom: '1rem',
            overflow: 'hidden',
            transition: 'box-shadow 0.2s'
        }}>
            <div
                className="tracker-header"
                onClick={() => setIsExpanded(!isExpanded)}
                style={{
                    padding: '1.25rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                    userSelect: 'none'
                }}
            >
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ color: 'var(--color-primary)' }}>
                        {isExpanded ? <ChevronDown /> : <ChevronRight />}
                    </div>
                    <div>
                        <h3 style={{ fontSize: '1.1rem', fontWeight: 600, margin: 0, color: 'var(--color-primary-dark)' }}>{title}</h3>
                        <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>{subtitle}</span>
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '2rem' }}>
                    {stats.map((stat, idx) => (
                        <div key={idx} style={{ textAlign: 'right' }}>
                            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-light)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                {stat.label}
                            </div>
                            <div style={{
                                fontSize: '1rem',
                                fontWeight: 600,
                                color: stat.highlight ? '#C62828' : 'var(--color-text-main)'
                            }}>
                                {stat.value}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {isExpanded && (
                <div className="tracker-content" style={{
                    padding: '0 1.25rem 1.25rem 3.5rem', // Indent content
                    borderTop: '1px solid var(--color-border)',
                    backgroundColor: '#FAFAFA'
                }}>
                    <div style={{ paddingTop: '1rem' }}>
                        {children}
                    </div>
                </div>
            )}
        </div>
    );
};

export default TrackerCard;
