import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/layout/Footer.css';

const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-sections">
                    <div className="footer-section">
                        <h4>Support</h4>
                        <Link to="/help">Help Center</Link>
                        <Link to="/terms">Terms of Service</Link>
                    </div>
                    <div className="footer-section">
                        <h4>Contact</h4>
                        <a href="mailto:contact@example.com">contact@example.com</a>
                    </div>
                </div>
                <div className="footer-bottom">
                    <p>© {currentYear} Project1. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
