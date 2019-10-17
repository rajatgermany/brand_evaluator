#!/usr/bin/env bash

cd frontend
npm install 
npm run build
cd ..
docker-compose up --build
