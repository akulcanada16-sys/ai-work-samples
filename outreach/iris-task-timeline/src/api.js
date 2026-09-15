export const API_BASE = "/api/admin";
export const ENDPOINTS = Object.freeze({
  login: "/login", tasks: "/v2/tasks", history: "/v2/task/history", upcoming: "/v2/task/upcoming"
});
const READ_ENDPOINTS = new Set([ENDPOINTS.tasks, ENDPOINTS.history, ENDPOINTS.upcoming]);

export class ApiError extends Error { constructor(code, message) { super(message); this.code = code; } }
export function isSafeOrigin(locationLike) {
  const protocol = locationLike?.protocol; const host = locationLike?.hostname;
  return protocol === "https:" || (protocol === "http:" && ["localhost", "127.0.0.1", "::1", "[::1]"].includes(host));
}
export function allowedRequest(path, query = {}) {
  if (!READ_ENDPOINTS.has(path)) throw new ApiError("BLOCKED", "Blocked request: endpoint is not allowlisted for read-only use.");
  const url = new URL(path, "https://same-origin.invalid");
  for (const [key, value] of Object.entries(query)) if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  return `${API_BASE}${url.pathname}${url.search}`;
}
function unwrapArray(payload) {
  if (!payload || !Object.hasOwn(payload, "result") || !Array.isArray(payload.result)) throw new ApiError("CONTRACT", "The server returned an unexpected response shape.");
  return payload.result;
}
function messageFor(status) {
  if (status === 401) return new ApiError("UNAUTHENTICATED", "Your sign-in has expired or was not accepted.");
  if (status === 403) return new ApiError("FORBIDDEN", "This account does not have permission to view this task data.");
  return new ApiError("REQUEST", `Request failed (${status}).`);
}
function loginAccessToken(payload) {
  for (const token of [payload?.result?.access_token, payload?.access_token]) {
    if (typeof token === "string" && token.trim() !== "") return token;
  }
  return null;
}

export function createApiClient(fetchImpl = fetch, locationLike = globalThis.location) {
  let accessToken = null;
  async function login(user, password) {
    accessToken = null;
    if (!isSafeOrigin(locationLike)) throw new ApiError("ORIGIN", "Sign-in is allowed only on HTTPS or a local development address.");
    const response = await fetchImpl(`${API_BASE}${ENDPOINTS.login}`, { method: "POST", credentials: "same-origin", headers: { Accept: "application/json", "Content-Type": "application/json" }, body: JSON.stringify({ user, password }) });
    if (!response.ok) throw messageFor(response.status);
    const token = loginAccessToken(await response.json());
    if (!token) throw new ApiError("CONTRACT", "The server did not return a usable access token.");
    accessToken = token;
  }
  async function get(path, query) {
    if (!accessToken) throw new ApiError("UNAUTHENTICATED", "Sign in before viewing task data.");
    const response = await fetchImpl(allowedRequest(path, query), { method: "GET", credentials: "same-origin", headers: { Accept: "application/json", Authorization: `Bearer ${accessToken}` } });
    if (!response.ok) throw messageFor(response.status);
    return unwrapArray(await response.json());
  }
  return Object.freeze({
    login, logout: () => { accessToken = null; }, signedIn: () => accessToken !== null,
    tasks: (filter) => get(ENDPOINTS.tasks, { filter }), history: (filter) => get(ENDPOINTS.history, { filter, maxRows: 100 }),
    upcoming: (filter) => get(ENDPOINTS.upcoming, { filter, hoursOffset: 168, maxRows: 100 })
  });
}
