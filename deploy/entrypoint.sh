#!/bin/sh
# Substitute TEST_WITH_AI_PORT in supervisord template and start supervisord.
# Default port 8088; override at runtime with -e TEST_WITH_AI_PORT=3000.
set -e
export TEST_WITH_AI_PORT="${TEST_WITH_AI_PORT:-8088}"
envsubst '${TEST_WITH_AI_PORT}' \
  < /etc/supervisor/conf.d/supervisord.conf.template \
  > /etc/supervisor/conf.d/supervisord.conf
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
