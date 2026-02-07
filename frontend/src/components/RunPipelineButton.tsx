'use client';

import React, { useState } from 'react';

const RunPipelineButton = () => {
    const [isLoading, setIsLoading] = useState(false);

    const runPipeline = async () => {
        setIsLoading(true);
        try {
            const res = await fetch('http://127.0.0.1:8000/api/process', { method: 'POST' });
            if (res.ok) {
                window.location.reload();
            } else {
                alert("Failed to run pipeline");
            }
        } catch (err) {
            console.error(err);
            alert("Error connecting to backend");
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
