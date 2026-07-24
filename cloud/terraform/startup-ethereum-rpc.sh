#!/usr/bin/env bash
set -euo pipefail
apt-get update
apt-get install -y docker.io
systemctl enable docker
systemctl start docker
mkdir -p /opt/cognira-eth
cat >/opt/cognira-eth/docker-compose.yml <<'YAML'
services:
  geth:
    image: ethereum/client-go:stable
    restart: always
    command:
      - --http
      - --http.addr=0.0.0.0
      - --http.port=8545
      - --http.api=eth,net,web3,txpool
      - --http.vhosts=*
      - --ws
      - --ws.addr=0.0.0.0
      - --ws.port=8546
      - --ws.api=eth,net,web3
      - --syncmode=snap
      - --cache=2048
    ports:
      - "8545:8545"
      - "8546:8546"
      - "30303:30303"
    volumes:
      - geth-data:/root/.ethereum
volumes:
  geth-data:
YAML
cd /opt/cognira-eth
docker compose up -d || docker run -d --restart always --name geth -p 8545:8545 -p 8546:8546 -p 30303:30303 ethereum/client-go:stable --http --http.addr=0.0.0.0 --http.port=8545 --http.api=eth,net,web3,txpool --http.vhosts='*' --ws --ws.addr=0.0.0.0 --ws.port=8546 --ws.api=eth,net,web3 --syncmode=snap --cache=2048
