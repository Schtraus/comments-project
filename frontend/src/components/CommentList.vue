<template>
  <div>
    <h2>Комментарии</h2>

    <label>
      Сортировать по:
      <select v-model="ordering" @change="loadComments()">
        <option value="-created_at">Новые сверху</option>
        <option value="created_at">Старые сверху</option>
        <option value="username">Имя (A→Я)</option>
        <option value="-username">Имя (Я→A)</option>
        <option value="email">Email (A→Я)</option>
        <option value="-email">Email (Я→A)</option>
      </select>
    </label>

    <div v-for="comment in comments" :key="comment.id" class="comment">
      <p><strong>{{ comment.username }}</strong> — {{ formatDate(comment.created_at) }}</p>
      <p v-html="comment.text"></p>

      <div v-if="comment.attachments.length">
        <p><strong>Файлы:</strong></p>
        <ul>
          <li v-for="file in comment.attachments" :key="file.id">
            <a :href="apiUrl + file.file" target="_blank">{{ file.file_type }}</a>
          </li>
        </ul>
      </div>

      <!-- Рекурсивные ответы -->
      <div class="replies" v-if="comment.replies.length">
        <CommentThread v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
      </div>
    </div>

    <!-- Пагинация -->
    <div class="pagination">
      <button @click="loadComments(previous)" :disabled="!previous">← Назад</button>
      <button @click="loadComments(next)" :disabled="!next">Вперёд →</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CommentThread from './CommentThread.vue'

export default {
  components: { CommentThread },
  data() {
    return {
      apiUrl: 'http://127.0.0.1:8000',
      comments: [],
      next: null,
      previous: null,
      ordering: '-created_at'
    }
  },
  methods: {
    async loadComments(url = null) {
      if (!url) {
      url = `${this.apiUrl}/api/comments/?ordering=${this.ordering}`
    }

      const response = await axios.get(url)
      this.comments = response.data.results
      this.next = response.data.next
      this.previous = response.data.previous
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    }
  },
  mounted() {
    this.loadComments()
  }
}
</script>

<style scoped>
.comment {
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}
.replies {
  padding-left: 20px;
  border-left: 2px dashed #ddd;
  margin-top: 10px;
}
</style>
