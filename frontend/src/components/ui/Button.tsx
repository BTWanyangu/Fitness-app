import type { ButtonHTMLAttributes, ReactNode } from 'react';

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'green' | 'orange' | 'light' | 'outline';
  children: ReactNode;
};

export const Button = ({
  variant = 'green',
  className = '',
  children,
  ...props
}: Props) => {
  const styles = {
    green: 'bg-brandGreen text-white hover:bg-brandGreenDark',
    orange: 'bg-brandOrange text-white hover:brightness-95',
    light: 'bg-white text-brandGreen hover:bg-green-50',
    outline: 'border border-brandGreen text-brandGreen hover:bg-green-50',
  };

  return (
    <button
      className={`inline-flex items-center justify-center px-7 py-4 text-sm font-extrabold transition ${styles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};