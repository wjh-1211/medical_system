<template>
  <div>
     <!-- :close-on-click-modal="false" -->
    <el-dialog :visible.sync="dialogVisible" :showClose="false">
        <el-form :model="form" class="login">
            <p class="title">管理员登录</p>
            <el-form-item label="用户名" label-width="100px">
                <el-input v-model="form.name" style="width:280px" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" label-width="100px">
                <el-input type="password" v-model="form.password" style="width:280px" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-button type="primary" @click="submit">登录</el-button>
        </el-form>
    </el-dialog>
    <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="用户评价数据" name="first">
            <el-table :data="filtertableData" style="width: 100%" v-if="!dialogVisible" border>
                <el-table-column prop="id" label="序号" width="50" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名" width="100" align="center"></el-table-column>
                <el-table-column prop="request" label="用户提问" width="250" align="center"></el-table-column>
                <el-table-column prop="answer" label="系统回答" width="400" align="center">
                </el-table-column>
                <el-table-column prop="time" label="提问时间" width="200" align="center"></el-table-column>
                <el-table-column prop="comment" label="用户建议" width="250" align="center"></el-table-column>
                <el-table-column prop="score" label="用户评分" width="80" align="center"></el-table-column>
                <el-table-column label="操作" width="150" align="center">
                    <template slot-scope="scope">
                        <el-button type="primary" @click="senddata(scope.row)" size="small">回复</el-button>
                        <el-button type="danger" @click="deletedata(scope.row)" size="small">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>            
        </el-tab-pane>
        <el-tab-pane label="疾病提问统计" name="second" class="second">
            <el-table :data="diseasedata" style="width:300px" class="tablelist"> 
                <el-table-column prop="id" label="序号" width="100" align="center"></el-table-column>
                <el-table-column prop="diseasename" label="疾病名称" width="100" align="center"></el-table-column>
                <el-table-column prop="num" label="提问次数" width="100" align="center"></el-table-column>
            </el-table>
            <el-button type="primary" @click="makeform(1)">生成统计图表</el-button>
            <el-button type="primary" @click="makeciyun(2)">生成词云</el-button>
            <div class="outer">
                <div class="chart" v-show="index===1">
                    <div class="echart" id="echart"></div>
                    <div class="circle" id="circle"></div>                    
                </div>
                <div class="cloud" id="cloud" v-show="index===2"></div>
            </div>
        </el-tab-pane>
        <el-tab-pane label="用户管理" name="third">
            <el-table :data="userData" style="width: 100%">
                <el-table-column prop="id" label="序号" width="50" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名" width="300" align="center"></el-table-column>
                <el-table-column prop="password" label="密码" width="250" align="center"></el-table-column>
                <el-table-column prop="phone" label="手机号" width="200" align="center"></el-table-column>
                <el-table-column prop="isvalid" label="状态" width="200" align="center"></el-table-column>
                <el-table-column prop="lasttime" label="上次登录时间" width="200" align="center"></el-table-column>
                <el-table-column label="操作" width="300" align="center">
                    <template slot-scope="scope">
                        <el-button 
                            type="danger" 
                            @click="userban(scope.row,'封禁中')" 
                            size="small" 
                            :disabled="scope.row.isvalid==='使用中'?false:true"
                        >
                            禁用
                        </el-button>
                        <el-button 
                            type="primary" 
                            @click="userban(scope.row,'使用中')" 
                            size="small"
                            :disabled="scope.row.isvalid==='封禁中'?false:true"
                        >
                            启用
                        </el-button>
                        <el-button type="warning" @click="userdelete(scope.row)" size="small">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>            
        </el-tab-pane>
    </el-tabs>
    <el-dialog :visible.sync="dialogVisible1">
        <el-form :model="form1" class="login">
            <p class="title">消息回复</p>
            <el-form-item label="用户提问" label-width="100px">
                <el-input v-model="form1.request" style="width:530px"></el-input>
            </el-form-item>
            <el-form-item label="修改回答" label-width="100px">
                <textarea v-model="form1.answer" cols="70" rows="10" style="resize:none;"></textarea>
            </el-form-item>
            <el-button type="warning" @click="submitvuex">提交</el-button>
        </el-form>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from "echarts";
import 'echarts-wordcloud'
export default {
    name:'BackPlat',
    data(){
        return{
            dialogVisible:false,
            dialogVisible1:false,
            form:{
                name:'',
                password:''
            },
            form1:{
                request:'',
                answer:'',
            },
            tableData: [],
            diseasedata:[],
            userData:[],
            activeName:'first',
            xData:[],
            yData:[],
            pieData:[],
            index:''
        }
    },
    computed:{
        filtertableData(){
            return this.tableData.filter(item=>{
                // 如果无法过滤掉第一行空数据，可能是因为第一行数据并非空字符串，而是 null 或 undefined，导致过滤条件不生效。为了解决这个问题，你可以在过滤函数中增加对 null 和 undefined 的判断。
                // 十分考验js的基本功
                return Object.values(item).some(value => value !== null && value !== undefined && value !== '');
            })
        }
    },
    methods:{
        submit(){
            if(this.form.name==='wjhzb'&&this.form.password==='123456'){
                this.dialogVisible=!this.dialogVisible
                this.$message.success("登录成功！")
            }
        },
        deletedata(row){
            const id = row.id
            this.$confirm('确定要删除吗','提示').then(()=>{
                this.$axios.post('http://127.0.0.1:5001/deleterecord',{id:id})
                .then(res=>{
                    if(res.status===200){
                        this.$message.warning('删除成功')
                        this.tableData = []
                        this.loaddata()
                    }
                })                
            })
        },
        // 加载数据库的第一个表到第一个table中
        loaddata(){
            this.$axios.get('http://127.0.0.1:5001/getrecord')
            .then(res=>{
                console.log(res);
                for(let i=0;i<res.data.length;i++){
                    this.tableData.push(
                        {
                            id:res.data[i].id,
                            request:res.data[i].request,
                            answer:res.data[i].answer,
                            time:res.data[i].time,
                            comment:res.data[i].comment,
                            score:res.data[i].satisfication,
                            username:res.data[i].username
                        }
                    )
                }
            })            
        },
        // 加载数据库中的第二个表到第二个table中
        loadnum(){
            this.$axios.get('http://127.0.0.1:5002/getnum')
            .then((res)=>{
                for(let i=0;i<res.data.length;i++){
                    this.diseasedata.push(
                        {
                            id:res.data[i].id,
                            diseasename:res.data[i].diseasename,
                            num:res.data[i].num
                        }
                    )
                    this.xData.push(res.data[i].diseasename)
                    this.yData.push(res.data[i].num)
                    this.pieData.push(
                        {
                            value:res.data[i].num,
                            name:res.data[i].diseasename
                        }
                    )
                }
            })
        },
        // 加载数据库的第三个表到第三个table中
        loaduser(){
            this.$axios.get('http://127.0.0.1:5003/getuserlist')
            .then((res)=>{
                console.log(res);
                for(let i=0;i<res.data.length;i++){
                    this.userData.push(
                        {
                            id:res.data[i].id,
                            username:res.data[i].username,
                            password:res.data[i].password,
                            phone:res.data[i].phone,
                            isvalid:res.data[i].isvalid,
                            lasttime:res.data[i].lasttime
                        }
                    )
                }
            })
        },
        handleClick(){
            this.activeName = 'second'
        },
        initEcharts(){
            const option ={
                xAxis:{
                    type:'category',
                    data:this.xData,
                    axisLabel:{
                        show:true,
                        formatter:function(value){
                            return value.split("").join("\n");
                        }
                    }
                },
                yAxis:{
                    type:'value'
                },
                series:[
                    {
                        type:"bar",
                        data:this.yData,
                        label:{
                            show:true,
                            position:'top'
                        },
                        barWidth: 20,
                        // barGap:'80%',
                        // barCategoryGap:'50%',
                        showBackground: true,
                        // 将背景完整的补充上
                        backgroundStyle: {
                            color: 'rgba(180, 180, 180, 0.2)'
                        },
                        itemStyle:{
                            normal:{
                                color:function(){return "#"+Math.floor(Math.random()*(256*256*256-1)).toString(16);}
                            }
                        }
                    }
                ]
            };
            const myChart = echarts.init(document.getElementById("echart"))
            myChart.setOption(option)
        },
        initpieEcharts(){
            const option ={
                legend:{
                    data:this.xData,
                    right:"10%",
                    // top:"30%",
                    // orient:"vertical"
                },
                title:{
                    
                },
                series:[
                    {
                        type:"pie",
                        label:{
                            show:true,
                            formatter:"{b}:{c}({d}%)"
                        },
                        data:this.pieData
                    }
                ]
            }
            const mycircle = echarts.init(document.getElementById("circle"))
            mycircle.setOption(option)
        },
        initciyuncharts(){
            const option={
                series:[
                    {
                        type:'wordCloud',
                        data:this.pieData,//配置数据，一定要是一个数组对象，否则将无法正确配置，一开始只是传递了一个对象
                        gridSize: 20,//用来调整词之间的距离
                        sizeRange: [14, 60],//用来调整字的大小范围
                        rotationRange: [-90,90],//设置词的旋转角度
                        fontSizeRange: [5, 40],//设置字体大小
                        textStyle:{
                            normal:{
                                color: function() {
                                    return 'rgb(' + [
                                        Math.round(Math.random() * 160),
                                        Math.round(Math.random() * 160),
                                        Math.round(Math.random() * 160)
                                    ].join(',') + ')';
                                }
                            }
                        }
                    }
                ]
            };
            const cloudmap = echarts.init(document.getElementById('cloud'))
            cloudmap.setOption(option)
        },
        makeform(index){
            this.index = index 
            this.initEcharts()
            this.initpieEcharts()
        },
        makeciyun(index){
            this.index = index
            this.initciyuncharts()
        },
        senddata(row){
            this.dialogVisible1 = !this.dialogVisible1
            console.log(row);
            this.form1.request = row.request
            this.form1.answer = row.answer
        },
        submitvuex(){
            this.$message.success('提交成功！')
            this.dialogVisible1 = !this.dialogVisible1
            this.$store.state.news.push({request:this.form1.request,answer:this.form1.answer})
        },
        userban(row,val){
            console.log(row);
            this.$axios.post('http://127.0.0.1:5003/changestate',{username:row.username,state:val})
            .then((res)=>{
                this.userData = []
                this.loaduser()
                
            })
        },
        userdelete(row){
            const id = row.id
            this.$confirm('确定要删除吗','提示').then(()=>{
                this.$axios.post('http://127.0.0.1:5003/deleteuser',{id:id})
                .then(res=>{
                    if(res.status===200){
                        this.userData = []
                        this.loaduser()
                    }
                })                
            })
        }
    },
    mounted(){
        this.dialogVisible = !this.dialogVisible
        this.loaddata()
        this.loadnum()
        this.loaduser()
    }
}
</script>

<style lang="less" scoped>
    .login{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        .title{
            font-weight: bold;
            font-size:20px;
        }
    }
    .second{
        .tablelist{
            float:left;
            height: 100%;
        }
        .outer{
            width: 1180px;
            height: 600px;
            margin-left: 300px;
            border: 5px solid;
            .chart{
                .echart{
                    float:left;
                    width: 500px;
                    height: 500px;
                }
                .circle{
                    float:right;
                    width:600px;
                    height: 500px;
                }                
            }
            .cloud{
                width: 800px;
                height: 600px;
                margin:0 auto;
            }
        }
    }
</style>