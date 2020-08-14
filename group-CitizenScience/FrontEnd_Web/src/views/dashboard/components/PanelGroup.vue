<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="directToRoute(1)">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="tree" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">我管理的项目</div>
          <div style="text-align:center">
            <count-to
              :start-val="0"
              :end-val="all_projects_count"
              :duration="2600"
              class="card-panel-num"
            />
          </div>
        </div>
      </div>
    </el-col>
    <!-- <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            New Visits
          </div>
          <count-to :start-val="0" :end-val="102400" :duration="2600" class="card-panel-num" />
        </div>
      </div>
    </el-col>-->
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="directToRoute(2)">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">用户参与人次</div>
          <div style="text-align:center">
            <count-to
              :start-val="0"
              :end-val="all_users_count"
              :duration="3000"
              class="card-panel-num"
            />
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="directToRoute(3)">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="skill" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">待标注的数据</div>
          <div style="text-align:center">
            <count-to
              :start-val="0"
              :end-val="to_rate_count"
              :duration="3200"
              class="card-panel-num"
            />
            <span class="card-panel-num">/</span>
            <count-to
              :start-val="0"
              :end-val="all_submits_count"
              :duration="3200"
              class="card-panel-num"
            />
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="directToRoute(4)">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="education" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">待审核的助理</div>
          <div style="text-align:center">
            <count-to
              :start-val="0"
              :end-val="all_verify_assistant"
              :duration="3600"
              class="card-panel-num"
            />
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import CountTo from "vue-count-to";
import global from "@/App";
export default {
  components: {
    CountTo
  },
  data() {
    return {
      all_projects_count: 0,
      all_users_count: 0,
      all_submits_count: 0,
      to_rate_count: 0,
      all_verify_assistant: 0
    };
  },
  created() {
    console.log(Date.now())
    console.log(this.$store.getters.token)
    this.axios
      .post(global.server + "admin/get_data/index_chart_1")
      .then(res => {
            console.log(this.$store.getters.token)
        if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
        console.log(res.data);
        this.all_projects_count = res.data.all_projects_count;
        this.all_users_count = res.data.all_users_count;
        this.all_submits_count = res.data.all_submits_count;
        this.to_rate_count = res.data.to_rate_count;
        this.all_verify_assistant = res.data.all_verify_assistant;
      });
  },
  methods: {
    directToRoute(op) {
      if (op == 1) {
        this.$router.push("/research_management/my_research");
      } else if (op == 2) {
        this.$router.push("/user_management/my_team");
      } else if (op == 3) {
        this.$router.push("/data");
      } else {
        this.$router.push("/user_management/apply_assistant");
      }
    },
    handleSetLineChartData(type) {
      this.$emit("handleSetLineChartData", type);
    }
  }
};
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 0, 0, 0.05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3;
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3;
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width: 550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
