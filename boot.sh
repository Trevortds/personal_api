#!/bin/sh

chmod 777 /home/manager/data

flask db upgrade

python -m flask run --host=0.0.0.0
