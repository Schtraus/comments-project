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

    <CommentThread v-for="comment in comments" :key="comment.id" :comment="comment" />


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
      ordering: '-created_at',
      socket: null,
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
    connectWebSocket() {
      this.socket = new WebSocket('ws://127.0.0.1:8000/ws/comments/')

      this.socket.onmessage = (event) => {
        const newComment = JSON.parse(event.data)
        
        newComment.attachments = newComment.attachments.map(file => {
          if (file.file_type === 'image') {
            return {
              ...file,
              file: file.file + '?t=' + Date.now()
            }
          }
          return file
        })

        this.loadComments()
        // Только если это корневой коммент (не ответ)
        // if (!newComment.parent) {
        //   this.comments.unshift(newComment)

        //   // обрезаем до 25, если превышает лимит
        //   if (this.comments.length > 25) {
        //     this.comments.pop()
        //   }
        // } else {
        //   // это ответ — просто перезагружаем дерево
        //   this.loadComments()
        // }
      }

      this.socket.onclose = () => {
        console.warn('WebSocket закрыт. Переподключаемся...')
        setTimeout(() => this.connectWebSocket(), 1000)
      }
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    }
  },
  mounted() {
    this.loadComments()
    this.connectWebSocket()
  }
}
</script>

<style scoped>

</style>
