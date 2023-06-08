#!/bin/env sh

REPO="signalapp/signal-desktop"
VERSION=$(./get-latest.sh)

echo Downloading version: $VERSION

mkdir SOURCES

wget https://github.com/${REPO}/archive/refs/tags/${VERSION}.tar.gz -O SOURCES/${VERSION}.tar.gz
