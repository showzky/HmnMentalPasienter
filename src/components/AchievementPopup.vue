<template>
    <div v-if="visible" class="achievement-popup">
      <img v-if="image" :src="image" class="achievement-image" />
      <div class="achievement-info">
        <h4 class="achievement-title">{{ title }}</h4>
        <p class="achievement-desc">{{ description }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: String,
      description: String,
      image: String,
      duration: { type: Number, default: 4000 }
    },
    data() {
      return { visible: false }
    },
    methods: {
      show() {
        this.visible = true;
        setTimeout(() => this.visible = false, this.duration);
      }
    }
  }
  </script>
  
  <style scoped>
  .achievement-popup {
    position: fixed;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    background: #23272a;
    color: #fff;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    padding: 18px 28px;
    z-index: 9999;
    animation: slideIn 0.5s;
  }
  .achievement-image {
    width: 48px;
    height: 48px;
    margin-right: 18px;
  }
  .achievement-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin: 0;
  }
  .achievement-desc {
    font-size: 0.95rem;
    margin: 0;
    color: #b9bbbe;
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translate(-50%, 60px);}
    to   { opacity: 1; transform: translate(-50%, 0);}
  }
  </style>