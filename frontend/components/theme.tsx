"use client";

import { useEffect, useState } from "react";

export function ThemeScript() {
  return (
    <script
      dangerouslySetInnerHTML={{
        __html: `try{if(localStorage.getItem('jobflow-theme')==='dark')document.documentElement.classList.add('dark')}catch(e){}`,
      }}
    />
  );
}

export function ThemeToggle() {
  const [dark, setDark] = useState(false);
  useEffect(() => setDark(document.documentElement.classList.contains("dark")), []);
  return (
    <button
      type="button"
      aria-label="Toggle color theme"
      className="rounded-xl border border-teal-900/10 px-3 py-2 text-sm"
      onClick={() => {
        const next = !dark;
        setDark(next);
        document.documentElement.classList.toggle("dark", next);
        localStorage.setItem("jobflow-theme", next ? "dark" : "light");
      }}
    >
      {dark ? "Light" : "Dark"}
    </button>
  );
}
