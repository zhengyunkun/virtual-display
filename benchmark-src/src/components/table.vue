<template>
  <table class="table is-bordered is-hoverable mx-6">
    <thead>
      <tr>
        <th><abbr title="name">{{ name }}</abbr></th>
        <th
          v-for="(item, index) in items"
          :key="index"
        ><abbr :title="item">{{ item }}</abbr></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th>{{ unit }}</th>
        <td
          v-for="(val, idx) in newLine"
          :key="idx"
        >
          <span v-if="idx === 0">-</span>
          <span
            v-else-if="val > 0"
            :class="colorType === 0 ? 'has-text-success' : 'has-text-danger'"
          >+{{ (val * 100).toFixed(1) }}%</span>
          <span v-else-if="Number(val) === 0">0</span>
          <span
            v-else
            :class="colorType === 0 ? 'has-text-danger' : 'has-text-success'"
          >{{ (val * 100).toFixed(1) }}%</span>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "Table",
  props: {
    name: {
      type: String
    },
    items: {
      type: Array
    },
    line: {
      type: Array
    },
    // 单位
    unit: {
      type: String
    },
    colorType: {
      type: Number // 0: 正绿负红; 1: 正红负绿
    }
  },
  computed: {
    // 返回以第一项为 baseline 的百分比数据
    newLine() {
      let ret = [0];
      for (let i = 1; i < this.line.length; i++) {
        const val = this.line[i] === 0 ? 0 : this.line[i] / this.line[0] - 1;
        ret.push(val);
      }
      return ret;
    }
  }
};
</script>

<style>
</style>