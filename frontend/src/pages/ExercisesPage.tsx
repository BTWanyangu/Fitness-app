import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { DashboardLayout } from '../components/dashboard/DashboardLayout';

export const ExercisesPage = () => {
  const [items, setItems] = useState<any[]>([]);
  const [q, setQ] = useState('');

  useEffect(() => {
    api
      .get('/exercises/', { params: { search: q } })
      .then((r) => setItems(r.data.results || r.data));
  }, [q]);

  return (
    <DashboardLayout>
      <h1 className="text-4xl font-black">Exercise Library</h1>

      <input
        className="mt-6 w-full rounded-2xl border p-4"
        placeholder="Search by name, body part or equipment"
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />

      <div className="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {items.map((e) => (
          <div
            key={e.id}
            className="overflow-hidden rounded-3xl bg-white shadow-soft"
          >
            <img
              className="h-56 w-full object-cover"
              src={
                e.image_url ||
                'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1000&auto=format&fit=crop'
              }
            />

            <div className="p-5">
              <h3 className="text-xl font-black">{e.name}</h3>

              <p className="mt-2 text-slate-600">
                {e.body_part} • {e.equipment}
              </p>

              <span className="mt-4 inline-block rounded-full bg-green-50 px-4 py-2 text-sm font-bold text-brandGreen">
                {e.difficulty}
              </span>
            </div>
          </div>
        ))}
      </div>
    </DashboardLayout>
  );
};