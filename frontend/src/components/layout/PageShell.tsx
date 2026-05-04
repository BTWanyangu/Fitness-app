import type { ReactNode } from 'react';
import { Header } from './Header';
import { Footer } from './Footer';

export const PageShell = ({ children }: { children: ReactNode }) => (
  <>
    <Header />

    <main>
      {children}
    </main>

    <Footer />
  </>
);
