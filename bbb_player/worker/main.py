#!/usr/bin/env python3
import argparse
import os
import shutil
from xml.etree import ElementTree

bbb_dir = "/var/bigbluebutton/"
working_dir = os.path.join(bbb_dir, "todo")
dest_dir = os.path.join(bbb_dir, "published", "presentation")


def create_recording_xml(args):
    tree = ElementTree.parse(os.path.join(working_dir, "metadata.xml"))
    root = tree.getroot()

    recording = ElementTree.Element("recording")
    recordingID = ElementTree.SubElement(recording, "recordingID")
    recordingID.text = root.find("id").text
    meetingID = ElementTree.SubElement(recording, "meetingID")
    meetingID.text = root.find("meeting").attrib["externalId"]
    internalMeetingID = ElementTree.SubElement(recording, "internalMeetingID")
    internalMeetingID.text = recordingID.text
    name = ElementTree.SubElement(recording, "name")
    name.text = root.find("meeting").attrib["name"]
    published = ElementTree.SubElement(recording, "published")
    published.text = root.find("published").text
    state = ElementTree.SubElement(recording, "state")
    state.text = root.find("state").text
    startTime = ElementTree.SubElement(recording, "startTime")
    startTime.text = root.find("start_time").text
    endTime = ElementTree.SubElement(recording, "endTime")
    endTime.text = root.find("end_time").text
    participants = ElementTree.SubElement(recording, "participants")
    participants.text = root.find("participants").text
    ElementTree.SubElement(recording, "metadata")
    playback = ElementTree.SubElement(recording, "playback")
    format = ElementTree.SubElement(playback, "format")
    typee = ElementTree.SubElement(format, "type")
    typee.text = root.find("playback/format").text
    url = ElementTree.SubElement(format, "url")
    url.text = f"https://{args.hostname}/playback/presentation/2.3/{args.internal_meeting_id}"
    processingTime = ElementTree.SubElement(format, "processingTime")
    processingTime.text = root.find("playback/processing_time").text
    length = ElementTree.SubElement(format, "length")
    length.text = str(int(int(root.find("playback/duration").text)/1000//60))
    size = ElementTree.SubElement(format, "size")
    size.text = root.find("playback/size").text
    preview = ElementTree.SubElement(format, "preview")
    images = ElementTree.SubElement(preview, "images")
    old_img = root.findall("playback/extensions/preview/images/image")
    for img in old_img:
        image = ElementTree.SubElement(images, "image")
        image.attrib["alt"] = img.attrib["alt"]
        image.attrib["height"] = img.attrib["height"]
        image.attrib["width"] = img.attrib["width"]
        url = img.text.lstrip("http://").lstrip("https://").split("/")[1:]
        image.text = f"https://{args.hostname}/{url}"

    # Save XML
    ElementTree.ElementTree(recording).write(os.path.join(working_dir, "recording.xml"))


def move_files():
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copy(working_dir, dest_dir)
    shutil.rmtree(working_dir)


def main(args):
    create_recording_xml(args)
    move_files()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--internalMeetingId",
        action="store",
        dest="internal_meeting_id",
        help="Internal Meeting Id to Process"
    )
    parser.add_argument(
        "-H", "--hostname",
        action="store",
        dest="hostname",
        help="Hostname of the player"
    )
    conf = parser.parse_args()
    working_dir = os.path.join(working_dir, conf.internal_meeting_id)
    dest_dir = os.path.join(dest_dir, conf.internal_meeting_id)
    main(conf)
