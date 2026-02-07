import React from 'react';

interface PulseCardProps {
    severity: 'low' | 'medium' | 'high' | 'notable';
    velocity?: 'new' | 'increasing' | 'stable' | 'decreasing';
    timeWindow: string;
    title: string;
    description: string;
}

const PulseCard: React.FC<PulseCardProps> = ({ severity, velocity, timeWindow, title, description }) => {
    return (
        <div className="card pulse-card">
            <div className="card-header">
                <span className={`tag severity-${severity}`}>{severity}</span>
                {velocity && <span className={`tag velocity-${velocity}`}>{velocity}</span>}
                <span className="time-window">{timeWindow}</span>
            </div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    );
};

export default PulseCard;
