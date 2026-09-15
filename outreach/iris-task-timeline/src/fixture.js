export const fixture = {
  tasks: [
    { Id: 7, Name: "Nightly Index", Namespace: "APP", Type: "User", Suspended: false, LastFinished: "2026-09-15 01:03:00", NextScheduled: "2026-09-16 01:00:00" },
    { Id: 8, Name: "Weekly Cleanup", Namespace: "APP", Type: "User", Suspended: true, LastFinished: "2026-09-14 04:00:00", NextScheduled: "2026-09-21 04:00:00" }
  ],
  history: [
    { TaskId: 7, LastStart: "2026-09-15 01:00:00", Completed: "2026-09-15 01:03:00", Status: "Complete", Result: "Index rebuilt", ErrDate: "", ErrNumber: 0, Namespace: "APP", Routine: "IndexTask", Pid: "411", LogDatetime: "2026-09-15 01:03:00" },
    { TaskId: 8, LastStart: "2026-09-14 04:00:00", Completed: "2026-09-14 04:00:02", Status: "Complete", Result: "Input unavailable", ErrDate: "2026-09-14", ErrNumber: 5001, Namespace: "APP", Routine: "CleanupTask", Pid: "412", LogDatetime: "2026-09-14 04:00:02" },
    { TaskId: 99, LastStart: "2026-09-13 02:00:00", Completed: "2026-09-13 02:00:01", Status: "Complete", Result: "Historical task", ErrDate: "", ErrNumber: 0, Namespace: "OLD", Routine: "Legacy", Pid: "413", LogDatetime: "2026-09-13 02:00:01" }
  ],
  upcoming: [{ Id: 7, Name: "Nightly Index", Namespace: "APP", Suspended: false, Datetime: "2026-09-16 01:00:00" }]
};
