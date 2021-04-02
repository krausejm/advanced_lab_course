FILE=./results.txt
if test -f "$FILE"; then
    rm results.txt
fi
for f in ./datasets/*; do python3 gauge_fit.py "$f"; done
