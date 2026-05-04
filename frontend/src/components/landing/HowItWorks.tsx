import { SectionHeading } from '../ui/SectionHeading';

const steps = [
  'Create your profile',
  'Choose a workout plan',
  'Train and track progress',
  'Improve using AI form feedback',
];

export const HowItWorks = () => (
  <section id="how" className="bg-[#F3F8F3] px-6 py-24">
    <SectionHeading
      eyebrow="How it works"
      title="A simple flow anyone can follow"
    />

    <div className="mx-auto mt-14 grid max-w-6xl gap-5 md:grid-cols-4">
      {steps.map((step, i) => (
        <div
          key={step}
          className="rounded-3xl bg-white p-7 shadow-soft"
        >
          <span className="text-5xl font-black text-brandOrange">
            0{i + 1}
          </span>

          <h3 className="mt-5 text-xl font-black">
            {step}
          </h3>

          <p className="mt-3 text-sm leading-7 text-slate-600">
            Clear actions, clean screens, and no login wall for public
            demonstration.
          </p>
        </div>
      ))}
    </div>
  </section>
);