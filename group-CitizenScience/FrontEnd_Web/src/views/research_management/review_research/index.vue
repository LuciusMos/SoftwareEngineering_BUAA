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
      <el-table-column align="center" label="状态" width="110">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" label="项目ID" width="95">
        <template  slot-scope="scope">{{ scope.row.project_id }}</template>
        <!-- <template v-else slot-scope="scope">{{ scope.row.project_id }}</template> -->
      </el-table-column>
      <el-table-column label="项目名称" align="center">
        <template slot-scope="scope">{{ scope.row.project_title }}</template>
      </el-table-column>
      <el-table-column label="发起人" width="180" align="center" prop="user_id">
        <template slot-scope="scope">
          <!-- <span>{{ scope.row.user_id }}</span> -->
          <el-button
            type="text"
            @click="handleUserDetail(scope.index,scope.row)"
          >{{scope.row.user_realname}} (用户ID:{{ scope.row.user_id }})</el-button>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="是否公开" width="90" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_public | publicFilter">{{ scope.row.is_public }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="project_start_time" label="创建时间" width="150">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.project_start_time }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="220">
        <template slot-scope="scope">
          <el-button
            style="margin-left:0"
            size="mini"
            v-if="scope.row.status == '重新审核'"
            @click="handleDetail2(scope.$index, scope.row)"
          >对比</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            v-else
            @click="handleDetail(scope.$index, scope.row)"
          >详情</el-button>
          <!-- <el-button style="margin-left:0" size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button> -->
          <el-button
            style="margin-left:0"
            size="mini"
            type="success"
            @click="handleAccept(scope.$index, scope.row)"
          >通过</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="danger"
            @click="handleRefuse(scope.$index, scope.row)"
          >拒绝</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="查看详情（左边为原项目详情，右边为新项目详情）" center :visible.sync="dialogDetail2" width="1250px">
      <el-row :gutter="2">
        <el-col :span="12">
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目名称：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.project_title}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>数据采集起止日期：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.data_start_time}}</span>
              <b>起至</b>
              <span>{{detailForm.data_end_time}}</span>
              <b>止</b>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>预计项目截止日期：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.end_time}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目类型：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.category}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>所属学科：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.branch}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目描述：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.project_introduction}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>参与方式：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.way_of_participation}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>背景资料：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.background_knowledge}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>注意事项：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm.note}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目主图：</b>
            </el-col>
            <el-col :span="17">
              <el-image
                style="width:350px"
                :src="global.noPortServer +'file/image/projectmainimage/'+detailForm.project_main_image_url"
              />
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right;margin-top:15px">
              <b>项目助理：</b>
            </el-col>
            <el-col :span="12">
              <el-table :data="detailForm.assistants" border stripe :cell-style="{padding:'4px'}">
                <el-table-column prop="id" label="ID"></el-table-column>
                <el-table-column prop="name" label="姓名"></el-table-column>
              </el-table>
            </el-col>
            <el-col :span="6"></el-col>
          </el-row>
        </el-col>
        <el-col :span="12">
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目名称：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.project_title}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>数据采集起止日期：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.data_start_time}}</span>
              <b>起至</b>
              <span>{{detailForm2.data_end_time}}</span>
              <b>止</b>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>预计项目截止日期：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.end_time}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目类型：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.category}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>所属学科：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.branch}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目描述：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.project_introduction}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>参与方式：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.way_of_participation}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>背景资料：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.background_knowledge}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>注意事项：</b>
            </el-col>
            <el-col :span="17">
              <span>{{detailForm2.note}}</span>
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right">
              <b>项目主图：</b>
            </el-col>
            <el-col :span="17">
              <el-image
                style="width:350px"
                :src="global.noPortServer +'file/image/projectmainimage/'+detailForm2.project_main_image_url"
              />
            </el-col>
          </el-row>
          <el-row style="margin-bottom:30px" type="flex" justify="center">
            <el-col :span="6" style="text-align:right;margin-top:15px">
              <b>项目助理：</b>
            </el-col>
            <el-col :span="12">
              <el-table :data="detailForm2.assistants" border stripe :cell-style="{padding:'4px'}">
                <el-table-column prop="id" label="ID"></el-table-column>
                <el-table-column prop="name" label="姓名"></el-table-column>
              </el-table>
            </el-col>
            <el-col :span="6"></el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-dialog>
    <el-dialog title="查看详情" :visible.sync="dialogDetail">
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>项目名称：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.project_title}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>数据采集起止日期：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.data_start_time}}</span>
          <b>起至</b>
          <span>{{detailForm.data_end_time}}</span>
          <b>止</b>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>预计项目截止日期：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.end_time}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>项目类型：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.category}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>所属学科：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.branch}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>项目描述：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.project_introduction}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>参与方式：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.way_of_participation}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>背景资料：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.background_knowledge}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>注意事项：</b>
        </el-col>
        <el-col :span="17">
          <span>{{detailForm.note}}</span>
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right">
          <b>项目主图：</b>
        </el-col>
        <el-col :span="17">
          <el-image
            style="width:350px"
            :src="global.noPortServer +'file/image/projectmainimage/'+detailForm.project_main_image_url"
          />
        </el-col>
      </el-row>
      <el-row style="margin-bottom:30px" type="flex" justify="center">
        <el-col :span="5" style="text-align:right;margin-top:15px">
          <b>项目助理：</b>
        </el-col>
        <el-col :span="12">
          <el-table :data="detailForm.assistants" border stripe :cell-style="{padding:'4px'}">
            <el-table-column prop="id" label="ID"></el-table-column>
            <el-table-column prop="name" label="姓名"></el-table-column>
          </el-table>
        </el-col>
        <el-col :span="5"></el-col>
      </el-row>
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
  filters: global.tagFilter,
  data() {
    return {
      showList: [],
      dialogDetailUser: false,
      dialogReason: false,
      reason: "",
      chooseRow: {},
      chooseIndex: -1,
      reason: "",
      global: global,
      currentPage: 1,
      pagesize: 10,
      list: [],
      listLoading: true,
      search: "",
      dialogDelete: false,
      dialogDetail: false,
      dialogDetail2: false,
      detailForm: [],
      detailForm2: [],
      detailform: [],
      dialogDetail2: false
    };
  },
  watch: {
    search: {
      handler(val) {
        this.showList = this.list.filter(
          data =>
            !val ||
            data.project_title.toLowerCase().includes(val.toLowerCase()) ||
            data.project_id
              .toString()
              .toLowerCase()
              .includes(val.toLowerCase()) ||
            data.user_id
              .toString()
              .toLowerCase()
              .includes(val.toLowerCase()) ||
            data.user_realname.toLowerCase().includes(val.toLowerCase())
        );
      }
    }
  },
  created() {
    this.fetchData();
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
    handleUserDetail(index, row) {
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
    fetchData() {
      this.listLoading = true;
      this.axios
        .post(global.server + "admin/get_data/review_research")
        .then(res => {
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
          console.log(res.data);
          this.listLoading = false;
        });
      // getList().then(response => {
      //   this.list = response.data.items;
      //   this.listLoading = false;
      // });
    },
    handleDetail(index, row) {
      //console.log(index, row);
      let params = new URLSearchParams();
      params.append("detailId", row.project_id);
      this.axios
        .post(global.server + "admin/get_data/show_detail", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(res.data);
          this.detailForm = res.data;
          this.detailForm.branch = this.detailForm.branch.join("，");
          this.dialogDetail = true;
        });
    },
    handleDetail2(index, row) {
      // console.log(index, row);
      let params = new URLSearchParams();
      params.append("detailId", row.project_id);
      this.axios
        .post(global.server + "admin/get_data/show_detail", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(res.data);
          this.detailForm = res.data;
          this.detailForm.branch = this.detailForm.branch.join("，");
          // this.dialogDetail = true;
        });
      // console.log(index, row);
      params = new URLSearchParams();
      params.append("detailId", row.prev_id);
      this.axios
        .post(global.server + "admin/get_data/show_detail", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(res.data);
          this.detailForm2 = res.data;
          this.detailForm2.branch = this.detailForm2.branch.join("，");
          this.dialogDetail2 = true;
        });
    },
    handleRefuse(index, row) {
      //console.log(index, row);
      this.dialogReason = true;
      this.chooseIndex = index;
      this.chooseRow = row;
    },
    confirmRefuse() {
      let params = new URLSearchParams();
      params.append("project_id", this.chooseRow.project_id);
      params.append("content", this.reason);
      params.append("user_id", this.chooseRow.user_id);
      this.axios
        .post(global.server + "admin/upload/refuse_research", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          this.fetchData();
          this.dialogReason = false;
          this.reason = "";
        });
      this.$message({ type: "info", message: "您已拒绝该申请！" });
    },
    handleAccept(index, row) {
      let params = new URLSearchParams();
      params.append("project_id", row.project_id);
      params.append("user_id", row.user_id);
      this.axios
        .post(global.server + "admin/upload/accept_research", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          this.fetchData();
          this.$message({ type: "success", message: "您已同意该申请！" });
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
