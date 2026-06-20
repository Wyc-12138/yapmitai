function normalizeApiBase(value) {
  const base = value || "/api/v1";
  if (typeof window === "undefined" || !base.startsWith("http://")) return base;
  try {
    const url = new URL(base);
    if (window.location.protocol === "https:" && url.hostname === window.location.hostname) {
      url.protocol = "https:";
      return url.toString().replace(/\/$/, "");
    }
  } catch {
    return base;
  }
  return base;
}

export const API_BASE = normalizeApiBase(import.meta.env.VITE_API_BASE_URL);

export const API_KEY =
  import.meta.env.VITE_API_KEY || "yap_demo_key_2026";
