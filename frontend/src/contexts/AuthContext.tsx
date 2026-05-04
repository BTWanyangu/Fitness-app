import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import { api } from '../services/api';

type User = { id: number; email: string; full_name: string; first_name?: string; last_name?: string };
type Profile = Record<string, any>;
type AuthContextValue = {
  user: User | null;
  profile: Profile | null;
  isAuthenticated: boolean;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (payload: Record<string, any>) => Promise<void>;
  signOut: () => void;
  refreshMe: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const saveAuth = (payload: any) => {
  localStorage.setItem('trainova_access', payload.access);
  localStorage.setItem('trainova_refresh', payload.refresh);
  localStorage.setItem('trainova_user', JSON.stringify(payload.user));
  localStorage.setItem('trainova_profile', JSON.stringify(payload.profile));
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(() => JSON.parse(localStorage.getItem('trainova_user') || 'null'));
  const [profile, setProfile] = useState<Profile | null>(() => JSON.parse(localStorage.getItem('trainova_profile') || 'null'));
  const [loading, setLoading] = useState(false);

  const applyPayload = (payload: any) => {
    saveAuth(payload);
    setUser(payload.user);
    setProfile(payload.profile);
  };

  const refreshMe = async () => {
    const token = localStorage.getItem('trainova_access');
    if (!token) return;
    const res = await api.get('/auth/me/');
    applyPayload({ ...res.data, access: token, refresh: localStorage.getItem('trainova_refresh') });
  };

  useEffect(() => { void refreshMe().catch(() => {}); }, []);

  const value = useMemo<AuthContextValue>(() => ({
    user,
    profile,
    isAuthenticated: Boolean(user),
    loading,
    signIn: async (email, password) => {
      setLoading(true);
      try { const res = await api.post('/auth/login/', { email, password }); applyPayload(res.data); }
      catch (err: any) { throw new Error(err?.response?.data?.detail || 'Login failed'); }
      finally { setLoading(false); }
    },
    signUp: async (payload) => {
      setLoading(true);
      try { const res = await api.post('/auth/register/', payload); applyPayload(res.data); }
      catch (err: any) {
        const data = err?.response?.data;
        const message = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Registration failed';
        throw new Error(message || 'Registration failed');
      } finally { setLoading(false); }
    },
    signOut: () => {
      localStorage.removeItem('trainova_access'); localStorage.removeItem('trainova_refresh');
      localStorage.removeItem('trainova_user'); localStorage.removeItem('trainova_profile');
      setUser(null); setProfile(null);
    },
    refreshMe,
  }), [user, profile, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
};
