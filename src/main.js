import Vue from 'vue'
import App from './App.vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import "bootstrap-vue/dist/bootstrap-vue.css"
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.use(BootstrapVue)

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyALma_bIrPD2I6AcEQ5kHreIHVu7qXg8aI',
    libraries: 'places,drawing,visualization'
  },
})

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
