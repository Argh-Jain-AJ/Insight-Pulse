import React from 'react';
import { ContextBlock } from '@/types';

interface InsightGroupProps {
    title: string;
    blocks: ContextBlock[];
}

const InsightGroup: React.FC<InsightGroupProps> = ({ title, blocks }) => {
    if (blocks.length === 0) return null;

    return (
        <div style={{ marginBottom: '1.5rem' }}>
            <h4 style={{
                fontSize: '0.9rem',
                fontWeight: 600,
                color: 'var(--color-text-muted)',
                marginBottom: '0.75rem',
                borderBottom: '1px solid #eee',
                paddingBottom: '4px'
            }}>
                {title}
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {blocks.map((block) => (
                    <div key={block.insight.id} style={{
                        background: 'white',
                        padding: '1rem',
                        borderRadius: '6px',
                        border: '1px solid #eee',
                        borderLeft: `3px solid ${block.insight.severity === 'high' ? '#C62828' :
                            block.insight.severity === 'medium' ? '#EF6C00' : '#2E7D32'
                            }`
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                            <span style={{
                                fontSize: '0.75rem',
                                fontWeight: 600,
                                background: '#f5f5f5',
                                padding: '2px 6px',
                                borderRadius: '4px'
                            }}>
                                {block.insight.category || 'General'}
                            </span>
                            <span style={{ fontSize: '0.75rem', color: '#888' }}>
                                {block.insight.velocity}
                            </span>
                        </div>
                        <p style={{ fontSize: '0.95rem', color: '#333', margin: '0 0 0.5rem 0' }}>
                            {block.insight.explanation}
                        </p>
                        <div style={{
                            fontSize: '0.85rem',
                            color: 'var(--color-primary)',
                            fontStyle: 'italic',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px'
                        }}>
                            <span style={{ fontWeight: 600 }}>Context:</span> {block.context_framing}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default InsightGroup;
