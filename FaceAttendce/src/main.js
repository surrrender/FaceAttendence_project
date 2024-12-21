import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
// 导入element_plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
//导入定义好的路由器
import router from './router'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
