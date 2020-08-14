
<template>
  <div class="app-container">
    <el-row style="margin-left:30px;margin-right:30px;margin-top:3%;">
      <el-col :span="24" style>
        <el-card shadow="hover">
          <div slot="header">
            <span>应用反馈</span>
            <el-switch style="margin-left:30px" v-model="ano" active-text="匿名"></el-switch>
            <el-button style="float: right; padding: 3px 0" type="text" @click="submit">提交</el-button>
          </div>
          <div>
            <el-form>
              <el-form-item prop="type" style="text-align:center">
                <el-radio-group v-model="form.type">
                  <el-radio :label="0">功能建议</el-radio>
                  <el-radio :label="1">内容举报</el-radio>
                  <el-radio :label="2">安全隐私</el-radio>
                  <el-radio :label="3">应用故障</el-radio>
                  <el-radio :label="4">其他问题</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item prop="feedback">
                <el-input type="textarea" v-model="form.feedback" autosize placeholder="请输入您想反馈的内容"></el-input>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="30" style="margin-top:5%;margin-left:20px;margin-right:20px">
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header">
            <span>关于我们</span>
          </div>
          <div>
            <p style="line-height:2"> 公民科学协会（CSA）是一个成员驱动的组织，它围绕着一个共同的目标将来自广泛经验的人们联系在一起：通过公众，为公众以及与公众进行的研究和监测来增进知识。公民科学-这种实践最可识别的术语-几乎在每个研究领域都在扩大科学的范围，相关性和影响力；在现场和在线；通过本地和全球努力。随着对公民科学的日益关注，CSA深入了解了如何将公民科学理解为公众参与和研究，并阐明了实践的完整性和复杂性。</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header">
            <span>公告栏</span>
          </div>
          <div>
            <p>测试版v0.2</p>
            <p>如有问题请及时反馈或者邮件沟通，谢谢</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import global from "@/App";
export default {
  data() {
    return {
      ano: false,
      form: {
        feedback: "",
        type: 0
      },
      rules: {
        feedback: [
          { required: true, message: "请输入反馈内容", trigger: "change" }
        ],
        type: [{ required: true, message: "请选择反馈类型", trigger: "change" }]
      }
    };
  },
  methods: {
    submit() {
      console.log(this.feedback);
      let params = new URLSearchParams();
      params.append("content", this.form.feedback);
      params.append("type", this.form.type);
      params.append("ano", this.ano);
      this.axios
        .post(global.server + "admin/user_feedback", params)
        .then(res => {
          if (res.data == "networkError") {
          this.$message({ type: "error", message: "验证过期，请重新登录！" });
          setTimeout(() => {
            this.$store.dispatch("user/logout");
          }, 2000);
          return;
        }
          this.$message({ type: "success", message: "提交成功！" });
          this.form.feedback = "";
          this.form.type = 0;
          console.log(res);
        });
    }
  }
};
</script>

