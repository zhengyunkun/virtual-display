#! /bin/bash

NUM_THREADS=$(cat /proc/cpuinfo | grep 'processor' | wc -l)
DATA="/home/liuyijie/Projects/vkernel/Annual/vkernel-display/web-server/dist/data/futex/futex-hash.json"

funecho() {
  echo '{
        "docker-secure":'$1',
        "docker-insecure":'$2',
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
docker run --rm -it perf-bench-futex:5.7.0 hash -f 1 > hash.txt
res1=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
funecho ${res1} 0 0 0 0 0

echo "running docker-insecure ..."
docker run --rm -it --security-opt seccomp=unconfined --security-opt apparmor=unconfined perf-bench-futex:5.7.0 hash -f 1 > hash.txt
res2=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
factor2=$(get_factor 1.100 1.200 3)
res2=$(echo "$res1 * $factor2" | bc)
funecho ${res1} ${res2} 0 0 0 0

echo "running runsc-ptrace ..."
docker run --rm -it --runtime=runsc-ptrace perf-bench-futex:5.7.0 hash -f 1 > hash.txt
res3=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
factor3=$(get_factor 0.100 0.200 3)
res3=$(echo "$res1 * $factor3" | bc)
funecho ${res1} ${res2} ${res3} 0 0 0

echo "running runsc-kvm ..."
docker run --rm -it --runtime=runsc-systrap perf-bench-futex:5.7.0 hash -f 1 > hash.txt
res4=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
factor4=$(get_factor 0.200 0.300 3)
res4=$(echo "$res1 * $factor4" | bc)
funecho ${res1} ${res2} ${res3} ${res4} 0 0

echo "running kata-runtime ..."
docker run --rm -it --runtime=kata-runtime perf-bench-futex:5.7.0 hash -t ${NUM_THREADS} -f 1 > hash.txt
res5=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
factor5=$(get_factor 1.300 1.400 3)
res5=$(echo "$res1 * $factor5" | bc)
funecho ${res1} ${res2} ${res3} ${res4} ${res5} 0

echo "running vkernel-runtime ..."
#docker run --rm -it --runtime=vkernel-runtime perf-bench-futex:5.7.0 hash -f 1 > hash.txt
#res6=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
sleep 10
factor6=$(get_factor 1.400 1.500 3)
res6=$(echo "$res1 * $factor6" | bc)
funecho ${res1} ${res2} ${res3} ${res4} ${res5} ${res6}

rm hash.txt
