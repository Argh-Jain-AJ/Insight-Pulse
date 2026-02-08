'use client';

import React, { useState } from 'react';

const RunPipelineButton = () => {
    const [isLoading, setIsLoading] = useState(false);

    const runPipeline = async () => {
        setIsLoading(true);
        try {
            const res = await fetch('http://127.0.0.1:8000/api/process', { method: 'POST' });
            if (res.ok) {
                // If backend is on, ensure demo mode is off
                localStorage.removeItem('DEMO_MODE');
                window.location.reload();
            } else {
                throw new Error("Backend failed");
            }
        } catch (err) {
            console.error(err);
            const enableDemo = confirm("Error connecting to backend or backend returned an error. Would you like to enable Demo Mode with precomputed data instead?");
            if (enableDemo) {
                localStorage.setItem('DEMO_MODE', 'true');
                window.location.reload();
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <button
            onClick={runPipeline}
            disabled={isLoading}
            className="btn-filter"
            style={{
                backgroundColor: isLoading ? '#ccc' : 'var(--color-primary)',
                color: 'white',
                border: 'none',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
            }}
        >
            {isLoading ? '⚙️ Processing...' : '⚡ Run Pipeline'}
        </button>
    );
};

export default RunPipelineButton;
