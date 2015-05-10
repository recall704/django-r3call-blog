#!/bin/bash
nohup gunicorn blogproject.wsgi:application -b 127.0.0.1:1010&
