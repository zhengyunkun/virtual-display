<template>
  <div id="app">
    <div class="is-flex is-justify-content-space-around">
      <highcharts :options="part === 0 ? chartOptions1 : chartOptionsFutexHash"></highcharts>
      <highcharts :options="part === 0 ? chartOptions2 : chartOptionsFutexWakeParallel"></highcharts>
    </div>
    <div class="is-flex is-justify-content-space-around mt-6">
      <Table
        v-if="part === 0"
        name="Nginx"
        :items="['docker-secure(baseline)', 'docker-insecure', 'gvisor-ptrace', 'gvisor-kvm', 'kata', 'vkernel']"
        :line="nginxLine"
        unit="QPS"
        :colorType=0
      />
      <Table
        v-else
        name="futex hash"
        :items="['docker-secure(baseline)', 'docker-insecure', 'gvisor-ptrace', 'gvisor-kvm', 'kata', 'vkernel']"
        :line="futexHashLine"
        unit="operations/sec"
        :colorType=0
      />
      <Table
        v-if="part === 0"
        name="Pwgen"
        :items="['docker-secure(baseline)', 'docker-insecure', 'gvisor-ptrace', 'gvisor-kvm', 'kata', 'vkernel']"
        :line="pwgenLine"
        unit="ms"
        :colorType=1
      />
      <Table
        v-else
        name="futex wake-parallel"
        :items="['docker-secure(baseline)', 'docker-insecure', 'gvisor-ptrace', 'gvisor-kvm', 'kata', 'vkernel']"
        :line="futexWakeParallelLine"
        unit="μs"
        :colorType=1
      />
    </div>
    <div class="is-flex is-justify-content-space-around">
      <div
        v-for="count in 2"
        :key="count"
      >
        <div>
          <span
            class="is-inline-block mr-2"
            style="width: 8px; height: 8px; background-color: #f14668;"
          />
          <code style="color: black;">worse</code>
        </div>
        <div>
          <span
            class="is-inline-block mr-2"
            style="width: 8px; height: 8px; background-color: #48c774;"
          />
          <code style="color: black;">better</code>
        </div>
      </div>
    </div>
    <div class="mt-6">
      <button
        class="button"
        @click="doSwitch"
      >{{ part === 1 ? 'performance' : 'futex' }}</button>
    </div>
  </div>
</template>

<script>
import Table from "@/components/table";
export default {
  name: "App",
  components: {
    Table
  },
  data() {
    return {
      part: 0, // 0: nginx + pwgen; 1: futex
      // nginx
      chartOptions1: {
        chart: {
          type: "column",
          backgroundColor: {
            linearGradient: [0, 0, 500, 500],
            stops: [
              [0, "rgb(255, 255, 255)"],
              [1, "rgb(240, 240, 255)"]
            ]
          }
        },
        credits: {
          enabled: false
        },
        title: {
          text: "nginx 的 Apache Benchmark 压力测试"
        },
        plotOptions: {
          column: {
            color: "rgb(46, 180, 255)",
            dataLabels: {
              enabled: true,
              inside: true
            }
          }
        },
        xAxis: {
          categories: [
            "docker-secure",
            "docker-insecure",
            "gvisor-ptrace",
            "gvisor-kvm",
            "kata",
            "vkernel"
          ],
          title: {
            text: null
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: "Requests per second"
          }
        },
        series: [
          {
            name: "nginx",
            data: [
              {
                name: "docker-secure",
                y: 0
              },
              {
                name: "docker-insecure",
                y: 0
              },
              {
                name: "gvisor-ptrace",
                y: 0
              },
              {
                name: "gvisor-kvm",
                y: 0
              },
              {
                name: "kata",
                y: 0
              },
              {
                name: "vkernel",
                y: 0
              }
            ]
          }
        ]
      },
      // pwgen
      chartOptions2: {
        chart: {
          type: "column",
          backgroundColor: {
            linearGradient: [0, 0, 500, 500],
            stops: [
              [0, "rgb(255, 255, 255)"],
              [1, "rgb(240, 240, 255)"]
            ]
          }
        },
        credits: {
          enabled: false
        },
        title: {
          text: "pwgen 密码生成时间开销测试"
        },
        plotOptions: {
          column: {
            color: "rgb(247, 163, 92)",
            dataLabels: {
              enabled: true,
              inside: true
            }
          }
        },
        xAxis: {
          categories: [
            "docker-secure",
            "docker-insecure",
            "gvisor-ptrace",
            "gvisor-kvm",
            "kata",
            "vkernel"
          ],
          title: {
            text: null
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: "单位：ms"
          }
        },
        series: [
          {
            name: "pwgen",
            data: [
              {
                name: "docker-secure",
                y: 0
              },
              {
                name: "docker-insecure",
                y: 0
              },
              {
                name: "gvisor-ptrace",
                y: 0
              },
              {
                name: "gvisor-kvm",
                y: 0
              },
              {
                name: "kata",
                y: 0
              },
              {
                name: "vkernel",
                y: 0
              }
            ]
          }
        ]
      },
      // futex hash
      chartOptionsFutexHash: {
        chart: {
          type: "column",
          backgroundColor: {
            linearGradient: [0, 0, 500, 500],
            stops: [
              [0, "rgb(255, 255, 255)"],
              [1, "rgb(240, 240, 255)"]
            ]
          }
        },
        credits: {
          enabled: false
        },
        title: {
          text: "容器 futex 系统调用性能测试 —— futex hash"
        },
        plotOptions: {
          column: {
            color: "rgb(46, 180, 255)",
            dataLabels: {
              enabled: true,
              inside: true
            }
          }
        },
        xAxis: {
          categories: [
            "docker-secure",
            "docker-insecure",
            "gvisor-ptrace",
            "gvisor-kvm",
            "kata",
            "vkernel"
          ],
          title: {
            text: null
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: "operations/sec"
          }
        },
        series: [
          {
            name: "futex wait 操作，计算 futex 锁的 hash",
            data: [
              {
                name: "docker-secure",
                y: 0
              },
              {
                name: "docker-insecure",
                y: 0
              },
              {
                name: "gvisor-ptrace",
                y: 0
              },
              {
                name: "gvisor-kvm",
                y: 0
              },
              {
                name: "kata",
                y: 0
              },
              {
                name: "vkernel",
                y: 0
              }
            ]
          }
        ]
      },
      // futex wake-parallel
      chartOptionsFutexWakeParallel: {
        chart: {
          type: "column",
          backgroundColor: {
            linearGradient: [0, 0, 500, 500],
            stops: [
              [0, "rgb(255, 255, 255)"],
              [1, "rgb(240, 240, 255)"]
            ]
          }
        },
        credits: {
          enabled: false
        },
        title: {
          text: "容器 futex 系统调用性能测试 —— futex wake-parallel"
        },
        plotOptions: {
          column: {
            color: "rgb(247, 163, 92)",
            dataLabels: {
              enabled: true,
              inside: true
            }
          }
        },
        xAxis: {
          categories: [
            "docker-secure",
            "docker-insecure",
            "gvisor-ptrace",
            "gvisor-kvm",
            "kata",
            "vkernel"
          ],
          title: {
            text: null
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: "平均每个线程被唤醒的时间（μs）"
          }
        },
        series: [
          {
            name: "并发 futex wake 操作",
            data: [
              {
                name: "docker-secure",
                y: 0
              },
              {
                name: "docker-insecure",
                y: 0
              },
              {
                name: "gvisor-ptrace",
                y: 0
              },
              {
                name: "gvisor-kvm",
                y: 0
              },
              {
                name: "kata",
                y: 0
              },
              {
                name: "vkernel",
                y: 0
              }
            ]
          }
        ]
      }
    };
  },
  created() {
    document.title = '整体性能测试'
  },
  mounted() {
    // 定时读取文件
    const interval = 1000;
    const nginxUrl = "data/nginx.json"; // 路径相对于 public
    const pwgenUrl = "data/pwgen.json";
    const futexHashUrl = "data/futex/futex-hash.json";
    const futexWakeParallelUrl = "data/futex/futex-wake-parallel.json";
    setInterval(() => {
      this.axios.get(`${nginxUrl}?time=${new Date().getTime()}`).then(
        response => {
          console.log(response.data);
          for (let key in response.data) {
            let value = response.data[key];
            for (let j = 0; j < this.chartOptions1.series[0].data.length; j++) {
              if (this.chartOptions1.series[0].data[j].name === key) {
                if (
                  value === undefined ||
                  typeof value !== "number" ||
                  value < 0
                ) {
                  value = 0;
                }
                this.chartOptions1.series[0].data[j].y = value;
              }
            }
          }
        },
        err => {
          console.log(err);
        }
      );
      this.axios.get(`${pwgenUrl}?time=${new Date().getTime()}`).then(
        response => {
          console.log(response.data);
          for (let key in response.data) {
            let value = response.data[key];
            for (let j = 0; j < this.chartOptions2.series[0].data.length; j++) {
              if (this.chartOptions2.series[0].data[j].name === key) {
                if (
                  value === undefined ||
                  typeof value !== "number" ||
                  value < 0
                ) {
                  value = 0;
                }
                this.chartOptions2.series[0].data[j].y = value;
              }
            }
          }
        },
        err => {
          console.log(err);
        }
      );
      this.axios.get(`${futexHashUrl}?time=${new Date().getTime()}`).then(
        response => {
          console.log(response.data);
          for (let key in response.data) {
            let value = response.data[key];
            for (
              let j = 0;
              j < this.chartOptionsFutexHash.series[0].data.length;
              j++
            ) {
              if (this.chartOptionsFutexHash.series[0].data[j].name === key) {
                if (
                  value === undefined ||
                  typeof value !== "number" ||
                  value < 0
                ) {
                  value = 0;
                }
                this.chartOptionsFutexHash.series[0].data[j].y = value;
              }
            }
          }
        },
        err => {
          console.log(err);
        }
      );
      this.axios.get(`${futexWakeParallelUrl}?time=${new Date().getTime()}`).then(
        response => {
          console.log(response.data);
          for (let key in response.data) {
            let value = response.data[key];
            for (let j = 0; j < this.chartOptionsFutexWakeParallel.series[0].data.length; j++) {
              if (this.chartOptionsFutexWakeParallel.series[0].data[j].name === key) {
                if (
                  value === undefined ||
                  typeof value !== "number" ||
                  value < 0
                ) {
                  value = 0;
                }
                this.chartOptionsFutexWakeParallel.series[0].data[j].y = Number((value * 1000).toFixed(1)); // 毫秒转为微秒
              }
            }
          }
        },
        err => {
          console.log(err);
        }
      );
    }, interval);
  },
  computed: {
    // 返回表格两行数据
    nginxLine() {
      return this.chartOptions1.series[0].data.map(item => {
        return item.y;
      });
    },
    pwgenLine() {
      return this.chartOptions2.series[0].data.map(item => {
        return item.y;
      });
    },
    futexHashLine() {
      return this.chartOptionsFutexHash.series[0].data.map(item => {
        return item.y;
      });
    },
    futexWakeParallelLine() {
      return this.chartOptionsFutexWakeParallel.series[0].data.map(item => {
        return item.y;
      });
    }
  },
  methods: {
    doSwitch() {
      this.part = this.part === 0 ? 1 : 0;
      document.title = this.part === 0 ? '整体性能演示' : 'futex系统调用性能测试'
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
