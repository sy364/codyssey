#!/usr/bin/env bash

APP_PATTERN="agent-leak-app-arm64"
PORT="15034"
LOG_FILE="/var/log/agent-app/monitor-leak.log"

MAX_LOG_SIZE=$((10 * 1024 * 1024))
MAX_BACKUPS=9

echo "====== AGENT LEAK MONITOR ======"
echo

PID="$(pgrep -n -f -- "$APP_PATTERN")"

if [[ -z "$PID" ]]; then
    echo "Checking process '$APP_PATTERN'... [FAIL]"
    echo "[ERROR] Application process is not running."
    exit 1
fi

echo "Checking process '$APP_PATTERN'... [OK] (PID: $PID)"

if ss -ltn | grep -qE ":${PORT}[[:space:]]"; then
    echo "Checking port $PORT... [OK]"
else
    echo "Checking port $PORT... [WARNING]"
    echo "[WARNING] TCP port $PORT is not in LISTEN state."
fi

echo
echo "[PROCESS RESOURCE MONITORING]"

# 대상 프로세스의 CPU 사용률
CPU_USAGE="$(ps -p "$PID" -o %cpu= | awk '{printf "%.1f", $1}')"

# 대상 프로세스의 실제 물리 메모리(RSS), KB -> MB
MEM_USAGE="$(ps -p "$PID" -o rss= | awk '{printf "%.1f", $1 / 1024}')"

echo "PID       : $PID"
echo "CPU Usage : ${CPU_USAGE}%"
echo "MEM RSS   : ${MEM_USAGE}MB"

rotate_logs() {
    if [[ ! -f "$LOG_FILE" ]]; then
        return
    fi

    LOG_SIZE="$(stat -c %s "$LOG_FILE")"

    if (( LOG_SIZE < MAX_LOG_SIZE )); then
        return
    fi

    rm -f "${LOG_FILE}.${MAX_BACKUPS}"

    for ((i=MAX_BACKUPS-1; i>=1; i--)); do
        if [[ -f "${LOG_FILE}.${i}" ]]; then
            mv "${LOG_FILE}.${i}" "${LOG_FILE}.$((i + 1))"
        fi
    done

    mv "$LOG_FILE" "${LOG_FILE}.1"
}

rotate_logs

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

LOG_LINE="[$TIMESTAMP] PID:$PID CPU:${CPU_USAGE}% MEM_RSS:${MEM_USAGE}MB"

printf '%s\n' "$LOG_LINE" >> "$LOG_FILE"

echo
echo "[INFO] Log appended: $LOG_FILE"
