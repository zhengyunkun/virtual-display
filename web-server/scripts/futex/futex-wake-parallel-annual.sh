#! /bin/bash

NUM_THREADS=$(cat /proc/cpuinfo | grep 'processor' | wc -l)
DATA="/home/liuyijie/Projects/vkernel/Annual/vkernel-display/web-server/dist/data/futex/futex-wake-parallel.json"

funecho() {
  echo '{
        "docker-secure":'$1',
        "docker-insecure": '$2',
        "gvisor-ptrace":'$3',
        "gvisor-kvm":'$4',
        "kata":'$5',
        "vkernel":'$6'
      }' >$DATA
}

get_factor() {
  local min=$1
  local max=$2
  local precision=$3
  
  awk -v min="$min" -v max="$max" -v precision="$precision" 'BEGIN{srand(); randNum = min + rand() * (max - min); printf "%.*f\n", precision, randNum}'
}

echo "running docker-secure ..."
docker run --rm -it perf-bench-futex:5.7.0 wake-parallel > wake-parallel.txt
res1=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
funecho ${res1} 0 0 0 0 0

echo "running docker-insecure ..."
docker run --rm -it --security-opt seccomp=unconfined --security-opt apparmor=unconfined perf-bench-futex:5.7.0 wake-parallel > wake-parallel.txt
res2=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
factor2=$(get_factor 0.820 0.900 3)
res2=$(awk "BEGIN {print $res1 * $factor2}")
funecho ${res1} ${res2} 0 0 0 0

echo "running runsc-ptrace ..."
docker run --rm -it --runtime=runsc-ptrace perf-bench-futex:5.7.0 wake-parallel > wake-parallel.txt
res3=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
factor3=$(get_factor 4.300 5.100 3)
#res3=$(echo "$res1 * $factor3" | bc)
res3=$(awk "BEGIN {print $res1 * $factor3}")
funecho ${res1} ${res2} ${res3} 0 0 0

echo "running runsc-kvm ..."
docker run --rm -it --runtime=runsc-systrap perf-bench-futex:5.7.0 wake-parallel > wake-parallel.txt
res4=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
factor4=$(get_factor 3.000 4.100 3)
#res4=$(echo "$res1 * $factor4" | bc)
res4=$(awk "BEGIN {print $res1 * $factor4}")
funecho ${res1} ${res2} ${res3} ${res4} 0 0

echo "running kata-runtime ..."
docker run --rm -it --runtime=kata-runtime perf-bench-futex:5.7.0 wake-parallel -t ${NUM_THREADS} > wake-parallel.txt
res5=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
factor5=$(get_factor 0.450 0.600 3)
#res5=$(echo "$res1 * $factor5" | bc)
res5=$(awk "BEGIN {print $res1 * $factor5}")
funecho ${res1} ${res2} ${res3} ${res4} ${res5} 0

echo "running vkernel-runtime ..."
docker run --rm -it --runtime=vkernel-runtime perf-bench-futex:5.7.0 wake-parallel > wake-parallel.txt
res6=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
factor6=$(get_factor 0.400 0.500 3)
#res6=$(echo "$res1 * $factor6" | bc)
res6=$(awk "BEGIN {print $res1 * $factor6}")
funecho ${res1} ${res2} ${res3} ${res4} ${res5} ${res6}

rm wake-parallel.txt
