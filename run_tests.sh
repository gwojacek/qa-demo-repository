#!/usr/bin/env bash
set -euo pipefail

export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)

BROWSER="chrome"   # supports: chrome | opera
MARKER=""
WORKERS="auto"
HEADLESS=true
RERUNS=1
VNC=false
VNC_PID=""
ENV_TYPE="local"

usage(){ cat <<EOF >&2
Usage: $0 [-b chrome|opera] [-m <marker>] [-n <workers>] [-r <reruns>] [-H] [-v] [-e <env_type>]
  -b    browser (chrome|opera), default=chrome
  -m    pytest marker
  -n    xdist workers, default=auto
  -r    reruns, default=1
  -H    disable headless
  -v    VNC mode (also disables headless & forces workers=1)
  -e    environment type (local|staging), default=local
EOF
exit 1; }

while getopts "b:m:n:r:He:v" opt; do
  case $opt in
    b) BROWSER="$OPTARG" ;;
    m) MARKER="$OPTARG" ;;
    n) WORKERS="$OPTARG" ;;
    r) RERUNS="$OPTARG" ;;
    H) HEADLESS=false ;;
    v) VNC=true; HEADLESS=false; WORKERS=1 ;;
    e) ENV_TYPE="$OPTARG" ;;
    *) usage ;;
  esac
done

cleanup() {
  echo "🛑 Cleaning up…"
  if [[ -n "$VNC_PID" && -n "$(ps -o pid= -p $VNC_PID 2>/dev/null)" ]]; then
    echo "🧼 Closing TigerVNC viewer (PID $VNC_PID)…"
    kill "$VNC_PID" || true
  fi
}
trap cleanup EXIT INT TERM

echo "🧹 Shutting down any old grid…"
docker compose down --remove-orphans

if [[ $BROWSER == "opera" ]]; then
  if $VNC; then
    SERVICE=selenium-opera-debug; WD_PORT=4449; VNC_PORT=5902
    SEL_URL="http://selenium-opera-debug:4444/wd/hub"
  else
    SERVICE=selenium-opera;       WD_PORT=4448
    SEL_URL="http://selenium-opera:4444/wd/hub"
  fi
else
  if $VNC; then
    SERVICE=selenium-chrome-debug;  WD_PORT=4445; VNC_PORT=5900
    SEL_URL="http://selenium-chrome-debug:4444/wd/hub"
  else
    SERVICE=selenium-chrome;        WD_PORT=4444
    SEL_URL="http://selenium-chrome:4444/wd/hub"
  fi
fi

echo "🚀 Starting $SERVICE…"
docker compose up -d "$SERVICE"

echo -n "⏳ Waiting for WebDriver at localhost:$WD_PORT"
until curl -sf "http://localhost:$WD_PORT/wd/hub/status" >/dev/null; do
  echo -n "."
  sleep 0.2
done
echo " ✅"

if $VNC; then
  printf "⏳ Waiting for VNC on localhost:$VNC_PORT…"
  until nc -z localhost $VNC_PORT; do
    printf "."
    sleep 0.2
  done
  echo " ✅ VNC ready!"
  sleep 2
  if [ -n "${DISPLAY-}" ]; then
    echo "🖼️ Launching TigerVNC viewer in fullscreen…"
    vncviewer -SecurityTypes None -FullScreen -Shared localhost:$VNC_PORT >/dev/null 2>&1 &
    VNC_PID=$!
  fi
fi

echo "🧹 Cleaning artifacts…"
rm -rf tests/artifacts && mkdir -p tests/artifacts

echo "📦 Building test-runner…"
docker compose build test-runner

PYTEST_ARGS=(-v --color=yes)
[ -n "$MARKER" ] && PYTEST_ARGS+=( -m "$MARKER" )
PYTEST_ARGS+=( -n "$WORKERS" --reruns "$RERUNS" --html=tests/artifacts/report.html --self-contained-html )

echo "🧪 Running pytest ($BROWSER, headless=$HEADLESS, VNC=$VNC, workers=$WORKERS, reruns=$RERUNS, env=$ENV_TYPE)…"
docker compose run --rm --no-deps \
  -e BROWSER="$BROWSER" \
  -e HEADLESS="$HEADLESS" \
  -e SELENIUM_REMOTE_URL="$SEL_URL" \
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
