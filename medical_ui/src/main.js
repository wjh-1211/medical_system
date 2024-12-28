import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'; // 2.1引入结构
import 'element-ui/lib/theme-chalk/index.css'; // 2.2引入样式


Vue.config.productionTip = false
Vue.prototype.$axios = axios;
Vue.use(ElementUI)

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app')
