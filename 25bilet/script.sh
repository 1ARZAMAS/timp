#!/bin/bash

# === Параметры подключения ===
REMOTE_USER="user"                      # имя пользователя
REMOTE_HOST="192.168.1.100"             # IP или домен удалённой машины
SSH_KEY_PATH="~/.ssh/id_rsa"            # путь к приватному ключу
LOG_FILE="ssh_output_$(date +%F_%T).log"  # лог-файл с датой

# === Команды для выполнения на удалённой машине ===
COMMANDS=$(cat <<EOF
echo "=== SYSTEM INFO ==="
uname -a
echo ""

echo "=== DISK USAGE ==="
df -h
echo ""

echo "=== /var/log LISTING ==="
ls -lh /var/log
EOF
)

# === Выполнение через SSH и сохранение в лог ===
echo "Connecting to $REMOTE_USER@$REMOTE_HOST..."
ssh -i "$SSH_KEY_PATH" "$REMOTE_USER@$REMOTE_HOST" "$COMMANDS" > "$LOG_FILE"

# === Вывод результата ===
echo "✅ Команды выполнены. Результат сохранён в $LOG_FILE"
