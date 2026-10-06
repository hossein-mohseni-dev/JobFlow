import { test, expect } from "@playwright/test";

test("landing explains the product in English", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /JobFlow keeps every application/i })).toBeVisible();
  await expect(page.getByRole("link", { name: "Log in" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Create account" })).toBeVisible();
});

test("login page exposes demo credentials and reset link", async ({ page }) => {
  await page.goto("/login");
  await expect(page.getByRole("heading", { name: "Log in" })).toBeVisible();
  await expect(page.getByLabel("Username")).toHaveValue("demo");
  await expect(page.getByRole("link", { name: "Forgot password" })).toBeVisible();
});

test("register page collects an email", async ({ page }) => {
  await page.goto("/register");
  await expect(page.getByRole("heading", { name: "Create account" })).toBeVisible();
  await expect(page.getByLabel("Email")).toBeVisible();
});

test("password reset page is reachable", async ({ page }) => {
  await page.goto("/forgot-password");
  await expect(page.getByRole("heading", { name: "Reset password" })).toBeVisible();
});
