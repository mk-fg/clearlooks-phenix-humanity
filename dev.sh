#!/bin/bash

killall -q eom
rm -f ~/diff.png
compare -fuzz 1% -compose src -highlight-color blue -lowlight-color none ~/2.png ~/3.png ~/diff.png
composite ~/diff.png ~/2.png ~/diff.png
eom ~/diff.png &
