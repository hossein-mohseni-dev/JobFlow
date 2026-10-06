export const API_URL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  if (!(options.body instanceof FormData) && !headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${API_URL}${path}`, { ...options, headers, credentials: "include" });
  if (response.status === 401 && typeof window !== "undefined") {
    const refreshed = await fetch(`${API_URL}/auth/refresh/`, { method: "POST", credentials: "include" });
    if (refreshed.ok && !path.includes("/auth/")) {
      return api<T>(path, options);
    }
    if (!window.location.pathname.startsWith("/login")) window.location.href = "/login";
  }
  if (!response.ok) {
    let detail = "Request failed";
    try {
      const body = await response.json();
      detail = body.detail || body.username?.[0] || body.email?.[0] || JSON.stringify(body);
    } catch {
      detail = await response.text();
    }
    throw new Error(detail);
  }
  if (response.status === 204) return undefined as T;
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/pdf")) return (await response.blob()) as T;
  return response.json();
}

export async function logout() {
  await api("/auth/logout/", { method: "POST" });
}

export const STATUS_LABELS: Record<string, string> = {
  applied: "Applied",
  interview: "Interview",
  technical_test: "Technical Test",
  offer: "Offer",
  rejected: "Rejected",
};

export const TYPE_LABELS: Record<string, string> = {
  full_time: "Full-time",
  part_time: "Part-time",
  contract: "Contract",
  internship: "Internship",
};

export const PLACE_LABELS: Record<string, string> = {
  remote: "Remote",
  hybrid: "Hybrid",
  onsite: "Onsite",
};
