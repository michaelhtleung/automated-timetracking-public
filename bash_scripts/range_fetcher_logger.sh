#!/bin/bash

#for ((i=$2; i >= $1; i--)); do
for ((i=$1; i <= $2; i++)); do
	python fetcher_logger.py -$i
done
