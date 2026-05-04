import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/Button';

export const AuthPanel = () => {
  const navigate = useNavigate();
  const { signIn, signUp, loading } = useAuth();
  const [mode, setMode] = useState<'signin' | 'signup'>('signin');
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    full_name: 'Alex Mwangi', email: 'alex@example.com', password: 'password12345',
    phone: '+254700000000', location: 'Nairobi', age: 28, gender: 'Male',
    height_cm: 178, weight_kg: 75, target_weight_kg: 80, goal: 'strength',
    training_level: 'intermediate', weekly_target: 4,
  });
  const update = (key: string, value: any) => setForm(prev => ({ ...prev, [key]: value }));
  const submit = async (e: FormEvent) => {
    e.preventDefault(); setError('');
    try {
      if (mode === 'signin') await signIn(form.email, form.password);
      else await signUp(form);
      navigate('/dashboard');
    } catch (err: any) { setError(err.message); }
  };
  return <div className="grid min-h-[calc(100vh-74px)] bg-[#f7faf7] lg:grid-cols-[1fr_520px]">
    <section className="hidden items-center bg-[linear-gradient(90deg,rgba(6,93,20,.88),rgba(6,93,20,.45)),url('https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1800&auto=format&fit=crop')] bg-cover bg-center px-12 text-white lg:flex">
      <div className="max-w-2xl"><p className="font-black uppercase tracking-[.25em] text-brandOrange">Trainova account</p><h1 className="mt-4 text-6xl font-black leading-tight">Your fitness profile powers smarter coaching.</h1><div className="mt-8 grid gap-4 text-lg"><p className="flex gap-3"><CheckCircle2 className="text-brandOrange"/> Track body metrics, sleep, readiness and sessions.</p><p className="flex gap-3"><CheckCircle2 className="text-brandOrange"/> Compare technique with approved exercise references.</p><p className="flex gap-3"><CheckCircle2 className="text-brandOrange"/> Keep your progress attached to your account.</p></div></div>
    </section>
    <section className="flex items-center justify-center px-5 py-10"><form onSubmit={submit} className="w-full max-w-xl rounded-[2rem] bg-white p-6 shadow-soft md:p-8"><div className="mb-6 flex items-center gap-3"><span className="flex h-12 w-12 items-center justify-center rounded-full bg-brandGreen text-white"><Activity/></span><div><h2 className="text-3xl font-black">{mode==='signin'?'Welcome back':'Create account'}</h2><p className="text-slate-600">{mode==='signin'?'Sign in to continue.':'Set up your training profile.'}</p></div></div>
      {mode === 'signup' && <div className="grid gap-4 md:grid-cols-2"><input className="rounded-2xl border p-4 md:col-span-2" value={form.full_name} onChange={e=>update('full_name',e.target.value)} placeholder="Full name"/><input className="rounded-2xl border p-4" value={form.phone} onChange={e=>update('phone',e.target.value)} placeholder="Phone"/><input className="rounded-2xl border p-4" value={form.location} onChange={e=>update('location',e.target.value)} placeholder="Location"/><input className="rounded-2xl border p-4" type="number" value={form.age} onChange={e=>update('age',Number(e.target.value))} placeholder="Age"/><input className="rounded-2xl border p-4" value={form.gender} onChange={e=>update('gender',e.target.value)} placeholder="Gender"/><input className="rounded-2xl border p-4" type="number" value={form.height_cm} onChange={e=>update('height_cm',Number(e.target.value))} placeholder="Height cm"/><input className="rounded-2xl border p-4" type="number" value={form.weight_kg} onChange={e=>update('weight_kg',Number(e.target.value))} placeholder="Weight kg"/><select className="rounded-2xl border p-4" value={form.goal} onChange={e=>update('goal',e.target.value)}><option value="general_fitness">General fitness</option><option value="fat_loss">Fat loss</option><option value="muscle_gain">Muscle gain</option><option value="strength">Strength</option><option value="endurance">Endurance</option></select><select className="rounded-2xl border p-4" value={form.training_level} onChange={e=>update('training_level',e.target.value)}><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></div>}
      <div className="mt-4 grid gap-4"><input type="email" className="rounded-2xl border p-4" value={form.email} onChange={e=>update('email',e.target.value)} placeholder="Email"/><input type="password" className="rounded-2xl border p-4" value={form.password} onChange={e=>update('password',e.target.value)} placeholder="Password"/></div>{error&&<div className="mt-4 rounded-2xl bg-red-50 p-4 text-sm font-bold text-red-700">{error}</div>}<Button className="mt-5 w-full rounded-xl" disabled={loading}>{loading?'Please wait...':mode==='signin'?'Sign In':'Create Account'} <ArrowRight size={18}/></Button><p className="mt-5 text-center text-sm text-slate-600">{mode==='signin'?"Don't have an account?":"Already have an account?"} <button type="button" onClick={()=>{setMode(mode==='signin'?'signup':'signin'); setError('')}} className="font-black text-brandGreen">{mode==='signin'?'Sign up':'Sign in'}</button></p></form></section>
  </div>;
};
