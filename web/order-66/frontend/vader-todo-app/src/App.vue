<template>
  <div id="app" class="vader-app">
    <div class="stars"></div>
    <div class="stars2"></div>
    <div class="stars3"></div>
    
    <header class="app-header">
      <div class="vader-helmet">
        <div class="helmet-shine"></div>
      </div>
      <h1 class="app-title star-wars-font">
        VADER'S TODO EMPIRE
      </h1>
      <p class="app-subtitle">
        "Your lack of organization is disturbing"
      </p>
    </header>

    <main class="app-main">
      <router-view />
    </main>

    <footer class="app-footer">
      <p>"The power of the Dark Side compels you to complete your tasks"</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Main app component for Vader Todo
</script>

<style scoped>
.vader-app {
  min-height: 100vh;
  background: 
    radial-gradient(ellipse at top left, rgba(108, 92, 231, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at bottom right, rgba(255, 107, 107, 0.1) 0%, transparent 50%),
    radial-gradient(ellipse at bottom, #1a1a2e 0%, #0f0f0f 100%);
  position: relative;
  overflow-x: hidden;
}

/* Enhanced Star Field with Better Performance */
.stars,
.stars2,
.stars3 {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 120%;
  transform: rotate(-45deg);
  will-change: transform;
  pointer-events: none;
}

.stars {
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.9), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.7), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.8), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.5), transparent);
  background-repeat: repeat;
  background-size: 200px 100px;
  animation: stellar-drift 25s linear infinite;
  opacity: 0.8;
}

.stars2 {
  background-image: 
    radial-gradient(1px 1px at 10px 10px, rgba(255,255,255,0.6), transparent),
    radial-gradient(1px 1px at 30px 60px, rgba(255,255,255,0.4), transparent),
    radial-gradient(1px 1px at 80px 20px, rgba(108, 92, 231, 0.3), transparent);
  background-repeat: repeat;
  background-size: 300px 150px;
  animation: stellar-drift 35s linear infinite reverse;
  opacity: 0.6;
}

.stars3 {
  background-image: 
    radial-gradient(1px 1px at 15px 25px, rgba(255,255,255,0.3), transparent),
    radial-gradient(1px 1px at 65px 85px, rgba(255,255,255,0.2), transparent),
    radial-gradient(2px 2px at 50px 50px, rgba(255, 107, 107, 0.2), transparent);
  background-repeat: repeat;
  background-size: 400px 200px;
  animation: stellar-drift 45s linear infinite;
  opacity: 0.4;
}

@keyframes stellar-drift {
  0% {
    transform: rotate(-45deg) translateX(0) translateY(0);
  }
  100% {
    transform: rotate(-45deg) translateX(-200px) translateY(-200px);
  }
}

/* Modern Header Design */
.app-header {
  text-align: center;
  padding: var(--space-3xl) var(--space-md);
  position: relative;
  z-index: 10;
}

.vader-helmet {
  width: 100px;
  height: 100px;
  background: 
    linear-gradient(135deg, #2d3748 0%, #1a202c 50%, #2d3748 100%);
  border-radius: 50% 50% 45% 45%;
  margin: 0 auto var(--space-xl);
  position: relative;
  box-shadow: 
    inset 0 8px 16px rgba(255,255,255,0.1),
    0 16px 32px rgba(0,0,0,0.8),
    0 0 40px rgba(var(--color-primary-rgb), 0.2);
  transition: all var(--transition-slow);
}

.vader-helmet:hover {
  transform: scale(1.05) rotateY(10deg);
  box-shadow: 
    inset 0 8px 16px rgba(255,255,255,0.2),
    0 20px 40px rgba(0,0,0,0.9),
    0 0 60px rgba(var(--color-primary-rgb), 0.4);
}

.vader-helmet::before {
  content: '';
  position: absolute;
  top: 30%;
  left: 50%;
  transform: translateX(-50%);
  width: 35px;
  height: 18px;
  background: linear-gradient(to bottom, #000, #1a1a1a);
  border-radius: 18px 18px 0 0;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.8);
}

.vader-helmet::after {
  content: '';
  position: absolute;
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
  width: 45px;
  height: 10px;
  background: linear-gradient(to bottom, #000, #333);
  border-radius: var(--radius-sm);
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.8);
}

.helmet-shine {
  position: absolute;
  top: 15%;
  left: 25%;
  width: 24px;
  height: 35px;
  background: linear-gradient(
    45deg, 
    transparent, 
    rgba(255,255,255,0.4), 
    transparent
  );
  border-radius: 50%;
  transform: rotate(-20deg);
  animation: helmet-gleam 4s ease-in-out infinite;
}

@keyframes helmet-gleam {
  0%, 100% {
    opacity: 0.3;
    transform: rotate(-20deg) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: rotate(-20deg) scale(1.1);
  }
}

/* Enhanced Title Typography */
.app-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  margin: var(--space-xl) 0 var(--space-md);
  color: var(--color-primary);
  font-weight: var(--font-weight-extrabold);
  text-shadow: 
    0 0 10px rgba(var(--color-primary-rgb), 0.8),
    0 0 20px rgba(var(--color-primary-rgb), 0.6),
    0 0 40px rgba(var(--color-primary-rgb), 0.4),
    0 4px 8px rgba(0, 0, 0, 0.8);
  animation: title-pulse 4s ease-in-out infinite alternate;
  letter-spacing: 0.05em;
  line-height: 1.1;
}

@keyframes title-pulse {
  0% {
    text-shadow: 
      0 0 10px rgba(var(--color-primary-rgb), 0.8),
      0 0 20px rgba(var(--color-primary-rgb), 0.6),
      0 0 40px rgba(var(--color-primary-rgb), 0.4),
      0 4px 8px rgba(0, 0, 0, 0.8);
    transform: scale(1);
  }
  100% {
    text-shadow: 
      0 0 20px rgba(var(--color-primary-rgb), 1),
      0 0 30px rgba(var(--color-primary-rgb), 0.8),
      0 0 60px rgba(var(--color-primary-rgb), 0.6),
      0 6px 12px rgba(0, 0, 0, 0.9);
    transform: scale(1.02);
  }
}

.app-subtitle {
  font-style: italic;
  color: var(--color-text-secondary);
  font-size: clamp(1rem, 2.5vw, 1.3rem);
  margin: 0;
  font-weight: var(--font-weight-light);
  letter-spacing: 0.02em;
  opacity: 0.9;
  transition: all var(--transition-normal);
}

.app-subtitle:hover {
  color: var(--color-text-primary);
  opacity: 1;
}

/* Modern Main Content Layout */
.app-main {
  position: relative;
  z-index: 10;
  padding: 0 var(--space-md);
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

/* Enhanced Footer */
.app-footer {
  text-align: center;
  padding: var(--space-3xl) var(--space-md);
  color: var(--color-text-muted);
  font-style: italic;
  position: relative;
  z-index: 10;
  font-size: 0.95rem;
  font-weight: var(--font-weight-light);
}

.app-footer p {
  margin: 0;
  transition: all var(--transition-normal);
}

.app-footer:hover p {
  color: var(--color-text-secondary);
  transform: scale(1.05);
}

/* Responsive Design */
@media (max-width: 768px) {
  .app-header {
    padding: var(--space-2xl) var(--space-md);
  }
  
  .vader-helmet {
    width: 80px;
    height: 80px;
  }
  
  .app-main {
    padding: 0 var(--space-sm);
  }
}

@media (max-width: 480px) {
  .app-header {
    padding: var(--space-xl) var(--space-sm);
  }
  
  .vader-helmet {
    width: 70px;
    height: 70px;
  }
}

/* Performance optimizations */
.vader-helmet,
.helmet-shine,
.app-title {
  will-change: transform;
}

@media (prefers-reduced-motion: reduce) {
  .stars, .stars2, .stars3 {
    animation: none;
  }
  
  .helmet-shine {
    animation: none;
  }
  
  .app-title {
    animation: none;
  }
  
  .vader-helmet:hover {
    transform: none;
  }
}
</style>