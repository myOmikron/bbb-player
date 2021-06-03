#!/usr/bin/ruby

require "trollop"
require File.expand_path('../../../lib/recordandplayback', __FILE__)

opts = Trollop::options do
  opt :meeting_id, "Meeting id to archive", :type => String
  opt :format, "Playback format name", :type => String
end
meeting_id = opts[:meeting_id]

system("/bin/bash /usr/local/bigbluebutton/core/scripts/post_publish/moveRecording.sh " + meeting_id)

exit 0
