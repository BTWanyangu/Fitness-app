import { PageShell } from '../components/layout/PageShell';
import { Hero } from '../components/landing/Hero';
import { Services } from '../components/landing/Services';
import { HowItWorks } from '../components/landing/HowItWorks';
import { FeatureBand } from '../components/landing/FeatureBand';
import { Testimonials } from '../components/landing/Testimonials';
import { Button } from '../components/ui/Button';

export const LandingPage = () => (
  <PageShell>
    <Hero />
    <Services />
    <HowItWorks />
    <FeatureBand />
    <Testimonials />

    <section className="bg-brandOrange px-6 py-20 text-center text-white">
      <h2 className="text-4xl font-black md:text-5xl">
        Start your fitness journey today
      </h2>

      <p className="mx-auto mt-4 max-w-2xl text-lg">
        Free access, no billing, and a design ready for Kenyan users.
      </p>

      <a href="/dashboard">
        <Button variant="green" className="mt-8">
          Open Dashboard
        </Button>
      </a>
    </section>
  </PageShell>
);