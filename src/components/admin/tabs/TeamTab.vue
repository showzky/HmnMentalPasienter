<template>
  <section class="team-manager">
    <div class="data-widget">
      <h3>Manage Team Members</h3>
      <div class="team-members-list">
        <div v-for="(member, index) in teamMembers" :key="member.id" class="team-member-card">
          <div class="member-avatar">
            <img :src="member.avatar || defaultAvatar" :alt="member.name" />
            <button class="change-avatar-btn" @click="$emit('triggerAvatarUpload', member.id)">
              <i class="fas fa-camera"></i>
            </button>
          </div>
          <div class="member-info">
            <input 
              type="text" 
              :value="member.name" 
              @input="updateMemberField(index, 'name', $event.target.value)" 
              placeholder="Name" />
            <input 
              type="text" 
              :value="member.title" 
              @input="updateMemberField(index, 'title', $event.target.value)" 
              placeholder="Title" />
            <textarea 
              :value="member.bio" 
              @input="updateMemberField(index, 'bio', $event.target.value)" 
              placeholder="Bio"></textarea>
          </div>
          <div class="member-actions">
            <button class="save-btn" @click="$emit('saveTeamMember', member)">Save</button>
            <button class="delete-btn" @click="$emit('deleteTeamMember', member.id)">Delete</button>
          </div>
        </div>
      </div>
      <button class="add-member-btn" @click="$emit('addNewTeamMember')">
        <i class="fas fa-plus"></i> Add Team Member
      </button>
      <div v-if="teamMessage" class="form-message" :class="{ success: teamSuccess, error: !teamSuccess }">
        {{ teamMessage }}
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: [
    'teamMembers',
    'defaultAvatar',
    'teamMessage',
    'teamSuccess'
  ],
  emits: [
    'saveTeamMember', 
    'deleteTeamMember', 
    'addNewTeamMember', 
    'triggerAvatarUpload', 
    'update:teamMembers'
  ],
  methods: {
    updateMemberField(index, field, value) {
      const updatedMembers = [...this.teamMembers];
      updatedMembers[index] = { 
        ...updatedMembers[index], 
        [field]: value 
      };
      this.$emit('update:teamMembers', updatedMembers);
    }
  }
}
</script>

<style scoped>
/* Add your styles here if needed */
</style>
