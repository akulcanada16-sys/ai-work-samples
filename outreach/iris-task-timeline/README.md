# Task Failure Timeline

An original, dependency-free, read-only interface for the InterSystems management-portal contest. It turns documented task history into a compact sequence of recent runs, flags only records with a non-zero documented `ErrNumber`, preserves raw server timestamps, and shows the next scheduled run and suspended state.

**Experimental candidate:** The fictional browser demo and local contract checks have passed. Real IRIS compatibility has not yet been verified, and this is not a submitted or accepted contest entry.

## Use it now

Open `index.html?demo=1` in a modern browser for a fully fictional offline demo. It makes no server request. The normal page must be served from the same InterSystems IRIS origin. It signs in directly to the documented same-origin `/api/admin/login` endpoint, holds only the documented `access_token` in page memory, clears the password input immediately, and sends that access token as a Bearer token for reads. It does not store credentials or tokens in browser storage, URLs, logs, or a proxy. Local sign-out removes the token from page memory.

The request allowlist is fixed in `src/api.js`: `/api/admin/v2/tasks`, `/api/admin/v2/task/history`, and `/api/admin/v2/task/upcoming`. The `/api/admin` same-origin base comes from the organizer-linked specification. All operational requests use `GET` and limit history/upcoming requests to 100 rows. Authentication is the sole `POST` exception and does not mutate IRIS administration data.

## Local IRIS installation

After a free IRIS Community Edition runtime is available, install this folder through a CSP web application and open it from that same origin. The application path should be `/csp/task-timeline`, with physical path `/usr/irissys/csp/task-timeline` in the Community Edition container and **Serve Files** set to **Always**. InterSystems documents that a CSP application’s physical path is relative to `install-dir/csp`, and that **Always** makes the CSP server serve static files for that path. The CI configuration creates only this disposable mapping and prints its final URL, physical path, and Serve Files value. The app rejects non-HTTPS remote origins; only `localhost`/`127.0.0.1` development addresses may use HTTP. Sign in with an account that already has the published read privileges. Do not use this application to change tasks or system state.

Run the offline checks with:

```text
npm test
```

## CI integration plan

`integration/github-actions-iris.yml` is the source for the repository's `.github/workflows/iris-task-timeline.yml` live verification workflow. It pins Docker Hub's 2026.2 linux-amd64 Community Edition digest, runs the Node contract suite, creates a dedicated disposable `/csp/task-timeline` static mapping, checks documented response wrappers, and exercises browser sign-in/read/logout against that same container. The static-page step prints the HTTP status, content type, a redirect path with its query removed, the first 1,500 bytes of this public fictional page, and both the expected requirement (the mapped directory must be searchable/readable and static files readable by the IRIS web-server process) and actual mapped-file permissions before failing. It uses `contents: read`, no stored secrets, no artifacts, and a 20-minute timeout. Check the Actions result before relying on live compatibility; no passing live run is claimed here.

The fixture script intentionally alters no IRIS task or database. The workflow verifies real read endpoints against the ephemeral empty/default Community Edition state; it does not claim task-history fixture coverage until a version-specific, documented safe task-seeding method is proven. The workflow therefore must not yet be represented as an integration test that has passed.

## Verification and safety

The Node tests cover Bearer authentication, safe-origin rejection, local logout, missing response wrappers, 401/403 handling, endpoint allowlisting, GET-only operational requests, percent encoding of hostile text, schema normalization, orphaned historical names, error-number handling, booleans, and timestamp ambiguity. UI rendering uses `textContent`, never HTML insertion, so API values such as task names/results cannot create markup.

## License and provenance

MIT License. This repository’s code and fictional fixture data were generated with an AI coding agent under the owner’s direction. It makes no claim of human review, prior experience, or organizer approval. Before contest submission, the owner must ensure the submission satisfies the organizer’s originality, rights, and truthfulness terms.
