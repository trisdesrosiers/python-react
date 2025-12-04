import React, { useState, useCallback } from 'react';
import '../../styles/index/HomePage.css';
import Footer from '../layout/Footer';
import { useAuth } from '../../contexts/AuthContext';
import { useTableChanges } from '../../hooks/useWebSocket';

const CopyIcon = ({ onClick, copied }) => (
    <svg 
        className={`copy-icon ${copied ? 'copied' : ''}`}
        onClick={onClick}
        width="16" 
        height="16" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        strokeWidth="2"
        strokeLinecap="round" 
        strokeLinejoin="round"
    >
        {copied ? (
            <path d="M20 6L9 17l-5-5" />
        ) : (
            <>
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
            </>
        )}
    </svg>
);

const HomePage = () => {
    const { isLoggedIn, user, loading, updateFirstname } = useAuth();
    const [copiedField, setCopiedField] = useState(null);
    const [firstname, setFirstname] = useState('');
    const [saving, setSaving] = useState(false);
    const [saveMessage, setSaveMessage] = useState('');
    const [realtimeFirstname, setRealtimeFirstname] = useState(null);

    // Listen for real-time profile changes
    const handleProfileChange = useCallback((change) => {
        if (change.operation === 'UPDATE' && change.data?.email === user?.email) {
            setRealtimeFirstname(change.data.firstname);
        }
    }, [user?.email]);

    const { isConnected } = useTableChanges('profiles', handleProfileChange, isLoggedIn);

    React.useEffect(() => {
        if (user?.firstname) {
            setFirstname(user.firstname);
        }
    }, [user?.firstname]);

    // Use realtime firstname if available, otherwise use user firstname
    const displayFirstname = realtimeFirstname || user?.firstname;

    const handleSaveFirstname = async () => {
        if (!firstname.trim()) return;
        setSaving(true);
        setSaveMessage('');
        try {
            await updateFirstname(firstname.trim());
            setSaveMessage('Saved!');
            setTimeout(() => setSaveMessage(''), 2000);
        } catch (error) {
            setSaveMessage('Error saving');
        } finally {
            setSaving(false);
        }
    };

    const handleCopy = (text, field) => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        setCopiedField(field);
        setTimeout(() => setCopiedField(null), 1500);
    };

    if (loading) {
        return (
            <div className="homepage-container">
                <header className="hero-section">
                    <div className="hero-content">
                        <div className="hero-text-content">
                            <h1 className="hero-title">Loading...</h1>
                        </div>
                    </div>
                </header>
                <Footer />
            </div>
        );
    }

    return (
        <div className="homepage-container">
            <header className="hero-section">
                <div className="hero-content">
                    <div className="hero-text-content">
                        {isLoggedIn ? (
                            <>
                                <h1 className="hero-title">
                                    Welcome, {displayFirstname} {user?.lastname}!
                                </h1>
                                <p className="hero-subtitle">
                                    You are successfully logged in to Project1
                                </p>
                                <div className="realtime-status">
                                    <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
                                    <span className="status-text">
                                        {isConnected ? 'Real-time updates active' : 'Connecting...'}
                                    </span>
                                </div>
                                <div className="firstname-edit-box">
                                    <input
                                        type="text"
                                        className="firstname-input"
                                        value={firstname}
                                        onChange={(e) => setFirstname(e.target.value)}
                                        placeholder="First name"
                                    />
                                    <button 
                                        className="firstname-save-btn"
                                        onClick={handleSaveFirstname}
                                        disabled={saving || !firstname.trim()}
                                    >
                                        {saving ? 'Saving...' : 'Save'}
                                    </button>
                                    {saveMessage && <span className="save-message">{saveMessage}</span>}
                                </div>
                            </>
                        ) : (
                            <>
                                <h1 className="hero-title">Hello World</h1>
                                <p className="hero-subtitle">
                                    A modern Python Django + React + PostgreSQL template
                                </p>
                                <div className="demo-credentials-box">
                                    <div className="demo-credentials-content">
                                        <div className="demo-credential">
                                            <span className="credential-key">Email</span>
                                            <code className="credential-value">demo@example.com</code>
                                            <CopyIcon 
                                                onClick={() => handleCopy('demo@example.com', 'email')} 
                                                copied={copiedField === 'email'} 
                                            />
                                        </div>
                                        <div className="demo-credential">
                                            <span className="credential-key">Password</span>
                                            <code className="credential-value">password123</code>
                                            <CopyIcon 
                                                onClick={() => handleCopy('password123', 'password')} 
                                                copied={copiedField === 'password'} 
                                            />
                                        </div>
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </header>
            
            <Footer />
        </div>
    );
};

export default HomePage;
