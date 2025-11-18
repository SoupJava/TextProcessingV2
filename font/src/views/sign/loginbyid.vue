<template>
  <div class="homepage-hero-module">
    <div class="video-container">
      <div :style="fixStyle" class="filter">
        <div class="content">
          <br>
          <div style="display: flex;flex-direction: column;align-items: center;">
            <img style="width: 180px; height: 180px" :src="require(`@/assets/login_image.jpg`)" />
            <!-- <img src="src/assets/login_image.jpg" /> -->
          </div>
          <div style="display: flex;margin-top: 10px;flex-direction: column;align-items: center;">
            <el-input placeholder="请输入验证码" maxlength="6" show-word-limit v-model="info.verification" style="width: 50%;"
              clearable>
            </el-input>
          </div>
          <div style="display: flex;flex-direction: row-reverse;margin: 10px;">
            <el-link type="primary" @click="loginBtn">账号密码登录</el-link>
          </div>
          <div class="btn">
            <el-button type="primary" @click="loginById">登录</el-button>
            <el-button type="primary" @click="registerBtn">注册</el-button>
          </div>
        </div>
      </div>
      <video :style="fixStyle" autoplay loop muted class="fillWidth" v-on:canplay="canplay">
        <source src="../../../public/video/BG.mp4" type="video/mp4" />
      </video>
    </div>
  </div>

</template>

<script>
import ValidCode from "@/components/ValidCode";
import { setUser, getUser } from "@/utils/testDataUtils"
import { emailReg, passwordReg } from "@/utils/regUtils"
import axios from "axios";
import qs from "qs";
export default {
  name: "loginbyid",
  components: {
    ValidCode
  },
  data() {
    return {
      vedioCanPlay: false,
      fixStyle: '',
      validCode: '',
      info: {
        verification: ''
      },
      loginInfo: {
        userId: '1234567',
        password: '1234567',
        // username : '',
        // userTel : '',
        // userMail : '',
        // userAvatarUrl : ''
      },
    }
  },
  mounted() {
    sessionStorage.removeItem("user")
    this.intoAlert()
    window.onresize = () => {
      const windowWidth = document.body.clientWidth
      const windowHeight = document.body.clientHeight
      const windowAspectRatio = windowHeight / windowWidth
      let videoWidth
      let videoHeight
      if (windowAspectRatio < 0.5625) {
        videoWidth = windowWidth
        videoHeight = videoWidth * 0.5625
        this.fixStyle = {
          height: windowWidth * 0.5625 + 'px',
          width: windowWidth + 'px',
          'margin-bottom': (windowHeight - videoHeight) / 2 + 'px',
          'margin-left': 'initial'
        }
      } else {
        videoHeight = windowHeight
        videoWidth = videoHeight / 0.5625
        this.fixStyle = {
          height: windowHeight + 'px',
          width: windowHeight / 0.5625 + 'px',
          'margin-left': (windowWidth - videoWidth) / 2 + 'px',
          'margin-bottom': 'initial'
        }
      }
    }
    window.onresize()
  },
  methods: {
    // 接收验证码组件提交的 4位验证码
    createValidCode(data) {
      this.validCode = data
    },
    canplay() {
      this.vedioCanPlay = true
    },
    /**
     * 登录按钮
     */
    async loginById() {
      if (this.info.verification !== '') {
        // let msg = await setUser(this.info.account, this.info.password)
        let userInfo = {
              yzid: this.info.verification,
            }
            const options = {
              method: 'POST',
              headers: { 'content-type': 'application/x-www-form-urlencoded' },
              data: qs.stringify(userInfo),
              url: "http://www.tcgweb.cn:80/yzid",
            };
            // TODO 发送网络请求
            axios(options).then((res) => {
              console.log(res)
              var msg=res.data
              if (msg === -1) {
                  // this.info.account = ""
                  // this.info.password = ""
                  this.$message({
                    message: '验证码错误',
                    type: 'warning'
                  });
                } else {
                  location.reload();
                  // console.log('>>>||')
                  this.$router.push({ path: '/article' })
                }
            })
      } else {
        this.$message({
          message: '请勿提交空内容',
          type: 'warning'
        });
      }
    },
    /**
     * 注册按钮
     */
    registerBtn() {
      this.$router.push('register')
    },
    loginBtn() {
      this.$router.push('Login')
    },
    /**
     * 测试账号密码的格式
     * @param account 账号
     * @param password 密码
     */
    regUnit(account, password) {
      let accountTest = emailReg(account)
      let passwordTest = passwordReg(password)
      if (accountTest) {
        if (passwordTest) {
          return true
        } else {
          this.$message({
            message: '密码格式不正确' + "\n" + '密码由8~16位：数字，字符，_ , . 组成,不能以 _ 开始',
            type: 'warning'
          });
          return false
        }
      } else {
        this.$message({
          message: '账号格式不正确' + '/邮箱格式不正确',
          type: 'warning'
        });
        return false
      }
    },
    /**
     * 进入页面时的提醒
     */
    intoAlert() {

    },
  }
}

</script>

<style scoped lang="less">
.homepage-hero-module,
.video-container {
  position: relative;
  height: 100vh;
  overflow: hidden;
}

.video-container .poster img {
  z-index: 0;
  position: absolute;
}

.video-container .filter {
  z-index: 1;
  position: absolute;
  width: 100%;
}

.fillWidth {
  width: 100%;
}

.content {
  padding: 0 2vw;
  width: 30vw;
  height: 50vh;
  margin: 10vw 30vw;
  background-color: rgba(83, 92, 104, 0.7);
  border-radius: 15px;

  .btn {
    text-align: center;

    * {
      margin: 0 2vw;
      width: 10vw;
    }
  }
}
</style>