import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const response = await axios.get('/api/check-auth/', {
                withCredentials: true
            });
            if (response.data.isAuthenticated) {
                setUser(response.data.user);
                setIsLoggedIn(true);
            }
        } catch (error) {
            console.error('Auth check failed:', error);
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        const response = await axios.post('/api/login/', {
            email,
            password
        }, {
            withCredentials: true
        });
        
        if (response.data.success) {
            setUser(response.data.user);
            setIsLoggedIn(true);
        }
        return response.data;
    };

    const logout = async () => {
        try {
            await axios.post('/api/logout/', {}, {
                withCredentials: true
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            setUser(null);
            setIsLoggedIn(false);
        }
    };

    const register = async (email, firstname, lastname) => {
        const response = await axios.post('/api/register/', {
            email,
            firstname,
            lastname
        }, {
            withCredentials: true
        });
        return response.data;
    };

    const updateFirstname = async (firstname) => {
        const response = await axios.post('/api/profile/update/', {
            firstname
        }, {
            withCredentials: true
        });
        return response.data;
    };

    return (
        <AuthContext.Provider value={{ user, isLoggedIn, loading, login, logout, register, updateFirstname }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

