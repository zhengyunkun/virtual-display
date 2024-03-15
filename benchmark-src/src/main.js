import Vue from 'vue'
import App from './App.vue'
import HighchartsVue from 'highcharts-vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(HighchartsVue)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
