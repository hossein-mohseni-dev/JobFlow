import { test, expect } from "@playwright/test";

test("kanban renders columns and accepts a dragged card", async ({ page }) => {
  await page.route("**/api/v1/applications/**", async (route) => {
    if (route.request().method() === "PATCH") {
      await route.fulfill({ json: { id: 1, status: "interview" } });
      return;
    }
    await route.fulfill({
      json: {
        results: [
          { id: 1, status: "applied", note: "Portfolio sent", deadline: "2026-10-20", job: { title: "Backend Engineer", company: { name: "Northline" } } },
        ],
      },
    });
  });
  await page.goto("/applications");
  await expect(page.getByRole("heading", { name: "Application kanban" })).toBeVisible();
  await expect(page.getByText("Backend Engineer")).toBeVisible();
  const card = page.getByText("Backend Engineer");
  const interview = page.getByRole("region", { name: "Interview" });
  await card.dragTo(interview);
  await expect(interview.getByText("Backend Engineer")).toBeVisible();
});
