<script>
   export default {
      props: ["loggedIn"],
      methods: {
         logoutUser: function() {
            this.token = null;
            localStorage.clear()
            this.$router.push('/')
         }
      }
   }
</script>

<template>
      <nav class="navbar bg-primary-subtle">
           <div class="container-fluid">
                <RouterLink class="navbar-brand" to="/dashboard">E-Card App</RouterLink>
                <!-- <button @click="this.$router.push('/')"  class="btn btn-danger">Logout</button> -->
                <button @click="logoutUser"  class="btn btn-danger">Logout</button>
           </div>
      </nav>
</template>

<style>

</style>