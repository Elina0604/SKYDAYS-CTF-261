#!/usr/bin/env bash
set -euo pipefail

# Small TUI for managing Bind9 zones and records.
# Provides: Add Domain (create zone + stanza) and Add Subdomain (add record to existing zone).
# Uses whiptail for UI. Defaults to /etc/bind but will use the BIND_DIR you enter.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_ZONE="${SCRIPT_DIR}/db.domain.tld"
TMP_BACKUP_DIR="/tmp/bind9-tui-backups-$(date +%s)"
BIND_DIR=""

cleanup() {
  local exit_code=$?
  if [ -n "$TMP_BACKUP_DIR" ] && [ -d "$TMP_BACKUP_DIR" ]; then
    rm -rf "$TMP_BACKUP_DIR" 2>/dev/null || true
  fi
  rm -f /tmp/named-checkzone.out 2>/dev/null || true
  exit $exit_code
}
trap cleanup EXIT INT TERM

err() { echo "ERROR: $*" >&2; }

validate_domain() {
  local domain="$1"
  if [[ ! "$domain" =~ ^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$ ]]; then
    return 1
  fi
  return 0
}

validate_ip() {
  local ip="$1"
  if [[ "$ip" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    local IFS='.'
    read -ra OCTETS <<< "$ip"
    for octet in "${OCTETS[@]}"; do
      if (( octet > 255 )); then
        return 1
      fi
    done
    return 0
  elif [[ "$ip" =~ ^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$ ]] || [[ "$ip" == "::1" ]]; then
    return 0
  fi
  return 1
}

command_exists() { command -v "$1" >/dev/null 2>&1; }

ensure_deps() {
  local miss=()
  for c in whiptail named-checkconf named-checkzone; do
    if ! command_exists "$c"; then
      miss+=("$c")
    fi
  done
  if [ ${#miss[@]} -ne 0 ]; then
    whiptail --title "Missing dependencies" --msgbox \
      "Missing: ${miss[*]}\nOn Debian/Ubuntu: sudo apt install whiptail bind9utils bind9" 12 60
    exit 1
  fi
}

backup() {
  mkdir -p "$TMP_BACKUP_DIR"
  if [ -e "$1" ]; then
    cp -a "$1" "$TMP_BACKUP_DIR/" || err "Failed to backup $1"
  fi
}

find_zone_file() {
  local domain="$1"; local named_local="$2"
  if [ ! -f "$named_local" ]; then
    echo ""
    return
  fi
  local file
  file=$(awk "/zone[[:space:]]+\"${domain}\"/{f=1} f && /file/{gsub(/.*file[[:space:]]*\"|\".*/,"",\$0); print; exit}" "$named_local" || true)
  echo "$file"
}

add_zone_stanza() {
  local domain="$1" zonefile="$2" named_local="$3"
  if grep -qE "zone[[:space:]]+\"${domain}\"" "$named_local" 2>/dev/null; then
    whiptail --msgbox "Zone stanza for ${domain} already exists in ${named_local}." 8 60
    return 1
  fi
  backup "$named_local"
  cat >>"$named_local" <<EOF

zone "${domain}" {
    type master;
    file "${zonefile}";
};
EOF
  return 0
}

create_zone_from_template() {
  local target="$1" domain="$2" ip_ns="$3" ip_at="$4"
  if [ -f "$TEMPLATE_ZONE" ]; then
    cp "$TEMPLATE_ZONE" "$target" || { err "Failed to copy template"; return 1; }
    sed -i.bak -e "s|<gateway-ip>|${ip_ns}|g" -e "s|<target-host-ip>|${ip_at}|g" "$target" 2>&1 | while read -r line; do err "sed warning: $line"; done || true
    rm -f "${target}.bak" || true
  else
    cat >"$target" <<EOF
$TTL 86400
@   IN  SOA ns.${domain}. admin.${domain}. (
        $(date +%Y%m%d)01  ; Serial
        3600        ; Refresh
        1800        ; Retry
        604800      ; Expire
        86400 )     ; Minimum TTL

    IN  NS  ns.${domain}.
ns  IN  A   ${ip_ns}
@   IN  A   ${ip_at}
EOF
  fi
  chmod 644 "$target" || err "Failed to set permissions on $target"
}

increment_serial() {
  local zonefile="$1"
  local serial
  serial=$(grep -oE '[0-9]{8}[0-9]{2}' "$zonefile" | head -n1 || true)
  if [ -n "$serial" ]; then
    local today=$(date +%Y%m%d)
    local prefix=${serial:0:8}
    local suffix=${serial:8:2}
    if [ "$prefix" = "$today" ]; then
      local next=$((10#$suffix + 1))
      printf -v nextp "%02d" "$next"
      local newserial="${today}${nextp}"
    else
      local newserial="${today}01"
    fi
    local escaped_serial=$(printf '%s' "$serial" | sed 's/[][.*^$/\\&]/\\&/g')
    local escaped_newserial=$(printf '%s' "$newserial" | sed 's/[][.*^$/\\&]/\\&/g')
    sed -i.bak "s/${escaped_serial}/${escaped_newserial}/" "$zonefile" && rm -f "${zonefile}.bak"
    return 0
  fi
  serial=$(awk '/SOA/{p=1;next} p && /;/{exit} p{for(i=1;i<=NF;i++) if ($i ~ /^[0-9]+$/) {print $i; exit}}' "$zonefile" | head -n1 || true)
  if [ -n "$serial" ]; then
    local newserial=$((serial + 1))
    local escaped_serial=$(printf '%s' "$serial" | sed 's/[][.*^$/\\&]/\\&/g')
    local escaped_newserial=$(printf '%s' "$newserial" | sed 's/[][.*^$/\\&]/\\&/g')
    sed -i.bak "s/${escaped_serial}/${escaped_newserial}/" "$zonefile" && rm -f "${zonefile}.bak"
    return 0
  fi
  err "Could not find serial number in $zonefile"
  return 1
}

add_record() {
  local zonefile="$1" name="$2" type="$3" value="$4" ttl="$5"
  local line
  if [ -z "$name" ] || [ "$name" = "@" ]; then
    line="@"
  else
    line="$name"
  fi
  if [ -n "$ttl" ]; then
    line="$line $ttl"
  fi
  line="$line IN $type $value"
  echo "$line" >>"$zonefile"
  increment_serial "$zonefile" || err "Failed to increment serial"
}

reload_bind_service() {
  local svc_name=""
  local try_sudo="${1:-false}"
  
  if command_exists systemctl; then
    for svc in bind9 named; do
      if $try_sudo; then
        if sudo systemctl is-active "$svc" >/dev/null 2>&1; then
          svc_name="$svc"
          break
        fi
      else
        if systemctl is-active "$svc" >/dev/null 2>&1; then
          svc_name="$svc"
          break
        fi
      fi
    done
    
    if [ -n "$svc_name" ]; then
      if $try_sudo; then
        sudo systemctl reload "$svc_name" && return 0 || return 1
      else
        systemctl reload "$svc_name" && return 0 || return 1
      fi
    fi
    
    if $try_sudo; then
      for svc in bind9 named; do
        if sudo systemctl reload "$svc" 2>/dev/null; then
          return 0
        fi
      done
    else
      for svc in bind9 named; do
        if systemctl reload "$svc" 2>/dev/null; then
          return 0
        fi
      done
    fi
  fi
  
  if command_exists service; then
    service bind9 reload 2>/dev/null && return 0
    service named reload 2>/dev/null && return 0
  fi
  
  return 1
}

validate_zone_and_reload() {
  local domain="$1" zonefile="$2" named_local="$3"
  if ! named-checkzone "$domain" "$zonefile" >/tmp/named-checkzone.out 2>&1; then
    local out; out=$(cat /tmp/named-checkzone.out)
    whiptail --title "named-checkzone failed" --msgbox "$out" 12 70
    return 1
  fi
  if whiptail --yesno "Validation OK. Reload bind9 now?" 8 60; then
    if reload_bind_service; then
      whiptail --msgbox "bind9 reloaded" 6 40
    elif reload_bind_service true; then
      whiptail --msgbox "bind9 reloaded (with sudo)" 6 40
    else
      whiptail --msgbox "Reload failed. Try manually: sudo systemctl reload bind9" 8 50
    fi
  fi
  return 0
}

select_bind_dir() {
  local d
  d=$(whiptail --inputbox "Bind configuration directory" 8 60 "/etc/bind" 3>&1 1>&2 2>&3) || exit 0
  BIND_DIR="$d"
  if [ ! -d "$BIND_DIR" ]; then
    if whiptail --yesno "${BIND_DIR} not found. Create?" 8 60; then
      mkdir -p "$BIND_DIR" || { err "Failed to create $BIND_DIR"; exit 1; }
    else
      err "Bind dir missing"; exit 1
    fi
  fi
}

flow_add_domain() {
  local domain ip_ns ip_at zonefile named_local
  domain=$(whiptail --inputbox "Domain (example: example.tld)" 8 60 3>&1 1>&2 2>&3) || return
  domain=$(echo "$domain" | tr -d '[:space:]')
  [ -z "$domain" ] && whiptail --msgbox "No domain" 6 40 && return
  
  if ! validate_domain "$domain"; then
    whiptail --msgbox "Invalid domain name: $domain" 8 50
    return
  fi
  
  ip_ns=$(whiptail --inputbox "IP for ns.${domain}" 8 60 "127.0.0.1" 3>&1 1>&2 2>&3) || return
  if ! validate_ip "$ip_ns"; then
    whiptail --msgbox "Invalid IP address: $ip_ns" 8 50
    return
  fi
  
  ip_at=$(whiptail --inputbox "IP for @ A record" 8 60 "$ip_ns" 3>&1 1>&2 2>&3) || return
  if ! validate_ip "$ip_at"; then
    whiptail --msgbox "Invalid IP address: $ip_at" 8 50
    return
  fi
  
  zonefile="${BIND_DIR}/db.${domain}"
  zonefile=$(whiptail --inputbox "Zone file path" 8 70 "$zonefile" 3>&1 1>&2 2>&3) || return
  named_local="${BIND_DIR}/named.conf.local"
  if [ -f "$zonefile" ]; then
    if ! whiptail --yesno "${zonefile} exists. Overwrite?" 8 60; then
      whiptail --msgbox "Cancelled" 6 40; return
    fi
    backup "$zonefile"
  fi
  
  if ! create_zone_from_template "$zonefile" "$domain" "$ip_ns" "$ip_at"; then
    whiptail --msgbox "Failed to create zone file" 8 50
    return
  fi
  
  if ! add_zone_stanza "$domain" "$zonefile" "$named_local"; then
    whiptail --msgbox "Failed to add zone stanza. Check permissions." 8 50
    return
  fi
  
  whiptail --msgbox "Zone file created: ${zonefile}\nStanza appended to ${named_local}" 10 70
  validate_zone_and_reload "$domain" "$zonefile" "$named_local"
}

flow_add_subdomain() {
  local domain named_local zonefile name type val ttl
  domain=$(whiptail --inputbox "Zone (domain) to modify (example: skydays.ctf)" 8 60 3>&1 1>&2 2>&3) || return
  domain=$(echo "$domain" | tr -d '[:space:]')
  [ -z "$domain" ] && whiptail --msgbox "No domain" 6 40 && return
  
  if ! validate_domain "$domain"; then
    whiptail --msgbox "Invalid domain name: $domain" 8 50
    return
  fi
  
  named_local="${BIND_DIR}/named.conf.local"
  zonefile=$(find_zone_file "$domain" "$named_local")
  if [ -z "$zonefile" ]; then
    zonefile=$(whiptail --inputbox "Could not find zonefile for ${domain}. Enter path or create new:" 10 70 "${BIND_DIR}/db.${domain}" 3>&1 1>&2 2>&3) || return
    if [ ! -f "$zonefile" ]; then
      if whiptail --yesno "Zonefile does not exist. Create minimal zone file?" 8 60; then
        local ip
        ip=$(whiptail --inputbox "IP for @ and ns" 8 60 "127.0.0.1" 3>&1 1>&2 2>&3) || return
        if ! validate_ip "$ip"; then
          whiptail --msgbox "Invalid IP address: $ip" 8 50
          return
        fi
        if ! create_zone_from_template "$zonefile" "$domain" "$ip" "$ip"; then
          whiptail --msgbox "Failed to create zone file" 8 50
          return
        fi
        if ! add_zone_stanza "$domain" "$zonefile" "$named_local"; then
          whiptail --msgbox "Failed to add zone stanza. Check permissions." 8 50
          return
        fi
      else
        whiptail --msgbox "Cancelled" 6 40; return
      fi
    fi
  fi
  whiptail --msgbox "Using zonefile: ${zonefile}" 8 60
  name=$(whiptail --inputbox "Record name (subdomain). Use @ for apex" 8 60 "www" 3>&1 1>&2 2>&3) || return
  type=$(whiptail --menu "Record type" 12 50 5 A "A (IPv4)" AAAA "AAAA" CNAME "CNAME" TXT "TXT" MX "MX" 3>&1 1>&2 2>&3) || return
  case "$type" in
    A) val=$(whiptail --inputbox "IPv4 for ${name}.${domain}" 8 60 "10.0.0.2" 3>&1 1>&2 2>&3) || return
       if ! validate_ip "$val"; then
         whiptail --msgbox "Invalid IPv4 address: $val" 8 50
         return
       fi
       ;;
    AAAA) val=$(whiptail --inputbox "IPv6 for ${name}.${domain}" 8 60 "::1" 3>&1 1>&2 2>&3) || return
       if ! validate_ip "$val"; then
         whiptail --msgbox "Invalid IPv6 address: $val" 8 50
         return
       fi
       ;;
    CNAME) val=$(whiptail --inputbox "CNAME target (fully qualified)" 8 60 "target.${domain}." 3>&1 1>&2 2>&3) || return ;;
    TXT) val=$(whiptail --inputbox "TXT content" 8 60 "hello" 3>&1 1>&2 2>&3) || return ;;
    MX) val=$(whiptail --inputbox "MX (priority target) e.g. 10 mail.${domain}." 10 70 "10 mail.${domain}." 3>&1 1>&2 2>&3) || return ;;
  esac
  ttl=$(whiptail --inputbox "TTL (leave blank for default)" 8 40 "" 3>&1 1>&2 2>&3) || return
  backup "$zonefile"
  add_record "$zonefile" "$name" "$type" "$val" "$ttl"
  whiptail --msgbox "Record added to ${zonefile}" 8 60
  validate_zone_and_reload "$domain" "$zonefile" "$named_local"
}

show_named_conf() {
  if [ -f "${BIND_DIR}/named.conf.local" ]; then
    whiptail --textbox "${BIND_DIR}/named.conf.local" 30 100
  else
    whiptail --msgbox "${BIND_DIR}/named.conf.local not found" 8 50
  fi
}

main_menu() {
  while true; do
    CHOICE=$(whiptail --title "Bind9 TUI" --menu "Select action" 15 60 6 \
      1 "Add Domain" \
      2 "Add Subdomain / Record" \
      3 "Show named.conf.local" \
      4 "Exit" 3>&1 1>&2 2>&3) || exit 0
    case "$CHOICE" in
      1) flow_add_domain ;;
      2) flow_add_subdomain ;;
      3) show_named_conf ;;
      4) exit 0 ;;
    esac
  done
}

ensure_deps
select_bind_dir
mkdir -p "$TMP_BACKUP_DIR"
whiptail --msgbox "Backups will be stored in $TMP_BACKUP_DIR. Template zone: $TEMPLATE_ZONE" 8 70
main_menu
