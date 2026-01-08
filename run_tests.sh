#!/usr/bin/env bash
set -euo pipefail

export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)

BROWSER="chromium" # supports: chromium | firefox | webkit
MARKER=""
WORKERS="auto"
HEADED=false
ENV_TYPE="local"

usage(){ cat <<EOF >&2
Usage: $0 [-b chromium|firefox|webkit] [-m <marker>] [-n <workers>] [-H] [-e <env_type>]
  -b    browser (chromium|firefox|webkit), default=chromium
  -m    pytest marker
  -n    xdist workers, default=auto
  -H    run in headed mode (not headless)
  -e    environment type (local|staging), default=local
EOF
exit 1; }

while getopts "b:m:n:He:" opt; do
  case $opt in
    b) BROWSER="$OPTARG" ;;
    m) MARKER="$OPTARG" ;;
    n) WORKERS="$OPTARG" ;;
    H) HEADED=true ;;
    e) ENV_TYPE="$OPTARG" ;;
    *) usage ;;
  esac
done

echo "🧹 Shutting down any old containers…"
docker compose down --remove-orphans

echo "🧹 Cleaning artifacts…"
rm -rf tests/artifacts && mkdir -p tests/artifacts

echo "📦 Building test-runner…"
docker compose build test-runner

PYTEST_ARGS=(-v --color=yes)
[ -n "$MARKER" ] && PYTEST_ARGS+=( -m "$MARKER" )
[ "$HEADED" = true ] && PYTEST_ARGS+=( --headed )
PYTEST_ARGS+=( --browser "$BROWSER" )
PYTEST_ARGS+=( -n "$WORKERS" --html=tests/artifacts/report.html --self-contained-html )

echo "🧪 Running pytest ($BROWSER, headed=$HEADED, workers=$WORKERS, env=$ENV_TYPE)…"
docker compose run --rm --no-deps \
  -e ENV_TYPE="$ENV_TYPE" \
  --entrypoint pytest \
  test-runner \
  "${PYTEST_ARGS[@]}" \
| sed -E '
    s|file:///app/tests/artifacts/report.html|file://'"$PWD"'/tests/artifacts/report.html|;
    /^[[:space:]]*[0-9]+ workers /d;
    /scheduling tests via/d;
    /^tests\/.*::/d;
    /^=+ short test summary info =+/,/^$/d
'

EXITCODE=${PIPESTATUS[0]}

echo "🧹 Tearing down…"
docker compose down

echo
echo "🏁 Report: file://$(realpath tests/artifacts/report.html)"
exit $EXITCODE
