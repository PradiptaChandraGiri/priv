/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#c0c1ff',
        'primary-dark': '#8083ff',
        'primary-light': '#e1e0ff',
        secondary: '#d0bcff',
        tertiary: '#ffb783',
        accent: '#06b6d4',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ffb4ab',
        background: '#0b0f1a',
        surface: '#11162a',
        'surface-container': '#1a202c',
        'surface-bright': '#252d3d',
        'on-surface': '#e4e1ed',
        'on-surface-variant': '#c7c4d7',
        'outline-variant': '#464554',
        outline: '#908fa0',
        'on-primary': '#1000a9',
        'primary-container': '#4f46e5',
      },
      fontFamily: {
        display: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      borderRadius: {
        sm: '8px',
        md: '12px',
        lg: '16px',
        xl: '24px',
      },
      boxShadow: {
        glow: '0 0 40px rgba(192,193,255,0.25)',
        'glow-sm': '0 0 20px rgba(192,193,255,0.15)',
        card: '0 10px 40px rgba(0,0,0,0.4)',
      },
      animation: {
        'float-slow': 'float 8s ease-in-out infinite',
        'float-med': 'float 10s ease-in-out infinite 2s',
        'float-fast': 'float 12s ease-in-out infinite 4s',
        'pulse-ring': 'pulseRing 2s cubic-bezier(0.215,0.61,0.355,1) infinite',
        'scroll-wheel': 'scrollWheel 2s ease infinite',
        blink: 'blink 1s step-end infinite',
        shimmer: 'shimmer 1.5s infinite',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        float: { '0%,100%': { transform: 'translateY(0) scale(1)' }, '50%': { transform: 'translateY(-24px) scale(1.04)' } },
        pulseRing: {
          '0%': { transform: 'scale(0.95)', boxShadow: '0 0 0 0 rgba(192,193,255,0.7)' },
          '70%': { transform: 'scale(1)', boxShadow: '0 0 0 20px rgba(192,193,255,0)' },
          '100%': { transform: 'scale(0.95)', boxShadow: '0 0 0 0 rgba(192,193,255,0)' },
        },
        scrollWheel: {
          '0%': { transform: 'translateY(0)', opacity: 1 },
          '80%': { transform: 'translateY(12px)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 0 },
        },
        blink: { '50%': { opacity: 0 } },
        shimmer: { '0%': { backgroundPosition: '-400px 0' }, '100%': { backgroundPosition: '400px 0' } },
      },
      backgroundImage: {
        'grid-pattern': 'linear-gradient(rgba(192,193,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(192,193,255,0.05) 1px, transparent 1px)',
      },
      backgroundSize: {
        'grid-sm': '40px 40px',
      },
    },
  },
  plugins: [],
};
