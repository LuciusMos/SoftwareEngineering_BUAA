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
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}
.avatar {
  width: 100px;
  display: block;
}
.el-upload-list--picture .el-upload-list__item-thumbnail {
  vertical-align: middle;
  display: inline-block;
  /* width: 70px; */
  height: 70px;
  float: left;
  position: relative;
  z-index: 1;
  margin-left: -80px;
  margin-right: 30px;
  background-color: #fff;
}
</style>
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
      <el-table-column align="center" label="项目ID" width="95" prop="project_id">
        <!-- <template slot-scope="scope">{{ scope.row.prev_id }}</template> -->
        <template slot-scope="scope">{{ scope.row.project_id }}</template>
      </el-table-column>
      <el-table-column label="项目名称" align="center" prop="project_title">
        <template slot-scope="scope">{{ scope.row.project_title }}</template>
      </el-table-column>
      <el-table-column label="发起人" width="190" align="center" prop="user_id">
        <template slot-scope="scope">
          <!-- <span>{{ scope.row.user_id }}</span> -->
          <el-button
            type="text"
            @click="handleUserDetail(scope.index,scope.row)"
          >{{scope.row.user_realname}} (用户ID:{{ scope.row.user_id }})</el-button>
        </template>
      </el-table-column>
      <!-- <el-table-column prop="user_realname" label="发起人姓名" width="95" align="center">
        <template slot-scope="scope">{{ scope.row.user_realname }}</template>
      </el-table-column>-->
      <el-table-column class-name="status-col" label="是否公开" width="80" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.is_public | publicFilter">{{ scope.row.is_public }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="project_start_time" label="创建时间" width="130" sortable>
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
            @click="handleInvite(scope.$index, scope.row)"
            :disabled="scope.row.status == '已结项'"
          >邀请</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="primary"
            :disabled="scope.row.status == '重新审核' || scope.row.status == '已结项'"
            @click="handleEdit(scope.$index, scope.row)"
          >编辑</el-button>
          <el-button
            style="margin-left:0"
            size="mini"
            type="danger"
            @click="handleComplete(scope.$index, scope.row)"
            :disabled="scope.row.status == '已结项'"
          >终止</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog title="邀请用户" :visible.sync="dialogInvite" width="50%">
      <el-table
        v-loading="userlistLoading"
        ref="multipleTable"
        :data="searchResult.slice((currentPage-1)*8,currentPage*8)"
        tooltip-effect="dark"
        style="width: 100%"
      >
        <el-table-column align="center" width="80">
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.in_project"
              size="mini"
              type="primary"
              @click="confirmInvite(scope.$index, scope.row)"
            >邀请</el-button>
            <el-button
              v-else
              size="mini"
              type="primary"
              disabled
              style="padding-left:8px;padding-right:8px"
            >已加入</el-button>
          </template>
        </el-table-column>
        <el-table-column label="用户ID" width="120">
          <template slot-scope="scope">{{ scope.row.user_id }}</template>
        </el-table-column>
        <el-table-column prop="user_nickname" label="用户名" width="120"></el-table-column>
        <el-table-column prop="user_email" label="邮箱" show-overflow-tooltip></el-table-column>
        <el-table-column align="right">
          <template slot="header" slot-scope="scope">
            <el-input v-model="searchUser" size="mini" placeholder="输入关键字搜索" @input="handleQuery" />
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        style="text-align:center"
        @current-change="handleCurrentChange"
        :page-size="8"
        :pager-count="5"
        layout="total, prev, pager, next"
        :total="searchResult.length"
      ></el-pagination>
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

    <el-dialog title="提示" :visible.sync="dialogComplete" width="30%">
      <span>确认终止该项目吗？该操作无法撤回。</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogComplete=false">取消</el-button>
        <el-button type="primary" @click="confirmComplete">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="修改项目详情" :visible.sync="dialogDetail">
      <el-form ref="applyForm" :model="form" label-width="150px" :rules="rules">
        <el-form-item label="项目名称" prop="name">
          <el-col :span="12">
            <el-input v-model="form.name" />
          </el-col>
        </el-form-item>
        <el-row>
          <el-col :span="8" style="text-align:right">
            <el-form-item label="数据采集起止日期" prop="date1">
              <el-date-picker
                v-model="form.date1"
                type="daterange"
                align
                unlink-panels
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="预计项目截止日期" prop="endDate">
          <el-date-picker
            v-model="form.endDate"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="请选择预计结项时间"
            style="width:150px"
          />
        </el-form-item>
        <el-form-item label="是否公开" prop="public">
          <el-switch v-model="form.public" />
        </el-form-item>
        <el-form-item label="项目类型" prop="type">
          <el-col :span="12">
            <el-input v-model="form.type" placeholder="各类型之间请用 '/' 分割" />
          </el-col>
        </el-form-item>
        <el-form-item label="所属学科" prop="branch">
          <el-checkbox-group v-model="form.branch" style="width:500px">
            <el-checkbox v-for="b in branch" :label="b" :key="b" border style="margin:1px 1px">{{b}}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="项目描述" prop="desc">
          <el-col :span="20">
            <el-input autosize v-model="form.desc" type="textarea" />
          </el-col>
        </el-form-item>
        <el-form-item label="参与方式" prop="participate_way">
          <el-col :span="20">
            <el-input
              autosize
              v-model="form.participate_way"
              type="textarea"
              placeholder="请输入参与方式（200字以内）"
            />
          </el-col>
        </el-form-item>
        <el-form-item
          v-for="(df, index) in form.data_formats"
          :label="'数据格式 ' + (index+1)"
          :key="df.dkey"
          :prop="'data_formats.' + index + '.value'"
        >
          <el-col :span="5" style="margin-right:10px">
            <el-input v-model="df.key" placeholder="数据名称"></el-input>
          </el-col>
          <el-col :span="4" style="margin-right:10px">
            <el-select v-model="df.value.type" placeholder="类型" style="width:80px">
              <el-option
                v-for="item in typeOps"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-col>
          <!-- <el-col :span="4" style="margin-right:10px">
            <el-input v-model="df.value.min" placeholder="最小值"></el-input>
          </el-col>
          <el-col :span="4">
            <el-input v-model="df.value.max" placeholder="最大值"></el-input>
          </el-col>-->
          <el-col :span="8">
            <el-input
              v-model="df.value.cate"
              placeholder="类别名称（各类别请用'/'分割）"
              v-if="df.value.type==8"
            ></el-input>
          </el-col>
          <el-col :span="3" style="margin-right:10px">
            <el-input v-model="df.value.min" placeholder="数据最小值" v-if="df.value.type<3"></el-input>
            <el-input v-model="df.value.min" placeholder="最小字数" v-else-if="df.value.type==3"></el-input>
            <el-input
              v-model="df.value.min"
              placeholder="文件大小下限"
              v-else-if="df.value.type>4 && df.value.type<8"
            ></el-input>
          </el-col>
          <el-col :span="3">
            <el-input v-model="df.value.max" placeholder="数据最大值" v-if="df.value.type<3"></el-input>
            <el-input v-model="df.value.max" placeholder="最大字数" v-else-if="df.value.type==3"></el-input>
            <el-input
              v-model="df.value.max"
              placeholder="文件大小上限"
              v-else-if="df.value.type>4 && df.value.type<8"
            ></el-input>
          </el-col>
          <el-button style="margin-left: 10px;" @click.prevent="removeDf(df)">删除</el-button>
          <el-upload
            :action="global.server +'admin/upload/img_example'"
            :on-remove="handleExampleRemove"
            :on-success="handleExampleSuccess"
            :before-upload="beforeAvatarUpload"
            multiple
            :on-progress="onProgress"
            v-if="df.value.type==5"
            style="margin:10px ;width:400px"
            list-type="picture"
          >
            <el-button
              :disabled="needDisable"
              size="small"
              type="primary"
              @click="exampleIndex=index"
            >上传样图</el-button>
            <b style="margin-left:20px">注：只能上传jpg/png文件，且不超过10M</b>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button @click="addDf">新增数据</el-button>
        </el-form-item>
        <el-form-item label="数据格式说明" prop="df_desc">
          <el-col :span="20">
            <el-input autosize v-model="form.df_desc" type="textarea" />
          </el-col>
        </el-form-item>
        <el-form-item label="背景资料" prop="background">
          <el-col :span="20">
            <el-input autosize v-model="form.background" type="textarea" />
          </el-col>
        </el-form-item>
        <el-form-item label="注意事项" prop="note">
          <el-col :span="20">
            <el-input autosize v-model="form.note" type="textarea" />
          </el-col>
        </el-form-item>
        <el-form-item label="项目主图" prop="pic">
          <!-- <el-image style="width:180px" :src="form.pic" /> -->
          <el-upload
            class="avatar-uploader"
            :action="global.server +'admin/upload/research_pic'"
            :show-file-list="false"
            :on-success="handleProjectIMGSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <el-image
              v-if="form.pic"
              :src="global.noPortServer +'file/image/projectmainimage/' + form.pic"
              class="avatar"
            />
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item
          v-for="(assistant, index) in form.assistants"
          :label="'项目助理 ' + (index+1)"
          :key="assistant.key"
          :prop="'assistants.' + index + '.value'"
        >
          <el-col :span="6">
            <el-autocomplete
              v-model="assistant.value"
              :fetch-suggestions="querySearchAsync"
              placeholder="请输入ID或姓名检索"
              @select="handleSelect"
              :disabled="assistant.value.indexOf('(ID:') != -1"
            ></el-autocomplete>
            <!-- <el-input v-model="assistant.value" placeholder="请输入助理ID"></el-input> -->
          </el-col>
          <el-button style="margin-left: 10px;" @click.prevent="removeAssistant(assistant)">删除</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="addAssistant">新增助理</el-button>
          <el-button type="primary" @click="reSubmit" :disabled="needDisable">重新审核</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
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
      needDisable: false,
      exampleIndex: -1,
      exampleList: [],
      branch: global.branch,
      global: global,
      currentPage: 1,
      pagesize: 10,
      userlistLoading: false,
      searchResult: [],
      // selectUsers: [],
      // showUsers: [],
      list: [],
      showList: [],
      listLoading: true,
      search: "",
      searchUser: "",
      chooseId: "",
      dialogComplete: false,
      dialogDetail: false,
      dialogInvite: false,
      chooseResearchId: "",
      typeOp: "",
      typeOps: global.dataType,
      form: {
        branch: [],
        name: "",
        date1: [],
        date2: "",
        endDate: "",
        public: "true",
        type: [],
        desc: "",
        participate_way: "",
        background: "",
        note: "",
        pic: "",
        assistants: [],
        df_desc: "",
        data_formats: []
      },
      rules: global.formRules
    };
  },
  created() {
    this.fetchData();
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
  methods: {
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
    handleSelect(item) {
      console.log(this.assistantIndex);

      console.log(item);
    },
    querySearchAsync(queryString, cb) {
      // clearTimeout(this.timeout);
      setTimeout(() => {
        let params = new URLSearchParams();
        params.append("keyword", queryString);
        this.axios
          .post(global.server + "admin/get_data/assistant_search", params)
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
            cb(res.data);
          });
      }, 1000);
    },
    onProgress(event, file, fileList) {
      console.log(event);
      this.needDisable = true;
    },
    handleProjectIMGSuccess(res, file, fileList) {
      this.form.pic = res.pic_url;
    },
    handleExampleSuccess(res, file, fileList) {
      console.log(res);
      if (res.root_list.length > 0) {
        this.$message({
          type: "success",
          message: "图片识别结果为：" + res.root_list.join()
        });
      } else {
        this.$message({
          type: "warning",
          message: "未能识别出较匹配的结果，请上传高清图片"
        });
      }
      this.needDisable = false;
      if (
        this.form.data_formats[this.exampleIndex].value.examples == undefined ||
        this.form.data_formats[this.exampleIndex].value.examples == null
      ) {
        this.form.data_formats[this.exampleIndex].value.examples = [];
        this.form.data_formats[this.exampleIndex].value.root_list = [];
      }
      this.form.data_formats[this.exampleIndex].value.examples.push(res.name);
      for (var i = 0; i < res.root_list.length; i++) {
        if (
          this.form.data_formats[this.exampleIndex].value.root_list.indexOf(
            res.root_list[i]
          ) == -1
        ) {
          this.form.data_formats[this.exampleIndex].value.root_list.push(
            res.root_list[i]
          );
        }
      }
      console.log(this.form.data_formats);
    },
    dis(index) {
      console.log(index);
    },
    handleExampleRemove(file, fileList) {
      // this.$message({type: "error",message: "暂无删除功能，删除失败！"});
    },
    fetchData() {
      this.listLoading = true;
      this.axios
        .post(global.server + "admin/get_data/my_research")
        .then(res => {
          console.log(res);
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
    clearTimer() {
      if (this.timer) {
        clearTimeout(this.timer);
      }
    },
    handleQuery(event) {
      this.clearTimer();
      this.userlistLoading = true;
      // if (this.searchUser = "") {
      //   this.searchResult = [];
      //   this.userlistLoading = false;
      //   return;
      // }
      this.timer = setTimeout(() => {
        let params = new URLSearchParams();
        params.append("keyword", this.searchUser);
        params.append("project_id", this.chooseResearchId);
        this.axios
          .post(global.server + "admin/get_data/user_search", params)
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
            console.log(res.data);
            this.searchResult = [];
            if (res.data != "error") {
              this.searchResult = res.data;
            }
            this.userlistLoading = false;
          });
      }, 1000);
    },
    reSubmit() {
      console.log(this.form);
      this.$refs["applyForm"].validate(valid => {
        if (valid) {
          let params = new URLSearchParams();
          params.append("pid", this.chooseId);
          params.append("name", this.form.name);
          params.append("date1", this.form.date1[0]);
          params.append("date2", this.form.date1[1]);
          params.append("endDate", this.form.endDate);
          params.append("public", this.form.public);
          params.append("type", this.form.type);
          params.append("desc", this.form.desc);
          params.append("participate_way", this.form.participate_way);
          params.append("background", this.form.background);
          params.append("note", this.form.note);
          for (var i = 0; i < this.form.assistants.length; i++) {
            console.log(i);
            console.log(this.form.assistants[i]);
            this.form.assistants[i].value = this.form.assistants[i].value
              .split(":")[1]
              .replace(")", "");
          }
          params.append("assistants", JSON.stringify(this.form.assistants));
          params.append("data_format", JSON.stringify(this.form.data_formats));
          params.append("df_desc", this.form.df_desc);
          params.append("branch", JSON.stringify(this.form.branch));
          params.append("pic", this.form.pic);
          this.axios
            .post(global.server + "admin/upload/form", params)
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
              if (res.data == "success") {
                this.$message({
                  type: "success",
                  message: "已提交申请，等待管理员审核！"
                });
                this.fetchData();
                this.dialogDetail = false;
              } else {
                this.$message({
                  type: "error",
                  message: "助理ID无效，请重新输入！"
                });
              }
            });
        } else {
          this.$message({ type: "error", message: "请完整填写表单！" });
        }
      });
    },
    removeDf(item) {
      var index = this.form.data_formats.indexOf(item);
      if (index !== -1) {
        this.form.data_formats.splice(index, 1);
      }
    },
    addDf() {
      this.form.data_formats.push({
        value: { type: "", min: "", max: "", cate: "" },
        dkey: Date.now()
      });
    },
    handleInvite(index, row) {
      this.chooseResearchId = row.project_id;
      this.dialogInvite = true;
    },
    handleSelectionChange(val) {
      console.log(val);
      this.selectUsers = val;
    },
    confirmInvite(index, row) {
      let params = new URLSearchParams();
      params.append("user_id", row.user_id);
      params.append("project_id", this.chooseResearchId);
      this.axios
        .post(global.server + "admin/upload_data/invite_user", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(res.data);
        });
      this.$message({ type: "success", message: "已成功发送邀请" });
    },
    handleEdit(index, row) {
      //console.log(index, row);
      console.log(this.search);
      console.log(this.list);
      this.form.type = [];
      this.form.assistants = [];
      this.form.data_formats = [];
      this.chooseId = row.project_id;
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
          this.form.name = res.data.project_title;
          this.form.date1[0] = res.data.data_start_time;
          this.form.date1[1] = res.data.data_end_time;
          // this.form.date2 = res.data.data_end_time;
          this.form.endDate = res.data.end_time;
          // this.form.public = res.data.is_public;
          if (res.data.is_public == "公开") this.form.public = true;
          else this.form.public = false;
          this.form.desc = res.data.project_introduction;
          this.form.participate_way = res.data.way_of_participation;
          this.form.background = res.data.background_knowledge;
          this.form.note = res.data.note;
          this.form.df_desc = res.data.df_desc;
          // this.form.assistants = res.data.assistants;
          // this.form.type = res.data.category.replace(/\s/g, "").split("/");
          this.form.type = res.data.category;
          this.form.branch = res.data.branch;
          console.log(this.form.type);
          for (var i = 0; i < res.data.assistants.length; i++) {
            console.log(res.data.assistants[i]);
            this.form.assistants.push({
              key: res.data.assistants[i].id,
              value:
                res.data.assistants[i].name +
                "(ID:" +
                res.data.assistants[i].id +
                ")"
            });
          }
          for (var i = 0; i < res.data.data_formats.length; i++) {
            this.form.data_formats.push({
              dkey: res.data.data_formats[i].dkey,
              key: res.data.data_formats[i].key,
              value: res.data.data_formats[i].value
            });
          }
          this.form.pic = res.data.project_main_image_url;
          console.log(this.form.pic);
          console.log(
            global.noPortServer + "file/image/projectmainimage/" + this.form.pic
          );
          // this.form.assistants = JSON.parse(res.data.assistants);
          // this.form.pic = "data:;base64," + res.data.pic;
          this.dialogDetail = true;
        });
    },
    handleComplete(index, row) {
      //console.log(index, row);
      this.dialogComplete = true;
      this.chooseId = row.project_id;
    },
    confirmComplete() {
      this.dialogComplete = true;
      this.listLoading = true;
      let params = new URLSearchParams();
      params.append("pid", this.chooseId);
      this.axios
        .post(global.server + "admin/upload/complete_research", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          //console.log(res);
          this.fetchData();
          this.listLoading = false;
          this.dialogComplete = false;
        });
    },
    removeAssistant(item) {
      var index = this.form.assistants.indexOf(item);
      if (index !== -1) {
        this.form.assistants.splice(index, 1);
      }
    },
    addAssistant() {
      this.form.assistants.push({
        value: "",
        key: Date.now()
      });
    },
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw);
      this.form.pic = res.pic_url;
    },
    beforeAvatarUpload(file) {
      const isJPG =
        file.type == "image/png" ||
        file.type == "image/jpeg" ||
        file.type == "image/jpg";
      const isLt2M = file.size / 1024 / 1024 < 10;

      if (!isJPG) {
        this.$message.error("上传图片只能是 jpg/png 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传图片大小不能超过 10MB!");
      }
      return isJPG && isLt2M;
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
