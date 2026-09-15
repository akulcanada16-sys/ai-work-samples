const asText = (value) => value === null || value === undefined ? "" : String(value);
const asInteger = (value) => typeof value === "number" && Number.isInteger(value) ? value : null;
const asBoolean = (value) => typeof value === "boolean" ? value : null;

export function taskMap(rows) {
  const map = new Map();
  for (const row of Array.isArray(rows) ? rows : []) { const id = asInteger(row.Id); if (id !== null) map.set(id, { id, name: asText(row.Name), namespace: asText(row.Namespace), type: asText(row.Type), suspended: asBoolean(row.Suspended), lastFinished: asText(row.LastFinished), nextScheduled: asText(row.NextScheduled) }); }
  return map;
}
export function rawTimestamp(value) { const raw = asText(value); return { raw, timezone: raw ? "Timezone not supplied by API" : "Not supplied" }; }
export function errorSignal(event) { return event.errorNumber === null ? "Error number not supplied" : event.hasError ? "Reported error" : "No reported error"; }
export function normalizeHistory(rows, tasks) {
  const map = tasks instanceof Map ? tasks : taskMap(tasks);
  return (Array.isArray(rows) ? rows : []).slice(0, 100).map((row, index) => {
    const taskId = asInteger(row.TaskId); const errNumber = asInteger(row.ErrNumber); const task = taskId === null ? undefined : map.get(taskId);
    return { key: `${taskId ?? "unknown"}-${asText(row.LogDatetime)}-${index}`, taskId, taskName: task?.name || asText(row.Name) || "Task no longer present", namespace: task?.namespace || asText(row.Namespace), orphan: !task, status: asText(row.Status), result: asText(row.Result), routine: asText(row.Routine), pid: asText(row.Pid), started: rawTimestamp(row.LastStart), completed: rawTimestamp(row.Completed), logged: rawTimestamp(row.LogDatetime), errorDate: asText(row.ErrDate), errorNumber: errNumber, hasError: errNumber !== null && errNumber !== 0, suspended: task ? task.suspended : null, nextScheduled: rawTimestamp(task?.nextScheduled) };
  }).sort((a, b) => Number(b.hasError) - Number(a.hasError));
}
export function normalizeUpcoming(rows) { return (Array.isArray(rows) ? rows : []).slice(0, 100).map((row) => ({ id: asInteger(row.Id), name: asText(row.Name), namespace: asText(row.Namespace), suspended: asBoolean(row.Suspended), datetime: rawTimestamp(row.Datetime) })); }
