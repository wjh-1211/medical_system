<template>
    <div>
        <el-breadcrumb separator="|" class="bread">
            <el-breadcrumb-item :to="{ path: '/' }" class="font" style="font-size:20px">
                <span>医疗知识图谱智能问答系统</span>
            </el-breadcrumb-item>
            <el-breadcrumb-item class="font">
                <router-link to="/main/chat">
                    <span @click="change(1)" :class="{'highlight':index===1}">对话系统</span>
                </router-link>
            </el-breadcrumb-item>
            <el-breadcrumb-item class="font">
                <router-link to="/main/neovisual">
                    <span @click="change(2)" :class="{'highlight':index===2}">图谱可视化</span>
                </router-link>
            </el-breadcrumb-item>
            <el-breadcrumb-item class="font" >
                <router-link to="/main/backplat">
                    <span @click="change(3)" :class="{'highlight':index===3}">后台管理</span>
                </router-link>
            </el-breadcrumb-item>
            <span class="name">你好，{{username}}</span>
        </el-breadcrumb>
        <div v-if="isshow" class="welcome">{{ welcomeMessage }}  </div>
        <keep-alive>
            <router-view></router-view>
        </keep-alive>
    </div>
</template>

<script>
export default {
    name:'MainBoard',
    data(){
        return{
            index:0,
            username:this.$store.state.username,
            isshow:true,
            welcomeChars: [], // 用于存储每个字符的数组  
        }
    },
    methods:{
        change(num){
            this.index = num
            this.isshow =false
        }
    },
    computed: {  
        welcomeMessage() {  
            return this.welcomeChars.join(''); // join方法用于将数组（或一个类数组对象）的所有元素连接到一个字符串中，中间不是空格符
        },  
    }, 
    mounted() {  
        const message = "欢迎使用智能问答系统!";  
        let index = 0;  
        const interval = setInterval(() => {  
        if (index < message.length) {  
            this.welcomeChars.push(message[index]);  
            index++;  
        } else {  
            clearInterval(interval); // 当所有字符都添加完后，清除定时器  ，一定要删除，否则会消耗内存
        }  
        }, 150);  
    },  
}
</script>

<style lang="less">
    .bread{
        text-align: center ;
        background-color: black;
        height: 50px;
        // 要为组件设置一个类的名称，否则样式不生效
        .font {
            span{
                cursor:pointer;
                margin-left: 5px;
                line-height: 50px;
                color: white;
            }
            .highlight{
                color:#fc9105
            }            
        }
        .name{
            float:right;
            color:#fff;
            font-weight: bold;
            line-height: 50px;
            margin-right: 15px;
        }
    }
    .welcome{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top:300px;
        font-size: 50px;
        font-family: 'KaiTi';
        color:#5d554c;
    }
</style>