<template>
  <div class="ArticleList" ArticleList>
    <el-input
        placeholder="请输入内容"
        style="width: 25vw ; margin-top: 5vh; margin-left: 3vw;"
        v-model="input"
        clearable>
      <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
    </el-input>
    <el-button style="margin-left: 1vw" icon="el-icon-refresh" @click="initSearch"></el-button>
    <el-button style="margin-left: 3vw" icon="el-icon-circle-plus" type="primary" @click="createArticleItem">新建论文项目</el-button>
    <el-button style="margin-left: 5vw;font-size: 1.8em;color: gray;font-weight: bold" type="text" v-if="selectValue">{{selectName = selectName.length >10?selectName.slice(0,7)+"...":selectName}}</el-button>
    <span v-if="selectValue" style="font-size: 1.8em;color: #a9a7a7;font-weight: bold">&nbsp;被选中</span>
    <br>
    <div class="box" v-for="item in tableData">
      <ArticliItem :p-info="{name:item.name,num:item.num,bate1: item.bate1,bate2: item.bate2,bate3: item.bate3,isSelected:item.isSelected}"></ArticliItem>
    </div>


  </div>
</template>

<script>
import axios from "axios";
import ArticliItem from "@/components/ArticliItem";
import qs from "qs";

export default {
  name: "ArticleList",
  components:{
    ArticliItem
  },
  mounted() {
    this.init()
    this.isSelect()
  },
  data(){
    return{
      input: '',
      dataf:new FormData(),
      tableData: [
        // {
        //   name : "1文章名称文章名称文章名称文章名称文章名称文章名称",
        //   num : 1
        // }
      ],
      selectValue : false,
      selectName :'',

    }
  },
  methods:{
    /**
     * 初始化数组
     */
    init(){
      this.tableData = []
        axios.post("http://www.tcgweb.cn:80/getAllProject").then((res) => {
          console.log(res.data)
          if(res.data.code === 1){
            console.log('====>>>>')
            console.log(res.data.data)
            if(res.data.data.length !== 0){
              for(let i = 0 ; i < res.data.data.length ; i ++){
                // todo num没有
                this.tableData.push({
                  name:res.data.data[i].DocxName.split("_")[1],
                  num:res.data.data[i].bigversion+'.'+res.data.data[i].smallversion,
                  bate1:res.data.data[i].version,
                  bate2:res.data.data[i].Iteration,
                  bate3:res.data.data[i].neglect,
                  isSelected : 0
                })
              }
            }
          }else {
            this.$message.error("获取信息失败")
          }
        })
    },
    /**
     * 搜索框
     */
    search(){
      if(this.input !== ''){
        const options = {
          method: 'POST',
          headers: { 'content-type': 'application/x-www-form-urlencoded'},
          data: qs.stringify({"ThesisName" : this.input}),
          url :"http://www.tcgweb.cn:80/SelectProject" ,
        };
        axios(options).then((res) => {
          console.log('查询')
          if(res.data != -1){
            console.log(res.data.data)
            if(res.data.data === null || res.data.data.length === 0){
              this.tableData = []
              return
            }
            let data ={
              date : res.data.data[0].remind,
              name : res.data.data[0].DocxName.split("_")[1]
            }
            this.tableData = []
            this.tableData.push(data)
          }else {
            this.$message.error('查询失败')
          }
        })
      }else {
        this.$message({
          message:"搜索内容为空",
          type : "info"
        })
      }
    },
    /**
     * 初始化搜索框内容
     */
    initSearch(){
      this.input = ''
      this.init()
    },
    /**
     * 判断被选中项目
     */
    isSelect(){
      axios.post("http://www.tcgweb.cn:80/getSelect").then(res => {
        console.log(res.data)
        if(res.data === -1){
          // res.data.data.docxName.split("_")[1]
          this.selectValue = false
        }else {
          this.selectValue = true
          this.selectName = res.data
          for(let i in this.tableData){
            if(this.selectName === this.tableData[i].name){
              this.tableData[i].isSelected = 1
            }else {
              this.tableData[i].isSelected = 0
            }
          }
        }
      })
    },
    /**
     * 创建新项目
     */
    createArticleItem(){
      // this.tableData.push({name : value})
      this.$prompt('请输入项目名称', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /\S/,
        inputErrorMessage: '项目名称不能为空'
      }).then(({ value }) => {
        for ( let i of this.tableData){
          if(i.name === value){
            this.$message({
              type: 'error',
              message: '项目名称重复'
            });
            return
          }
        }
        this.$message({
          type: 'success',
          message: '新建成功'
        });
        // this.tableData.push({name : value})
        this.newProject(value)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消输入'
        });
      });
    },
    /**
     * 新建项目
     * @param name 项目名称
     */
    newProject(name){
      const options = {
        method: 'POST',
        headers: { 'content-type': 'application/x-www-form-urlencoded'},
        data: qs.stringify({"ThesisName" : name}),
        url :"http://www.tcgweb.cn:80/newProject" ,
      };
      axios(options).then((res) => {
        if(res.data.code === 0){
          this.tableData.push({name : name})
        }else {
          this.$message.error("创建失败")
        }
      })
    }

  },
}
</script>

<style scoped lang="less">
[ArticleList]{
  padding-left: 2vw;
}
</style>