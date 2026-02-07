import React from 'react';

interface ActivityItemProps {
    severity: 'low' | 'medium' | 'high' | 'notable'; // 'notable' from CSS
    velocity?: 'new' | 'increasing' | 'stable' | 'decreasing';
    timestamp: string;
    title: string;
    description: string;
    type: string;
}

const ActivityItem: React.FC<ActivityItemProps> = ({ severity, velocity, timestamp, title, description, type }) => {
    return (
        <div className="activity-item">
            <div className="activity-meta">
                <span className={`tag severity-${severity}`}>{severity}</span>
                {velocity && <span className={`tag velocity-${velocity}`}>{velocity}</span>}
                <span className="timestamp">{timestamp}</span>
            </div>
            <div className="activity-content">
                <h3>{title}</h3>
                <p>{description}</p>
                <span className="activity-type">{type}</span>
            </div>
        </div>
    );
};

export default ActivityItem;
