#! /bin/bash

echo '{
    "docker-secure": 0,
    "docker-insecure": 0,
    "gvisor-ptrace": 0,
    "gvisor-kvm": 0,
    "kata": 0,
    "vkernel": 0
    }' >../../dist/data/futex/futex-hash.json
