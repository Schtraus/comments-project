<template>
  <div class="comment">
    <p><strong>{{ comment.username }}</strong> — {{ formatDate(comment.created_at) }}</p>
    <p v-html="comment.text"></p>

    <div v-if="comment.attachments.length">
      <ul>
        <li v-for="file in comment.attachments" :key="file.id">
          <a
            v-if="file.file_type === 'image'"
            :href="file.file"
            data-lightbox="comment-images"
          >
            <img :src="file.file" style="max-width: 150px; max-height: 100px; margin: 5px;" />
          </a>

          <a
            v-else
            :href="file.file"
            target="_blank"
          >
            {{ file.file_type }}
          </a>
        </li>
      </ul>
    </div>

    
    <button @click="showReplyForm = !showReplyForm">
      {{ showReplyForm ? 'Отмена' : 'Ответить' }}
    </button>
    
    <div v-if="showReplyForm" class="reply-form">
      <CommentForm
      :parent-id="comment.id"
      @submitted="onReplySubmitted"
      />
    </div>
    
    <div class="replies" v-if="comment.replies.length">
      <CommentThread v-for="reply in comment.replies" :key="reply.id" :comment="reply" />
    </div>
  </div>
</template>

<script>
import CommentThread from './CommentThread.vue'
import CommentForm from './CommentForm.vue'

export default {
  name: 'CommentThread',
  components: { 
    CommentThread,
    CommentForm,
   },
  props: ['comment'],
  data() {
    return {
      apiUrl: 'http://127.0.0.1:8000',
      showReplyForm: false
    }
  },
  methods: {
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString()
    },
    onReplySubmitted() {
      this.showReplyForm = false
    }
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

.reply-form {
  margin-top: 10px;
  padding-left: 15px;
  border-left: 2px dotted #aaa;
}
</style>
