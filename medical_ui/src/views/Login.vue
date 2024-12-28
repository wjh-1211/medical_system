<template>
    <div class="outerimage">
        <div class="outer">
            <h2 style="">登录</h2>
            <div class="input">
                <span>用户名</span>
                <el-input placeholder="请输入用户名" prefix-icon="el-icon-s-custom" style="width:250px" v-model="username"></el-input>
            </div>
            <div class="input">
                <span>密码</span>
                <el-input 
                    placeholder="请输入密码" 
                    prefix-icon="el-icon-s-grid" 
                    style="width:250px;margin-left:15px" 
                    type="password"
                    v-model="password"
                >    
                </el-input>
            </div>
            <div class="input" style="display: flex;">
                <span style="flex: 1;line-height:40px;">验证码</span>
                <el-input placeholder="请输入验证码" prefix-icon="el-icon-s-data" style="width:180px;flex: 3.5;" v-model="code">
                    
                </el-input>
                <el-tag 
                    style="width:60px;margin-left:10px;line-height:40px;flex: 1;height:40px;"
                    @click="getCode">
                {{viewCode}}
                </el-tag>
            </div>
            <div class="button">
                <el-button type="primary" @click="login">登录</el-button>
                <el-button type="success" @click="sign">注册</el-button>
            </div>
        </div>
        <el-dialog :visible.sync="dialogVisible" customClass="dialog">
            <el-form :model="form" class="login">
                <h2 class="title">用户注册</h2>
                <el-form-item label="用户名" label-width="100px">
                    <el-input v-model="form.username" style="width:280px" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item label="密码" label-width="100px">
                    <el-input type="password" v-model="form.password" style="width:280px" placeholder="请输入密码"></el-input>
                </el-form-item>
                <el-form-item label="手机号" label-width="100px">
                    <el-input v-model="form.phone" style="width:280px" placeholder="请输入手机号"></el-input>
                </el-form-item>
                <el-button type="warning" @click="submit">提交</el-button>
            </el-form>
        </el-dialog>
    </div>
</template>

<script>
export default {
    name:'Login',
    data(){
        return{
            username:'',
            password:'',
            code:'',
            viewCode:'',
            form:{
                username:'',
                password:'',
                phone:'',
            },
            dialogVisible:false,
        }
    },
    methods:{
        login(){
            if(this.code===this.viewCode){
                const time = this.getcurrenttime()
                this.$axios.post('http://127.0.0.1:5003/login',{'username':this.username,'password':this.password,'lasttime':time})
                .then((res)=>{    
                    console.log(res);
                    if(res.status===200){
                            this.$router.push({name:'main'})
                            this.$message.success('登录成功！')
                            this.$store.commit('setshowwelcome',false)
                            this.$store.commit('setusername',this.username)
                    }
                })
                .catch((err)=>{
                    if(err.response.status===401){
                        this.$message.error('用户名或密码错误！')
                    }
                    else this.$message.error('该账号被封禁！')
                })                
            }
            else{
                this.$message.error('验证码错误！')
            }
        },
        sign(){
            this.dialogVisible = !this.dialogVisible
        },
        submit(){
            this.$axios.post('http://127.0.0.1:5003/sign',
            {
                'username':this.form.username,
                'password':this.form.password,
                'phone':this.form.phone
            })
            .then((res)=>{
                if(res.status===200){
                    this.$message.success('注册成功！')
                    this.dialogVisible = !this.dialogVisible
                }
            })
            .catch((err)=>{
                this.$message.error('该用户已存在，请重新输入用户名！')
            })
        },
        // 验证码的制作
        getCode () {
            this.viewCode = ''
            let codeString = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'//split('')是将字符串拆分为单个字符的数组
            let codeArray = codeString.split('')
            let num = codeArray.length
            let newCodeArray = []
            for (let i = 0; i < 5; i++) {
                let index = Math.floor(Math.random() * num)
                newCodeArray.push(codeArray[index])
            }
            this.viewCode = newCodeArray.join('')
        },
        // 获取当前登陆时间
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
    },
    mounted(){
        this.getCode()
    }
}
</script>

<style lang="less">
    .outerimage{
        height:100vh;
        overflow:hidden;
        background-image:url('~@/assets/mainpage.jpeg');
        // 一下两个样式使得背景图片能够居于中心位置
        background-size: cover;
        background-position: center;
        .outer{
            width: 500px;
            height: 500px;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin:0 auto;
            margin-top:100px;
            border-radius:15px;
            // 这样只是设置了该父元素背景的透明度，而子元素不受影响
            background: rgba(0,0,0,0.5);
            .input{
                margin:15px;
                font-weight: bold;
            }
            .button{
                margin-top:15px;
            }
        }    
        .dialog{
            border-radius:20px;
            margin-left: 515px;
            width: 500px;
            .login{
                height: 400px;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }            
        }
    }
</style>