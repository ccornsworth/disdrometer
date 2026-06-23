#!/bin/bash
cd /workspaces/disdrometer/docs
jupyter nbconvert --execute --inplace source/data.ipynb
make clean html
git add .
git commit -m "Data Updated"
git push origin main
ghp-import -n -p -f build/html