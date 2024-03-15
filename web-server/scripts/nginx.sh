#! /bin/bash

PORT=7000
AB_REQUESTS=30000 # ab 请求总数
AB_CONCURRENCY=30  # ab 并发数
SLEEP=5 # 防止连接 reset

DATA="/home/liuyijie/Projects/vkernel/Annual/vkernel-display/web-server/dist/data/nginx.json"
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
name=benchmark-nginx-secure
docker run --rm --name ${name} -itd -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res1=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
if [ "$res1" = "" ]; then
  res1=0
fi
funecho ${res1} 0 0 0 0 0

echo "running docker-insecure ..."
name=benchmark-nginx-insecure
docker run --rm --name ${name} -itd --security-opt seccomp=unconfined --security-opt apparmor=unconfined -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res2=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
if [ "$res2" = "" ]; then
  res2=0
fi
funecho ${res1} ${res2} 0 0 0 0

echo "running runsc-ptrace ..."
name=benchmark-nginx-runsc-ptrace
docker run --rm --name ${name} -itd --runtime=runsc-ptrace -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res3=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
if [ "$res3" = "" ]; then
  res3=0
fi
funecho ${res1} ${res2} ${res3} 0 0 0

echo "running runsc-kvm ..."
name=benchmark-nginx-runsc-kvm
docker run --rm --name ${name} -itd --runtime=runsc-systrap -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res4=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
if [ "$res4" = "" ]; then
  res4=0
fi
funecho ${res1} ${res2} ${res3} ${res4} 0 0

echo "running kata-runtime ..."
name=benchmark-nginx-kata-runtime
docker run --rm --name ${name} -itd --runtime=kata-runtime -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res5=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
if [ "$res5" = "" ]; then
  res5=0
fi
funecho ${res1} ${res2} ${res3} ${res4} ${res5} 0

echo "running vkernel-runtime ..."
name=benchmark-nginx-vkernel-runtime
docker run --rm --name ${name} -itd --runtime=vkernel-runtime -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res6=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
if [ "$res6" = "" ]; then
  res6=0
fi
funecho ${res1} ${res2} ${res3} ${res4} ${res5} ${res6}

rm ab.txt