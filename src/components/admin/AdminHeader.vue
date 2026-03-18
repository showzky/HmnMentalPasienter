<template>
    <div class="admin-content-header">
    <h2>Management Dashboard</h2>
    <div class="profile-info">
      <div class="user-meta">
        <h1 class="username">Welcome, {{ displayName }}</h1>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'AdminHeader',
  props: ['displayName']
}
</script>
