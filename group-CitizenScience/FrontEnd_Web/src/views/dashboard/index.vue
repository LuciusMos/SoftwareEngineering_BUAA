<template>
  <div class="dashboard-editor-container">
    <!-- <panel-group @handleSetLineChartData="handleSetLineChartData" /> -->
    <div class="dashboard-text">
      <p style="font-size:30px">欢迎您， {{ name }}</p>
    </div>
    <panel-group />
    <!-- <panel-group @handleSetLineChartData="handleSetLineChartData" /> -->

    <!-- <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>-->
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="dashboard-text">
          <p style="font-size:30px">项目概览</p>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="dashboard-text">
          <p style="font-size:30px">个人信息</p>
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="dashboard-text">
          <p style="font-size:30px">工作背景</p>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <pie-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <el-row style="margin-bottom:25px" type="flex" justify="center">
            <el-col :span="9" style="text-align:right">
              <b>真实姓名：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.user_realname}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:25px" type="flex" justify="center">
            <el-col :span="9" style="text-align:right">
              <b>用户ID：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.user_id}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:25px" type="flex" justify="center">
            <el-col :span="9" style="text-align:right">
              <b>用户名：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.user_nickname}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:25px" type="flex" justify="center">
            <el-col :span="9" style="text-align:right">
              <b>邮箱：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.user_email}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:25px" type="flex" justify="center">
            <el-col :span="9" style="text-align:right">
              <b>注册时间：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.register_time}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:25px;padding-bottom:25px" type="flex" justify="center">
            <el-col :span="9" style="text-align:right">
              <b>申请时间：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.apply_time}}</span>
            </el-col>
          </el-row>
        </div>
      </el-col>

      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <el-row
            style="margin-bottom:25px"
            type="flex"
            justify="center"
            v-if="detailform.association != null"
          >
            <el-col :span="9" style="text-align:right">
              <b>工作单位：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.association}}</span>
            </el-col>
          </el-row>
          <el-row
            style="margin-bottom:25px"
            type="flex"
            justify="center"
            v-if="detailform.research_team != null"
          >
            <el-col :span="9" style="text-align:right">
              <b>所属团队：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.research_team}}</span>
            </el-col>
          </el-row>
          <el-row
            style="margin-bottom:25px"
            type="flex"
            justify="center"
            v-if="detailform.job_title != null"
          >
            <el-col :span="9" style="text-align:right">
              <b>职称：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.job_title}}</span>
            </el-col>
          </el-row>
          <el-row
            style="margin-bottom:25px"
            type="flex"
            justify="center"
            v-if="detailform.academic_degree != null"
          >
            <el-col :span="9" style="text-align:right">
              <b>学历：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.academic_degree}}</span>
            </el-col>
          </el-row>
          <el-row
            style="margin-bottom:25px;padding-bottom:25px"
            type="flex"
            justify="center"
            v-if="detailform.research_area != null"
          >
            <el-col :span="9" style="text-align:right">
              <b>研究方向：</b>
            </el-col>
            <el-col :span="15">
              <span>{{detailform.research_area}}</span>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>

    <!-- <el-row :gutter="8">
      <el-col
        :xs="{span: 24}"
        :sm="{span: 24}"
        :md="{span: 24}"
        :lg="{span: 12}"
        :xl="{span: 12}"
        style="padding-right:8px;margin-bottom:30px;"
      >
        <transaction-table />
    </el-col>-->
    <!-- <el-col
        :xs="{span: 24}"
        :sm="{span: 12}"
        :md="{span: 12}"
        :lg="{span: 6}"
        :xl="{span: 6}"
        style="margin-bottom:30px;"
      >
        <todo-list />
    </el-col>-->
    <!-- <el-col
        :xs="{span: 24}"
        :sm="{span: 12}"
        :md="{span: 12}"
        :lg="{span: 6}"
        :xl="{span: 6}"
        style="margin-bottom:30px;"
      >
    <box-card />-->
    <!-- </el-col>
    </el-row>-->
  </div>
</template>

<script>
import PanelGroup from "./components/PanelGroup";
import LineChart from "./components/LineChart";
import RaddarChart from "./components/RaddarChart";
import PieChart from "./components/PieChart";
import BarChart from "./components/BarChart";
import TransactionTable from "./components/TransactionTable";
import TodoList from "./components/TodoList";
import BoxCard from "./components/BoxCard";
import global from "@/App";

const lineChartData = {
  newVisitis: {
    expectedData: [100, 120, 161, 134, 105, 160, 165],
    actualData: [120, 82, 91, 154, 162, 140, 145]
  },
  messages: {
    expectedData: [200, 192, 120, 144, 160, 130, 140],
    actualData: [180, 160, 151, 106, 145, 150, 130]
  },
  purchases: {
    expectedData: [80, 100, 121, 104, 105, 90, 100],
    actualData: [120, 90, 100, 138, 142, 130, 130]
  },
  shoppings: {
    expectedData: [130, 140, 141, 142, 145, 150, 160],
    actualData: [120, 82, 91, 154, 162, 140, 130]
  }
};

export default {
  components: {
    PanelGroup,
    LineChart,
    RaddarChart,
    PieChart,
    BarChart,
    TransactionTable,
    TodoList,
    BoxCard
  },
  created() {
    this.axios.post(global.server + "admin/get_data/my_detail").then(res => {
      console.log(res);
      if (res.data == "networkError") {
        this.$message({ type: "error", message: "验证过期，请重新登录！" });
        setTimeout(() => {
          this.$store.dispatch("user/logout");
        }, 2000);
        return;
      }
      this.detailform = res.data;
    });
    this.name = this.$store.getters.name;
  },
  data() {
    return {
      name: "请登录！",
      lineChartData: lineChartData.newVisitis,
      detailform: []
    };
  },
  methods: {
    handleSetLineChartData(type) {
      this.lineChartData = lineChartData[type];
    }
  }
};
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width: 1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
