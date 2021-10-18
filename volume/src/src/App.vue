<template>
    <v-app>
        <v-app-bar absolute app color="primary" dark>
            <div class="d-flex align-center" @click="$router.push('/')">
                <img
                    alt="Site Logo"
                    class="shrink mr-2"
                    contain
                    src="@/assets/cooltext395320672852798.png"
                    transition="scale-transition"
                    width="80"
                />
                <v-toolbar-title>re:glas</v-toolbar-title>
            </div>

            <v-spacer></v-spacer>
            <!-- <v-btn v-show="isManagerAuthenticated" text to="/jobs">Jobs</v-btn> -->
            <v-btn v-show="!isAuthenticated" text to="/login">Login</v-btn>
            <v-btn v-show="isAuthenticated" text to="/logout">Logout</v-btn>
        </v-app-bar>

        <v-main class="px-12">
            <router-view />
        </v-main>
    </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'App',

  data () {
    return {
      activeIndex: this.$route.name
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'isManagerAuthenticated'])
  }
}
</script>

<style scoped>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    /* text-align: center; */
    color: #2c3e50;
    font-size: 1em;
    margin: 0 auto;
}
a {
    text-decoration: none;
}
</style>
