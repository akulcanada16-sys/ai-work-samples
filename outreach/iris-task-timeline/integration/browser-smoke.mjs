import { chromium } from "playwright";
const expected = new Set(["/api/admin/v2/tasks", "/api/admin/v2/task/history", "/api/admin/v2/task/upcoming"]);
const seen = new Map();
const user = process.env.IRIS_TEST_USER;
const password = process.env.IRIS_TEST_PASSWORD;
if (!user || !password) throw new Error("Missing CI-only IRIS test credentials.");
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
page.on("request", (request) => {
  const url = new URL(request.url());
  if (expected.has(url.pathname)) seen.set(url.pathname, request.headers());
});
await page.goto("http://localhost:52773/csp/task-timeline/index.html");
await page.locator("#user").fill(user);
await page.locator("#password").fill(password);
await page.locator("#signin button").click();
await page.waitForFunction(() => document.querySelector("#message")?.textContent === "Read-only data loaded.");
if (await page.locator("#message.error, #message.warning").count()) throw new Error("The page reported an error or partial-data warning.");
for (const path of expected) {
  const headers = seen.get(path);
  if (!headers || !headers.authorization?.startsWith("Bearer ")) throw new Error(`Missing successful Bearer GET for ${path}`);
}
await page.locator("#logout").click();
await page.waitForFunction(() => document.querySelector("#signin")?.hidden === false);
await browser.close();
