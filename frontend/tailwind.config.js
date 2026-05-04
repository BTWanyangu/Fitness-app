export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brandGreen: '#0B6E18',
        brandGreenDark: '#07530F',
        brandOrange: '#F59E0B',
        ink: '#07111F',
      },
      boxShadow: {
        soft: '0 20px 60px rgba(3,15,31,.14)',
      },
    },
  },
  plugins: [],
};