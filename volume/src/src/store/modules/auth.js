import axios from 'axios'

const state = {
  name: 'guest',
  pass: 'pass',
  token: ''
}

const getters = {
  token: state => state.token,
  name: state => state.name,
  pass: state => state.pass
}

const mutations = {
  updateName: (state, name) => (state.name = name),
  updatePass: (state, pass) => (state.pass = pass),
  // setToken: (state, token) => (state.token = token.token),
  setToken: function (state, token) {
    state.token = token.data.token
  },
  unsetToken: function (state) {
    state.token = ''
    state.user = ''
    state.pass = ''
  }
}

const actions = {
  async authUser ({ commit, state }) {
    const response = await axios.post('/api/login', { name: state.name, password: state.pass })
    commit('setToken', response)
  },
  async destoryUser ({ commit }) {
    commit('unsetToken')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
