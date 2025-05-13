#!/usr/bin/env bash
set -euo pipefail

export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)

BROWSER="chrome"
MARKER=""
WORKERS="auto"
HEADLESS=true
VNC=false

usage(){ cat <<EOF >&2
Usage: $0 [-b chrome|firefox] [-m <marker>] [-n <workers>] [-H] [-v]
  -b    browser (chrome|firefox), default=chrome
  -m    pytest marker
  -n    xdist workers, default=auto
  -H    disable headless
  -v    VNC mode (also disables headless & forces workers=1)
EOF
exit 1; }

while getopts "b:m:n:Hv" opt; do
  case $opt in
    b) BROWSER="$OPTARG" ;;
    m) MARKER="$OPTARG" ;;
    n) WORKERS="$OPTARG" ;;
    H) HEADLESS=false ;;
    v) VNC=true; HEADLESS=false; WORKERS=1 ;;
    *) usage ;;
  esac
done

echo "🧹 Cleaning up any old grid…"
docker compose down --remove-orphans

# pick the right service + ports
if [[ $BROWSER == "firefox" ]]; then
  if $VNC; then
    SERVICE=selenium-firefox-debug; WD_PORT=4447; VNC_PORT=5901
    SEL_URL="http://selenium-firefox-debug:4444/wd/hub"
  else
    SERVICE=selenium-firefox;       WD_PORT=4446
    SEL_URL="http://selenium-firefox:4444/wd/hub"
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

echo -n "⏳ Connecting to WebDriver at localhost:$WD_PORT"
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

  # give X session a moment to finish booting
  sleep 2

  if [ -n "${DISPLAY-}" ]; then
    echo "🖼️ Launching TigerVNC viewer in fullscreen…"
    vncviewer \
      -SecurityTypes None \
      -FullScreen \
      -Shared \
      localhost:$VNC_PORT \
      >/dev/null 2>&1 &
  fi
fi

echo "🧹 Cleaning old artifacts…"
rm -rf tests/artifacts && mkdir -p tests/artifacts

echo "📦 Building test-runner image…"
docker compose build test-runner

# assemble pytest args
PYTEST_ARGS=(-v --color=yes)
[ -n "$MARKER" ] && PYTEST_ARGS+=( -m "$MARKER" )
PYTEST_ARGS+=( -n "$WORKERS" --html=tests/artifacts/report.html)

echo "🧪 Running pytest on '$BROWSER' (headless=$HEADLESS, VNC=$VNC)…"
docker compose run --rm --no-deps \
  -e BROWSER="$BROWSER" \
  -e HEADLESS="$HEADLESS" \
  -e SELENIUM_REMOTE_URL="$SEL_URL" \
  --entrypoint pytest \
  test-runner \
  "${PYTEST_ARGS[@]}" 2>&1 | sed -E '
    s|file:///app/tests/artifacts/report.html|file://'"$PWD"'/tests/artifacts/report.html|;
    /^[[:space:]]*[0-9]+ workers /d;
    /scheduling tests via/d;
    /^tests\/.*::/d;
    /^=+ short test summary info =+/,/^$/d
'

EXITCODE=${PIPESTATUS[0]}

 echo "🧹 Tearing down grid…"
 docker compose down

 echo
 echo "🏁 Report: file://$(realpath tests/artifacts/report.html)"
 exit $EXITCODE

