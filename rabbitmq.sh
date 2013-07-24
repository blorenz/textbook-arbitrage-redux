#!/bin/sh
# call "rabbitmqctl stop" when exiting
trap "{ echo Stopping rabbitmq; rabbitmqctl stop; exit 0; }" EXIT

echo Starting rabbitmq
rabbitmq-server