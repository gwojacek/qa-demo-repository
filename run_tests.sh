#!/usr/bin/env bash
set -euo pipefail

export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)

echo "🚀 Starting Selenium Grid..."
docker compose up -d selenium

echo -n "⏳ Waiting for Grid readiness…"
until curl -sSL "http://localhost:4444/wd/hub/status" \
       | jq -e '.value.ready == true' >/dev/null; do
    printf "."
    sleep 0.2
done
echo " ✅ Grid is ready!"

echo "🧹 Cleaning artifacts…"
rm -rf tests/artifacts
mkdir -p tests/artifacts



echo "📦 Building test-runner…"
docker compose build test-runner

# parse -m <marker> and -n <workers>
MARKER=""
WORKERS="auto"
while getopts "m:n:" opt; do
  case "$opt" in
    m) MARKER="$OPTARG" ;;
    n) WORKERS="$OPTARG" ;;
    *)
      echo "Usage: $0 [-m <marker>] [-n <workers>]" >&2
      exit 1
      ;;
  esac
done

# assemble pytest args
PYTEST_ARGS=(
  -v
  --color=yes
)
[[ -n $MARKER ]] && PYTEST_ARGS+=( -m "$MARKER" )
PYTEST_ARGS+=(
  -n "$WORKERS"
  --html=tests/artifacts/report.html  # ✅ correct location
)

echo "🧪 Running pytest ${PYTEST_ARGS[*]}…"
docker compose run --rm \
  --entrypoint pytest \
  test-runner \
  "${PYTEST_ARGS[@]}" 2>&1 | sed -E '
    # rewrite the html‐report URI to your host‐side path
    s|file:///app/tests/artifacts/report.html|file://'"$PWD"'/tests/artifacts/report.html|g;

    # drop xdist startup noise
    /^[[:space:]]*[0-9]+ workers \[.*\]/d;
    /scheduling tests via/d;

    # drop raw collection listings
    /^tests\/.*::/d;
'

EXITCODE=${PIPESTATUS[0]}

echo "🧹 Tearing down…"
docker compose down

HOST_REPORT_PATH="$(realpath tests/artifacts/report.html)"

echo
echo "----------- Generated html report: file://$HOST_REPORT_PATH -----------"
echo

exit $EXITCODE