#! /bin/bash

NUM_THREADS=$(cat /proc/cpuinfo | grep 'processor' | wc -l)

funecho() {
  echo '{
        "docker-secure":'$1',
        "docker-insecure": '$2',
        "gvisor-ptrace":'$3',
        "gvisor-kvm":'$4',
        "kata":'$5',
        "vkernel":'$6'
      }' >../../dist/data/futex/futex-wake-parallel.json
}

echo "running docker-secure ..."
docker run --rm -it autubrew/perf-bench-futex wake-parallel > wake-parallel.txt
res1=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
funecho ${res1} 0 0 0 0 0

echo "running docker-insecure ..."
docker run --rm -it --security-opt seccomp=unconfined --security-opt apparmor=unconfined autubrew/perf-bench-futex wake-parallel > wake-parallel.txt
res2=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
funecho ${res1} ${res2} 0 0 0 0

echo "running runsc-ptrace ..."
docker run --rm -it --runtime=runsc-ptrace autubrew/perf-bench-futex wake-parallel > wake-parallel.txt
res3=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
funecho ${res1} ${res2} ${res3} 0 0 0

echo "running runsc-kvm ..."
docker run --rm -it --runtime=runsc-kvm autubrew/perf-bench-futex wake-parallel > wake-parallel.txt
res4=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
funecho ${res1} ${res2} ${res3} ${res4} 0 0

echo "running kata-runtime ..."
docker run --rm -it --runtime=kata-runtime autubrew/perf-bench-futex wake-parallel -t ${NUM_THREADS} > wake-parallel.txt
res5=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
funecho ${res1} ${res2} ${res3} ${res4} ${res5} 0

echo "running vkernel-runtime ..."
docker run --rm -it --runtime=vkernel-runtime autubrew/perf-bench-futex wake-parallel > wake-parallel.txt
res6=$(tail -n 1 wake-parallel.txt | awk '{print $8}')
funecho ${res1} ${res2} ${res3} ${res4} ${res5} ${res6}

rm wake-parallel.txt
