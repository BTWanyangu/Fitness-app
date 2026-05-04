import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { DashboardLayout } from '../components/dashboard/DashboardLayout';

export const AdminPage = () => {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    api.get('/dashboard/').then((r) => setStats(r.data));
  }, []);

  return (
    <DashboardLayout>
      <h1 className="text-4xl font-black">Admin Control Panel</h1>

      <p className="mt-2 text-slate-600">
        Use Django Admin for secure CRUD: exercises, videos, references, users,
        recommendations and form submissions.
      </p>

      <a
        className="mt-6 inline-flex rounded-xl bg-brandGreen px-6 py-4 font-black text-white"
        href="http://localhost:8000/admin/"
        target="_blank"
        rel="noreferrer"
      >
        Open Django Admin
      </a>

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {stats?.stats?.map((s: any) => (
          <div
            key={s.label}
            className="rounded-3xl bg-white p-6 shadow-soft"
          >
            <b>{s.label}</b>

            <div className="mt-3 text-4xl font-black text-brandGreen">
              {s.value}
            </div>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
};