#!/bin/bash
# This is for debian-based only
# NOTE:
#  This downloading script is for testing purpose only
#  The real package should handle this for the users...
./install -v --download-only --tag stable --directory . systemconfigurator \
systemimager-client systemimager-common \
systemimager-boot-i386-standard systemimager-initrd-template-i386 \
systemimager-server systemimager-server-bittorrent systemimager-server-flamethrowerd
