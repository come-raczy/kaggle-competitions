#!/usr/bin/env bash

# Split the training data into chunks of LINES lines each
#TOTAL="${TOTAL:-$(wc -l < train.csv)}"
CHUNK_SIZE="${CHUNK_SIZE:-6000000}"
TRAIN_CSV="${TRAIN_CSV:-train.csv}"
# note that the first line of train.csv is the header and is skipped
#CHUNKS=$(((TOTAL + CHUNK_SIZE - 2) / CHUNK_SIZE))
#echo "Splitting $TOTAL lines from $TRAIN_CSV into $CHUNKS chunks of $CHUNK_SIZE lines each"
echo "Splitting $TRAIN_CSV into chunks of $CHUNK_SIZE lines each"

tail -n +2 "$TRAIN_CSV" | split -d -l "$CHUNK_SIZE"  --additional-suffix=.csv - train_

#remaining=$((TOTAL - 1))

#for i in $(seq 1 $CHUNKS); do
#  suffix=$(printf "%02d" $i)
#  top_count=$((1 + i * CHUNK_SIZE))
#  top_count=$(( top_count > TOTAL ? TOTAL : top_count ))
#  tail_count=$((remaining > CHUNK_SIZE ? CHUNK_SIZE : remaining))
#  remaining=$((remaining - tail_count))
#  echo $suffix: top_count=$top_count tail_count=$tail_count
#  head -n $top_count train.csv | tail -n $tail_count > train_$suffix.csv
#done
