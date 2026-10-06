import "./globals.css";
import type { Metadata } from "next";
import { ThemeScript } from "@/components/theme";

export const metadata: Metadata = {
  title: { default: "JobFlow", template: "%s | JobFlow" },
  description: "Track applications, interviews, deadlines, and tailored CVs.",
  robots: { index: true, follow: true },
  openGraph: { title: "JobFlow", description: "Job search and application tracker", type: "website" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <ThemeScript />
      </head>
      <body className="min-h-screen antialiased">
        <a className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:bg-white focus:p-2" href="#main">
          Skip to content
        </a>
        {children}
      </body>
    </html>
  );
}
