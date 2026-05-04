import { ArrowUpRight } from 'lucide-react';
import { Button } from '../ui/Button';

export const Hero = () => (
  <section
    id="home"
    className="relative overflow-hidden bg-[linear-gradient(90deg,rgba(6,55,11,.90),rgba(6,55,11,.56)),url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1800&auto=format&fit=crop')] bg-cover bg-center"
  >
    <div className="mx-auto grid min-h-[680px] max-w-7xl items-center px-6 py-24 lg:grid-cols-[1.05fr_.95fr]">
      
      {/* Left Content */}
      <div className="max-w-2xl text-white">
        <p className="font-black uppercase tracking-[.25em] text-brandOrange">
          Kenya-ready fitness companion
        </p>

        <h1 className="mt-5 text-5xl font-black leading-tight md:text-7xl">
          Train Smarter. Recover Better.
        </h1>

        <p className="mt-6 text-xl leading-9 text-white/85">
          Plan workouts, manage exercises, upload reference media, and compare
          user form using AI-assisted scoring in one free platform.
        </p>

        <div className="mt-9 flex flex-wrap gap-4">
          <a href="#services">
            <Button>
              Explore Our Services
              <ArrowUpRight className="ml-3" size={18} />
            </Button>
          </a>

          <a href="#about">
            <Button variant="light">More About Us</Button>
          </a>
        </div>
      </div>

      {/* Right Card */}
      <div className="mt-12 rounded-[2rem] bg-white/10 p-4 shadow-soft backdrop-blur lg:mt-0">
        <div className="rounded-[1.5rem] bg-white p-5">
          
          <img
            className="h-96 w-full rounded-[1.2rem] object-cover"
            src="https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=1200&auto=format&fit=crop"
          />

          <div className="mt-4 grid grid-cols-3 gap-3 text-center">
            <div>
              <b className="text-2xl text-brandGreen">20+</b>
              <p className="text-xs text-slate-500">Exercises</p>
            </div>

            <div>
              <b className="text-2xl text-brandGreen">AI</b>
              <p className="text-xs text-slate-500">Form checks</p>
            </div>

            <div>
              <b className="text-2xl text-brandGreen">Free</b>
              <p className="text-xs text-slate-500">Access</p>
            </div>
          </div>

        </div>
      </div>

    </div>
  </section>
);