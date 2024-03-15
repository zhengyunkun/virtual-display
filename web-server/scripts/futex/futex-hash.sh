#! /bin/bash

NUM_THREADS=$(cat /proc/cpuinfo | grep 'processor' | wc -l)

funecho() {
  echo '{
        "docker-secure":'$1',
        "docker-insecure":'$2',
        "gvisor-ptrace":'$3',
        "gvisor-kvm":'$4',
        "kata":'$5',
        "vkernel":'$6'
      }' >../../dist/data/futex/futex-hash.json
}

echo "running docker-secure ..."
docker run --rm -it autubrew/perf-bench-futex hash > hash.txt
res1=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
funecho ${res1} 0 0 0 0 0

echo "running docker-insecure ..."
docker run --rm -it --security-opt seccomp=unconfined --security-opt apparmor=unconfined autubrew/perf-bench-futex hash > hash.txt
res2=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
funecho ${res1} ${res2} 0 0 0 0

echo "running runsc-ptrace ..."
docker run --rm -it --runtime=runsc-ptrace autubrew/perf-bench-futex hash > hash.txt
res3=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} 0 0 0

echo "running runsc-kvm ..."
docker run --rm -it --runtime=runsc-kvm autubrew/perf-bench-futex hash > hash.txt
res4=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} ${res4} 0 0

echo "running kata-runtime ..."
docker run --rm -it --runtime=kata-runtime autubrew/perf-bench-futex hash -t ${NUM_THREADS} > hash.txt
res5=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} ${res4} ${res5} 0

echo "running vkernel-runtime ..."
docker run --rm -it --runtime=vkernel-runtime autubrew/perf-bench-futex hash > hash.txt
res6=$(cat hash.txt | grep 'operations/sec' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} ${res4} ${res5} ${res6}

rm hash.txt
