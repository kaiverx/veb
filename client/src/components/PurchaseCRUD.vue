<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import axios from 'axios'

const purchases = ref([])
const games = ref([])
const purchaseToAdd = ref({})
const purchaseToEdit = ref({})
const stats = ref({})

const filters = ref({
  price_min: '',
  price_max: '',
})

const filteredPurchases = computed(() => {
  return purchases.value.filter(p => {
    if (filters.value.price_min && Number(p.price_at_purchase) < Number(filters.value.price_min)) return false
    if (filters.value.price_max && Number(p.price_at_purchase) > Number(filters.value.price_max)) return false
    return true
  })
})

function clearFilters() {
  filters.value = { price_min: '', price_max: '' }
}

function onExportExcel() {
  window.location.href = "/api/purchases/export-excel/"
}

async function fetchPurchases() {
  const r = await axios.get("/api/purchases/")
  purchases.value = r.data
}

async function fetchGames() {
  const r = await axios.get("/api/games/")
  games.value = r.data
}

async function fetchStats() {
  const r = await axios.get("/api/purchases/stats/")
  stats.value = r.data
}

async function onPurchaseAdd() {
  await axios.post("/api/purchases/", { ...purchaseToAdd.value })
  await fetchPurchases()
  await fetchStats()
  purchaseToAdd.value = {}
}

async function onUpdatePurchase() {
  await axios.put(`/api/purchases/${purchaseToEdit.value.id}/`, { ...purchaseToEdit.value })
  await fetchPurchases()
  await fetchStats()
}

async function onPurchaseEditClick(purchase) {
  purchaseToEdit.value = { ...purchase }
}

async function onRemoveClick(purchase) {
  await axios.delete(`/api/purchases/${purchase.id}/`)
  await fetchPurchases()
  await fetchStats()
}

onBeforeMount(async () => {
  await fetchPurchases()
  await fetchGames()
  await fetchStats()
})
</script>

<template>
  <div class="container-fluid px-4">
    <h1>Покупки</h1>

    <div class="mb-3 p-2 border rounded bg-light d-flex justify-content-between align-items-center">
      <div>Всего: <strong>{{ stats.count }}</strong> | Средняя цена: <strong>{{ stats.avg?.toFixed(2) }}₽</strong> | Макс: <strong>{{ stats.max }}₽</strong> | Мин: <strong>{{ stats.min }}₽</strong></div>
      <button class="btn btn-success btn-sm" @click="onExportExcel"><i class="bi bi-file-earmark-excel"></i> Экспорт в Excel</button>
    </div>

    <div class="p-2 px-0">
      <form @submit.prevent.stop="onPurchaseAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="purchaseToAdd.game" required>
                <option :value="g.id" v-for="g in games">{{ g.game_name }}</option>
              </select>
              <label>Игра</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="number" class="form-control" v-model="purchaseToAdd.price_at_purchase" required />
              <label>Цена покупки</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary"><i class="bi bi-plus-lg"></i></button>
          </div>
        </div>
      </form>
    </div>

    <div class="row mb-2">
      <div class="col">
        <input class="form-control form-control-sm" type="number" v-model="filters.price_min" placeholder="Цена от" />
      </div>
      <div class="col">
        <input class="form-control form-control-sm" type="number" v-model="filters.price_max" placeholder="Цена до" />
      </div>
      <div class="col-auto">
        <button class="btn btn-secondary btn-sm" @click="clearFilters">Сбросить</button>
      </div>
    </div>

    <div class="px-0">
      <div v-for="item in filteredPurchases" class="item mb-2 p-2 border rounded">
        <div>
          <strong>Игра #{{ item.game }}</strong> — {{ item.price_at_purchase }}₽
          <br/><small>{{ item.purchase_date }}</small>
        </div>
        <div class="mt-2">
          <button class="btn btn-success me-2" @click="onPurchaseEditClick(item)" data-bs-toggle="modal" data-bs-target="#editPurchaseModal">
            <i class="bi bi-pencil-fill"></i>
          </button>
          <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editPurchaseModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать покупку</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating mb-2">
              <select class="form-select" v-model="purchaseToEdit.game">
                <option :value="g.id" v-for="g in games">{{ g.game_name }}</option>
              </select>
              <label>Игра</label>
            </div>
            <div class="form-floating mb-2">
              <input type="number" class="form-control" v-model="purchaseToEdit.price_at_purchase" />
              <label>Цена покупки</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal"><i class="bi bi-x-lg"></i></button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdatePurchase"><i class="bi bi-check-lg"></i></button>
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
.item > div:first-child { flex: 1; }
button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}
button i { font-size: 16px; }
</style>
