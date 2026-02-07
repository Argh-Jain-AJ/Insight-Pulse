import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

export default function Login() {
  return (
    <div className="split-layout">
      {/* Left Section: Product Overview */}
      <div className="product-section">
        <header>
          <div className="logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 2L16 30" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              <path d="M2 16H30" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              <circle cx="16" cy="16" r="6" stroke="currentColor" strokeWidth="2" fill="none" />
              <path d="M24 8L8 24" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="2 4" />
              <path d="M8 8L24 24" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="2 4" />
            </svg>
            <span>Insight Pulse</span>
          </div>
        </header>

        <main className="product-content">
          <h1>Always-On Market Intelligence for Pharma Decision-Making</h1>

          <p className="hero-description">
            Empowering strategic and operational decisions with continuous monitoring of the pharmaceutical landscape. We deliver synthesized insights, not just raw data, to keep you ahead of the curve.
          </p>

          <div className="feature-list">
            <h2>What Insight Pulse Is Used For</h2>
            <ul>
              <li>
                <span className="icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" xmlns="http://www.w3.org/2000/svg"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                </span>
                Tracking market and competitor activity in real-time
              </li>
              <li>
                <span className="icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" xmlns="http://www.w3.org/2000/svg"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                </span>
                Monitoring product and adjacent therapeutic area changes
              </li>
              <li>
                <span className="icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" xmlns="http://www.w3.org/2000/svg"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
                </span>
                Understanding GTM, positioning, and thematic shifts
              </li>
              <li>
                <span className="icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>
                </span>
                Supporting informed decision-making with context
              </li>
            </ul>
          </div>
        </main>

        <footer>
          <p>&copy; 2026 Insight Pulse Intelligence. All rights reserved.</p>
        </footer>
      </div>

      {/* Right Section: Login Panel */}
      <div className="login-section">
        <div className="login-card">
          <div className="login-header">
            <h2>Access Insight Pulse</h2>
            <p>Available exclusively to partner organizations</p>
          </div>

          <form className="login-form" action="/dashboard"> {/* Mock action for now */}
            <div className="form-group">
              <label htmlFor="email">Email or Username</label>
              <input type="text" id="email" name="email" required placeholder="name@company.com" autoComplete="username" />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="password" id="password" name="password" required placeholder="••••••••" autoComplete="current-password" />
            </div>

            <div className="form-actions">
              <label className="checkbox-container">
                <input type="checkbox" name="remember" />
                <span className="checkmark"></span>
                Remember me
              </label>
              <Link href="#" className="forgot-password">Forgot password?</Link>
            </div>

            <button type="submit" className="btn-primary">Sign In</button>

            <div className="access-note">
              <p>Access is provisioned by your organization.</p>
              <Link href="#" className="secondary-link">Request access or contact support</Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
