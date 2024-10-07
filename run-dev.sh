#! /usr/bin/env bash

docker run --rm --entrypoint="" -it --name="cycle-calc" -v ./cycle-calc:/code cycle-calc:latest sh -c 'while /bin/true; do sleep 5; done'
