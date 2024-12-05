#!/bin/bash
python ./server.py &   # Avvia server.py in background
python ./altro_file.py  # Avvia un altro file Python
wait                       # Attende la terminazione di entrambi