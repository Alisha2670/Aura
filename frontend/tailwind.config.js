/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        aura: {
          50: '#f0f4ff',
          100: '#e0eaff',
          200: '#c7d7fe',
          300: '#a4bcfd',
          400: '#7e9bfb',
          500: '#6172f3',
          600: '#444ce7',
          700: '#3538cd',
          800: '#2d31a6',
          900: '#2d3282',
          950: '#1d204e',
        },
        dark: {
          bg: '#0B0F19',
          card: '#111827',
          border: '#1F2937',
          muted: '#9CA3AF'
        }
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 15px rgba(97, 114, 243, 0.2)' },
          '100%': { boxShadow: '0 0 30px rgba(97, 114, 243, 0.6)' },
        }
      }
    },
  },
  plugins: [],
}
