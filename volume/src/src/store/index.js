import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userId: 'guest',
    userToken: '',
    userTeam: ''
  },
  getters: {
    isAuthenticated: state => !!state.userToken,
    isManagerAuthenticated: state => !!state.userToken && state.userTeam === 'manager'
  },
  mutations: {
    updateUser (state, response) {
      state.userId = response.username
      state.userToken = response.access_token
      state.userTeam = response.team
    }
  },
  actions: {
    async auth ({ commit }, payload) {
      var responseData = {
        username: '',
        access_token: ''
      }
      return new Promise((resolve, reject) => {
        axios.post('/api/login', { name: payload.userId, password: payload.userPass })
          .then(response => {
            responseData = response.data
            resolve()
          })
          .catch(error => reject(error))
          .finally(() => commit('updateUser', responseData))
      })
    },
    deauth ({ commit }) {
      commit('updateUser', { userId: '', userToken: '', userTeam: '' })
    }
  }
})
