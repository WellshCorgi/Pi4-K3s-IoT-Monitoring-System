#!/bin/bash
libcamera-vid -t 0 --inline --width 320 --height 320 --framerate 15 -o - | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264