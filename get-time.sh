TIME_IN_SECONDS=$(date "+%H*60*60 + %M*60 + %S")
EARLIEST_HOUR=5
LATEST_HOUR=21
(( $TIME_IN_SECONDS < $EARLIEST_HOUR*60*60 )) && $SCRIPTS_DIR/shutdown.sh now
(( $TIME_IN_SECONDS > $LATEST_HOUR*60*60 ))   && $SCRIPTS_DIR/shutdown.sh now
MINUTES_FOREWARNING=30
(( $TIME_IN_SECONDS > $LATEST_HOUR*60*60-$MINUTES_FOREWARNING*60 )) && notify-send -u Critical "The time is late. Shutdown imminent." -t 3000
date
