<template>
  <div class="login-container">
    <el-form
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      auto-complete="on"
      label-position="left"
    >
      <div class="title-container">
        <img
          style="width:80px;float:left;margin-left:20px;margin-bottom: 20px;"
          src="https://s1.ax1x.com/2020/06/12/tXNNY8.png"
        />
        <!-- <el-image style="width: 100px; height: 100px" src="https://ftp.bmp.ovh/imgs/2020/06/13e79ee5047f004d.png"></el-image> -->
        <div class="title">欢迎您，请登录</div>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        style="width:100%;margin-bottom:10px;"
        @click.native.prevent="handleLogin"
      >登录</el-button>
      <!-- <el-button
        :loading="loading"
        type="primary"
        style="width:100%;margin-bottom:20px;margin-left:0px"
        @click.native.prevent="handleForget"
      >Forget</el-button>-->

      <!-- <div class="tips">
        <span style="margin-right:20px;">username: admin</span>
        <span>password: any</span>
      </div>-->
    </el-form>
  </div>
</template>

<script>
import { validUsername } from "@/utils/validate";
import global from "@/App";

export default {
  name: "Login",
  data() {
    // const validateUsername = (rule, value, callback) => {
    //   if (!validUsername(value)) {
    //     callback(new Error("Please enter the correct user name"));
    //   } else {
    //     callback();
    //   }
    // };
    // const validatePassword = (rule, value, callback) => {
    //   if (value.length < 6) {
    //     callback(new Error("The password can not be less than 6 digits"));
    //   } else {
    //     callback();
    //   }
    // };
    return {
      loginForm: {
        username: "",
        password: ""
      },
      loginRules: {
        username: [
          { required: true, trigger: "blur", message: "请输入登录邮箱" }
        ],
        password: [{ required: true, trigger: "blur", message: "请输入密码" }]
      },
      loading: false,
      passwordType: "password",
      redirect: undefined
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    handleLogin() {
      // URLSearchParams对象是为了让参数以form data形式
      this.$refs["loginForm"].validate(valid => {
        if (valid) {
          this.loading = true;
          this.$store
            .dispatch("user/login", this.loginForm)
            .then(res => {
              console.log(res);
              if (
                res == "该邮箱尚未注册" ||
                res == "密码错误" ||
                res == "您无权访问管理端"
              ) {
                this.$message({
                  type: "error",
                  message: "登陆失败，" + res
                });
              } else {
                this.$router.push({ path: this.redirect || "/" });
              }
            })
            .catch(() => {
              this.loading = false;
            });
        } else {
          this.$message({ type: "error", message: "请完整填写表单" });
        }
        this.loading = false;
      });
      // this.$refs.loginForm.validate(valid => {
      //   if (valid) {
      //     this.loading = true;
      //     this.$store
      //       .dispatch("user/login", this.loginForm)
      //       .then(() => {
      //         this.$router.push({ path: this.redirect || "/" });
      //         this.loading = false;
      //       })
      //       .catch(() => {
      //         this.loading = false;
      //       });
      //   } else {
      //     console.log("error submit!!");
      //     return false;
      //   }
      // });
    },
    handleForget() {
      this.loading = true;
      console.log(this.$router);
      this.loading = false;
    }
  }
};
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 30px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 30px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  // background-color: $bg;
  background: url(backg.jpg);
  overflow: hidden;

  .login-form {
    position: absolute;
    width: 400px;
    max-width: 100%;
    margin: 0 auto;
    padding: 35px 35px 0;
    top: 25%;
    right: 10%;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.2);
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;
    display: table-cell;
    text-align: center;
    // height: 100px;
    // margin: 0px auto 40px auto;
    // text-align: center;

    .title {
      // width: 60px;
      position: relative;
      margin-left: 10px;
      float: right;
      font-size: 26px;
      letter-spacing: 1px;
      color: $light_gray;
      line-height: 80px;
      // padding-bottom: 20px;
      // margin: 0px auto 40px auto;
      // margin-bottom: 20px;
      text-align: left;
      font-weight: bold;
      vertical-align: middle;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
