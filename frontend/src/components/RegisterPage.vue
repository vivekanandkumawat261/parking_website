<script>
import axios from "axios";

export default {
  data() {
    return {
      formData: {
        username: "",
        email: "",
        password: ""
      },
      message: "",
      error: ""
    };
  },
  methods: {
    async registerUser() {
      try {
        const res = await axios.post(
          "http://127.0.0.1:5000/api/register",
          JSON.stringify(this.formData),
          {
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*"
            }
          }
        );

        if (res.status === 201 || res.status === 200) {
          this.message = "Registration successful! Please login.";
          this.error = "";
          // redirect to login page
          this.$router.push("/login");
        }
      } catch (err) {
        this.error = err.response?.data?.message || "Registration failed!";
      }
    }
  }
};
</script>

<template>
  <div id="main">
    <div id="canvas">
      <div id="form-body">
        <h1>Register Form</h1>

        <p class="err" v-if="error">{{ error }}</p>
        <p class="success" v-if="message">{{ message }}</p>

        <form @submit.prevent="registerUser">
          <div class="mb-3">
            <label for="Input1" class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              id="Input1"
              v-model="formData.username"
              required
            />
          </div>

          <div class="mb-3">
            <label for="Input3" class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              id="Input3"
              v-model="formData.email"
              required
            />
          </div>

          <div class="mb-3">
            <label for="Input2" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="Input2"
              v-model="formData.password"
              required
            />
          </div>

          <div style="text-align: center;">
            <input type="submit" class="btn btn-primary" value="Register" />
            <br />
            Already have an account?
            <router-link to="/login">Login</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style>
#form-body {
  height: auto;
  padding: 20px;
  max-width: 400px;
  margin: auto;
}
.err {
  color: red;
}
.success {
  color: green;
}
</style>
