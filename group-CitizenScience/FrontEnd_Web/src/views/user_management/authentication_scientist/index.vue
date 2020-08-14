<template>
  <div class="app-container">
    <el-header style="padding:0 0;float:right">
      <el-input v-model="search" placeholder="请输入检索内容" suffix-icon="el-icon-edit"></el-input>
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
      <el-table-column align="center" label="用戶ID" width="95">
        <template slot-scope="scope">{{ scope.row.user_id }}</template>
      </el-table-column>
      <el-table-column label="真实姓名" align="center" width="95">
        <template slot-scope="scope">{{ scope.row.user_realname }}</template>
      </el-table-column>
      <el-table-column label="工作单位/学校" align="center">
        <template slot-scope="scope">{{ scope.row.association }}</template>
      </el-table-column>、
      <el-table-column label="所属团队" align="center">
        <template slot-scope="scope">{{ scope.row.research_team }}</template>
      </el-table-column>
      <el-table-column align="center" prop="apply_time" label="申请时间" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.apply_time }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="210">
        <template slot-scope="scope">
          <el-button
            style="margin-left:0"
            size="mini"
            @click="handleDetail(scope.$index, scope.row)"
          >详情</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="success"
            @click="handleAccept(scope.$index, scope.row)"
          >同意</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="danger"
            @click="handleRefuse(scope.$index, scope.row)"
          >拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
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
    <el-dialog title="拒绝理由" :visible.sync="dialogReason">
      <el-input type="textarea" autosize placeholder="请输入拒绝理由" v-model="reason"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="confirmRefuse">提交</el-button>
      </span>
    </el-dialog>
    <el-pagination
      style="text-align:center;margin-top:10px"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :page-sizes="[10, 15, 20]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="showList.length"
    ></el-pagination>
  </div>
</template>

<script>
import global from "@/App";

export default {
  data() {
    return {
      showList:[],
      reason: "",
      chooseId: "",
      dialogReason: false,
      chooseIndex: -1,
      chooseRow: {},
      global: global,
      dialogDetail: false,
      detailform: [],
      search: "",
      list: [],
      listLoading: true,
      currentPage: 1,
      pagesize: 10
    };
  },
  created() {
    this.fetchData();
  },
  watch:{
    search:{
      handler(val){
        this.showList = this.list.filter(data => !val || data.user_id.toString().toLowerCase().includes(val.toLowerCase())
                          || data.association.toLowerCase().includes(val.toLowerCase())
                          || data.user_realname.toLowerCase().includes(val.toLowerCase())
                          || data.apply_time.toLowerCase().includes(val.toLowerCase())
                          || data.research_team.toLowerCase().includes(val.toLowerCase()))
      }
    }
  },
  methods: {
    outputZip() {
      let params = new URLSearchParams();
      params.append("id", this.chooseId);
      this.axios
        .post(global.server + "admin/proof_zip", params, {
          responseType: "blob"
        })
        .then(response => {
          console.log(response);
          let blob = new Blob([response.data], { type: "application/zip" });
          let url = window.URL.createObjectURL(blob);
          const link = document.createElement("a"); // 创建a标签
          link.href = url;
          link.download = "证明文件_用户ID:" + this.chooseId; // 重命名文件
          link.click();
          URL.revokeObjectURL(url); // 释放内存
        });
    },
    fetchData() {
      this.listLoading = true;
      this.axios
        .post(global.server + "admin/get_data/authen_scientist")
        .then(res => {
          if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
          this.list = res.data;
          this.showList = res.data;
          this.listLoading = false;
        });
    },
    handleDetail(index, row) {
      let params = new URLSearchParams();
      params.append("id", row.user_id);
      this.chooseId = row.user_id;
      this.axios
        .post(
          global.server + "admin/get_data/detail_scientist_assistant",
          params
        )
        .then(res => {
          if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
          this.dialogDetail = true;
          this.detailform = res.data;
          this.listLoading = false;
        });
      console.log(index, row);
    },
    handleAccept(index, row) {
      let params = new URLSearchParams();
      params.append("id", row.user_id);
      this.axios
        .post(global.server + "admin/upload_data/accept_scientist", params)
        .then(res => {
          if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
          if (res.data == "success") {
            this.$message({
              type: "success",
              message: "您已通过该科学家申请！"
            });
            this.fetchData();
          }
        });
      console.log(index, row);
    },
    handleRefuse(index, row) {
      //console.log(index, row);
      this.dialogReason = true;
      this.chooseIndex = index;
      this.chooseRow = row;
    },
    confirmRefuse() {
      let params = new URLSearchParams();
      params.append("content", this.reason);
      params.append("user_id", this.chooseRow.user_id);
      this.axios
        .post(global.server + "admin/upload_data/refuse_scientist", params)
        .then(res => {
          if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
          this.dialogReason = false;
          this.reason = "";
          this.$message({
            type: "info",
            message: "您已拒绝该科学家申请！"
          });
          this.fetchData();
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
