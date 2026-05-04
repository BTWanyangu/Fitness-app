import { SectionHeading } from '../ui/SectionHeading';

const people = ['Brian, Nairobi', 'Amina, Mombasa', 'Kelvin, Kisumu'];

export const Testimonials = () => (
  <section className="bg-white px-6 py-24">
    <SectionHeading
      eyebrow="Community"
      title="Built for real everyday training"
    />

    <div className="mx-auto mt-12 grid max-w-6xl gap-6 md:grid-cols-3">
      {people.map((p) => (
        <div
          key={p}
          className="rounded-3xl border border-slate-100 p-7 shadow-soft"
        >
          <p className="leading-8 text-slate-600">
            “Trainova feels practical. I can see workouts, form guidance, and
            progress without struggling through a complicated app.”
          </p>

          <div className="mt-6 font-black text-brandGreen">
            {p}
          </div>
        </div>
      ))}
    </div>
  </section>
);