import {
  Activity,
  BarChart3,
  Dumbbell,
  Home,
  Settings,
  UploadCloud,
  UserCircle,
} from 'lucide-react';
import { Link } from 'react-router-dom';

const items = [
  ['Dashboard', '/dashboard', Home],
  ['Exercises', '/exercises', Dumbbell],
  ['Form Analysis', '/form-analysis', UploadCloud],
  ['Progress', '/progress', BarChart3],
  ['Profile', '/profile', UserCircle],
  ['Admin Panel', '/admin', Settings],
];

export const Sidebar = () => (
  <aside className="sticky top-[73px] hidden h-[calc(100vh-73px)] w-64 shrink-0 border-r border-slate-200 bg-white p-5 lg:block">
    <div className="mb-6 flex items-center gap-2 text-xl font-black text-brandGreen">
      <Activity />
      Trainova
    </div>

    <nav className="space-y-2">
      {items.map(([label, href, Icon]: any) => (
        <Link
          key={label}
          to={href}
          className="flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-bold text-slate-600 hover:bg-green-50 hover:text-brandGreen"
        >
          <Icon size={18} />
          {label}
        </Link>
      ))}
    </nav>
  </aside>
);