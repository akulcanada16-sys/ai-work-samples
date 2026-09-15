import { ApiError, createApiClient } from "./api.js";
import { fixture } from "./fixture.js";
import { errorSignal, normalizeHistory, normalizeUpcoming, taskMap } from "./normalize.js";

const $ = (id) => document.getElementById(id); const text = (value) => value === null || value === undefined || value === "" ? "—" : String(value);
const demo = new URLSearchParams(location.search).get("demo") === "1"; const api = createApiClient(); let selectedTaskId = "";
function appendCell(row, value) { const cell = document.createElement("td"); cell.textContent = text(value); row.append(cell); }
function renderRows(body, rows, columns) { body.replaceChildren(); for (const item of rows) { const row = document.createElement("tr"); for (const column of columns) appendCell(row, column(item)); body.append(row); } }
function showMessage(message, kind = "") { const node = $("message"); node.textContent = message; node.className = kind; }
function showApp(signedIn) { $("signin").hidden = !(!demo && !signedIn); $("workspace").hidden = !signedIn && !demo; $("logout").hidden = demo || !signedIn; }
function populateTaskSelector(tasks) { const select = $("taskSelect"); select.replaceChildren(new Option("All tasks", "")); for (const task of tasks.values()) select.add(new Option(`${task.name} (${task.id})`, String(task.id))); select.value = selectedTaskId; }
function userMessage(error) { if (error instanceof ApiError && error.code === "UNAUTHENTICATED") return "Sign in again to continue."; if (error instanceof ApiError && error.code === "FORBIDDEN") return "This account can sign in but lacks permission to view task data."; return error.message || "Unable to load task data."; }

async function load() {
  const filter = $("filter").value.trim(); showMessage(demo ? "Fictional offline demonstration data. No server contacted." : "Loading read-only task data…");
  try {
    const data = demo ? (() => { const query = filter.toLowerCase(); const taskIds = new Set(fixture.tasks.filter(x => !query || `${x.Name} ${x.Namespace}`.toLowerCase().includes(query)).map(x => x.Id)); return { tasks: fixture.tasks.filter(x => taskIds.has(x.Id)), history: fixture.history.filter(x => !query || taskIds.has(x.TaskId) || `${x.Name || ""} ${x.Namespace || ""}`.toLowerCase().includes(query)), upcoming: fixture.upcoming.filter(x => !query || taskIds.has(x.Id)) }; })() : await (async () => { const [tasks, history, upcoming] = await Promise.allSettled([api.tasks(filter), api.history(filter), api.upcoming(filter)]); if (tasks.status !== "fulfilled") throw tasks.reason; return { tasks: tasks.value, history: history.status === "fulfilled" ? history.value : [], upcoming: upcoming.status === "fulfilled" ? upcoming.value : [], partial: history.status !== "fulfilled" || upcoming.status !== "fulfilled" }; })();
    const tasks = taskMap(data.tasks); const selected = selectedTaskId === "" ? null : Number(selectedTaskId); populateTaskSelector(tasks);
    const history = normalizeHistory(data.history, tasks).filter(x => selected === null || x.taskId === selected); const upcoming = normalizeUpcoming(data.upcoming).filter(x => selected === null || x.id === selected);
    renderRows($("history"), history, [errorSignal, x => x.taskName, x => x.started.raw, x => x.completed.raw, x => x.result, x => x.errorNumber === null ? "Unknown" : x.errorNumber, x => x.suspended === null ? "Unknown" : x.suspended ? "Yes" : "No", x => x.nextScheduled.raw]);
    renderRows($("upcoming"), upcoming, [x => x.name, x => x.namespace, x => x.datetime.raw, x => x.suspended === null ? "Unknown" : x.suspended ? "Yes" : "No"]); showMessage(demo ? "Fictional offline demonstration data. No server contacted." : (data.partial ? "Some task data could not be loaded; available read-only results are shown." : "Read-only data loaded."), data.partial ? "warning" : "");
  } catch (error) { showMessage(userMessage(error), "error"); }
}
$("signin").addEventListener("submit", async (event) => { event.preventDefault(); const user = $("user").value; let password = $("password").value; $("password").value = ""; try { await api.login(user, password); password = ""; showApp(true); await load(); } catch (error) { showMessage(userMessage(error), "error"); } finally { password = ""; } });
$("logout").addEventListener("click", () => { api.logout(); showApp(false); showMessage("Signed out. The access token was removed from this page’s memory."); });
$("reload").addEventListener("click", load); $("filter").addEventListener("keydown", (event) => { if (event.key === "Enter") load(); }); $("taskSelect").addEventListener("change", (event) => { selectedTaskId = event.target.value; load(); });
showApp(demo); if (demo) load(); else showMessage("Sign in to view read-only task data.");
