#!/bin/env sh

REPO="$1"
VERSION=$(./get-latest.sh $1)

echo Downloading version: $VERSION $(pwd)

mkdir SOURCES

wget https://github.com/${REPO}/archive/refs/tags/${VERSION}.tar.gz -O SOURCES/${VERSION}.tar.gz
