import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { DashboardLayout } from '../components/dashboard/DashboardLayout';
import { StatGrid } from '../components/dashboard/StatGrid';
import { Button } from '../components/ui/Button';

export const DashboardPage = () => {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    api.get('/dashboard/').then((r) => setData(r.data));
  }, []);

  return (
    <DashboardLayout>
      <div className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="font-black uppercase tracking-[.2em] text-brandOrange">
            Dashboard
          </p>

          <h1 className="mt-2 text-4xl font-black">
            Welcome back
            {data?.user?.full_name
              ? `, ${data.user.full_name.split(' ')[0]}`
              : ''}{' '}
            👋
          </h1>

          <p className="mt-2 text-slate-600">
            Your free training workspace is ready.
          </p>
        </div>

        <a href="/form-analysis">
          <Button className="rounded-xl">Upload Form</Button>
        </a>
      </div>

      <StatGrid stats={data?.stats || []} />

      <div className="mt-8 grid gap-6 xl:grid-cols-[1.3fr_.8fr]">
        {/* Featured Workout */}
        <div className="rounded-3xl bg-white p-6 shadow-soft">
          <h2 className="text-2xl font-black">Featured Workout</h2>

          <p className="text-slate-600">
            {data?.todayWorkout?.description}
          </p>

          <div className="mt-5 space-y-3">
            {data?.todayWorkout?.items?.map((it: any) => (
              <div
                key={it.id}
                className="flex items-center justify-between rounded-2xl bg-green-50 p-4"
              >
                <div>
                  <b>{it.exercise_detail.name}</b>
                  <p className="text-sm text-slate-500">
                    {it.exercise_detail.target_muscle}
                  </p>
                </div>

                <span className="font-black text-brandGreen">
                  {it.sets} x {it.reps}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Coach Preview */}
        <div className="rounded-3xl bg-white p-6 shadow-soft">
          <h2 className="text-2xl font-black">Coach Preview</h2>

          <div className="mt-5 space-y-4">
            {data?.recommendations?.map((r: any) => (
              <div key={r.id} className="rounded-2xl border p-4">
                <b>{r.title}</b>
                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {r.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};