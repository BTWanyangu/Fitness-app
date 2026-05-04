import { FormEvent, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { DashboardLayout } from '../components/dashboard/DashboardLayout';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import { Button } from '../components/ui/Button';

const numericFields = ['age', 'height_cm', 'weight_kg', 'target_weight_kg', 'weekly_target'];

export const ProfilePage = () => {
  const { profile, refreshMe, user, isAuthenticated } = useAuth();
  const [form, setForm] = useState<any>({});
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    setForm({ ...(profile || {}) });
  }, [profile]);

  const update = (key: string, value: any) => setForm((prev: any) => ({ ...prev, [key]: value }));

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      await api.patch('/auth/me/', form);
      await refreshMe();
      setMessage('Profile updated successfully.');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Could not update profile. Please sign in and try again.');
    }
  };

  return (
    <DashboardLayout>
      <h1 className="text-4xl font-black">Profile & Fitness Details</h1>
      <p className="mt-2 text-slate-600">These details help Trainova personalize progress and coaching recommendations.</p>

      {!isAuthenticated ? (
        <div className="mt-8 rounded-3xl bg-white p-6 shadow-soft">
          <h2 className="text-2xl font-black">Create an account to manage your profile</h2>
          <p className="mt-2 text-slate-600">Public pages are browsable, but your personal profile and saved metrics need an account.</p>
          <Link to="/auth" className="mt-5 inline-flex rounded-xl bg-brandGreen px-6 py-4 font-black text-white">Sign in or create account</Link>
        </div>
      ) : (
        <form onSubmit={submit} className="mt-8 grid gap-5 rounded-3xl bg-white p-6 shadow-soft md:grid-cols-2">
          <div className="rounded-2xl bg-green-50 p-4 md:col-span-2">
            <b>{user?.full_name}</b>
            <p className="text-sm text-slate-600">{user?.email}</p>
          </div>

          {[
            ['phone', 'Phone'], ['location', 'Location'], ['age', 'Age'], ['gender', 'Gender'],
            ['height_cm', 'Height cm'], ['weight_kg', 'Weight kg'], ['target_weight_kg', 'Target weight kg'],
            ['weekly_target', 'Weekly sessions target'], ['available_equipment', 'Available equipment'],
          ].map(([key, label]) => (
            <label key={key} className="grid gap-2 text-sm font-bold text-slate-600">
              {label}
              <input
                className="rounded-2xl border p-4 font-normal"
                value={form?.[key] ?? ''}
                onChange={(e) => update(key, numericFields.includes(key) ? Number(e.target.value) : e.target.value)}
              />
            </label>
          ))}

          <label className="grid gap-2 text-sm font-bold text-slate-600">
            Goal
            <select className="rounded-2xl border p-4 font-normal" value={form?.goal ?? ''} onChange={(e) => update('goal', e.target.value)}>
              <option value="general_fitness">General fitness</option>
              <option value="fat_loss">Fat loss</option>
              <option value="muscle_gain">Muscle gain</option>
              <option value="strength">Strength</option>
              <option value="endurance">Endurance</option>
              <option value="rehab">Rehabilitation</option>
            </select>
          </label>

          <label className="grid gap-2 text-sm font-bold text-slate-600">
            Training level
            <select className="rounded-2xl border p-4 font-normal" value={form?.training_level ?? ''} onChange={(e) => update('training_level', e.target.value)}>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </label>

          <label className="grid gap-2 text-sm font-bold text-slate-600 md:col-span-2">
            Injury notes
            <textarea className="min-h-28 rounded-2xl border p-4 font-normal" value={form?.injury_notes ?? ''} onChange={(e) => update('injury_notes', e.target.value)} />
          </label>

          {message && <p className="font-bold text-brandGreen">{message}</p>}
          {error && <p className="font-bold text-red-600">{error}</p>}

          <div className="md:col-span-2">
            <Button className="rounded-xl">Save Profile</Button>
          </div>
        </form>
      )}
    </DashboardLayout>
  );
};
