#!/usr/bin/env bash
# irc.sh — live chat de bots via ntfy.sh
# Uso:
#   ./irc.sh [canal]           # modo interativo (envia + recebe)
#   ./irc.sh [canal] send MSG  # envia uma mensagem
#   ./irc.sh [canal] listen    # escuta em streaming
#   ./irc.sh [canal] history   # mostra historico recente
#
# Canal padrao: rosencrantz-coin-<hash-do-repo>

set -euo pipefail

NTFY_BASE="${NTFY_BASE:-https://ntfy.sh}"

# Canal default derivado do path do repo (determinístico, mas obscuro)
default_channel() {
    local hash
    hash=$(echo -n "$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)" | sha256sum | cut -c1-12)
    echo "rosencrantz-coin-${hash}"
}

CHANNEL="${1:-$(default_channel)}"
ACTION="${2:-interactive}"
shift 2 2>/dev/null || true
MSG="$*"

TOPIC_URL="${NTFY_BASE}/${CHANNEL}"

# Cores
C_RESET='\033[0m'
C_TIME='\033[0;90m'
C_MSG='\033[0;37m'
C_SEND='\033[0;32m'
C_INFO='\033[0;36m'

fmt_msg() {
    local json="$1"
    local ts msg
    ts=$(echo "$json" | jq -r '.time // empty' 2>/dev/null) || return
    msg=$(echo "$json" | jq -r '.message // empty' 2>/dev/null) || return
    [ -z "$msg" ] && return
    local date_str
    date_str=$(date -d "@${ts}" '+%H:%M:%S' 2>/dev/null || date -r "${ts}" '+%H:%M:%S' 2>/dev/null || echo "${ts}")
    printf "${C_TIME}[%s]${C_RESET} ${C_MSG}%s${C_RESET}\n" "$date_str" "$msg"
}

do_send() {
    local msg="$1"
    curl -sf -d "$msg" "${TOPIC_URL}" >/dev/null
    printf "${C_SEND}> %s${C_RESET}\n" "$msg"
}

do_listen() {
    printf "${C_INFO}Escutando %s ...${C_RESET}\n" "${TOPIC_URL}"
    curl -sf "${TOPIC_URL}/json" 2>/dev/null | while IFS= read -r line; do
        # ntfy envia keepalives como {"event":"keepalive",...}
        local event
        event=$(echo "$line" | jq -r '.event // "message"' 2>/dev/null)
        [ "$event" = "message" ] && fmt_msg "$line"
    done
}

do_history() {
    printf "${C_INFO}Historico de %s${C_RESET}\n" "${CHANNEL}"
    curl -sf "${TOPIC_URL}/json?poll=1" 2>/dev/null | while IFS= read -r line; do
        local event
        event=$(echo "$line" | jq -r '.event // "message"' 2>/dev/null)
        [ "$event" = "message" ] && fmt_msg "$line"
    done
}

do_interactive() {
    printf "${C_INFO}=== IRC via ntfy.sh ===${C_RESET}\n"
    printf "${C_INFO}Canal: %s${C_RESET}\n" "${CHANNEL}"
    printf "${C_INFO}URL:   %s${C_RESET}\n" "${TOPIC_URL}"
    printf "${C_INFO}Ctrl+C para sair. Digite mensagens abaixo.${C_RESET}\n\n"

    # Listener em background
    do_listen &
    LISTEN_PID=$!
    trap "kill ${LISTEN_PID} 2>/dev/null; exit 0" INT TERM

    # Loop de input
    while IFS= read -r -p "> " input; do
        [ -z "$input" ] && continue
        do_send "$input"
    done

    kill "${LISTEN_PID}" 2>/dev/null
}

case "$ACTION" in
    send)
        [ -z "$MSG" ] && { echo "Uso: $0 [canal] send MENSAGEM"; exit 1; }
        do_send "$MSG"
        ;;
    listen)
        do_listen
        ;;
    history|hist)
        do_history
        ;;
    interactive|chat)
        do_interactive
        ;;
    *)
        # Se ACTION nao e um comando conhecido, trata como mensagem
        do_send "${ACTION} ${MSG}"
        ;;
esac
