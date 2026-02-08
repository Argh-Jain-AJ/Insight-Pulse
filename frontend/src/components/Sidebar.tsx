'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Sidebar = () => {
    const pathname = usePathname();

    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 2L16 30" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                        <path d="M2 16H30" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                        <circle cx="16" cy="16" r="6" stroke="currentColor" strokeWidth="2" fill="none" />
                    </svg>
                    <span>Insight Pulse</span>
                </div>
            </div>

            <nav className="sidebar-nav">
                <ul>
                    <li>
                        <Link href="/dashboard" className={pathname === '/dashboard' ? 'active' : ''}>
                            <span className="icon">📊</span> Dashboard
                        </Link>
                    </li>
                    <li>
                        <Link href="/competitors" className={pathname === '/competitors' ? 'active' : ''}>
                            <span className="icon">🕵️</span> Competitor Tracker
                        </Link>
                    </li>
                    <li>
                        <Link href="/products" className={pathname === '/products' ? 'active' : ''}>
                            <span className="icon">💊</span> Product Tracker
                        </Link>
                    </li>
                </ul>
            </nav>

            <div className="sidebar-footer">
                <div className="user-profile">
                    <div className="avatar">JD</div>
                    <div className="user-info">
                        <span className="user-name">Lilly Analyst</span>
                        <span className="user-org">Eli Lilly and Company</span>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
