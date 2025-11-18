<template>
<div class="info">
  <p style="text-align: center;font-size: 2.4em;font-weight: bold;color: #99a9bf">用户信息</p>
<!--  <el-row-->
<!--      style="margin-left: 5vw ; margin-top: 5vh ; font-size: 1.2em ;">-->
<!--    <el-col :span="4"><div class="grid-content bg-purple" style="text-align: center ; line-height: 100px; font-weight: bold ;">头像</div></el-col>-->
<!--    <el-col :span="12"><div class="grid-content bg-purple-light">-->
<!--      <el-image-->
<!--          @click="changeUserAvatar"-->
<!--          style="width: 100px;cursor: pointer; height: 100px ; border-radius: 50px ;margin-left: 5vw ; float: left;margin-right: 2vw"-->
<!--          :src="user.userAvatar"-->
<!--          fit="fill"></el-image>-->
<!--    </div>-->
<!--      <el-upload-->
<!--          ref="upload"-->
<!--          class="upload-demo"-->
<!--          action="no"-->
<!--          :before-upload="beforeUpload"-->
<!--          name="file"-->
<!--          multiple-->
<!--          :limit="1"-->
<!--          :file-list="fileList"-->
<!--          :auto-upload="false"-->
<!--          :http-request="uploadFile2Back">-->
<!--        <el-button size="small" :disabled="canChange" type="primary">修改头像</el-button>-->
<!--        <div  class="el-upload__tip">只能上传jpg/jpeg/png文件</div>-->
<!--      </el-upload>-->
<!--    </el-col>-->
<!--  </el-row>-->
  <el-row
      style="margin-left: 5vw ; margin-top: 5vh ; text-align: center ; font-size: 1.2em; font-weight: bold ;">
    <el-col :span="4"><div class="grid-content bg-purple">用户名</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple-light">
      <el-input v-model="user.name" placeholder="请输入内容" :disabled="canChange"></el-input>
    </div></el-col>
  </el-row>
  <el-row
      style="margin-left: 5vw ; margin-top: 5vh ; text-align: center ; font-size: 1.2em ; font-weight: bold ;">
    <el-col :span="4"><div class="grid-content bg-purple">手机号</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple-light">
      <el-input v-model="user.phone" placeholder="请输入内容" :disabled="canChange"></el-input>
    </div></el-col>
  </el-row>
  <el-row
      style="margin-left: 5vw ; margin-top: 5vh ; text-align: center ; font-size: 1.2em ; font-weight: bold ;">
    <el-col :span="4"><div class="grid-content bg-purple">邮箱</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple-light">
      <el-input v-model="user.email" placeholder="请输入内容" :disabled="canChange"></el-input>
    </div></el-col>
  </el-row>
  <el-row
      style="margin-left: 5vw ; margin-top: 5vh ; text-align: center ; font-size: 1.2em ; font-weight: bold ;">
    <el-col :span="4"><div class="grid-content bg-purple">密码</div></el-col>
    <el-col :span="12"><div class="grid-content bg-purple-light">
      <el-input v-model="user.password"  :show-password='this.canChange' placeholder="请输入内容" :disabled="canChange"></el-input>
    </div></el-col>
  </el-row>
  <div class="ctrl">
    <el-button type="primary" @click="changeInfo">{{btnInfo}}</el-button>
  </div>
</div>
</template>

<script>
import {user,getUserInfo} from "@/utils/user";
import axios from "axios";
import qs from "qs";
export default {
  name: "Info",
  data(){
    return{
      canChange : true,
      btnInfo : '修改信息',
      fileList: [],
      user : {
        name : user.name,
        phone : user.phone,
        email : user.email,
        password : user.password
      }
    }
  },
  mounted() {
  this.init()
    },
  methods:{
    /**
     * 初始化用户信息
     */
    init(){
      axios.post("http://www.tcgweb.cn:80/getMyInfo").then((res) => {
        console.log(user)
        let userData = res.data.data
        //res.data.data.userId
        user.name = userData.name === null ? ' ' : userData.name
        user.phone = userData.phone === null ? ' ' : userData.phone
        user.email = userData.email === null ? ' ' : userData.email
        user.password = userData.password
        
      })
    },
    /**
     * 修改用户信息
     */
    changeUserInfo(){

      const userInfo = {
        username : this.user.name,
        userTel : this.user.phone,
        userMail: this.user.email,
        password : this.user.password,
      }
      const options = {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        data: qs.stringify(userInfo),
        url :"http://www.tcgweb.cn:80/updateMyInfo" ,
      };
      axios(options).then((res) => {
        // console.log('============>')
        console.log(res)
      })
      this.init()
      // this.init()
    },
    /**
     * 上传用户邮箱
     */
    uploadMyAvatar(){

    },
    /**
     * 修改用户信息
     */
    changeInfo(){
      this.canChange = !this.canChange
      if(this.canChange){
        this.btnInfo = '修改信息'
        // TODO 将修改的信息发送至后端
        this.$message({
          message : '修改信息',
          type:"info"
        })
        this.changeUserInfo()
        // this.$refs.upload.submit()
      }else {
        this.btnInfo = '保存信息'
      }
    },
    changeUserAvatar(){

    },
    /**
     * 上传按钮点击事件
     */
    startUpload() {
      this.$refs.upload.submit();
    },
    /**
     * 上传按钮点击之后要发生的事件
     * @param op
     */
    uploadFile2Back(op) {
      let userInfo = {
              username : this.user.name,
              password : this.user.password,
              userMail : this.user.email,
              userTel : this.user.phone
            }
      const options = {
              method: 'POST',
              headers: { 'content-type': 'application/x-www-form-urlencoded' },
              data: qs.stringify(userInfo),
              url :"http://www.tcgweb.cn:80/updateMyInfo" ,
            };
      axios(options).then((res) => {
        this.init()
        this.init()
      })
    },
    beforeUpload(file) {
      // console.log(file)
      if (file.name.split(".")[1] !== 'jpg' && file.name.split(".")[1] !== 'jpeg' && file.name.split(".")[1] !== 'png') {
        this.$message.error('上传文件只能 jpg/jpeg/png 格式!');
        return false;
      }
      return true
    },
  }
}
</script>

<style scoped lang="less">
.info{
  margin-left: 5vw;
  margin-top: 10vh;
  //padding-top: 2vh;
  padding-bottom: 5vh;
  background-color: white;
  border-radius: 0  50px 50px 0;
  border: solid 1px gray;
  width: 60vw;
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }

  }
  .upload{
    margin-left: 2vw;
  }
  .el-col {
    border-radius: 4px;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    //background-color: #f9fafc;
  }
  .ctrl{
    text-align: center;
  }
}
</style>