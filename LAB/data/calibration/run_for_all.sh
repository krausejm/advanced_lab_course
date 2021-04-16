FILE=./results.txt
if test -f "$FILE"; then
    rm results.txt
fi
for f in ./align_data/*; do python3 calibration.py "$f"; done
