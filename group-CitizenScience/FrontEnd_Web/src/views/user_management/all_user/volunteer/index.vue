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
      <el-table-column label="用户名" align="center">
        <template slot-scope="scope">{{ scope.row.user_nickname }}</template>
      </el-table-column>
      <el-table-column align="center" prop="register_time" label="注册时间" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.register_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户邮箱" align="center">
        <template slot-scope="scope">{{ scope.row.user_email }}</template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="100">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            disabled
            @click="handleDelete(scope.$index, scope.row)"
          >删除</el-button>
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
    <el-dialog title="提示" :visible.sync="dialogDelete" width="30%">
      <span>确认删除该用户吗？该操作无法撤回。</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogDelete=false">取消</el-button>
        <el-button type="primary" @click="confirmDelete">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import global from "@/App";

export default {
  data() {
    return {
      showList: [],
      list: [],
      listLoading: true,
      search: "",
      chooseId: "",
      chooseIndex: 0,
      dialogDelete: false,
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
        this.showList = this.list.filter(data => !val || data.user_nickname.toLowerCase().includes(val.toLowerCase())
                          || data.user_id.toString().toLowerCase().includes(val.toLowerCase())
                          || data.user_email.toLowerCase().includes(val.toLowerCase())
                          || data.register_time.toLowerCase().includes(val.toLowerCase()))
      }
    }
  },
  methods: {
    fetchData() {
      this.listLoading = true;
      this.axios
        .post(global.server + "admin/get_data/all_volunteer")
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
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      //console.log(index, row);
      this.dialogDelete = true;
      this.chooseId = row.id;
      this.chooseIndex = index;
    },
    confirmDelete() {
      this.dialogDelete = false;
      this.listLoading = true;
      let params = new URLSearchParams();
      params.append("deleteId", this.chooseId);
      this.axios
        .post(global.server + "admin/upload/delete_user", params)
        .then(res => {
          if (res.data == "networkError") {
            this.$message({ type: "error", message: "验证过期，请重新登录！" });
            setTimeout(() => {
              this.$store.dispatch("user/logout");
            }, 2000);
            return;
          }
          console.log(res);
          this.fetchData();
          this.listLoading = false;
        });
      this.$message({ type: "success", message: "已成功删除该用户！" });
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
