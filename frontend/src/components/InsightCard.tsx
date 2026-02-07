import React from 'react';

interface InsightCardProps {
    title: string;
    description: string;
    severity: 'low' | 'medium' | 'high' | 'notable';
}

const InsightCard: React.FC<InsightCardProps> = ({ title, description, severity }) => {
    return (
        <div className="card insight-card">
            <h4>{title}</h4>
            <p>{description}</p>
            <div className="card-meta">
                <span className={`tag severity-${severity}`}>{severity}</span>
            </div>
        </div>
    );
};

export default InsightCard;
