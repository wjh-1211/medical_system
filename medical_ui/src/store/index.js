import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

export default new Vuex.Store({
    state:{
        username:'',//用于在右上角展示登陆后的用户名称
        news:[],//用于管理员向用户回复修改后的消息
    },
    mutations:{
        setusername(state,value){
            state.username = value
        }
    }
})