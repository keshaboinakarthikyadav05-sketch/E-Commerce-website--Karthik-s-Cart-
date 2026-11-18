import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { authApi } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  loading: boolean;
  login: (credentials: { email: string; password: string }) => Promise<{ success: boolean; message?: string }>;
  register: (data: any) => Promise<{ success: boolean; message?: string }>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('shopora_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('shopora_token'));
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    if (!localStorage.getItem('shopora_token')) {
      setLoading(false);
      return;
    }
    try {
      const res = await authApi.getMe();
      if (res.data?.success && res.data?.user) {
        setUser(res.data.user);
        localStorage.setItem('shopora_user', JSON.stringify(res.data.user));
      }
    } catch (err) {
      console.warn('Session expired or network error', err);
      setUser(null);
      setToken(null);
      localStorage.removeItem('shopora_token');
      localStorage.removeItem('shopora_user');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (credentials: { email: string; password: string }) => {
    try {
      const res = await authApi.login(credentials);
      if (res.data?.success && res.data?.token) {
        const { token, user } = res.data;
        setToken(token);
        setUser(user);
        localStorage.setItem('shopora_token', token);
        localStorage.setItem('shopora_user', JSON.stringify(user));
        return { success: true };
      }
      return { success: false, message: res.data?.message || 'Login failed' };
    } catch (err: any) {
      const message = err.response?.data?.message || 'Invalid email or password';
      return { success: false, message };
    }
  };

  const register = async (data: any) => {
    try {
      const res = await authApi.register(data);
      if (res.data?.success && res.data?.token) {
        const { token, user } = res.data;
        setToken(token);
        setUser(user);
        localStorage.setItem('shopora_token', token);
        localStorage.setItem('shopora_user', JSON.stringify(user));
        return { success: true };
      }
      return { success: false, message: res.data?.message || 'Registration failed' };
    } catch (err: any) {
      const message = err.response?.data?.message || 'Registration failed. Check details.';
      return { success: false, message };
    }
  };

  const logout = () => {
    try {
      authApi.logout().catch(() => {});
    } finally {
      setUser(null);
      setToken(null);
      localStorage.removeItem('shopora_token');
      localStorage.removeItem('shopora_user');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token && !!user,
        isAdmin: user?.role === 'admin',
        loading,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
