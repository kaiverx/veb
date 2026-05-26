<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Navbar</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/developers">Разработчики</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/games">Игры</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profiles">Профили</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/purchases">Покупки</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/reviews">Отзывы</router-link>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Пользователь
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="/admin/">Админка</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <router-view />
</template>

<script setup>
import { onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})
</script>