#!/bin/bash

pip3 install -r requirements.txt --break-system-packages

python3 create_db.py

echo "END"
