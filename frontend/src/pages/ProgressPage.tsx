import { FormEvent, useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';

import { api } from '../services/api';
import { DashboardLayout } from '../components/dashboard/DashboardLayout';
import { Button } from '../components/ui/Button';
import { useAuth } from '../contexts/AuthContext';

const metrics = [
  ['weight', 'Body weight', 'kg'],
  ['body_fat', 'Body fat', '%'],
  ['waist', 'Waist', 'cm'],
  ['sleep', 'Sleep', 'hrs'],
  ['steps', 'Steps', 'steps'],
  ['protein', 'Protein', 'g'],
  ['readiness', 'Readiness', '%'],
];

export const ProgressPage = () => {
  const { isAuthenticated } = useAuth();

  const [data, setData] = useState<any[]>([]);

  const [form, setForm] = useState({
    metric: 'weight',
    value: '',
    unit: 'kg',
    recorded_at: new Date().toISOString().slice(0, 10),
    notes: '',
  });

  const load = () =>
    api.get('/progress/').then((r) =>
      setData(r.data.results || r.data)
    );

  useEffect(() => {
    load();
  }, []);

  const submit = async (e: FormEvent) => {
    e.preventDefault();

    await api.post('/progress/', {
      ...form,
      value: Number(form.value),
    });

    setForm({ ...form, value: '', notes: '' });
    load();
  };

  return (
    <DashboardLayout>
      <div className="flex flex-wrap items-end justify-between gap-5">
        <div>
          <h1 className="text-4xl font-black">Progress</h1>

          <p className="mt-2 max-w-3xl text-slate-600">
            Track globally standard fitness metrics: body composition, sleep,
            readiness, nutrition, steps and training load.
          </p>
        </div>

        {!isAuthenticated && (
          <a href="/auth" className="font-bold text-brandGreen">
            Create an account to save your progress →
          </a>
        )}
      </div>

      <div className="mt-8 grid gap-6 xl:grid-cols-[1.2fr_.8fr]">
        {/* Chart */}
        <div className="rounded-3xl bg-white p-6 shadow-soft">
          <ResponsiveContainer width="100%" height={360}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="recorded_at" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Form */}
        <form
          onSubmit={submit}
          className="rounded-3xl bg-white p-6 shadow-soft"
        >
          <h2 className="text-2xl font-black">Log a metric</h2>

          <select
            className="mt-5 w-full rounded-2xl border p-4"
            value={form.metric}
            onChange={(e) => {
              const m = metrics.find((x) => x[0] === e.target.value);

              setForm({
                ...form,
                metric: e.target.value,
                unit: m?.[2] || '',
              });
            }}
          >
            {metrics.map(([k, label]) => (
              <option key={k} value={k}>
                {label}
              </option>
            ))}
          </select>

          <input
            className="mt-4 w-full rounded-2xl border p-4"
            placeholder="Value"
            value={form.value}
            onChange={(e) =>
              setForm({ ...form, value: e.target.value })
            }
          />

          <input
            className="mt-4 w-full rounded-2xl border p-4"
            type="date"
            value={form.recorded_at}
            onChange={(e) =>
              setForm({ ...form, recorded_at: e.target.value })
            }
          />

          <textarea
            className="mt-4 w-full rounded-2xl border p-4"
            placeholder="Optional notes"
            value={form.notes}
            onChange={(e) =>
              setForm({ ...form, notes: e.target.value })
            }
          />

          <Button className="mt-5 rounded-xl" disabled={!isAuthenticated}>
            Save Progress
          </Button>

          {!isAuthenticated && (
            <p className="mt-3 text-sm text-slate-500">
              Sign in first so this entry belongs to your account.
            </p>
          )}
        </form>
      </div>
    </DashboardLayout>
  );
};