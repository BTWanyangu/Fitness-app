import { Activity, LogOut, Menu, UserCircle, X } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../ui/Button';
import { useAuth } from '../../contexts/AuthContext';

const links = [
  ['Home', '/#home'],
  ['Features', '/#services'],
  ['How It Works', '/#how'],
  ['Exercises', '/exercises'],
  ['Progress', '/progress'],
  ['Form Analysis', '/form-analysis'],
];

export const Header = () => {
  const { isAuthenticated, user, signOut } = useAuth();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-white/20 bg-white/90 shadow-sm backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-6">
        <Link to="/" className="flex items-center gap-2" onClick={() => setOpen(false)}>
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-brandGreen text-white"><Activity size={20} /></span>
          <span className="text-2xl font-black text-brandGreen">Trainova</span>
        </Link>

        <nav className="hidden gap-7 text-sm font-semibold text-slate-700 lg:flex">
          {links.map(([label, href]) => <a key={label} href={href} className="hover:text-brandGreen">{label}</a>)}
        </nav>

        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <Link to="/profile" className="hidden items-center gap-2 text-sm font-bold text-slate-700 md:flex"><UserCircle size={20} />{user?.first_name || 'Profile'}</Link>
              <button onClick={signOut} className="hidden items-center gap-2 rounded-lg bg-slate-100 px-4 py-3 text-sm font-black text-slate-700 md:inline-flex"><LogOut size={16} /> Sign out</button>
            </>
          ) : (
            <Link to="/auth" className="hidden md:block"><Button className="rounded-lg px-5 py-3">Get Started</Button></Link>
          )}
          <button className="rounded-xl bg-slate-100 p-3 lg:hidden" onClick={() => setOpen((value) => !value)} aria-label="Toggle navigation">
            {open ? <X /> : <Menu />}
          </button>
        </div>
      </div>

      {open && (
        <div className="border-t bg-white px-4 py-4 lg:hidden">
          <nav className="grid gap-2 text-sm font-bold text-slate-700">
            {links.map(([label, href]) => <a key={label} href={href} onClick={() => setOpen(false)} className="rounded-xl px-4 py-3 hover:bg-green-50 hover:text-brandGreen">{label}</a>)}
            <Link to="/dashboard" onClick={() => setOpen(false)} className="rounded-xl px-4 py-3 hover:bg-green-50 hover:text-brandGreen">Dashboard</Link>
            <Link to="/admin" onClick={() => setOpen(false)} className="rounded-xl px-4 py-3 hover:bg-green-50 hover:text-brandGreen">Admin Panel</Link>
            {isAuthenticated ? (
              <button onClick={() => { signOut(); setOpen(false); }} className="rounded-xl px-4 py-3 text-left text-red-600 hover:bg-red-50">Sign out</button>
            ) : (
              <Link to="/auth" onClick={() => setOpen(false)} className="rounded-xl bg-brandGreen px-4 py-3 text-center text-white">Get Started</Link>
            )}
          </nav>
        </div>
      )}
    </header>
  );
};
