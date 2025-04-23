<template>
  <form @submit.prevent="submitComment" enctype="multipart/form-data">
    <input v-model="form.username" placeholder="Имя" required />
    <input v-model="form.email" placeholder="Email" type="email" required />
    <input v-model="form.homepage" placeholder="Сайт (необязательно)" />

    <div class="formatting-buttons">
      <button type="button" @click="wrapText('strong')"><strong>B</strong></button>
      <button type="button" @click="wrapText('i')"><i>I</i></button>
      <button type="button" @click="wrapText('code')"><code>&lt;/&gt;</code></button>
      <button type="button" @click="insertLink()">[a]</button>
    </div>

    <textarea ref="textArea" v-model="form.text" placeholder="Комментарий" required></textarea>

    <!-- CAPTCHA -->
    <div v-if="captcha.image_url" class="captcha-block">
      <img :src="apiUrl + captcha.image_url" alt="captcha" />
      <button type="button" @click="getCaptcha">Обновить</button>
      <input v-model="form.captcha_text" placeholder="Введите капчу" required />
    </div>

    <!-- Файлы -->
    <input type="file" multiple @change="handleFiles" />

    <button type="submit">Отправить</button>
    <hr />
    <h3>Предпросмотр:</h3>
    <div class="preview" v-html="form.text"></div>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    parentId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      apiUrl: 'http://127.0.0.1:8000',
      form: {
        username: '',
        email: '',
        homepage: '',
        text: '',
        captcha_key: '',
        captcha_text: '',
        uploaded_files: []
      },
      captcha: {}
    }
  },
  methods: {
    async getCaptcha() {
      const res = await axios.get(`${this.apiUrl}/api/captcha/`)
      this.captcha = res.data
      this.form.captcha_key = res.data.key
    },
    handleFiles(e) {
      this.form.uploaded_files = Array.from(e.target.files)
    },
    async submitComment() {
      const formData = new FormData()
      for (const key in this.form) {
        if (key === 'uploaded_files') {
          this.form.uploaded_files.forEach(file => formData.append('uploaded_files', file))
        } else {
          formData.append(key, this.form[key])
        }
      }
      if (this.parentId) {
        formData.append('parent', this.parentId)
      }

      try {
        await axios.post(`${this.apiUrl}/api/comments/`, formData)
        this.resetForm()
        this.getCaptcha()
        this.$emit('submitted')
      } catch (error) {
        console.error(error.response?.data)
        alert('Ошибка при отправке')
        this.getCaptcha()
      }
    },
    resetForm() {
      this.form.username = ''
      this.form.email = ''
      this.form.homepage = ''
      this.form.text = ''
      this.form.captcha_text = ''
      this.form.uploaded_files = []
    },
    wrapText(tag) {
      const textarea = this.$refs.textArea
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selected = this.form.text.slice(start, end)

      const before = this.form.text.slice(0, start)
      const after = this.form.text.slice(end)

      this.form.text = `${before}<${tag}>${selected}</${tag}>${after}`

      this.$nextTick(() => {
        textarea.focus()
        textarea.selectionStart = textarea.selectionEnd = start + tag.length + 2
      })
    },
    insertLink() {
      const url = prompt("Введите ссылку:")
      const title = prompt("Введите текст ссылки:")
      if (url && title) {
        const textarea = this.$refs.textArea
        const pos = textarea.selectionStart
        const before = this.form.text.slice(0, pos)
        const after = this.form.text.slice(pos)
        const link = `<a href="${url}" title="${title}">${title}</a>`
        this.form.text = before + link + after

        this.$nextTick(() => {
          textarea.focus()
          textarea.selectionStart = textarea.selectionEnd = pos + link.length
        })
      }
    }

  },
  mounted() {
    this.getCaptcha()
  }
}
</script>

<style scoped>
  .preview {
  padding: 10px;
  background: #f5f5f5;
  border: 1px solid #ccc;
  white-space: pre-wrap;
  margin-top: 10px;
  }

  .formatting-buttons {
    margin-bottom: 5px;
  }
  .formatting-buttons button {
    margin-right: 5px;
    padding: 2px 6px;
    font-size: 14px;
  }
</style>