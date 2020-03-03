ffmpeg -i /dev/video0 -f mpegts -r 20 -s 640X480 udp://192.168.43.158:8009 &
ffmpeg -i /dev/video1 -f mpegts -r 20 -s 640X480 udp://192.168.43.158:8010 &
ffmpeg -i /dev/video3 -f mpegts -r 20 -s 640X480 udp://192.168.43.158:8011



