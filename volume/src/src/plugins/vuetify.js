import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#00d1b2',
        secondary: '#92D1C8',
        accent: '#e91e63',
        error: '#b71c1c'
      }
    }
  }
})
