'use client';

import React, { useEffect, useState } from 'react';
import Sidebar from '@/components/Sidebar';

export default function ProtectedLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const [isDemo, setIsDemo] = useState(false);

    useEffect(() => {
        setIsDemo(localStorage.getItem('DEMO_MODE') === 'true');
    }, []);

    const exitDemo = () => {
        localStorage.removeItem('DEMO_MODE');
        window.location.reload();
    };

    return (
        <div className="dashboard-layout">
            <Sidebar />
            <main className="main-content">
                {isDemo && (
                    <div style={{
                        backgroundColor: 'rgba(255, 165, 0, 0.1)',
                        border: '1px solid orange',
                        padding: '10px 20px',
                        marginBottom: '20px',
                        borderRadius: '8px',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        color: 'orange',
                        fontWeight: 'bold'
                    }}>
                        <span>⚠️ Demo Mode Active: Showing precomputed static data</span>
                        <button
                            onClick={exitDemo}
                            className="btn-filter"
                            style={{ padding: '4px 12px', fontSize: '13px' }}
                        >
                            Exit Demo Mode
                        </button>
                    </div>
                )}
                {children}
            </main>
        </div>
    );
}
