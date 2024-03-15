FROM ubuntu:18.04
LABEL maintainer "Autubrew <violettime@foxmail.com>"

# 1. cve-2019-14287
# 2. CDK 容器逃逸

COPY ./cdk /usr/local/bin

RUN chmod +x /usr/local/bin/cdk \
    && sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && apt update -y \
    && apt install --no-install-recommends -y \
    openssh-server sudo=1.8.21p2-3ubuntu1 \
    && mkdir -p /var/run/sshd \
    && mkdir -p /root/.ssh \
    # Add user to sudoers
    && useradd -m testuser -s /bin/bash \
    && mkdir -p /home/testuser/.ssh \
    && echo "testuser:testuser" | chpasswd \
    && echo "testuser ALL=(ALL,!root) NOPASSWD: /bin/bash" >> /etc/sudoers \
    # Take values from ARGS and modify sshd_config accordingly
    && cd /etc/ssh \
    && echo "root:testuser" | chpasswd \
    && sed --in-place 's/^\(UsePAM\|UseDNS\)/#\1/' sshd_config \
    && echo "" >> sshd_config \
    && echo "UsePAM no" >> sshd_config \
    && echo "UseDNS no" >> sshd_config

COPY ./cdk.sh /

EXPOSE 22

CMD    ["/usr/sbin/sshd", "-D"]