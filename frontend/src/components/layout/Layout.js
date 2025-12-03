import React from 'react';
import { Link } from 'react-router-dom';
import { Layout as AntLayout, Button } from 'antd';
import { useAuth } from '../../contexts/AuthContext';
import '../../styles/layout/Layout.css';

const { Header } = AntLayout;

const Layout = ({ children }) => {
    const { isLoggedIn, logout, user } = useAuth();

    const handleLogout = async () => {
        await logout();
    };

    return (
        <AntLayout className="layout-container">
            <Header className="header">
                <Link to="/" className="logo-container">
                    <span className="logo-text">Project1</span>
                </Link>
                
                <nav className="nav">
                    {isLoggedIn ? (
                        <>
                            <span className="user-greeting">Hello, {user?.firstname}!</span>
                            <Button onClick={handleLogout} type="default">
                                Logout
                            </Button>
                        </>
                    ) : (
                        <>
                            <Link to="/login">
                                <Button type="default">Login</Button>
                            </Link>
                            <Link to="/register">
                                <Button type="primary">Register</Button>
                            </Link>
                        </>
                    )}
                </nav>
            </Header>
            <main className="main-content">
                {children}
            </main>
        </AntLayout>
    );
};

export default Layout;
