import Vue, { KeepAlive } from 'vue'
import VueRouter from 'vue-router'

import ChatBot from '../views/ChatBot'
import NeoVisual from '../views/NeoVisual'
import MainBoard from '../views/MainBoard'
import BackPlat from '../views/BackPlat'
import Login from '../views/Login'

Vue.use(VueRouter)


const VueRouterPush = VueRouter.prototype.push
VueRouter.prototype.push = function push (to) {
  return VueRouterPush.call(this, to).catch(err => err)
}

const routes = [
    {
        path:'/',
        redirect:'/login'
    },
    {
        path:'/login',
        component:Login
    },
    {
        path:'/main',
        component:MainBoard,
        name:'main',
        meta:{
            keepAlive:true
        },
        children:[
            {
                path:'chat',
                name:'chat',
                component:ChatBot,
                meta:{
                    keepAlive:true
                }
            },
            {
                path:'neovisual',
                name:'neovisual',
                component:NeoVisual,
                meta:{
                    keepAlive:true
                }
            },
            {
                path:'backplat',
                name:'backplat',
                component:BackPlat,
                meta:{
                    keepAlive:true
                }
            }
        ]
    }
]

const router = new VueRouter({
    routes 
})

export default router