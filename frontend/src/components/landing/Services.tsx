import {
  BrainCircuit,
  ChartNoAxesCombined,
  Dumbbell,
  Salad,
} from 'lucide-react';

import { SectionHeading } from '../ui/SectionHeading';

const services = [
  [
    'Personalized Workouts',
    Dumbbell,
    'Structured plans for gym, home, and outdoor sessions.',
  ],
  [
    'AI Form Analysis',
    BrainCircuit,
    'Upload technique media and compare against approved references.',
  ],
  [
    'Progress Tracking',
    ChartNoAxesCombined,
    'Track consistency, weight, strength, and performance trends.',
  ],
  [
    'Nutrition Guidance',
    Salad,
    'Simple habit-based guidance tailored to everyday Kenyan routines.',
  ],
];

export const Services = () => (
  <section id="services" className="bg-white px-6 py-24">
    <SectionHeading
      eyebrow="Our Services"
      title="Everything needed to train with structure"
      body="Designed as a free, practical fitness product with admin-controlled content and real exercise data."
    />

    <div className="mx-auto mt-14 grid max-w-7xl gap-6 md:grid-cols-2 lg:grid-cols-4">
      {services.map(([title, Icon, description]: any) => (
        <div
          key={title}
          className="group rounded-3xl border border-slate-100 bg-white p-7 shadow-soft transition hover:-translate-y-1"
        >
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brandGreen text-white">
            <Icon />
          </div>

          <h3 className="mt-6 text-xl font-black text-ink">
            {title}
          </h3>

          <p className="mt-3 leading-7 text-slate-600">
            {description}
          </p>

          <span className="mt-6 inline-block h-1 w-12 bg-brandOrange transition group-hover:w-20" />
        </div>
      ))}
    </div>
  </section>
);