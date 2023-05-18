#!bin/sh


if python3 -h &> /dev/null; then
    python3 src/main.py
else
    python src/main.py
fi

