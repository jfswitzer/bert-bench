#!/usr/bin/env bash
END=$(($1-1))
echo $END
for i in $(seq 0 $END)
do
	 taskset -c $i ./run_bench.sh $i $END &
done
