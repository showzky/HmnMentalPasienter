<template>
  <div class="dino-runner-container">
    <canvas ref="gameCanvas" width="600" height="180"></canvas>
    <div class="score">Score: {{ score }}</div>
    <button @click="startGame" class="start-btn">Start</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';

const score = ref<number>(0);
const groundY = 30; // Distance from bottom to ground line
const canvasHeight = 180; // Should match your canvas height
const obstacles = ref<{ x: number; y: number; width: number; height: number; speed: number }[]>([]);
const isGameOver = ref(false);
const dino = ref({
  x: 50,
  // Start at ground level:
  y: canvasHeight - groundY - 48, // 48 is dino height
  width: 44,
  height: 48,
  velocityY: 0,
  gravity: 0.9,
  jumpPower: -16,
  isJumping: false,
});
const gameCanvas = ref<HTMLCanvasElement | null>(null);

function handleKeyDown(e: KeyboardEvent){
    if (e.code === 'Space'){   // <-- FIXED: 'Space'
        e.preventDefault();
        jump();
    }
}

function draw() {
    if (!gameCanvas.value) return;
    const ctx = gameCanvas.value.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, gameCanvas.value.width, gameCanvas.value.height);

    // Draw ground
    ctx.strokeStyle = "#222";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, canvasHeight - groundY);
    ctx.lineTo(gameCanvas.value.width, canvasHeight - groundY);
    ctx.stroke();

    // Draw dino
    ctx.fillStyle = "#50bcdf";
    ctx.fillRect(
      dino.value.x,
      dino.value.y,
      dino.value.width,
      dino.value.height
    );

    // Draw obstacles
    ctx.fillStyle = "#e07a5f";
    obstacles.value.forEach(obstacle => {
      ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
    });

    // Draw Game Over
    if (isGameOver.value) {
      ctx.fillStyle = "rgba(0,0,0,0.7)";
      ctx.fillRect(0, 0, gameCanvas.value!.width, gameCanvas.value!.height);
      ctx.fillStyle = "#fff";
      ctx.font = "bold 32px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Game Over", gameCanvas.value!.width / 2, gameCanvas.value!.height / 2);
    }
}

let obstacleInterval: NodeJS.Timeout;

function startGame(): void {
  score.value = 0;
  dino.value.y = canvasHeight - groundY - dino.value.height;
  dino.value.velocityY = 0;
  dino.value.isJumping = false;
  obstacles.value = [];
  isGameOver.value = false;
  stopGameLoop();
  clearInterval(obstacleInterval);
  obstacleInterval = setInterval(spawnObstacle, 1500);
  gameLoop();
  draw();
}

function jump() {
    if(!dino.value.isJumping){
        dino.value.velocityY = dino.value.jumpPower;
        dino.value.isJumping = true;
    }
}


function spawnObstacle() {
  const height = 30 + Math.random() * 20; // random height for variety
  obstacles.value.push({
    x: gameCanvas.value ? gameCanvas.value.width : 600, // start at right edge
    y: canvasHeight - groundY - height,
    width: 20 + Math.random() * 20, // random width
    height,
    speed: 6,
  });
}
function checkCollision(
  dino: { x: number; y: number; width: number; height: number },
  obstacle: { x: number; y: number; width: number; height: number }
) {
  return (
    dino.x < obstacle.x + obstacle.width &&
    dino.x + dino.width > obstacle.x &&
    dino.y < obstacle.y + obstacle.height &&
    dino.y + dino.height > obstacle.y
  );
}

let animationFrame: number;
function gameLoop() {
  dino.value.velocityY += dino.value.gravity;
  dino.value.y += dino.value.velocityY;

  // Floor collision
  const dinoBottom = canvasHeight - groundY - dino.value.height;
  if (dino.value.y > dinoBottom) {
    dino.value.y = dinoBottom;
    dino.value.velocityY = 0;
    dino.value.isJumping = false;
  }

  // Move obstacles
  obstacles.value.forEach(obstacle => {
    obstacle.x -= obstacle.speed;
  });
  // Remove obstacles that have gone off screen
  obstacles.value = obstacles.value.filter(obstacle => obstacle.x + obstacle.width > 0);

  // Check for collision
  for (const obstacle of obstacles.value) {
    if (checkCollision(dino.value, obstacle)) {
      isGameOver.value = true;
      stopGameLoop();
      break;
    }
  }

  draw();
  if (!isGameOver.value) {
    animationFrame = requestAnimationFrame(gameLoop);
  }
}

function stopGameLoop() {
  cancelAnimationFrame(animationFrame);
  clearInterval(obstacleInterval);
}

onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
    draw();
});
onBeforeUnmount(() => {
    window.removeEventListener('keydown', handleKeyDown);
});
</script>



<style scoped>
.dino-runner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(to bottom, #e0eafc 0%, #cfdef3 100%);
  padding: 2rem 0;
  border-radius: 2rem;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
}

canvas {
  background: #fff;
  border: 2px solid #bdbdbd;
  border-radius: 1rem;
  margin-bottom: 1rem;
}

.score {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 1rem;
}

.start-btn {
  background: #22223b;
  color: #fff;
  border: none;
  border-radius: 1rem;
  padding: 0.7rem 2rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: background 0.2s;
}
.start-btn:hover {
  background: #4a4e69;
}
</style>
