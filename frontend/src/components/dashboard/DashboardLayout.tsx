import type { ReactNode } from 'react';
import { Header } from '../layout/Header';
import { Sidebar } from './Sidebar';

export const DashboardLayout = ({ children }: { children: ReactNode }) => (
  <>
    <Header />

    <div className="flex bg-[#F7FAF7]">
      <Sidebar />

      <main className="min-h-screen flex-1 px-5 py-8 lg:px-10">
        {children}
      </main>
    </div>
  </>
);