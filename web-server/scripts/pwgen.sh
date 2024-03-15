#! /bin/bash

LEN=100
NUM=10240

DATA="/home/liuyijie/Projects/vkernel/Annual/vkernel-display/web-server/dist/data/pwgen.json"
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

echo "running docker-secure ..."
/usr/bin/time -o pwgen.txt -p docker run --rm pwgen-image pwgen -s ${LEN} ${NUM} >/dev/null
res1=$(cat pwgen.txt | grep 'real' | awk '{print $2}')
funecho ${res1} 0 0 0 0 0

echo "running docker-insecure ..."
/usr/bin/time -o pwgen.txt -p docker run --security-opt seccomp=unconfined --security-opt apparmor=unconfined --rm pwgen-image pwgen -s ${LEN} ${NUM} >/dev/null
res2=$(cat pwgen.txt | grep 'real' | awk '{print $2}')
funecho ${res1} ${res2} 0 0 0 0

echo "running runsc-ptrace ..."
/usr/bin/time -o pwgen.txt -p docker run --runtime=runsc-ptrace --rm pwgen-image pwgen -s ${LEN} ${NUM} >/dev/null
res3=$(cat pwgen.txt | grep 'real' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} 0 0 0

echo "running runsc-kvm ..."
/usr/bin/time -o pwgen.txt -p docker run --runtime=runsc-systrap --rm pwgen-image pwgen -s ${LEN} ${NUM} >/dev/null
res4=$(cat pwgen.txt | grep 'real' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} ${res4} 0 0

echo "running kata-runtime ..."
/usr/bin/time -o pwgen.txt -p docker run --runtime=kata-runtime --rm pwgen-image pwgen -s ${LEN} ${NUM} >/dev/null
res5=$(cat pwgen.txt | grep 'real' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} ${res4} ${res5} 0

echo "running vkernel-runtime ..."
/usr/bin/time -o pwgen.txt -p docker run --runtime=vkernel-runtime --rm pwgen-image pwgen -s ${LEN} ${NUM} >/dev/null
res6=$(cat pwgen.txt | grep 'real' | awk '{print $2}')
funecho ${res1} ${res2} ${res3} ${res4} ${res5} ${res6}

rm pwgen.txt
