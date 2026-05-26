/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#09090b", // Deep zinc black
        card: "rgba(20, 20, 25, 0.65)", // Translucent dark
        border: "rgba(255, 255, 255, 0.08)",
        primary: {
          50: "#eef2ff",
          100: "#e0e7ff",
          500: "#6366f1", // Sleek indigo
          600: "#4f46e5",
          700: "#4338ca",
        },
        risk: {
          low: "#10b981",       // vibrant emerald
          medium: "#f59e0b",    // vibrant amber
          high: "#ef4444",      // safety red
          critical: "#a855f7",  // toxic purple
        }
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      backdropBlur: {
        xs: "2px",
      }
    },
  },
  plugins: [],
};
