
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
    <el-form ref="applyForm" :model="form" label-width="150px" :rules="rules">
      <el-form-item label="项目名称" prop="name">
        <el-col :span="12">
          <el-input v-model="form.name" placeholder="请输入项目名称（18字以内）" />
        </el-col>
      </el-form-item>
      <el-row>
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
      </el-row>

      <el-form-item label="预计结项日期" prop="endDate">
        <el-date-picker
          v-model="form.endDate"
          type="date"
          value-format="yyyy-MM-dd"
          placeholder="请选择预计结项日期"
          style="width:215px"
        />
      </el-form-item>

      <el-form-item label="是否公开" prop="public">
        <el-switch v-model="form.public" />
      </el-form-item>
      <el-form-item label="项目类型" prop="type">
        <el-col :span="8">
          <el-input v-model="form.type" placeholder="各类型之间请用 '/' 分割" />
        </el-col>
      </el-form-item>
      <el-form-item label="所属学科" prop="branch">
        <el-checkbox-group v-model="form.branch" style="width:700px">
          <el-checkbox v-for="b in branch" :label="b" :key="b" border style="margin:1px 1px">{{b}}</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="项目描述" prop="desc">
        <el-col :span="16">
          <el-input autosize v-model="form.desc" type="textarea" placeholder="请输入项目描述（500字以内）" />
        </el-col>
      </el-form-item>
      <el-form-item label="参与方式" prop="participate_way">
        <el-col :span="16">
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
        <el-col :span="4" style="margin-right:10px">
          <el-input v-model="df.key" placeholder="请输入数据名称"></el-input>
        </el-col>
        <el-col :span="2" style="margin-right:10px">
          <el-select v-model="df.value.type" placeholder="类型" style="width:80px">
            <el-option
              v-for="item in typeOps"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-input v-model="df.value.cate" placeholder="类别名称（各类别请用'/'分割）" v-if="df.value.type==8"></el-input>
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
        <el-button @click="addDf(index)" v-if="index+1==form.data_formats.length">新增数据</el-button>
        <el-upload
          :action="global.server +'admin/upload/img_example'"
          :on-remove="handleExampleRemove"
          :on-success="handleExampleSuccess"
          :before-upload="beforeAvatarUpload"
          multiple
          :on-progress="onProgress"
          v-if="df.value.type==5"
          style="margin:10px 200px;width:400px"
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
      <el-form-item label="数据格式描述" prop="df_desc">
        <el-col :span="16">
          <el-input
            autosize
            v-model="form.df_desc"
            type="textarea"
            placeholder="请输入数据格式描述（500字以内）"
          />
        </el-col>
      </el-form-item>
      <el-form-item label="背景资料" prop="background">
        <el-col :span="16">
          <el-input
            autosize
            v-model="form.background"
            type="textarea"
            placeholder="请输入背景资料（1000字以内）"
          />
        </el-col>
      </el-form-item>
      <el-form-item label="注意事项" prop="note">
        <el-col :span="16">
          <el-input autosize v-model="form.note" type="textarea" placeholder="请输入注意事项（500字以内）" />
        </el-col>
      </el-form-item>
      <el-form-item label="项目主图" prop="pic">
        <el-upload
          class="avatar-uploader"
          :action="global.server +'admin/upload/research_pic'"
          :show-file-list="false"
          :on-success="handleProjectIMGSuccess"
          :before-upload="beforeAvatarUpload"
        >
          <img v-if="imageUrl" :src="imageUrl" class="avatar" />
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-form-item>
      <el-form-item
        v-for="(assistant, index) in form.assistants"
        :label="'项目助理 ' + (index+1)"
        :key="assistant.key"
        :prop="'assistants.' + index + '.value'"
      >
        <div @click="assistantIndex=index">
          <el-col :span="8">
            <!-- <el-input v-model="assistant.value" placeholder="请输入助理ID"></el-input> -->
            <el-autocomplete
              v-model="assistant.value"
              :fetch-suggestions="querySearchAsync"
              placeholder="请输入ID或姓名检索"
              @select="handleSelect"
              style="width:300px"
              :disabled="assistant.value.indexOf('(ID:') != -1"
            ></el-autocomplete>
          </el-col>
        </div>
        <el-button style="margin-left: 10px;" @click.prevent="removeAssistant(assistant)">删除</el-button>
      </el-form-item>
      <el-form-item>
        <el-button @click="addAssistant">新增助理</el-button>
        <el-button @click="resetForm('applyForm')" :disabled="needDisable">重置</el-button>
        <el-button type="primary" @click="onSubmit" :disabled="needDisable">申请</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import global from "@/App";
export default {
  data() {
    return {
      needDisable: false,
      exampleIndex: -1,
      exampleList: [],
      // rootList:[],
      assistantIndex: -1,
      branch: global.branch,
      global: global,
      form: {
        branch: [],

        name: "",
        date1: "",
        date2: "",
        endDate: "",
        public: true,
        type: "",
        desc: "",
        participate_way: "",
        background: "",
        note: "",
        pic: "",
        assistants: [],
        data_formats: [
          {
            dkey: Date.now(),
            value: {
              min: "",
              max: "",
              type: "",
              cate: "",
              examples: [],
              root_list: []
            },
            key: ""
          }
        ],
        df_desc: ""
      },
      typeOp: "",
      typeOps: global.dataType,
      imageUrl: "",
      rules: global.formRules
    };
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
    handleSelect(item) {
      console.log(this.assistantIndex);

      console.log(item);
    },
    onProgress(event, file, fileList) {
      console.log(event);
      this.needDisable = true;
    },
    handleExampleSuccess(res, file, fileList) {
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
    },
    dis(index) {
      console.log(index);
    },
    handleExampleRemove(file, fileList) {
      // this.$message({type: "error",message: "暂无删除功能，删除失败！"});
    },
    onSubmit() {
      console.log(this.form.date1);
      this.$refs["applyForm"].validate(valid => {
        if (valid) {
          let params = new URLSearchParams();
          params.append("pid", "");
          params.append("name", this.form.name);
          params.append("date1", this.form.date1[0]);
          params.append("date2", this.form.date1[1]);
          params.append("endDate", this.form.endDate);
          params.append("public", this.form.public);
          params.append("type", this.form.type);
          params.append("branch", JSON.stringify(this.form.branch));
          params.append("desc", this.form.desc);
          params.append("participate_way", this.form.participate_way);
          params.append("background", this.form.background);
          params.append("note", this.form.note);
          for (var i=0;i<this.form.assistants.length;i++) {
            console.log(i)
            console.log(this.form.assistants[i])
            if (this.form.assistants[i].value == undefined) continue;
            this.form.assistants[i].value = this.form.assistants[i].value.split(":")[1].replace(")", "");
          }
          params.append("assistants", JSON.stringify(this.form.assistants));
          params.append("df_desc", this.form.df_desc);
          params.append("pic", this.form.pic);
          // for(var i=0;i<this.form.data_formats.length;i++){
          //   if(this.form.data_formats[i].value.type == 8) {
          //     this.form.data_formats[i].value.cate = this.form.data_formats[i].value.cate.split('/');
          //   }
          // }
          console.log(this.data_formats);
          params.append("data_format", JSON.stringify(this.form.data_formats));
          this.axios
            .post(global.server + "admin/upload/form", params)
            .then(res => {
              console.log(res);
              if (res.data == "success") {
                this.$message({
                  type: "success",
                  message: "已提交申请，等待管理员审核！"
                });
                this.$router.push('/form')
              } else {
                this.$message({
                  type: "error",
                  message: "输入信息有误，请重新输入！"
                });
              }
            });
        } else {
          this.$message({
            type: "error",
            message: "请完整填写表单！"
          });
        }
      });
    },
    onCancel() {
      this.$message({
        message: "cancel!",
        type: "warning"
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
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
    removeDf(item) {
      var index = this.form.data_formats.indexOf(item);
      if (index !== -1) {
        this.form.data_formats.splice(index, 1);
      }
    },
    addDf(index) {
      // this.form.data_formats[this.exampleIndex].value.examples = this.exampleList;
      // exampleList = []
      // this.form.data_formats[this.exampleIndex].value.examples = this.exampleList;
      this.form.data_formats.push({
        value: {
          type: "",
          min: "",
          max: "",
          cate: "",
          examples: [],
          root_list: []
        },
        dkey: Date.now()
      });
    },
    handleProjectIMGSuccess(res, file) {
      this.form.pic = res.pic_url;
      this.imageUrl = URL.createObjectURL(file.raw);
      // this.form.pic = this.imageUrl;
    },
    beforeAvatarUpload(file) {
      // const isJPG = file.type === "image/jpeg" || file.type === "image/png";
      console.log(file.type)
      const isJPG = (file.type == "image/png") || (file.type == "image/jpeg")|| (file.type == "image/jpg");
      const isLt2M = file.size / 1024 / 1024 < 10;

      if (!isJPG) {
        this.$message.error("上传图片只能是 png/jpg 格式!");
      }
      if (!isLt2M) {
        this.$message.error("上传图片大小不能超过 10MB!");
      }
      return isJPG && isLt2M;
    }
  }
};
</script>

<style scoped>
.line {
  text-align: center;
}
</style>

