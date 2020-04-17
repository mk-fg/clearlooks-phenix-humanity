#!/bin/bash

killall -q eom
rm -f ~/diff4.png
compare -fuzz 1% -compose src -highlight-color blue -lowlight-color none ~/2.png ~/4.png ~/diff4.png
composite ~/diff4.png ~/2.png ~/diff4.png
eom ~/diff4.png &