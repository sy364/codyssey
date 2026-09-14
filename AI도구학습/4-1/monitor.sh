#!/usr/bin/env bash

CPU_THRESHOLD="20"
MEM_THRESHOLD="10"
DISK_THRESHOLD="80"
APP_PATTERN="agent-app-linux-arm64"
PORT="15034"
LOG_FILE="/var/log/agent-app/monitor.log"
MAX_LOG_SIZE=$((10 * 1024 * 1024))
MAX_BACKUPS=9

echo "====== SYSTEM MONITOR RESULT ======"
echo
echo "[HEALTH CHECK]"

PID="$(pgrep -o -f -- "$APP_PATTERN")"

if [[ -z "$PID" ]]; then
    echo "Checking process '$APP_PATTERN'... [FAIL]"
    echo "[ERROR] Application process is not running."
    exit 1
fi

echo "Checking process '$APP_PATTERN'... [OK] (PID: $PID)"

if ! ss -ltn | grep -qE ":${PORT}[[:space:]]"; then
    echo "Checking port $PORT... [FAIL]"
    echo "[ERROR] TCP port $PORT is not in LISTEN state."
    exit 1
fi

echo "Checking port $PORT... [OK]"

if systemctl is-active --quiet ufw \
    && grep -q '^ENABLED=yes' /etc/ufw/ufw.conf; then
    echo "Checking firewall UFW... [OK]"
else
    echo "Checking firewall UFW... [WARNING]"
    echo "[WARNING] UFW firewall is not active."
fi

echo
echo "[RESOURCE MONITORING]"

CPU_USAGE="$(vmstat 1 2 | tail -1 | awk '{printf "%.1f", 100 - $15}')"

MEM_USAGE="$(free | awk '/Mem:/ {
    printf "%.1f", (($2 - $7) / $2) * 100
}')"

DISK_USAGE="$(df -P / | awk 'NR==2 {
    gsub("%", "", $5)
    print $5
}')"

echo "CPU Usage : ${CPU_USAGE}%"
echo "MEM Usage : ${MEM_USAGE}%"
echo "DISK Used : ${DISK_USAGE}%"
echo

if awk -v value="$CPU_USAGE" -v limit="$CPU_THRESHOLD" \
    'BEGIN { exit !(value > limit) }'; then
    echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"
fi

if awk -v value="$MEM_USAGE" -v limit="$MEM_THRESHOLD" \
    'BEGIN { exit !(value > limit) }'; then
    echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_THRESHOLD}%)"
fi

if awk -v value="$DISK_USAGE" -v limit="$DISK_THRESHOLD" \
    'BEGIN { exit !(value > limit) }'; then
    echo "[WARNING] DISK threshold exceeded (${DISK_USAGE}% > ${DISK_THRESHOLD}%)"
fi

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
    echo "[INFO] Log rotated: ${LOG_FILE}.1"
}

rotate_logs

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
LOG_LINE="[$TIMESTAMP] PID:$PID CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USAGE}%"

printf '%s\n' "$LOG_LINE" >> "$LOG_FILE"

echo
echo "[INFO] Log appended: $LOG_FILE"
