<template>
  <div class="container">
    <h1>Отзывы</h1>

    <form @submit.prevent.stop="onReviewAdd">
      <div class="row">
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="reviewToAdd.user" required />
            <label>ID пользователя</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <select class="form-select" v-model="reviewToAdd.game" required>
              <option :value="g.id" v-for="g in games">{{ g.game_name }}</option>
            </select>
            <label>Игра</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="text" class="form-control" v-model="reviewToAdd.review_text" required />
            <label>Текст отзыва</label>
          </div>
        </div>
        <div class="col">
          <div class="form-floating">
            <input type="number" class="form-control" v-model="reviewToAdd.rating" min="1" max="10" required />
            <label>Оценка</label>
          </div>
        </div>
        <div class="col-auto">
          <button class="btn btn-primary">Добавить</button>
        </div>
      </div>
    </form>

    <div v-for="item in reviews" class="d-flex gap-2 align-items-center mt-2">
      <div>{{ item.user }}</div>
      <div>{{ item.game }}</div>
      <div>{{ item.review_text }}</div>
      <div>{{ item.rating }}</div>
      <button
        class="btn btn-success"
        @click="onReviewEditClick(item)"
        data-bs-toggle="modal"
        data-bs-target="#editReviewModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>

    <div class="modal fade" id="editReviewModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">редактировать</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="reviewToEdit.user" />
                  <label>ID пользователя</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="reviewToEdit.game">
                    <option :value="g.id" v-for="g in games">{{ g.game_name }}</option>
                  </select>
                  <label>Игра</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="text" class="form-control" v-model="reviewToEdit.review_text" />
                  <label>Текст отзыва</label>
                </div>
              </div>
              <div class="col">
                <div class="form-floating">
                  <input type="number" class="form-control" v-model="reviewToEdit.rating" min="1" max="10" />
                  <label>Оценка</label>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateReview">Сохранить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'
import Cookies from 'js-cookie'

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
  fetchReviews()
  fetchGames()
})

const reviews = ref([])
const games = ref([])
const reviewToAdd = ref({})
const reviewToEdit = ref({})

async function fetchReviews() {
  const response = await axios.get("/api/reviews/")
  reviews.value = response.data
}

async function fetchGames() {
  const response = await axios.get("/api/games/")
  games.value = response.data
}

async function onReviewAdd() {
  await axios.post("/api/reviews/", {
    ...reviewToAdd.value,
  })
  await fetchReviews()
}

async function onRemoveClick(review) {
  await axios.delete(`/api/reviews/${review.id}/`)
  await fetchReviews()
}

async function onReviewEditClick(review) {
  reviewToEdit.value = { ...review }
}

async function onUpdateReview() {
  await axios.put(`/api/reviews/${reviewToEdit.value.id}/`, {
    ...reviewToEdit.value,
  })
  await fetchReviews()
}
</script>
