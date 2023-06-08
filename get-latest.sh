#!/bin/env sh

REPO="signalapp/signal-desktop"
GITHUB_API_VERSION="2022-11-28"

curl -sL  \
	-H "Accept: application/vnd.github+json" \
	-H "X-GitHub-Api-Version: ${GITHUB_API_VERSION}" \
	https://api.github.com/repos/${REPO}/releases/latest | jq ".tag_name" | sed 's/\"//g'

