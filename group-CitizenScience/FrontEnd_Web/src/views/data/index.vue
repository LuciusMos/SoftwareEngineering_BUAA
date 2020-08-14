<style>
.demo-table-expand {
  font-size: 0;
}
.demo-table-expand label {
  width: 200px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
.el-message {
  line-height: 16px;
}
</style>

<template>
  <div class="app-container">
    <el-header>
      <el-select
        style="padding:0 0;float: left;width:300px"
        v-model="chooseProject"
        filterable
        placeholder="请选择项目（可输入）"
      >
        <el-option
          v-for="item in project_list"
          :key="item.project_id"
          :label=" item.project_title + ' (项目ID:' +item.project_id + ')'"
          :value="item.project_id"
        ></el-option>
      </el-select>
      <el-button
        style="margin-left:40px;margin-top:2px"
        type="primary"
        size="medium"
        @click="showOutput=true"
      >批量导出</el-button>

      <el-switch
        style="margin-left:40px;margin-top:2px"
        v-model="dis_unrate"
        active-text="未标注"
        inactive-text="已标注"
      ></el-switch>
      <el-input
        style="padding:0 0;float:right;width: 160px"
        v-model="search"
        placeholder="请输入检索内容"
        suffix-icon="el-icon-edit"
      ></el-input>
    </el-header>
    <el-table
      ref="dataTable"
      v-loading="listLoading"
      :data="showList.slice((currentPage-1)*pagesize,currentPage*pagesize)"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      :row-style="{height:'20px'}"
      :cell-style="{padding:'5px'}"
      empty-text="请先选择项目或该项目暂无用户上传数据"
      @sort-change="sortChange"
    >
      <el-table-column type="expand">
        <template slot-scope="scope">
          <el-form label-position="left" class="demo-table-expand">
            <el-form-item
              v-for="(d, index) in scope.row.datas"
              :key="d.data_id"
              :label="d.data_name"
              label-width="auto"
            >
              <span v-if="d.data_type != 5">{{ d.content }}</span>
              <el-button
                type="text"
                v-if="d.data_type == 5"
                @click="showPic(d.content)"
              >查看图片 (置信度:{{d.ai}})</el-button>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column align="center" label="提交ID" width="90">
        <template slot-scope="scope">{{ scope.row.submit_id }}</template>
      </el-table-column>
      <el-table-column label="上传者 (用户名)" align="center" width>
        <template slot-scope="scope">
          <!-- <span>{{ scope.row.user_id }}</span> -->
          <el-button
            type="text"
            @click="handleDetail(scope.index,scope.row)"
          >{{scope.row.user_nickname}} (用户ID:{{ scope.row.user_id }})</el-button>
        </template>
      </el-table-column>
      <el-table-column label="平均置信度" align="center" width="120" sortable>
        <template slot-scope="scope">{{ scope.row.avg_ai }}</template>
      </el-table-column>
      <el-table-column align="center" prop="submit_time" label="提交时间" width="180">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.submit_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="审核者" align="center" width>
        <template slot-scope="scope" v-if="scope.row.e_user_id">
          <el-button
            type="text"
            @click="handleDetail(scope.index,scope.row)"
          >{{scope.row.e_user_name}} (用户ID:{{ scope.row.e_user_id }})</el-button>
        </template>
      </el-table-column>
      <el-table-column label="得分" align="center" width="90" sortable prop="star_rating">
        <template slot-scope="scope" v-if="scope.row.star_rating>-1">
          <el-tag
            :type="scope.row.star_rating | rateFilter"
            size="medium"
          >{{ scope.row.star_rating }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="数据标注" align="center" width="220">
        <template slot-scope="scope">
          <el-button
            style="margin-left:0"
            size="mini"
            @click="rate=true;chooseId=scope.row.submit_id;chooseIndex=scope.$index"
          >打分</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="danger"
            @click="rate0=true;chooseId=scope.row.submit_id;chooseIndex=scope.$index"
          >无效</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="primary"
            @click="outputZip(scope.row, scope.$index)"
          >导出</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      style="text-align:center;margin-top:10px"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :page-sizes="[10, 15, 20]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="showList.length"
    ></el-pagination>
    <el-dialog title="数据标注(五级制)" :visible.sync="rate" width="300px">
      <div style="text-align:center;margin-bottom:10px">
        <span>提交ID:{{chooseId}}</span>
      </div>
      <el-rate
        v-model="score"
        :colors="{ 2: '#99A9BF', 4: { value: '#F7BA2A', excluded: true }, 5: '#FF9900' }"
        show-score
        style="text-align:center;margin-bottom:20px"
      ></el-rate>
      <el-input type="textarea" autosize placeholder="请输入评价内容" v-model="rateContent"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="confirmRate">提交</el-button>
      </span>
    </el-dialog>
    <el-dialog title="标注无效" :visible.sync="rate0" width="300px">
      <div style="text-align:center;margin-bottom:20px">
        <span>提交ID:{{chooseId}} 为无效数据</span>
      </div>
      <el-input type="textarea" autosize placeholder="请输入理由" v-model="rateContent"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="invalid">提交</el-button>
      </span>
    </el-dialog>
    <el-dialog title="个人详情" :visible.sync="dialogDetailUser">
      <el-row style="margin-bottom:25px" type="flex" justify="center">
        <el-col :span="6" style="text-align:right">
          <b>真实姓名：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.user_realname}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:25px" type="flex" justify="center">
        <el-col :span="6" style="text-align:right">
          <b>用户ID：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.user_id}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:25px" type="flex" justify="center">
        <el-col :span="6" style="text-align:right">
          <b>用户名：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.user_nickname}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:25px" type="flex" justify="center">
        <el-col :span="6" style="text-align:right">
          <b>邮箱：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.user_email}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:25px" type="flex" justify="center">
        <el-col :span="6" style="text-align:right">
          <b>注册时间：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.register_time}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:25px" type="flex" justify="center">
        <el-col :span="6" style="text-align:right">
          <b>申请时间：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.apply_time}}</span>
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.association != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>工作单位/学校：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.association}}</span>
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.research_team != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>所属团队：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.research_team}}</span>
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.photo_url != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>个人照片：</b>
        </el-col>
        <el-col :span="17">
          <el-image
            style="width:200px"
            :src="global.noPortServer +'file/image/photo/'+detailform.photo_url"
          />
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.resume_url != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>简历：</b>
        </el-col>
        <el-col :span="17">
          <el-image
            style="width:350px"
            :src="global.noPortServer +'file/image/proofphoto/' + detailform.resume_url"
          />
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.job_title != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>职称：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.job_title}}</span>
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.academic_degree != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>学历：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.academic_degree}}</span>
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.research_area != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>研究方向：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.research_area}}</span>
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.personal_info != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>个人简介：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailform.personal_info}}</span>
        </el-col>
      </el-row>
      <el-row
        style="margin-bottom:25px"
        type="flex"
        justify="center"
        v-if="detailform.proof_photo != null"
      >
        <el-col :span="6" style="text-align:right">
          <b>证明文件：</b>
        </el-col>
        <el-col :span="17">
          <el-button style="margin-top:0px" type="primary" @click="outputZip()" size="mini">点击下载</el-button>
        </el-col>
      </el-row>
    </el-dialog>
    <el-dialog title="查看图片" :visible.sync="onPic" style="margin:0 auto;text-align:center">
      <el-image :src="picUrl"></el-image>
      <span slot="footer" class="dialog-footer">
        <el-button @click="onPic = false">返回</el-button>
      </span>
    </el-dialog>
    <el-dialog title="批量导出" :visible.sync="showOutput">
      <el-checkbox
        :indeterminate="isIndeterminate"
        v-model="checkAll"
        @change="handleCheckAllChange"
      >全选</el-checkbox>
      <div style="margin: 15px 0;"></div>
      <el-checkbox-group
        v-model="checkedScores"
        @change="handleCheckedScoreChange"
        style="margin:0 auto;text-align:center"
      >
        <el-checkbox v-for="score in scores" :label="score[0]" :key="score[0]">{{score}}</el-checkbox>
      </el-checkbox-group>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="confirmOutputs">导出</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import global from "@/App";

export default {
  filters: global.tagFilter,
  data() {
    return {
      dialogDetailUser: false,
      detailform: [],
      showList: [],
      dis_unrate: true,
      checkAll: false,
      checkedScores: [],
      scores: ["0分", "1分", "2分", "3分", "4分", "5分"],
      isIndeterminate: true,
      showOutput: false,
      rate0: false,
      chooseProject: "",
      rateContent: "",
      project_list: [],
      global: global,
      chooseId: "",
      chooseIndex: 0,
      currentPage: 1,
      pagesize: 10,
      onPic: false,
      onText: false,
      rate: false,
      listLoading: false,
      picUrl: "",
      text: "",
      score: null,
      list: [],
      search: "",
      iconClasses: ["icon-rate-face-1", "icon-rate-face-2", "icon-rate-face-3"]
    };
  },
  created() {
    this.fetchData();
  },
  watch: {
    chooseProject: {
      handler(val) {
        this.$refs.dataTable.clearSort();
        this.fetchProjectData();
      }
    },
    dis_unrate: {
      handler(val) {
        if (val) {
          this.showList = this.list.filter(
            data =>
              (!this.search ||
                data.submit_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_nickname
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase())) &&
              data.star_rating == -1
          );
        } else {
          this.showList = this.list.filter(
            data =>
              (!this.search ||
                data.submit_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_nickname
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase())) &&
              data.star_rating > -1
          );
        }
      }
    },
    search: {
      handler(val) {
        if (this.dis_unrate) {
          this.showList = this.list.filter(
            data =>
              (!val ||
                data.submit_id
                  .toString()
                  .toLowerCase()
                  .includes(val.toLowerCase()) ||
                data.user_nickname.toLowerCase().includes(val.toLowerCase()) ||
                data.user_id
                  .toString()
                  .toLowerCase()
                  .includes(val.toLowerCase())) &&
              data.star_rating == -1
          );
        } else {
          this.showList = this.list.filter(
            data =>
              (!val ||
                data.submit_id
                  .toString()
                  .toLowerCase()
                  .includes(val.toLowerCase()) ||
                data.user_nickname.toLowerCase().includes(val.toLowerCase()) ||
                data.user_id
                  .toString()
                  .toLowerCase()
                  .includes(val.toLowerCase())) &&
              data.star_rating > -1
          );
        }
      }
    }
  },
  methods: {
    handleDetail(index, row) {
      let params = new URLSearchParams();
      this.chooseId = row.user_id;
      params.append("id", row.user_id);
      this.axios
        .post(
          global.server + "admin/get_data/detail_scientist_assistant",
          params
        )
        .then(res => {
          console.log(res);
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          this.detailform = res.data;
          this.listLoading = false;
          this.dialogDetailUser = true;
        });
      console.log(index, row);
    },
    confirmOutputs() {
      let params = new URLSearchParams();
      params.append("project_id", this.chooseProject);
      params.append("checked_score", JSON.stringify(this.checkedScores));
      this.$message({ type: "success", message: "正在加载下载资源..." });
      this.axios
        .post(global.server + "admin/output_datas", params, {
          responseType: "blob"
        })
        .then(response => {
          if (response.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(response);
          let blob = new Blob([response.data], { type: "application/zip" });
          let url = window.URL.createObjectURL(blob);
          const link = document.createElement("a"); // 创建a标签
          link.href = url;
          link.download = "批量导出_项目ID:" + this.chooseProject; // 重命名文件
          link.click();
          URL.revokeObjectURL(url); // 释放内存
        });
    },
    handleCheckAllChange(val) {
      this.checkedScores = val ? ["0", "1", "2", "3", "4", "5"] : [];
      this.isIndeterminate = false;
    },
    handleCheckedScoreChange(value) {
      console.log(this.checkedScores);
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.scores.length;
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.scores.length;
    },
    sortChange(column, prop, order) {
      this.listLoading = true;
      console.log(column);
      if (column.prop == "star_rating") {
        if (column.order == "ascending") {
          this.list.sort(this.mySortAsc);
        } else {
          this.list.sort(this.mySortDsc);
        }
      } else {
        if (column.order == "ascending") {
          this.list.sort(this.mySortAsc2);
        } else {
          this.list.sort(this.mySortDsc2);
        }
      }
      this.listLoading = false;
    },
    mySortAsc(a, b) {
      return a.star_rating - b.star_rating;
    },
    mySortDsc(a, b) {
      return -a.star_rating + b.star_rating;
    },
    mySortAsc2(a, b) {
      return a.avg_ai - b.avg_ai;
    },
    mySortDsc2(a, b) {
      return -a.avg_ai + b.avg_ai;
    },
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
        this.chooseProject = this.project_list[
          this.project_list.length - 1
        ].project_id;
      });
    },
    fetchProjectData() {
      let params = new URLSearchParams();
      params.append("project_id", this.chooseProject);
      this.axios
        .post(global.server + "admin/get_data/data", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(res.data);
          this.list = res.data;
          this.showList = this.list
          if (this.dis_unrate) {
          this.showList = this.list.filter(
            data =>
              (!this.search ||
                data.submit_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_nickname
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase())) &&
              data.star_rating == -1
          );
        } else {
          this.showList = this.list.filter(
            data =>
              (!this.search ||
                data.submit_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_nickname
                  .toLowerCase()
                  .includes(this.search.toLowerCase()) ||
                data.user_id
                  .toString()
                  .toLowerCase()
                  .includes(this.search.toLowerCase())) &&
              data.star_rating > -1
          );
        }
          this.listLoading = false;
        });
    },
    showPic(url) {
      this.picUrl = global.noPortServer + "file/image/dataimage/" + url;
      this.onPic = true;
    },
    showText(row) {
      console.log(row);
    },
    invalid() {
      let params = new URLSearchParams();
      params.append("submit_id", this.chooseId);
      params.append("rateContent", this.rateContent);
      params.append("rate", 0);
      this.listLoading = true;
      this.axios
        .post(global.server + "admin/upload_data/rate", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          this.rate0 = false;
          this.score = 0;
          this.rateContent = "";
          this.fetchProjectData();
          this.listLoading = false;
          this.$message({ type: "info", message: "您已标注该数据无效！" });
        });
      console.log(row, index);
    },
    confirmRate() {
      let params = new URLSearchParams();
      params.append("submit_id", this.chooseId);
      params.append("rate", this.score);
      params.append("rateContent", this.rateContent);
      this.listLoading = true;
      this.axios
        .post(global.server + "admin/upload_data/rate", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          this.list[this.chooseIndex].star_rating = this.score;
          this.score = 0;
          this.rate = false;
          this.rateContent = "";
          this.$message({ type: "success", message: "您已成功打分！" });
          this.fetchProjectData();
          this.listLoading = false;
        });
    },
    outputZip(row, index) {
      let params = new URLSearchParams();
      params.append("submit_id", row.submit_id);
      this.axios
        .post(global.server + "admin/zip", params, {
          responseType: "blob"
        })
        .then(response => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(response);
          let blob = new Blob([response.data], { type: "application/zip" });
          let url = window.URL.createObjectURL(blob);
          const link = document.createElement("a"); // 创建a标签
          link.href = url;
          link.download = "项目ID：" + row.submit_id; // 重命名文件
          link.click();
          URL.revokeObjectURL(url); // 释放内存
        });
    },
    handleSizeChange(val) {
      this.pagesize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    }
  }
};
</script>
