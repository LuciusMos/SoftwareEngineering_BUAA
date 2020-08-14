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
          :label="item.project_title + ' (项目ID:' + item.project_id + ')'"
          :value="item.project_id"
        ></el-option>
      </el-select>
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
      empty-text="请先选择项目"
      @sort-change="sortChange"
    >
      <el-table-column align="center" label="用户ID" width="100">
        <template slot-scope="scope">{{ scope.row.user_id }}</template>
      </el-table-column>
      <el-table-column align="center" label="用户名" width="150">
        <template slot-scope="scope">{{ scope.row.user_nickname }}</template>
      </el-table-column>
      <el-table-column align="center" label="真实姓名" width="150">
        <template slot-scope="scope">{{ scope.row.user_realname }}</template>
      </el-table-column>
      <el-table-column label="用户身份" align="center" width="110" sortable prop="identity">
        <template slot-scope="scope">
          <el-tag
            :type="scope.row.identity | identityFilter"
            effect="plain"
          >{{ userMap[scope.row.identity-1] }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="join_time" label="加入时间">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.join_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="提交数据" align="center" width="100">
        <template slot-scope="scope">{{ scope.row.submit_amount }}</template>
      </el-table-column>
      <el-table-column label="平均得分" align="center" width="110" sortable prop="star_rating">
        <template slot-scope="scope" v-if="scope.row.star_rating>-1">
          <el-tag
            :type="Math.round(scope.row.star_rating) | rateFilter"
            size="medium"
          >{{ scope.row.star_rating }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="220">
        <template slot-scope="scope">
          <el-button
            size="mini"
            :disabled="scope.row.user_realname == null"
            @click="handleDetail(scope.$index, scope.row)"
          >详情</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="danger"
            disabled
            @click="deleteUser(scope.row, scope.$index)"
          >删除</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="primary"
            @click="inform=true;chooseId=scope.row.user_id;"
          >通知</el-button>
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
    <el-dialog title="个人详情" :visible.sync="dialogDetail">
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
    <el-dialog title="发布通知" :visible.sync="inform" width="300px">
      <div style="margin-bottom:15px;text-align:center">
        <el-radio-group v-model="toall">
          <el-radio :label="0">用户ID:{{chooseId}}</el-radio>
          <el-radio :label="1">群发</el-radio>
        </el-radio-group>
      </div>
      <el-input type="textarea" autosize placeholder="请输入通知内容" v-model="informContent"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="confirmInform">发送</el-button>
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
      userMap: ["志愿者", "助理", "科学家"],
      chooseProject: "",
      informContent: "",
      project_list: [],
      global: global,
      chooseId: "",
      chooseIndex: 0,
      currentPage: 1,
      pagesize: 10,
      inform: false,
      toall: 0,
      listLoading: false,
      text: "",
      score: null,
      showList: [],
      list: [],
      search: "",
      dialogDetail: false,
      detailform: []
    };
  },
  created() {
    this.fetchData();
  },
  watch: {
    chooseProject: {
      handler(val) {
        this.$refs.dataTable.clearSort();
        this.fetchUserData();
      }
    },
    search: {
      handler(val) {
        this.showList = this.list.filter(
          data =>
            !val ||
            data.user_id
              .toString()
              .toLowerCase()
              .includes(val.toLowerCase()) ||
            data.identity
              .toString()
              .toLowerCase()
              .includes(val.toLowerCase()) ||
            data.user_realname.toLowerCase().includes(val.toLowerCase()) ||
            data.user_nickname.toLowerCase().includes(val.toLowerCase())
        );
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
          this.dialogDetail = true;
        });
      console.log(index, row);
    },
    sortChange(column, prop, order) {
      this.listLoading = true;
      console.log(column);
      if (prop == "star_rating") {
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
      return a.identity - b.identity;
    },
    mySortDsc2(a, b) {
      return -a.identity + b.identity;
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
    fetchUserData() {
      let params = new URLSearchParams();
      params.append("project_id", this.chooseProject);
      this.axios
        .post(global.server + "admin/get_data/up_data", params)
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
          this.showList = res.data;
          this.listLoading = false;
        });
    },
    deleteUser(row, index) {
      this.chooseId = row.user_id;
      let params = new URLSearchParams();
      params.append("submit_id", row.submit_id);
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
          //console.log(res);
          this.list[index].star_rating = 0;
          this.listLoading = false;
          this.$message({ type: "info", message: "您已标注该数据无效！" });
        });
      console.log(row, index);
    },
    confirmInform() {
      let params = new URLSearchParams();
      if (this.toall == 0) {
        params.append("user_id", this.chooseId);
      } else {
        params.append("user_id", "all");
      }
      params.append("project_id", this.chooseProject);
      params.append("informContent", this.informContent);
      this.listLoading = true;
      this.axios
        .post(global.server + "admin/upload_data/inform", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          //console.log(res);
          this.inform = false;
          this.informContent = "";
          if (this.toall == 0) {
            this.$message({ type: "success", message: "您已成功通知该用户！" });
          } else {
            this.$message({
              type: "success",
              message: "您已成功群发至团队内用户！"
            });
          }
          this.listLoading = false;
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
