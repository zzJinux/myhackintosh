#!/usr/bin/env bash

die() {
  printf '%s\n' "$1" >&2
  exit 1
}

show_help() {
  cat << EOF
Usage: ${0##*/} [-h] [--debug] {--baremetal|--kvm} DEST
EOF
}

debug=
type=
dest=
while :; do
  case $1 in
  -h)
    show_help
    exit;;
  --baremetal)
    type=baremetal
    ;;
  --kvm)
    type=kvm
    ;;
  --debug)
    debug=yes
    ;;
  *)
    dest=$1
    break;;
  esac
  shift
done

/usr/bin/env EFI_DEBUG=$debug python3 -m "$type".oc_efi "$dest"
