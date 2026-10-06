"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Bell, Briefcase, Building2, Calendar, FileText, LayoutDashboard, LogOut, UserRound } from "lucide-react";
import { Brand } from "@/components/ui";
import { ThemeToggle } from "@/components/theme";
import { logout } from "@/lib/api";
import { cn } from "@/lib/utils";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/jobs", label: "Jobs" },
  { href: "/applications", label: "Kanban" },
  { href: "/interviews", label: "Calendar" },
  { href: "/companies", label: "Companies" },
  { href: "/profile", label: "Profile & CV" },
  { href: "/letters", label: "Cover letters" },
  { href: "/notifications", label: "Notifications" },
];

export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  return (
    <div className="min-h-screen dark:bg-ink dark:text-sand">
      <header className="sticky top-0 z-20 border-b border-teal-900/10 bg-white/80 backdrop-blur dark:bg-ink/80">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <Brand />
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <button
              className="inline-flex items-center gap-2 rounded-xl px-3 py-2 text-sm hover:bg-sand dark:hover:bg-white/10"
              onClick={() => logout().finally(() => router.push("/login"))}
            >
              <LogOut size={16} /> Log out
            </button>
          </div>
        </div>
      </header>
      <div className="mx-auto grid max-w-6xl gap-6 px-4 py-6 md:grid-cols-[220px_1fr]">
        <nav aria-label="Primary" className="h-fit rounded-2xl border border-white bg-white/80 p-2 shadow-sm dark:border-white/10 dark:bg-white/5">
          {links.map((link) => {
            const active = pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn("mb-1 block rounded-xl px-3 py-2 text-sm", active ? "bg-pine text-white" : "hover:bg-sand dark:hover:bg-white/10")}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
        <main id="main">{children}</main>
      </div>
    </div>
  );
}
