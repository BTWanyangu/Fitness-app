import { UploadCloud } from 'lucide-react';
import { Button } from '../ui/Button';

export const FeatureBand = () => (
  <section id="about" className="grid lg:grid-cols-2">
    <div
      className="min-h-[520px] bg-[linear-gradient(rgba(11,110,24,.2),rgba(11,110,24,.2)),url('https://images.unsplash.com/photo-1599058917212-d750089bc07e?q=80&w=1200&auto=format&fit=crop')] bg-cover bg-center"
    />

    <div className="flex items-center bg-brandGreen px-8 py-20 text-white lg:px-20">
      <div>
        <UploadCloud size={46} className="text-brandOrange" />

        <h2 className="mt-6 text-4xl font-black md:text-5xl">
          Upload references. Score technique. Coach better.
        </h2>

        <p className="mt-5 text-lg leading-9 text-white/80">
          Admins can upload correct exercise images and videos. Users can upload
          training media for AI-assisted scoring and comparison.
        </p>

        <a href="/form-analysis">
          <Button variant="orange" className="mt-8">
            Try Form Analysis
          </Button>
        </a>
      </div>
    </div>
  </section>
);