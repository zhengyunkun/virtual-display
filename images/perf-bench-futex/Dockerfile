FROM d202181178/futex-test:latest

COPY ./perf-5.7.0 /usr/local/bin

ENTRYPOINT ["/usr/local/bin/perf-5.7.0", "bench", "futex"]
