#!/bin/bash

####
# Usage:
#   Change vars below
#   Execute
###

player_server="https://10.1.2.3"
rcp_secret="change_me"
rsync_path="bbb-player:/var/bigbluebutton/todo/"

# Do not touch!
meeting_id=$1
published_files="/var/bigbluebutton/published/presentation/$meeting_id/"

rsync -a "$published_files" $rsync_path"/$meeting_id"
curl -H "Content-Type: application/json" -d '{"internalMeetingId": "'$meeting_id'", "checksum": "'$(python3 -c "import rc_protocol; print(rc_protocol.get_checksum({\"internalMeetingId\": \"$meeting_id\"}, \"$rcp_secret\", \"updatePublishState\"))")'"}' "$player_server/api/v1/updatePublishState"

# Delete files locally
rm -r "$published_files"
