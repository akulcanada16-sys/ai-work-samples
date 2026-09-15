import test from "node:test";
import assert from "node:assert/strict";
import { ApiError, ENDPOINTS, allowedRequest, createApiClient, isSafeOrigin } from "../src/api.js";
import { errorSignal, normalizeHistory, normalizeUpcoming, rawTimestamp, taskMap } from "../src/normalize.js";

test("normalizes documented integer and boolean fields without coercing missing values", () => {
  const tasks = taskMap([{ Id: 1, Name: "Safe task", Namespace: "APP", Suspended: true, NextScheduled: "2026-09-16 10:00:00" }, { Id: null, Name: "ignored" }]);
  const [event] = normalizeHistory([{ TaskId: 1, ErrNumber: null, LastStart: "2026-09-15 10:00:00" }], tasks);
  assert.equal(event.taskName, "Safe task"); assert.equal(event.errorNumber, null); assert.equal(event.hasError, false); assert.equal(event.suspended, true); assert.equal(tasks.has(null), false);
});
test("uses only a documented non-zero integer error number as failure signal", () => {
  const result = normalizeHistory([{ TaskId: 1, ErrNumber: 0 }, { TaskId: 1, ErrNumber: 42 }, { TaskId: 1, ErrNumber: "42" }, { TaskId: 1, ErrNumber: false }], new Map());
  assert.deepEqual(result.map(x => x.hasError), [true, false, false, false]);
  assert.equal(errorSignal(result[0]), "Reported error"); assert.equal(errorSignal(result[1]), "No reported error"); assert.equal(errorSignal(result[2]), "Error number not supplied");
});
test("retains historical name for orphan and uses fallback only when name is absent", () => {
  const events = normalizeHistory([{ TaskId: 99, Name: "Deleted task" }, { TaskId: 100 }], new Map());
  assert.equal(events[0].taskName, "Deleted task"); assert.equal(events[1].taskName, "Task no longer present");
});
test("preserves raw timestamp and does not invent timezone", () => { const timestamp = rawTimestamp("2026-09-15 10:00:00"); assert.equal(timestamp.raw, "2026-09-15 10:00:00"); assert.match(timestamp.timezone, /not supplied/i); });
test("normalizes only literal boolean suspended values and preserves unknown", () => { assert.equal(normalizeUpcoming([{ Id: 1, Suspended: "true" }, { Id: 2, Suspended: true }])[0].suspended, null); assert.equal(normalizeUpcoming([{ Id: 2, Suspended: true }])[0].suspended, true); assert.equal(normalizeUpcoming([{ Id: 3, Suspended: false }])[0].suspended, false); });
test("enforces read allowlist and encodes hostile text", () => { assert.equal(allowedRequest(ENDPOINTS.history, { filter: "<script>" }), "/api/admin/v2/task/history?filter=%3Cscript%3E"); assert.throws(() => allowedRequest("/v2/task/run"), ApiError); });
test("rejects remote non-HTTPS sign-in origins while allowing HTTPS and local development", () => { assert.equal(isSafeOrigin({ protocol: "http:", hostname: "example.test" }), false); assert.equal(isSafeOrigin({ protocol: "https:", hostname: "example.test" }), true); assert.equal(isSafeOrigin({ protocol: "http:", hostname: "localhost" }), true); });
test("uses documented access_token transiently and operational requests are GET Bearer calls", async () => {
  const calls = []; const client = createApiClient(async (url, options) => { calls.push({ url, options }); return { ok: true, status: 200, json: async () => url.endsWith("/login") ? { result: { access_token: "short-token", refresh_token: "ignored" } } : { result: [] } }; }, { protocol: "https:", hostname: "example.test" });
  await client.login("reader", "password"); await client.tasks('<img src=x>');
  assert.equal(calls[0].options.method, "POST"); assert.equal(calls[1].options.method, "GET"); assert.equal(calls[1].options.headers.Authorization, "Bearer short-token"); assert.match(calls[1].url, /%3Cimg/);
  client.logout(); assert.equal(client.signedIn(), false); await assert.rejects(client.tasks(), error => error.code === "UNAUTHENTICATED");
});
test("reports missing wrappers and 401/403 states", async () => {
  let call = 0; const client = createApiClient(async () => ({ ok: true, status: 200, json: async () => call++ === 0 ? { result: { access_token: "t" } } : {} }), { protocol: "https:", hostname: "test" }); await client.login("u", "p"); await assert.rejects(client.tasks(), error => error.code === "CONTRACT");
  for (const status of [401, 403]) { let deniedCall = 0; const denied = createApiClient(async () => ({ ok: deniedCall++ === 0, status, json: async () => ({ result: { access_token: "t" } }) }), { protocol: "https:", hostname: "test" }); await denied.login("u", "p"); await assert.rejects(denied.tasks(), error => error.code === (status === 401 ? "UNAUTHENTICATED" : "FORBIDDEN")); }
});
