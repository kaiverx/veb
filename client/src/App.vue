<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container">
      <a class="navbar-brand" href="#">Game Store</a>

      <div>
        <router-link to="/games" class="btn btn-outline-light me-2">Games</router-link>
        <router-link to="/developers" class="btn btn-outline-light me-2">Developers</router-link>
        <router-link to="/profiles" class="btn btn-outline-light me-2">User Profiles</router-link>
        <router-link to="/purchases" class="btn btn-outline-light me-2">Purchases</router-link>
        <router-link to="/reviews" class="btn btn-outline-light">Reviews</router-link>
      </div>
    </div>
  </nav>

  <div class="container">
    <router-view />
  </div>
</template>
