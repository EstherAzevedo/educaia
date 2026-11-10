
<script setup lang="ts">
import { computed, ref } from 'vue'

// Tipos de tarefas que o EducaIA oferece
type StudyTask = 'summarize' | 'explain' | 'quiz'

// Opções disponíveis na interface
const tasks = [
  {
    id: 'summarize',
    title: 'Resumir',
    description: 'Principais ideias',
    icon: '📄',
  },
  {
    id: 'explain',
    title: 'Explicar',
    description: 'Entenda os conceitos',
    icon: '💡',
  },
  {
    id: 'quiz',
    title: 'Quiz',
    description: 'Teste seu conhecimento',
    icon: '✏️',
  },
] as const

// Estado: tarefa selecionada
const selectedTask = ref<StudyTask | null>(null)

// Estado: texto informado pelo usuário
const studyText = ref('')

// Valor calculado: quantidade de caracteres
const characterCount = computed(() => studyText.value.length)

// Verifica se o texto respeita os limites do backend
const isTextValid = computed(
  () => characterCount.value >= 20 && characterCount.value <= 12000,
)

// Verifica se o formulário pode ser enviado
const canGenerate = computed(
  () => selectedTask.value !== null && isTextValid.value,
)

// Seleciona uma tarefa
function selectTask(task: StudyTask) {
  selectedTask.value = task
}
</script>

<template>
  <div class="app-container">
    <header class="header">
      <a href="#" class="brand">
        <span class="brand-icon">✦</span>
        <span>EducaIA</span>
      </a>

      <span class="header-label">Seu assistente de estudos com IA</span>
    </header>

    <main class="main-content">
      <section class="hero">
        <span class="hero-tag">INTELIGÊNCIA ARTIFICIAL NA EDUCAÇÃO</span>

        <h1>
          Aprender ficou mais
          <span>inteligente.</span>
        </h1>

        <p>
          Transforme seus materiais em conhecimento.
          Resuma, compreenda e teste o que você aprendeu
          com a ajuda da inteligência artificial.
        </p>
      </section>

      <section class="study-card">
        <div class="card-heading">
          <h2>Vamos estudar?</h2>
          <p>Escolha como deseja trabalhar seu material.</p>
        </div>

        <div class="task-options">
          <button
            v-for="task in tasks"
            :key="task.id"
            type="button"
            class="task-option"
            :class="{ selected: selectedTask === task.id }"
            :aria-pressed="selectedTask === task.id"
            @click="selectTask(task.id)"
          >
            <span class="task-icon">{{ task.icon }}</span>
            <strong>{{ task.title }}</strong>
            <span>{{ task.description }}</span>
          </button>
        </div>

        <div class="input-section">
          <label for="study-text">Seu material de estudo</label>

          <textarea
            id="study-text"
            v-model="studyText"
            maxlength="12000"
            placeholder="Cole aqui o texto que deseja estudar..."
          ></textarea>

          <div class="input-footer">
            <span>Insira entre 20 e 12.000 caracteres.</span>
            <span>{{ characterCount }} / 12.000</span>
          </div>
        </div>

        <button
          class="generate-button"
          type="button"
          :disabled="!canGenerate"
        >
          Gerar conteúdo
          <span>✦</span>
        </button>
      </section>
    </main>

    <footer class="footer">
      Desenvolvido para tornar o aprendizado mais acessível.
      <span>EducaIA © 2026</span>
    </footer>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Inter, Arial, sans-serif;
  background: #f8f6fc;
  color: #29213b;
}

button,
textarea {
  font: inherit;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  width: 100%;
  min-height: 76px;
  padding: 0 8%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border-bottom: 1px solid #eee9f5;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #29213b;
  font-size: 22px;
  font-weight: 700;
  text-decoration: none;
}

.brand-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 11px;
  background: #e9ddff;
  color: #7c3aed;
  font-size: 22px;
}

.header-label {
  color: #827b91;
  font-size: 13px;
}

.main-content {
  width: 100%;
  max-width: 850px;
  margin: 0 auto;
  padding: 65px 24px 55px;
  flex: 1;
}

.hero {
  text-align: center;
  margin-bottom: 42px;
}

.hero-tag {
  display: inline-block;
  margin-bottom: 18px;
  color: #8055ce;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
}

.hero h1 {
  font-size: clamp(32px, 5vw, 46px);
  line-height: 1.15;
  letter-spacing: -1.5px;
}

.hero h1 span {
  color: #8b5cf6;
}

.hero p {
  max-width: 520px;
  margin: 16px auto 0;
  color: #777083;
  font-size: 15px;
  line-height: 1.7;
}

.study-card {
  padding: 32px;
  background: #ffffff;
  border: 1px solid #eee9f5;
  border-radius: 20px;
  box-shadow: 0 12px 40px rgba(69, 43, 110, 0.06);
}

.card-heading h2 {
  font-size: 21px;
}

.card-heading p {
  margin-top: 7px;
  color: #827b91;
  font-size: 13px;
}

.task-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin: 25px 0 30px;
}

.task-option {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 7px;
  padding: 17px;
  background: #ffffff;
  border: 1px solid #e9e3f0;
  border-radius: 12px;
  cursor: pointer;
  text-align: left;
  transition: 0.2s;
}

.task-option:hover {
  border-color: #a78bfa;
  background: #faf8ff;
}

.task-option.selected {
  border: 2px solid #8b5cf6;
  background: #f5f0ff;
  padding: 16px;
}

.task-option:focus-visible {
  outline: 3px solid rgba(139, 92, 246, 0.3);
  outline-offset: 3px;
}

.task-icon {
  margin-bottom: 5px;
  font-size: 22px;
}

.task-option strong {
  font-size: 14px;
}

.task-option > span:last-child {
  color: #898294;
  font-size: 12px;
  line-height: 1.4;
}

.input-section label {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
  font-weight: 600;
}

.input-section textarea {
  width: 100%;
  min-height: 155px;
  padding: 15px;
  resize: vertical;
  border: 1px solid #e6e0ed;
  border-radius: 12px;
  outline: none;
  font-size: 13px;
  line-height: 1.6;
}

.input-section textarea:focus {
  border-color: #a78bfa;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.input-section textarea::placeholder {
  color: #aaa4b4;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-top: 9px;
  color: #9992a3;
  font-size: 11px;
}

.generate-button {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 9px;
  margin-top: 24px;
  padding: 15px;
  border: none;
  border-radius: 11px;
  background: #8b5cf6;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.generate-button:disabled {
  background: #c9b8ed;
  cursor: not-allowed;
}

.generate-button:not(:disabled):hover {
  background: #7541df;
}

.footer {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  padding: 22px 8%;
  border-top: 1px solid #eee9f5;
  color: #918a9d;
  font-size: 11px;
}

@media (max-width: 600px) {
  .header {
    padding: 0 20px;
  }

  .header-label {
    display: none;
  }

  .main-content {
    padding: 45px 16px;
  }

  .study-card {
    padding: 22px 17px;
  }

  .task-options {
    gap: 7px;
  }

  .task-option {
    padding: 12px 9px;
  }

  .task-option.selected {
    padding: 11px 8px;
  }

  .task-option strong {
    font-size: 12px;
  }

  .task-option > span:last-child {
    font-size: 10px;
  }

  .footer {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
</style>
