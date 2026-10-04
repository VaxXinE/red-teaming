#!/bin/sh
set -eu
/usr/sbin/cron
exec tail -f /dev/null
