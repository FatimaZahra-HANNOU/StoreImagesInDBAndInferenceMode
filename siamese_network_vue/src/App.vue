<template>
  <NavBar/>

  <router-view/>
</template>

<script>
  import NavBar from './components/NavBar.vue'

  export default {
    name: 'App',
    components: {
      NavBar
    },
    data() {
      return {
      }
    },
    beforeCreate() {
      this.$store.commit('initializeStore');
    }
  }
</script>
