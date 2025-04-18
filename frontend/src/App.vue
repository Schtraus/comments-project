<template>
  <div class="app">
    <h1>Комментарии</h1>
    <CommentForm />
    <hr />
    <CommentList />
  </div>
</template>

<script>
import CommentForm from './components/CommentForm.vue'
import CommentList from './components/CommentList.vue'

export default {
  components: {
    CommentForm,
    CommentList
  }
}
</script>
