<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-content">
      <button class="modal-close" @click="close">✕</button>
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  emits: ['close'],
  methods: {
    close() {
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  z-index: 1000;
  inset: 0;
  background: rgba(30,41,59, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  border-radius: 1rem;
  max-width: 600px;
  width: 96%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem 1.5rem 1.5rem;
  position: relative;
}
.modal-close {
  position: absolute;
  top: 0.7rem;
  right: 1rem;
  background: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
}
</style> 