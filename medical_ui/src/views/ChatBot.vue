<template>
<div>
    <transition name="rec-in-left">
        <div class="recognize" v-show="multishow">
            <div class="title">识别检测功能</div>
            <div class="searchbox">
                <div style="margin-top:10px;font-weight:bold">请在下面的文本框输入问句</div>
                <textarea cols="40" rows="10" style="resize:none;" v-model="multiword"></textarea>
                <el-button type="primary" @click="getword(0)">实体识别</el-button>
                <el-button type="primary" @click="getword(1)">意图识别</el-button>
            </div>
            <div class="answer">
                <div style="font-weight:bold">识别结果</div>
                <div class="realword" ref="showanswer" style="width:300px;height:150px;border:2px solid black;margin-left:15px;"></div>
                <el-button type="danger" style="margin-top:5px;" @click="multishow=!multishow">退出</el-button>
            </div>
        </div>            
    </transition>

    <div class="outer">
        <div class="header">
            <div class="header-title">
                <i class="el-icon-caret-left" title="返回" v-show="isshow" @click="backend"></i>
                <i class="el-icon-search" title="实体识别" @click="multishow=!multishow" v-show="!isshow"></i>
                <p class="title">医疗智能问答系统</p>
                <i class="el-icon-message" @click="shownews" title="消息">
                    <div class="newscircle" v-show="newsnum">
                        <span>{{newsnum}}</span>
                    </div>
                </i>
            </div>
        </div>
        <div class="show1" v-show="!isshow">
            <div class="main" ref="dialogueContainer">
                <div class="screen-inner">
                    <div v-for="(message,index) in messages" :key="index" :class="message.sender==='robot'?'robot-dialogue':'man-dialogue'">
                        <!-- 若动态进行绑定src，则需要将引入的图片放到data中，然后再引用变量 -->
                        <img :src="message.sender==='robot' ? robotImg : manImg" 
                            :class="message.sender==='robot'?'robotinfo':'userinfo'">
                        <div :class="message.sender==='robot'?'dialogue-text':'dialogue-input'">{{message.text}}</div>
                        <i class="el-icon-chat-dot-square" title="评价" v-if="message.sender==='robot'" @click="comment(message)"></i>
                    </div>
                </div>
                <!-- 点击每条消息后面的消息提示标识所弹出的评价对话框 -->
                <el-dialog :visible.sync="dialogVisible" :close-on-click-modal="false">
                    <el-form :model="form" :rules="rules" ref="ruleForm" class="comment">
                        <p style="font-weight:bold;font-size:20px;margin-top:-20px;text-align:center;">评价</p>
                        <el-form-item label="问题" label-width="50px">
                            <el-input v-model="form.request"></el-input>
                        </el-form-item>
                        <el-form-item label="回答" label-width="50px">
                            <textarea v-model="form.answer" cols="85" rows="10" style="resize:none;"></textarea>
                        </el-form-item>
                        <el-form-item label="时间" label-width="50px">
                            <el-input v-model="form.time"></el-input>
                        </el-form-item>
                        <el-form-item label="回答满意度" label-width="95px" prop="satisfication">
                            <el-input v-model="form.satisfication" placeholder="评分标准为0-5"></el-input>
                        </el-form-item>
                        <el-form-item label="建议" label-width="55px" prop="comment">
                            <el-input v-model="form.comment"></el-input>
                        </el-form-item>
                        <el-button type="primary" style="display:block;margin:0 auto" @click="submitcomment('ruleForm')">提交</el-button>
                    </el-form>
                </el-dialog>
            </div>
            <div class="submit">
                <textarea 
                    id="dialogue-input" 
                    @keydown.enter="submit" 
                    @keydown.enter.prevent
                    v-model="notedata" 
                    placeholder="请输入您的问题,按Enter键提交">
                </textarea>
            </div>        
        </div>
        <!-- 头部点击消息提示后向上滑动的界面 -->
        <transition name="slide-up-down">
            <div class="show2" v-show="isshow">
                <div v-for="(item,index) in news" :key="index" class="outer-box-card">
                    <el-card class="box-card">
                        <h2>消息{{index+1}}</h2>
                        <span style="display:block;width:800px;">
                            <p style="font-weight:bold;">你的提问：</p>{{item.request}}
                        </span>            
                        <span><p style="font-weight:bold;">修正回答：</p>{{item.answer}}</span>
                    </el-card>
                </div>
            </div>    
        </transition>
    </div> 

    <transition name="rec-on-right">
        <div class="information" v-if="diseasename">
            <div class="firstline">
                <i class="el-icon-info"></i>
                <h4>实体识别结果</h4>            
            </div>
            <span>{{diseasename}}</span>
        </div>      
    </transition>
</div>
</template>

<script>
export default {
    name:'ChatBot',
    data(){
        return{
            notedata:'',
            multiword:'',
            showmutiword:[],
            showicon:true,
            robotImg:require('../assets/robot.png'),
            manImg:require('../assets/man.jpg'),
            messages:[
                {text:'你好，欢迎使用医疗自助问答服务系统，你可以对疾病从定义、病因、预防、临床表现、相关病症、治疗方法、所属科室、治愈率、禁忌、治疗时间等方面向我提问，祝您身体健康！',sender:'robot'}
            ],
            dialogVisible:false,
            form:{
                request:'',
                answer:'',
                comment:'',
                satisfication:'',
                time:'',
                username:this.$store.state.username
            },
            rules:{
                satisfication:[
                    { required: true, message: '请输入评分', trigger: 'blur' },
                ],
                comment:[
                    { required: true, message: '请输入评价', trigger: 'blur' },
                ]
            },
            diseasename:'',
            news:[],
            newsnum:0,
            isshow:false,//是否展示消息列表
            multishow:false,//是否展示实体搜索列表
        }
    },
    methods:{
        submit(){
            const text = this.notedata.replace(/\n/g, "")//将最后的回车空格去掉
            const requestData = {sent:text}
            this.$axios.get('http://127.0.0.1:5000/index',{
                params:requestData
            })
            .then((res)=>{
                console.log(res);
                this.messages.push({text:this.notedata,sender:'man'})
                if(!(res.data.diseasename instanceof Array)){
                    this.diseasename = res.data.diseasename
                    this.updatenum(this.diseasename)
                    // diseasename用来控制实体识别结果动画的消失，将该效果持续三秒
                    setTimeout(()=>{
                        this.diseasename = ''
                    },3000)
                }
                
                setTimeout(()=>{
                    this.messages.push({text:res.data.reply,sender:'robot'})
                },1000)
               
                this.notedata=''
                
            })
            .catch((error)=>{
                console.error(error)
            })
        },
        // 调用疾病统计函数
        updatenum(name){
            // 注意，如果使用post进行数据的传递，一定要使用json格式将其进行传递，前面是后端requst调用的名称，后面写的是传入的值
            this.$axios.post('http://127.0.0.1:5002/savenum',{diseasename:name})
            .then((res)=>{
                console.log(res)
            })
            .catch((err)=>{
                console.log(err);
            })
        },
        scrollToBottom(){
            this.$refs.dialogueContainer.scrollTop = this.$refs.dialogueContainer.scrollHeight
        },
        comment(message){
            this.dialogVisible = !this.dialogVisible
            const lastmessage =  this.getlastmessage(message)
            this.form.request = lastmessage.text
            this.form.answer = message.text
            this.form.time = this.getcurrenttime()
            
        },
        getlastmessage(message){
            for(let i = this.messages.indexOf(message)-1;i>=0;i--){
                if(this.messages[i].sender === 'man'){
                    return this.messages[i]
                }
            }
        },
        getcurrenttime(){
            const now = new Date();
            const year = now.getFullYear();
            // 一下返回的都是数字，但是如果不能够达到两位数，就需要进行字符串的填充，因此需要先转换到string类型
            const month = String(now.getMonth() + 1).padStart(2, '0');
            const day = String(now.getDate()).padStart(2, '0');
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        },
        submitcomment(ruleForm){
            console.log(this.form)
            this.$refs[ruleForm].validate((valid)=>{
                if(valid){
                    this.$axios.post('http://127.0.0.1:5001/saverecord',this.form)
                    .then(res=>{
                        if(res.status===200){
                            this.$message.success("提交成功！")
                            this.dialogVisible = !this.dialogVisible
                            this.form.request =''
                            this.form.answer =''
                            this.form.time =''
                            this.form.satisfication =''
                            this.form.comment =''
                        }
                    })
                    .catch(err=>{
                        console.error('ERROR',err)
                    })                    
                }
                else{
                    return false
                }
            })
        },
        shownews(){
            this.isshow = !this.isshow
            this.newsnum = 0
        },
        backend(){
            this.isshow = !this.isshow
            this.$store.state.news = []
        },
        getword(type){
            const requestData = {sent:this.multiword}
            this.$axios.get('http://127.0.0.1:5000/getmutiword',{
                params:requestData
            })
            .then((res)=>{
                console.log(res);
                if(type===0)this.showmutiword = res.data.mutianswer[0]
                else this.showmutiword = res.data.mutianswer[1]
                this.$refs.showanswer.innerHTML = this.showmutiword
            })
            .catch(()=>{
                this.$refs.showanswer.innerHTML = "未检测到相关结果！"
            })
        },
    },
    watch:{
        // 对路由的切换进行监听
        '$route'(){
            this.news = this.$store.state.news
            this.newsnum = this.$store.state.news.length
        }
    },
    // 在数据更改导致的虚拟 DOM 重新渲染和更新完毕之后被调用。
    updated(){
        this.scrollToBottom()
    }
}
</script>

<style lang="less" scoped>
.recognize{
    width: 340px;
    height: 600px;
    float: left;
    border: 2px solid black;
    .title{
        border: 2px solid black;
        text-align: center;
        font-weight: bold;
        height: 50px;
        line-height: 50px;
        margin-bottom:15px 0;
        background-color: #d6d6d6;
    }
    .searchbox{
        margin-top: 20px;
        height: 240px;
        text-align: center;
        border: 2px solid black;
    }
    .answer{
        margin-top: 40px;
        text-align: center;
        height: 240px;
        border: 2px solid black;
    }
}
.outer{
    flex-direction: column;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 800px;
    height: 600px;
    box-shadow: 0px 0px 15px 15px #b0b0b0;
    margin-left: 350px;
    margin-top: 50px;
    border: solid;
    background-color: #d6d6d6;
    .header{
        .header-title{
            width: 800px;
            border-bottom: 2px solid black;
            text-align: center;
            display: flex;
            .el-icon-caret-left{
                line-height:54px;
                cursor:pointer;
                margin-left:10px;
                font-size:25px;
            }
            .title{
                flex-grow: 1;
                margin-left: 20px;
            }
            .el-icon-search{
                line-height:54px;
                font-size:20px;
                cursor:pointer;
                margin-left: 20px;
            }
            .el-icon-message{
                line-height: 54px;
                margin-right: 20px;
                font-size:25px;
                position: relative;
                cursor:pointer;
                .newscircle{
                    width: 15px;
                    height: 15px;
                    border-radius: 50%;
                    background-color: red;
                    position: absolute;
                    right:-3px;
                    top:12px;
                    display: flex; /* 将 .newscircle 设置为 Flexbox 容器 */
                    justify-content: center; /* 水平居中 */
                    align-items: center; /* 垂直居中 */
                    span{
                        font-size:15px;
                        color:white;
                    }
                }                
            }
        }
    }
    .show1{
        .main{
            width: 800px;
            height: 410px;
            max-height: 410px;
            overflow-y:auto;
            .screen-inner{
                margin: 15px;
                .robot-dialogue{
                    width: 100%;//宽度一定要设置成100%，确保其拥有父元素的整个宽度
                    // 添加 overflow: hidden; 主要是为了清除浮动（clear float）。在这种情况下，由于子元素使用了浮动，父元素不会自动扩展以包含浮动元素，可能导致布局问题。通过为父元素设置 overflow: hidden;，可以强制父元素包含其浮动子元素。
                    // 它的工作原理是，设置 overflow: hidden; 的元素会创建一个 BFC（块级格式化上下文），BFC 会包含浮动元素并防止其溢出到父元素之外，从而解决了浮动元素导致的布局问题。
                    overflow:hidden;
                    margin-top: 15px;
                    // 图片圆框样式
                    .robotinfo{
                        width: 35px;
                        height: 35px;
                        float: left;
                        margin-right: 10px;
                        border-radius: 15px;
                    }
                    .dialogue-text{
                        max-width: 665px;//需要设置出最大长度，以避免文本太长将文本框撑开导致文本框样式不一致
                        background-color: #fff;
                        float: left;
                        padding:10px;
                        font-size: 14px;
                        position:relative;
                    }
                    .el-icon-chat-dot-square{
                        cursor: pointer;
                        margin-left:5px;
                        line-height: 35px;
                    }
                    // 在每个文本框前面添加一个小三角形样式
                    .dialogue-text::before{
                        position:absolute;
                        left: -8px;
                        content: '';
                        border-right: 10px solid #FFF;
                        border-top: 8px solid transparent;
                        border-bottom: 8px solid transparent;
                    }
                }
                .man-dialogue{
                    width: 100%;
                    overflow:hidden;
                    margin-top: 15px;
                    .userinfo{
                        float: right;
                        width: 35px;
                        height: 35px;
                        margin-left: 15px;
                        border-radius: 20px;
                    }
                    .dialogue-input{
                        background: #6aee75;
                        float: right;
                        padding:10px;
                        font-size: 14px;
                        position:relative
                    }
                    .el-icon-chat-dot-square{
                        cursor: pointer;
                        margin-right:5px;
                        line-height: 35px;
                        float:right;
                    }
                    .dialogue-input::after{
                        position:absolute;
                        right:-8px;
                        content:'';
                        border-left:10px solid #6aee75;
                        border-bottom:8px solid transparent;
                        border-top:8px solid transparent;
                    }
                }
            }
            .comment{
                width: 700px;
                height: 500px;
            }
        }
        .submit{
            #dialogue-input{
                width: 796px;
                height: 130px;
                resize:none;
                outline:none;
                // border-bottom-left-radius: 15px;
                // border-bottom-right-radius: 15px;
                font-size: 25px;
            }
        }        
    }
    .show2{
        width: 800px;
        height: 545px;
        background-color: white;
        max-width: 800px;
        max-height: 545px;
        overflow-y:auto;  
        .outer-box-card{
            border-bottom: 5px solid;
            .box-card:hover{
                background-color: rgb(184, 182, 182);
            }
        }
    }

}

.slide-up-down-enter-active,.slide-up-down-leave-active{
    transition: transform 0.5s ease;
}
.slide-up-down-enter,.slide-up-down-leave-to{
    transform: translateY(100%)
}
.information{
    position:absolute;
    top:120px;
    right:10px;
    width: 290px;
    height: 70px;
    background-color: #e2dede;
    border:2px solid #000;
    border-radius:5px;
    .firstline{
        margin: 5px;
        display: flex;//这一步可以将i和h4放在同一排，记住！
        .el-icon-info{
            color:#0ac429;
            font-size:20px;
            margin-right: 5px;
        }
        h4{
            width: 100px;
            margin:0;
        }            
    }
    span{
        display: block;
        margin: 10px;
        font-weight: bold;
        font-size: 20px;
    }
}
@keyframes slideInFromRight {
    from {
        transform: translateX(100%);
    }
    to {
        transform: translateX(0);
    }
}

@keyframes slideOutToLeft {
    from {
        transform: translateX(0);
    }
    to {
        transform: translateX(100%);
    }
}
.rec-on-right-enter-active {
    animation: slideInFromRight 1s ease;
}

.rec-on-right-leave-active {
    animation: slideOutToLeft 1s ease;
}

@keyframes slideOutFromLeft{
    from {
        transform: translateX(-100%)
    }
    to{
        transform: translateX(0)
    }
}

@keyframes slideOutToRight{
    from {
        transform: translateX(0)
    }
    to{
        transform:translateX(-100%)
    }
}

.rec-in-left-enter-active{
    animation:slideOutFromLeft 0.5s ease
}

.rec-in-left-leave-active{
    animation:slideOutToRight 0.5s ease
}

</style>