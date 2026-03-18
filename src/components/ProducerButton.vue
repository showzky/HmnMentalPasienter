<template>
  <button
    v-if="canSeeProducerButton"
    class="dropdown-item producer-btn"
    @click="goToProducerPanel"
  >
    <i class="fas fa-sliders"></i>
    Dashboard
  </button>
</template>

<script>
export default {
  name: 'ProducerButton',
  computed: {
    canSeeProducerButton() {
      // List of allowed roles (add more as needed)
      const allowedRoles = ['producer', 'admin', 'developer'];
      let user = null;
      try {
        user = JSON.parse(localStorage.getItem('user'));
      } catch {}
      if (!user || !user.roles) return false;
      return user.roles.some(role =>
        allowedRoles.includes(role.name.toLowerCase())
      );
    }
  },
  methods: {
    goToProducerPanel() {
      // Change this route to wherever your producer panel is
      this.$router.push('/management');
    }
  }
};
</script>

<style scoped>
.producer-btn {
  color: #fff;
  background: #43b581;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  transition: background 0.2s;
}
.producer-btn:hover {
  background: #389e6b;
}
</style>