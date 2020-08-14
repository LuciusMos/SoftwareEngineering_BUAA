<template>
  <div class="app-container">
    <el-form ref="sizeForm" :model="sizeForm" label-width="150px">
      <el-form-item
        label="选择项目"
        prop="project_id"
        :rules="[{ required: true, message: '请选择项目', trigger: 'blur' }]"
      >
        <el-col :span="8">
          <el-select v-model="sizeForm.project_id" clearable filterable placeholder="请选择项目ID">
            <el-option
              v-for="item in project_list"
              :key="item.project_id"
              :label="item.project_id + '(' + item.project_title + ')'"
              :value="item.project_id"
            ></el-option>
          </el-select>
        </el-col>
      </el-form-item>
      <el-form-item
        label="图表名称"
        prop="figureName"
        :rules="[{required: true, message: '请输入图表名称', trigger: 'blur'},
        {min: 1, max: 25, message: '长度在 1 到 25 个字符', trigger: 'blur'}]"
      >
        <el-col :span="12">
          <el-input v-model="sizeForm.figureName"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item
        label="图表类型"
        prop="figureType"
        :rules="[{ required: true, message: '请选择展示类型', trigger: 'blur' }]"
      >
        <el-col :span="5">
          <el-select v-model="sizeForm.visualType" clearable placeholder="请选择展示类型">
            <el-option
              v-for="item in visual_ops"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="5" v-if="sizeForm.visualType===1">
          <el-select v-model="sizeForm.figureType" clearable placeholder="请选择图表类型">
            <el-option
              v-for="item in configure_ops1"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="5" v-if="sizeForm.visualType===2">
          <el-select v-model="sizeForm.figureType" clearable placeholder="请选择图表类型">
            <el-option
              v-for="item in configure_ops2"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="5" v-if="sizeForm.visualType===3">
          <el-select v-model="sizeForm.figureType" clearable placeholder="请选择图表类型">
            <el-option
              v-for="item in configure_ops3"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
      </el-form-item>
      <el-form-item label="坐标轴名称" v-if="sizeForm.figureType!=='map' && sizeForm.figureType!=='pie'">
        <el-col :span="4" style="margin-right:10px">
          <el-form-item label prop="xName">
            <el-input v-model="sizeForm.xName" placeholder="x轴名称/单位"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item label prop="yName">
            <el-input v-model="sizeForm.yName" placeholder="y轴名称/单位"></el-input>
          </el-form-item>
        </el-col>
      </el-form-item>
      <el-form-item
        label="X坐标轴范围"
        v-if="sizeForm.figureType!=='map' && sizeForm.figureType!=='pie'"
        :rules="[{required: true, message: '请输入x轴下限', trigger: 'blur'}]"
      >
        <el-col :span="3">
          <el-form-item
            prop="xRangeL"
            :rules="[{required: true, message: '请输入x轴下限', trigger: 'blur'}]"
          >
            <el-input v-model="sizeForm.xRangeL" placeholder="x轴下限"></el-input>
          </el-form-item>
        </el-col>
        <el-col style="text-align:center" :span="1">-</el-col>
        <el-col :span="3">
          <el-form-item
            prop="xRangeH"
            :rules="[{required: true, message: '请输入x轴上限', trigger: 'blur'}]"
          >
            <el-input v-model="sizeForm.xRangeH" placeholder="x轴上限"></el-input>
          </el-form-item>
        </el-col>
      </el-form-item>
      <el-form-item
        label="Y坐标轴范围"
        v-if="sizeForm.figureType!=='map' && sizeForm.figureType!=='pie'"
        :rules="[{required: true, message: '请输入x轴下限', trigger: 'blur'}]"
      >
        <el-col :span="3">
          <el-form-item
            prop="yRangeL"
            :rules="[{required: true, message: '请输入y轴下限', trigger: 'blur'}]"
          >
            <el-input v-model="sizeForm.yRangeL" placeholder="y轴下限"></el-input>
          </el-form-item>
        </el-col>
        <el-col style="text-align:center" :span="1">-</el-col>
        <el-col :span="3">
          <el-form-item
            prop="yRangeH"
            :rules="[{required: true, message: '请输入y轴上限', trigger: 'blur'}]"
          >
            <el-input v-model="sizeForm.yRangeH" placeholder="y轴上限"></el-input>
          </el-form-item>
        </el-col>
      </el-form-item>

      <el-form-item label="数量范围" v-if="sizeForm.figureType==='map'">
        <el-col :span="3">
          <el-form-item prop="xRangeL">
            <el-input v-model="sizeForm.RangeL" placeholder="数据下限"></el-input>
          </el-form-item>
        </el-col>
        <el-col style="text-align:center" :span="1">-</el-col>
        <el-col :span="3">
          <el-form-item prop="xRangeH">
            <el-input v-model="sizeForm.RangeH" placeholder="数据上限"></el-input>
          </el-form-item>
        </el-col>
      </el-form-item>

      <el-form-item
        label="数据"
        prop="xDataTitle"
        :rules="[ { required: true, message: '请选择数据', trigger: 'blur' }]"
        v-if="sizeForm.visualType===2||sizeForm.visualType===1"
      >
        <el-col :span="6" v-if="sizeForm.visualType===1">
          <el-select v-model="sizeForm.xDataTitle" clearable placeholder="请选择x轴类别/数据">
            <el-option
              v-for="item in x_data_ops"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="6" v-if="sizeForm.visualType===2">
          <el-select v-model="sizeForm.xDataTitle" clearable placeholder="请选择x轴类别/数据">
            <el-option
              v-for="item in y_data_ops"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="6" v-if="sizeForm.visualType===2||sizeForm.visualType===1">
          <el-select v-model="sizeForm.yDataTitle" clearable placeholder="请选择y轴数据">
            <el-option
              v-for="item in y_data_ops"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
      </el-form-item>
      <el-form-item
        label="数据"
        prop="cataDataTitle"
        :rules="[ { required: true, message: '请选择数据', trigger: 'blur' }]"
        v-if="sizeForm.figureType=='pie'"
      >
        <el-col :span="6">
          <el-select v-model="sizeForm.cataDataTitle" clearable placeholder="类别（可选）">
            <el-option
              v-for="item in cata_data_ops"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
      </el-form-item>
      <el-form-item
        label="数据"
        prop="cataDataTitle"
        v-if="sizeForm.figureType!='map' && sizeForm.figureType!='pie'"
      >
        <el-col :span="6">
          <el-select v-model="sizeForm.cataDataTitle" clearable placeholder="类别（可选）">
            <el-option
              v-for="item in cata_data_ops"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
      </el-form-item>
      <el-form-item
        label="数据"
        prop="mapDataTitle"
        :rules="[ { required: true, message: '请选择数据', trigger: 'blur' }]"
        v-if="sizeForm.figureType=='map'"
      >
        <el-col :span="6">
          <el-select v-model="sizeForm.mapDataTitle" clearable placeholder="类别（必选）">
            <el-option
              v-for="item in map_data_ops"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
      </el-form-item>
      <el-form-item
        label="APP中展示"
        prop="display"
        :rules="[{ required: true, message: '请选择是否在APP展示', trigger: 'change' }]"
      >
        <el-radio-group v-model="sizeForm.display">
          <el-radio label="1">是</el-radio>
          <!--boolean-->
          <el-radio label="0">否</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item size="large">
        <el-button type="primary" @click="submitForm('sizeForm')">提交</el-button>
        <el-button @click="previewForm('sizeForm')">预览</el-button>
        <el-button @click="resetForm('sizeForm')">重置</el-button>
      </el-form-item>
    </el-form>
    <el-dialog title="图表预览" :visible.sync="dialogPreview" ref="preview" width="800px">
      <div id="main" style="width: 700px;height:400px;text-align:center;margin:0 auto"></div>
    </el-dialog>
  </div>
</template>

<script>
import "../../../node_modules/echarts/map/js/china";
import global from "@/App";

export default {
  name: "selection",
  data() {
    return {
      // project_id: "", //其他页面传进来的
      dialogPreview: false,
      project_list: [],
      project_ops: "",
      visual_data: "",
      myLegends: [],
      mySeries: [],
      myXAxis: [],
      size: 0,
      sizeForm: {
        project_id: "",
        yShowType: "",
        figureName: "",
        figureType: "",
        visualType: "",
        cataDataTitle: "",
        xDataTitle: "",
        yDataTitle: "",
        xName: "",
        yName: "",
        xRangeL: "dataMin",
        xRangeH: "dataMax",
        yRangeL: "dataMin",
        yRangeH: "dataMax",
        display: "0",
        RangeL: "0",
        RangeH: "100",
        show_legend: ""
      },
      configure_ops1: [
        {
          value: "bar",
          label: "柱状图"
        },
        {
          value: "line",
          label: "折线图"
        }
      ],
      configure_ops2: [
        {
          value: "bar",
          label: "柱状图"
        },
        {
          value: "line",
          label: "折线图"
        },
        {
          value: "scatter",
          label: "散点图"
        }
      ],
      configure_ops3: [
        {
          value: "map",
          label: "地图"
        },
        {
          value: "pie",
          label: "扇形图"
        }
      ],
      visual_ops: [
        {
          value: 1,
          label: "对比类"
        },
        {
          value: 2,
          label: "描点类"
        },
        {
          value: 3,
          label: "展示类"
        }
      ],
      x_data_ops: [],
      y_data_ops: [],
      cata_data_ops: [],
      map_data_ops: []
    };
  },
  created() {
    this.fetchData();
  },
  watch: {
    "sizeForm.project_id": {
      handler(val) {
        this.updateOption();
      }
    }
  },
  mounted() {},
  methods: {
    fetchData() {
      this.axios.post(global.server + "admin/get_my_project").then(res => {
        if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
        this.project_list = res.data;
      });
    },
    updateOption() {
      let params = new URLSearchParams();
      params.append("project_id", this.sizeForm.project_id);
      this.axios.post(global.server + "get_data_ops", params).then(res => {
        console.log(res);
        console.log(res.data);
        this.x_data_ops = res.data.xData_ops;
        this.y_data_ops = res.data.yData_ops;
        this.cata_data_ops = res.data.cataData_ops;
        this.map_data_ops = res.data.mapData_ops;
      });
    },
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.sizeForm.figureType == "map") {
            this.$message({
              type: "warning",
              message: "提交地图可能等待时间较长，请稍等"
            });
          }
          let params = new URLSearchParams();
          params.append("project_id", this.sizeForm.project_id);
          params.append("is_display", this.sizeForm.display);
          params.append("figure_type", this.sizeForm.figureType);
          params.append("figure_title", this.sizeForm.figureName);
          params.append("visual_type", this.sizeForm.visualType);
          params.append("x_label", this.sizeForm.xName);
          params.append("y_label", this.sizeForm.yName);
          params.append("x_data_title", this.sizeForm.xDataTitle);
          params.append("y_data_title", this.sizeForm.yDataTitle);
          params.append("cata_data_title", this.sizeForm.cataDataTitle);
          params.append("map_data_title", this.sizeForm.mapDataTitle);
          if (this.sizeForm.figureType === "map") {
            params.append("x_rangeL", this.sizeForm.RangeL);
            params.append("x_rangeH", this.sizeForm.RangeH);
          } else {
            params.append("x_rangeL", this.sizeForm.xRangeL);
            params.append("x_rangeH", this.sizeForm.xRangeH);
          }
          params.append("y_rangeL", this.sizeForm.yRangeL);
          params.append("y_rangeH", this.sizeForm.yRangeH);
          this.axios
            .post(global.server + "add_visualization", params)
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
              console.log(res);
              console.log(res.data);
              this.$message({
                message: "提交成功",
                type: "success"
              });
              // this.$router.push('/Myvisual')
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetForm(formName) {
      this.sizeForm.visualType = "";
      this.sizeForm.xDataTitle = "";
      this.sizeForm.yDataTitle = "";
      this.sizeForm.cataDataTitle = "";
      this.sizeForm.mapDataTitle = "";
      this.$refs[formName].resetFields();
    },
    previewForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.dialogPreview = true;
          this.$nextTick(() => {
            this.drawChart();
          });
          // this.bus.$emit("main",this.sizeForm);
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    drawChart() {
      //基于准备好的dom，初始化echarts实例
      let params = new URLSearchParams();
      params.append("project_id", this.sizeForm.project_id);
      params.append("x_data_title", this.sizeForm.xDataTitle);
      params.append("y_data_title", this.sizeForm.yDataTitle);
      params.append("cata_data_title", this.sizeForm.cataDataTitle);
      params.append("visual_type", this.sizeForm.visualType);
      params.append("figure_type", this.sizeForm.figureType);
      params.append("map_data_title", this.sizeForm.mapDataTitle);
      var tmp = [];
      this.axios
        .post(global.server + "get_visual_data", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          this.visual_data = res.data.mydata;
          this.myXAxis = res.data.myxAxis;
          this.size = res.data.mySize;
          this.myLegends = res.data.myLegends;
        })
        .then(() => {
          for (var i = 0; i < this.size; i++) {
            tmp.push({
              name: this.myLegends[i],
              data: this.visual_data[i],
              type: this.sizeForm.figureType
            });
          }
          let myChart = this.$echarts.init(document.getElementById("main"));
          // 指定图表的配置项和数据
          console.log(tmp);
          let option1 = {
            backgroundColor: "#404a59",
            title: {
              text: this.sizeForm.figureName,
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
              min: this.sizeForm.RangeL,
              max: this.sizeForm.RangeH,
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
                symbolSize: 5,
                emphasis: {
                  itemStyle: {
                    borderColor: "#fff",
                    borderWidth: 1
                  }
                }
              }
            ]
          };

          let option2 = {
            title: {
              text: this.sizeForm.figureName
            },
            tooltip: {},
            legend: {
              data: this.myLegends,
              orient: "vertical",
              top: "top",
              left: "right",
            },
            xAxis: {
              name: this.sizeForm.xName,
              type: "category",
              data: this.myXAxis,
              nameLocation: "middle",
              nameGap: 20,
              min: this.sizeForm.xRangeL,
              max: this.sizeForm.xRangeH
            },
            yAxis: {
              type: "value",
              name: this.sizeForm.yName,
              min: this.sizeForm.yRangeL,
              max: this.sizeForm.yRangeH
            },
            series: tmp
          };
          let option3 = {
            legend: {
              orient: "vertical",
              left: "right",
              data: this.myLegends,
              orient: "vertical",
              top: "top",
              left: "right",
            },
            title: {
              text: this.sizeForm.figureName
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
              text: this.sizeForm.figureName
            },
            tooltip: {},
            legend: {
              data: this.myLegends,
              orient: "vertical",
              top: "top",
              left: "right",
            },
            xAxis: {
              type: "value",
              name: this.sizeForm.xName,
              min: this.sizeForm.xRangeL,
              max: this.sizeForm.xRangeH,
              nameLocation: "middle",
              nameGap: 20
            },
            yAxis: {
              type: "value",
              name: this.sizeForm.yName,
              min: this.sizeForm.yRangeL,
              max: this.sizeForm.yRangeH
            },
            series: tmp
          };
          // 使用刚指定的配置项和数据显示图表。
          if (this.sizeForm.figureType === "map") {
            myChart.clear();
            myChart.setOption(option1);
          } else if (
            this.sizeForm.figureType === "bar" ||
            this.sizeForm.figureType === "line"
          ) {
            myChart.clear();
            myChart.setOption(option2);
          } else if (this.sizeForm.figureType === "pie") {
            myChart.clear();
            myChart.setOption(option3);
          } else if (this.sizeForm.figureType === "scatter") {
            myChart.clear();
            myChart.setOption(option4);
          }
        });
    }
  }
};
</script>

<style scoped>
.selectSize {
  width: 360px;
}
</style>
