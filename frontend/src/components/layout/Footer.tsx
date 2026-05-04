import {
  Activity,
  Facebook,
  Instagram,
  Mail,
  MapPin,
  Twitter,
} from 'lucide-react';

export const Footer = () => (
  <footer className="bg-[#06370B] text-white">
    <div className="mx-auto grid max-w-7xl gap-10 px-6 py-14 md:grid-cols-4">
      
      {/* Brand */}
      <div>
        <div className="flex items-center gap-2">
          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-white/10">
            <Activity size={20} />
          </span>
          <span className="text-2xl font-black">Trainova</span>
        </div>

        <p className="mt-4 text-sm leading-7 text-white/75">
          Free AI-assisted fitness guidance for Kenyan gym, home, and outdoor
          training communities.
        </p>
      </div>

      {/* Quick Links */}
      <div>
        <h4 className="font-black">Quick Links</h4>
        <ul className="mt-4 space-y-3 text-sm text-white/75">
          <li>Home</li>
          <li>Dashboard</li>
          <li>Exercises</li>
          <li>AI Form Analysis</li>
        </ul>
      </div>

      {/* Features */}
      <div>
        <h4 className="font-black">Features</h4>
        <ul className="mt-4 space-y-3 text-sm text-white/75">
          <li>Exercise library</li>
          <li>Reference videos</li>
          <li>Technique scoring</li>
          <li>Admin controls</li>
        </ul>
      </div>

      {/* Contact */}
      <div>
        <h4 className="font-black">Kenya Office</h4>

        <p className="mt-4 flex gap-2 text-sm text-white/75">
          <MapPin size={18} />
          Nairobi, Kenya
        </p>

        <p className="mt-3 flex gap-2 text-sm text-white/75">
          <Mail size={18} />
          hello@trainova.local
        </p>

        <div className="mt-5 flex gap-3">
          <Facebook />
          <Twitter />
          <Instagram />
        </div>
      </div>
    </div>

    <div className="border-t border-white/10 px-6 py-5 text-center text-sm text-white/60">
      © 2026 Trainova. Built for accessible fitness coaching.
    </div>
  </footer>
);