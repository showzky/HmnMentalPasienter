<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-slate-900 to-blue-900 px-2">
    <div class="w-full max-w-md rounded-3xl shadow-2xl p-6 bg-white/10 backdrop-blur-md border border-white/10">
      <!-- Banner Ribbon -->
      <div class="absolute left-1/2 -top-8 -translate-x-1/2 z-10 flex flex-col items-center">
        <!-- Main ribbon -->
        <div class="relative">
          <div class="bg-gradient-to-r from-blue-500 to-cyan-400 text-white font-extrabold text-2xl px-10 py-2 rounded-b-2xl shadow-lg tracking-wider border-4 border-blue-400 drop-shadow-lg">
            LEADERBOARD
          </div>
          <!-- Left tail -->
          <div class="absolute left-0 -bottom-3 w-8 h-4 bg-gradient-to-r from-blue-500 to-cyan-400 rounded-bl-lg border-l-4 border-b-4 border-blue-400 -rotate-12 shadow-md"></div>
          <!-- Right tail -->
          <div class="absolute right-0 -bottom-3 w-8 h-4 bg-gradient-to-r from-blue-500 to-cyan-400 rounded-br-lg border-r-4 border-b-4 border-blue-400 rotate-12 shadow-md"></div>
        </div>
      </div>
      <ul>
        <li
          v-for="(user, idx) in users"
          :key="user.id"
          class="flex items-center gap-3 py-3 px-4 rounded-2xl mb-4 shadow-lg border-4 transition-all duration-200 relative"
          :class="{
            'bg-yellow-300/90 border-yellow-400 text-yellow-900': idx === 0,
            'bg-blue-300/90 border-blue-400 text-blue-900': idx === 1,
            'bg-amber-400/90 border-amber-500 text-amber-900': idx === 2,
            'bg-white/20 border-white/20 text-white': idx > 2
          }"
        >
          <!-- Rank badge -->
          <span class="w-8 text-center text-2xl font-bold select-none">
            <span v-if="idx === 0">🥇</span>
            <span v-else-if="idx === 1">🥈</span>
            <span v-else-if="idx === 2">🥉</span>
            <span v-else>{{ idx + 1 }}</span>
          </span>
          <!-- Avatar -->
          <img
            v-if="user.avatar"
            :src="user.avatar"
            class="w-10 h-10 rounded-full object-cover border-2 border-white/30 shadow"
            alt="avatar"
          />
          <div v-else class="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center text-white text-lg font-bold border-2 border-white/30 shadow">
            ?
          </div>
          <!-- Username -->
          <div class="flex-1 min-w-0">
            <span class="truncate font-semibold text-lg">{{ user.username }}</span>
          </div>
          <!-- Score chip -->
          <span class="flex items-center gap-1 bg-white/80 text-yellow-700 font-extrabold px-3 py-1 rounded-full text-lg shadow tabular-nums">
            🪙
            {{ user.fitte_points }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from '@/axios';

interface LeaderboardUser {
  id: number;
  username: string | null;
  avatar: string | null;
  fitte_points: number;
}

const users = ref<LeaderboardUser[]>([]);

onMounted(async () => {
  try {
    const res = await axios.get('/clicker/leaderboard');
    users.value = res.data.filter(
      (u: LeaderboardUser) => u.username && u.username.trim() !== ""
    );
  } catch {
    users.value = [];
  }
});
</script>
