<template>
  <nav>
    <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
      <ul class="navbar-nav">
      </ul>
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Пользователь
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="/admin">Админка</a></li>
          </ul>
        </li>
      </ul>
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
 