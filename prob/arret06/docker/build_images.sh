#!/bin/bash
docker build -f Dockerfile.client -t a6-client:latest .
docker build -f Dockerfile.gestionnaire -t a6-gestionnaire:latest .
docker build -f Dockerfile.serveur -t a6-serveur:latest .
