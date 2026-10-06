import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function money(value?: number | null, currency = "EUR") {
  if (!value) return "Negotiable";
  return `${new Intl.NumberFormat("en-US").format(value)} ${currency}`;
}
