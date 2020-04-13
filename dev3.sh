#!/bin/bash

killall -q eom
rm -f ~/diff3.png
compare -fuzz 1% -compose src -highlight-color blue -lowlight-color none ~/2.png ~/3.png ~/diff3.png
composite ~/diff3.png ~/2.png ~/diff3.png
eom ~/diff3.png &
