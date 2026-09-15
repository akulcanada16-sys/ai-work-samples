# Task Failure Timeline

An original, dependency-free, read-only interface for the InterSystems management-portal contest. It turns documented task history into a compact sequence of recent runs, flags only records with a non-zero documented `ErrNumber`, preserves raw server timestamps, and shows the next scheduled run and suspended state.

**Experimental candidate:** The fictional browser demo, local contract checks, and [pinned IRIS 2026.2 Community Edition integration run](https://github.com/akulcanada16-sys/ai-work-samples/actions/runs/35032649000) have passed. That run verified static serving, sign-in, all three read endpoints, browser rendering, local sign-out, and container teardown. It is evidence for that pinned 2026.2 image, not a guarantee for future IRIS versions. This is not a submitted or accepted contest entry, and it has received no contest award.

## Use it now

Open `index.html?demo=1` in a modern browser for a fully fictional offline demo. It makes no server request. The normal page must be served from the same InterSystems IRIS origin. It signs in directly to the documented same-origin `/api/admin/login` endpoint, holds the `access_token` in page memory, clears the password input immediately, and sends that access token as a Bearer token for reads. It accepts the specification’s `result.access_token` response and the root-level `access_token` observed from the pinned IRIS 2026.2 Community Edition image in Actions run 35032336458; it does not refresh tokens. It does not store credentials or tokens in browser storage, URLs, logs, or a proxy. Local sign-out removes the token from page memory.

The request allowlist is fixed in `src/api.js`: `/api/admin/v2/tasks`, `/api/admin/v2/task/history`, and `/api/admin/v2/task/upcoming`. The `/api/admin` same-origin base comes from the organizer-linked specification. All operational requests use `GET` and limit history/upcoming requests to 100 rows. Authentication is the sole `POST` exception and does not mutate IRIS administration data.

## Local IRIS installation

This page requires InterSystems IRIS **2026.2 or newer**, because the organizer-linked API documents `/api/admin/login` from that release onward. Start with an existing IRIS instance and an account that already has `%Admin_Operate:Use`; this account can read the three task endpoints used here. Do not create a broad test account on a real server for this page.

Clone the existing portfolio repository, then copy this exact subdirectory into the IRIS container or server:

```text
git clone https://github.com/akulcanada16-sys/ai-work-samples.git
cd ai-work-samples/outreach/iris-task-timeline
```

Create a CSP web application at `/csp/task-timeline` with these settings:

| Setting | Value |
| --- | --- |
| Namespace | `USER` (the page is static) |
| Physical path | `task-timeline`, relative to `install-dir/csp`; in the Community Edition container this is `/usr/irissys/csp/task-timeline` |
| Serve Files | **Always** |
| Recurse | Enabled |
| Enabled | Enabled |

Copy the contents of `ai-work-samples/outreach/iris-task-timeline/` to that physical path and browse to `https://your-iris-host/csp/task-timeline/index.html`. InterSystems documents that a CSP application’s physical path is relative to `install-dir/csp`, and that **Always** makes the CSP server serve static files for that application path. The page permits HTTP only on `localhost` or `127.0.0.1` for development; a remote IRIS host must use HTTPS.

The CI workflow’s `TaskTimelineCI` account is generated inside a loopback-only disposable container, has only `%Operator`, and is destroyed with that container. It is a CI mechanism, not an installation instruction for a real server.

Run the offline checks with:

```text
cd ai-work-samples/outreach/iris-task-timeline
npm test
```

## CI integration plan

`integration/github-actions-iris.yml` is the source for the repository's `.github/workflows/iris-task-timeline.yml` live verification workflow. It pins a Docker Hub IRIS 2026.2 linux-amd64 Community Edition digest, runs the Node contract suite, creates a dedicated disposable `/csp/task-timeline` static mapping through the documented `iris terminal IRIS` command, and exercises browser sign-in, the three Bearer-authenticated reads, and local sign-out against that same container. The [successful run 35032649000](https://github.com/akulcanada16-sys/ai-work-samples/actions/runs/35032649000) recorded login HTTP 200 and task/history/upcoming HTTP 200 responses with 16, 26, and 80 rows respectively, then completed browser and teardown steps. It uses `contents: read`, no stored secrets, no artifacts, and a 20-minute timeout.

The fixture script intentionally alters no IRIS task or database. The successful workflow verifies real read endpoints against the ephemeral Community Edition state, but it does not provide seeded error-task fixture coverage. Do not infer error-history behavior from that integration run alone.

## Focused use and limitations

Use the page after signing in to answer a narrow operations question: “Which scheduled tasks have recently reported an error, what task do they belong to, and what is scheduled next?” Select a task to narrow the timeline, then compare its recent records with the next scheduled entry. The app preserves the timestamp text supplied by IRIS because these API responses do not provide timezone metadata; it does not convert or infer timezones.

Only `/v2/tasks`, `/v2/task/history`, and `/v2/task/upcoming` are read. The page cannot start, stop, edit, suspend, resume, or delete a task. It limits history and upcoming responses to 100 rows, so it is a focused recent-view tool rather than a complete audit archive. A deleted task can still appear as an orphaned historical record, and missing error numbers are displayed as unknown rather than assumed to be zero.

## Contest and API references

This project responds to the [InterSystems Programming Contest: Build Your Own Management Portal](https://community.intersystems.com/post/intersystems-programming-contest-build-your-own-management-portal), whose listed ideas include task management and logs. Its routes and fields come from the organizer-linked [SysAdmin API specification](https://github.com/intersystems-community/sysadmin-api-specification/blob/master/mainspec_v2.json). CSP mapping behavior is described in InterSystems’ [CSP application configuration documentation](https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=GSA_cspappdef).

## Verification and safety

The Node tests cover Bearer authentication, safe-origin rejection, local logout, missing response wrappers, 401/403 handling, endpoint allowlisting, GET-only operational requests, percent encoding of hostile text, schema normalization, orphaned historical names, error-number handling, booleans, and timestamp ambiguity. UI rendering uses `textContent`, never HTML insertion, so API values such as task names/results cannot create markup.

## License and provenance

MIT License. This repository’s code and fictional fixture data were generated with an AI coding agent under the owner’s direction. It makes no claim of human review, prior experience, or organizer approval. Before contest submission, the owner must ensure the submission satisfies the organizer’s originality, rights, and truthfulness terms.

