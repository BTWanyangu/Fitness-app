export const StatGrid = ({ stats }: { stats: any[] }) => (
  <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
    {stats.map((s) => (
      <div
        key={s.label}
        className="rounded-3xl border border-slate-100 bg-white p-6 shadow-soft"
      >
        <p className="text-sm font-bold text-slate-500">
          {s.label}
        </p>

        <h3 className="mt-3 text-4xl font-black text-brandGreen">
          {s.value}
        </h3>

        <p className="mt-2 text-sm text-slate-500">
          {s.helper}
        </p>
      </div>
    ))}
  </div>
);