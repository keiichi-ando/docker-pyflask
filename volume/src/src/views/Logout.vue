<template>
  <v-card width="400px" class="mx-auto mt-5">
    <v-card-title>
      <h1 class="display-1">ログアウト</h1>
    </v-card-title>
    <v-card-text>ご利用ありがとうございました</v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'Logout',
  created () {
    this.$store.dispatch('deauth')
  }
}
</script>
