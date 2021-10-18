<template>
  <v-card width="400px" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">ログイン</h1>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field
          prepend-icon="mdi-account-circle"
          v-model="userId"
          label="ユーザ"
        />
        <v-text-field
          prepend-icon="mdi-lock"
          v-bind:append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
          v-bind:type="showPass ? 'text' : 'password'"
          @click:append="showPass = !showPass"
          v-model="userPass"
          label="パスワード"
        />
        <div class="red--text">{{ message }}</div>
        <v-card-actions>
          <v-btn block class="primary" @click="login" :loading="isloading">ログイン</v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'Login',
  data: () => ({
    message: '',
    isloading: false,
    showPass: false,
    userId: 'user01',
    userPass: 'pass'
  }),
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  methods: {
    ...mapActions(['auth']),
    login () {
      this.isloading = true
      this.auth({
        userId: this.userId,
        userPass: this.userPass
      }).then(() => {
        if (this.isAuthenticated) {
          const to = (this.$route.query.redirect || '/')
          this.$router.push(to)
        } else {
          this.message = 'Missing token'
        }
      })
        .catch(error => (this.message = error))
        .finally(() => (this.isloading = false))
    }
  }
}
</script>
