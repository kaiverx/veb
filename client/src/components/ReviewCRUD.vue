<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const reviews = ref([])
const games = ref([])
const reviewToAdd = ref({})
const reviewToEdit = ref({})

async function fetchReviews() {
  const r = await axios.get("/api/reviews/")
  reviews.value = r.data
}

async function fetchGames() {
  const r = await axios.get("/api/games/")
  games.value = r.data
}

async function onReviewAdd() {
  await axios.post("/api/reviews/", { ...reviewToAdd.value })
  await fetchReviews()
  reviewToAdd.value = {}
}

async function onUpdateReview() {
  await axios.put(`/api/reviews/${reviewToEdit.value.id}/`, { ...reviewToEdit.value })
  await fetchReviews()
}

async function onReviewEditClick(review) {
  reviewToEdit.value = { ...review }
}

async function onRemoveClick(review) {
  await axios.delete(`/api/reviews/${review.id}/`)
  await fetchReviews()
}

onBeforeMount(async () => {
  await fetchReviews()
  await fetchGames()
})
</script>

<template>
  <div class="container-fluid px-4">
    <h1>Отзывы</h1>

    <div class="p-2 px-0">
      <form @submit.prevent.stop="onReviewAdd">
        <div class="row">
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
              <label>Оценка (1-10)</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary"><i class="bi bi-plus-lg"></i></button>
          </div>
        </div>
      </form>
    </div>

    <div class="px-0">
      <div v-for="item in reviews" class="item mb-2 p-2 border rounded">
        <div>
          <strong>Игра #{{ item.game }}</strong> - Оценка: {{ item.rating }}/10
          <br/><small>{{ item.review_text }}</small>
        </div>
        <div class="mt-2">
          <button class="btn btn-success me-2" @click="onReviewEditClick(item)" data-bs-toggle="modal" data-bs-target="#editReviewModal">
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editReviewModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать отзыв</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <select class="form-select" v-model="reviewToEdit.game">
                <option :value="g.id" v-for="g in games">{{ g.game_name }}</option>
              </select>
              <label>Игра</label>
            </div>
            <div class="form-floating mb-2">
              <input type="text" class="form-control" v-model="reviewToEdit.review_text" />
              <label>Текст отзыва</label>
            </div>
            <div class="form-floating mb-2">
              <input type="number" class="form-control" v-model="reviewToEdit.rating" min="1" max="10" />
              <label>Оценка (1-10)</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"><i class="bi bi-x-lg"></i></button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateReview"><i class="bi bi-check-lg"></i></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.item {
  padding: 0.5rem 1rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.item > div:first-child {
  flex: 1;
}
button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}
button i {
  font-size: 16px;
}
</style>
