import { createApp } from 'vue'
import App from './App.vue'
import {router} from "./routes.js"
createApp(App).use(router).mount('#app')


//  usually we do 
// const app=new Vue({
//   el:
//   data:
//  method: 
//})



// alterantely use .mount for el repacement and createApp ceates other things n components 