<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
</style>

<template>
  <div class="app-container">
    <el-header>
      <!-- <el-button class="el-icon-plus" type="primary" circle style="float: left" @click="createNew"></el-button> -->
      <el-input
        v-model="search"
        placeholder="请输入检索内容"
        suffix-icon="el-icon-edit"
        style="padding:0 0;float:right;width: 160px"
      ></el-input>
    </el-header>
    <el-table
      v-loading="listLoading"
      :data="showList.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      :row-style="{height:'20px'}"
      :cell-style="{padding:'5px'}"
    >
      <el-table-column align="center" label="可视化ID" width="80">
        <template slot-scope="scope">{{ scope.row.display_id }}</template>
      </el-table-column>
      <el-table-column align="center" label="可视化图名称">
        <template slot-scope="scope">{{ scope.row.figure_title}}</template>
      </el-table-column>
      <el-table-column align="center" label="图表类型" width="90">
        <template slot-scope="scope">{{ scope.row.figure_type}}</template>
      </el-table-column>
      <el-table-column align="center" label="项目ID" width="80">
        <template slot-scope="scope">{{ scope.row.project_id }}</template>
      </el-table-column>
      <el-table-column align="center" label="项目名称">
        <template slot-scope="scope">{{ scope.row.project_title }}</template>
      </el-table-column>
      <el-table-column align="center" prop="create_time" label="创建时间" width="130" sortable>
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="220">
        <template slot-scope="scope">
          <el-button
            style="margin-left:0"
            size="mini"
            @click="handlePreview(scope.$index, scope.row)"
          >预览</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
          >删除</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="primary"
            v-if="scope.row.figure_type == '地图'"
            @click="handleUpdate(scope.$index, scope.row)"
          >更新</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      style="text-align:center;margin-top:10px"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :pager-count="5"
      :page-sizes="[10, 15, 20]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="showList.length"
    ></el-pagination>
    <el-dialog title="预览" :visible.sync="dialogInvite" width="650px">
      <div id="app">
        <div id="pre" style="width: 600px;height:400px;"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import global from "@/App";
import "../../../node_modules/echarts/map/js/china";

// import '../../../node_modules/echarts/map/js/china'
export default {
  name: "MyVisual",
  data() {
    return {
      currentPage: 1,
      pagesize: 10,
      search: "",
      list: [],
      listLoading: true,
      dialogInvite: false,
      visual_data: "",
      myXAxis: "",
      size: "",
      myLegends: "",
      figureName: "",
      figureType: "",
      xName: "",
      yName: "",
      xRangeL: "",
      xRangeH: "",
      yRangeL: "",
      yRangeH: ""
    };
  },
  created() {
    this.fetchData();
  },
  watch:{
    search:{
      handler(val){
        this.showList = this.list.filter(data => !val || data.project_title.toLowerCase().includes(val.toLowerCase())
                          || data.project_id.toString().toLowerCase().includes(val.toLowerCase())
                          || data.figure_title.toLowerCase().includes(val.toLowerCase())
                          || data.figure_type.toLowerCase().includes(val.toLowerCase())
                          || data.display_id.toString().toLowerCase().includes(val.toLowerCase()))
      }
    }
  },
  methods: {
    handleSizeChange(val) {
      this.pagesize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    handleUpdate(index, row) {
      let params = new URLSearchParams();
      params.append("display_id", row.display_id);
      params.append("project_id", row.project_id);
      if (row.figure_type == "地图") {
        this.$message({
          type: "warning",
          message: "更新地图可能等待时间较长，请稍等"
        });
      }
      this.axios.post(global.server + "update_map", params).then(res => {
        if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
        this.$message({ type: "success", message: "地图已重新渲染！" });
      });
    },
    createNew() {
      this.$router.push("/visual");
    },
    fetchData() {
      this.listLoading = true;
      this.axios.post(global.server + "get_my_visual_research").then(res => {
        if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
        console.log(res);
        this.list = res.data;
        this.showList = res.data;
        this.listLoading = false;
      });
    },
    handlePreview(index, row) {
      //基于准备好的dom，初始化echarts实例
      let params = new URLSearchParams();
      params.append("display_id", row.display_id);
      this.dialogInvite = true;
      this.$nextTick(() => {
        this.axios
          .post(global.server + "get_visualization_each", params)
          .then(res => {
            if (res.data == "networkError") {
              this.$message({
                type: "error",
                message: "验证过期，请重新登录！"
              });
              setTimeout(() => {
                this.$store.dispatch("user/logout");
              }, 2000);
              return;
            }
            this.visual_data = res.data.mydata;
            this.myXAxis = res.data.myxAxis;
            this.size = res.data.mySize;
            this.myLegends = res.data.myLegends;
            this.figureName = res.data.figure_name;
            this.figureType = res.data.figure_type;
            this.xName = res.data.xName;
            this.yName = res.data.yName;
            this.xRangeL = res.data.xRangeL;
            this.xRangeH = res.data.xRangeH;
            this.yRangeH = res.data.yRangeH;
            this.yRangeL = res.data.yRangeL;
          })
          .then(() => {
            var tmp = [];
            for (var i = 0; i < this.size; i++) {
              tmp.push({
                name: this.myLegends[i],
                data: this.visual_data[i],
                type: this.figureType
              });
            }
            let myChart = this.$echarts.init(document.getElementById("pre"));
            // 指定图表的配置项和数据
            console.log(tmp);
            let option1 = {
              backgroundColor: "#404a59",
              title: {
                text: this.figureName,
                x: "center",
                textStyle: {
                  color: "#fff"
                }
              },
              tooltip: {
                trigger: "item",
                formatter: function(params) {
                  return params.name + " : " + params.value[2];
                }
              },
              legend: {
                orient: "vertical",
                top: "bottom",
                left: "right",
                data: ["pm2.5"],
                textStyle: {
                  color: "#fff"
                }
              },
              visualMap: {
                min: this.xRangeL,
                max: this.xRangeH,
                calculable: true,
                inRange: {
                  color: ["#50a3ba", "#eac736", "#d94e5d"]
                },
                textStyle: {
                  color: "#fff"
                }
              },
              geo: {
                map: "china",
                itemStyle: {
                  areaColor: "#323c48",
                  borderColor: "#111"
                },
                emphasis: {
                  itemStyle: {
                    areaColor: "#2a333d"
                  },
                  label: {
                    show: false
                  }
                }
              },
              series: [
                {
                  type: "scatter",
                  coordinateSystem: "geo",
                  data: this.visual_data,
                  symbolSize: 5
                }
              ]
            };

            let option2 = {
              title: {
                text: this.figureName
              },
              tooltip: {},
              legend: {
                data: this.myLegends,
                orient: "vertical",
                top: "bottom",
                left: "right",
              },
              xAxis: {
                name: this.xName,
                type: "category",
                data: this.myXAxis,
                nameLocation: "middle",
                nameGap: 20,
                min: this.xRangeL,
                max: this.xRangeH
              },
              yAxis: {
                type: "value",
                name: this.yName,
                min: this.yRangeL,
                max: this.yRangeH
              },
              series: tmp
            };
            let option3 = {
              legend: {
                orient: "vertical",
                left: "right",
                data: this.myLegends,
                orient: "vertical",
                top: "bottom",
              },
              title: {
                text: this.figureName
              },
              tooltip: {},
              series: [
                {
                  type: "pie",
                  radius: "55%",
                  center: ["50%", "60%"],
                  data: this.visual_data,
                  emphasis: {
                    itemStyle: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: "rgba(0, 0, 0, 0.5)"
                    }
                  }
                }
              ]
            };
            let option4 = {
              title: {
                text: this.figureName
              },
              tooltip: {},
              legend: {
                data: this.myLegends,
                orient: "vertical",
                top: "bottom",
                left: "right",
              },
              xAxis: {
                type: "value",
                name: this.xName,
                min: this.xRangeL,
                max: this.xRangeH,
                nameLocation: "middle",
                nameGap: 20
              },
              yAxis: {
                type: "value",
                name: this.yName,
                min: this.yRangeL,
                max: this.yRangeH
              },
              series: tmp
            };
            if (this.figureType === "map") {
              myChart.clear();
              myChart.setOption(option1);
            } else if (
              this.figureType === "bar" ||
              this.figureType === "line"
            ) {
              myChart.clear();
              myChart.setOption(option2);
            } else if (this.figureType === "pie") {
              myChart.clear();
              myChart.setOption(option3);
            } else if (this.figureType === "scatter") {
              myChart.clear();
              myChart.setOption(option4);
            }
          });
      });
    },
    handleDelete(index, row) {
      let params = new URLSearchParams();
      params.append("display_id", row.display_id);
      this.axios
        .post(global.server + "delete_visualization", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          if (res.data === "OK") {
            this.list.splice(index, 1);
            this.$message({
              message: "删除成功",
              type: "success"
            });
            this.fetchData()
          }
        });
    }
  }
};
</script>
