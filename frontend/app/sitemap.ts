import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  return ["", "/login", "/register"].map((path) => ({
    url: `http://localhost:3000${path}`,
    lastModified: new Date(),
  }));
}
