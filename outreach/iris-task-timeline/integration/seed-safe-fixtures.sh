#!/bin/sh
set -eu
# The only fixture is the static fictional browser-demo data already copied with this app.
# It is served from the disposable container and does not create, run, or alter an IRIS task.
test -f /usr/irissys/csp/samples/task-timeline/src/fixture.js
