<template>
  <div class="comment">
    <p><strong>{{ comment.username }}</strong> — {{ formatDate(comment.created_at) }}</p>
    <p v-html="comment.text"></p>

    <div v-if="comment.attachments.length">
      <ul>
        <li v-for="file in comment.attachments" :key="file.id">
          <a :href="apiUrl + file.file" target="_blank">{{ file.file_type }}</a>
        </li>
      </ul>
    </div>

    <div class="replies" v-if="comment.replies.length">
      <CommentThread v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
    </div>
  </div>
</template>

<script>
import CommentThread from './CommentThread.vue'

export default {
  name: 'CommentThread',
  components: { CommentThread },
  props: ['comment'],
  data() {
    return {
      apiUrl: 'http://127.0.0.1:8000'
    }
  },
  methods: {
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    }
  }
}
</script>

<style scoped>
.comment {
  border-left: 2px solid #aaa;
  margin-top: 10px;
  padding-left: 10px;
}
</style>
