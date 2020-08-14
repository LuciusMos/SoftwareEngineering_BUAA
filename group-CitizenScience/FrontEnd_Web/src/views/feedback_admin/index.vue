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
      <el-table-column fixed align="center" prop="feedback_id" label="反馈ID" width="90"></el-table-column>
      <el-table-column align="center" prop="user_id" label="用户ID" width="90"></el-table-column>
      <el-table-column align="center" prop="feedback_type" label="反馈类型" width="120"></el-table-column>
      <el-table-column align="center" prop="feedback_time" label="反馈时间" width="140">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.feedback_time }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="feedback_content" label="反馈内容" width></el-table-column>
      <el-table-column align="center" fixed="right" label="操作" width="170">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row)" type="danger" size="small" disabled>删除</el-button>
        <el-button @click="handleClick(scope.row)" type="primary" size="small" disabled>回应</el-button>
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
  </div>
</template>

<script>
import global from "@/App";
export default {
  data() {
    return {
      showList:[],
      list: [],
      listLoading: false,
      currentPage: 1,
      pagesize: 10,
      search: ""
    };
  },
  watch:{
    search:{
      handler(val){
        this.showList = this.list.filter(data => !val || data.feedback_content.toLowerCase().includes(val.toLowerCase())
                          || data.user_id.toString().toLowerCase().includes(val.toLowerCase())
                          || data.feedback_type.toLowerCase().includes(val.toLowerCase())
                          || data.feedback_id.toString().toLowerCase().includes(val.toLowerCase()))
      }
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    handleSizeChange(val) {
      this.pagesize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    fetchData() {
      console.log(this.feedback);
      let params = new URLSearchParams();
      params.append("content", this.feedback);
      this.axios
        .post(global.server + "admin/feedback_admin", params)
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
          console.log(res);
        });
    },
    submit() {}
  }
};
</script>

