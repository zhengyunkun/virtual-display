FROM ubuntu:20.04

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt update -y \
    && apt install --no-install-recommends -y \
    && apt install pwgen -y

CMD ["/usr/bin/pwgen"]
