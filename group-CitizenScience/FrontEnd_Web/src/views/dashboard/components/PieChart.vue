<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from "echarts";
require("echarts/theme/macarons"); // echarts theme
import resize from "./mixins/resize";
import global from "@/App";

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: "chart"
    },
    width: {
      type: String,
      default: "100%"
    },
    height: {
      type: String,
      default: "300px"
    }
  },
  data() {
    return {
      chart: null,
      datas: []
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.axios
        .post(global.server + "admin/get_data/index_chart_2")
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(res.data);
          this.datas = res.data;
          this.initChart();
        });
    });
  },
  created() {},
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, "macarons");

      this.chart.setOption({
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          left: "center",
          bottom: "10",
          data: ["待审核", "已通过", "数据收集", "数据分析", "已结项", "未通过"]
        },
        series: [
          {
            name: "项目状态统计",
            type: "pie",
            roseType: "radius",
            radius: [15, 95],
            center: ["50%", "38%"],
            data: [
              { value: this.datas.a1, name: "待审核" },
              { value: this.datas.a2, name: "已通过" },
              { value: this.datas.a3, name: "数据收集" },
              { value: this.datas.a4, name: "数据分析" },
              { value: this.datas.a5, name: "已结项" },
              { value: this.datas.a6, name: "未通过" }
            ],
            animationEasing: "cubicInOut",
            animationDuration: 2600
          }
        ]
      });
    }
  }
};
</script>
