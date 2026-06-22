<template>
  <div v-if="open" class="modal-overlay open" @click="onOverlayClick">
    <div class="askme-modal" @click.stop>
      <div class="askme-header">
        <div class="askme-header-icon">💬</div>
        <div>
          <div class="askme-header-title">Ask Me — YAPMIT AI 知识问答</div>
          <div class="askme-header-sub">基于 YAPMIT 自建知识库 · 产品库 · 行业数据库 · yapmit.ai</div>
        </div>
        <button type="button" class="modal-close askme-close" @click="close">✕</button>
      </div>

      <div ref="messagesEl" class="askme-messages">
        <div class="msg ai">
          <div class="msg-avatar">🤖</div>
          <div class="msg-bubble">
            你好！我是 YAPMIT AI，可以回答关于品牌增长、跨境出海、导购文旅、招商引资的专业问题。<br><br>试着问我一个你最关心的问题吧 👇
          </div>
        </div>
        <div v-for="(message, index) in messages" :key="index" class="msg" :class="message.role">
          <div class="msg-avatar">{{ message.role === "ai" ? "🤖" : "👤" }}</div>
          <div class="msg-bubble" v-html="message.text"></div>
        </div>
        <div v-if="typing" class="msg ai">
          <div class="msg-avatar">🤖</div>
          <div class="msg-bubble">
            <div class="typing-dots"><span></span><span></span><span></span></div>
          </div>
        </div>
      </div>

      <div class="askme-input-area">
        <div class="askme-chips">
          <button v-for="chip in askMeChips" :key="chip" type="button" class="askme-chip" @click="sendChip(chip)">{{ chip }}</button>
        </div>
        <div class="askme-input-row">
          <textarea
            ref="inputEl"
            v-model="input"
            placeholder="问任何关于 YAPMIT AI OS 或行业场景的问题…"
            rows="1"
            @keydown.enter.exact.prevent="sendMsg"
            @input="resizeInput"
          ></textarea>
          <button type="button" class="askme-send" @click="sendMsg">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M13.5 8L2.5 2.5L5.5 8L2.5 13.5L13.5 8Z" fill="white" /></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { nextTick, ref, watch } from "vue";
import { askMeChips, getAskMeReply } from "./ask-me.js";

const props = defineProps({
  open: { type: Boolean, default: false }
});

const emit = defineEmits(["update:open"]);

const input = ref("");
const messages = ref([]);
const typing = ref(false);
const messagesEl = ref(null);
const inputEl = ref(null);

watch(
  () => props.open,
  (value) => {
    if (value) {
      nextTick(() => inputEl.value?.focus());
    }
  }
);

function close() {
  emit("update:open", false);
}

function onOverlayClick(event) {
  if (event.target.classList.contains("modal-overlay")) close();
}

function resizeInput(event) {
  const el = event.target;
  el.style.height = "auto";
  el.style.height = `${el.scrollHeight}px`;
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
  });
}

function sendChip(text) {
  input.value = text;
  sendMsg();
}

function sendMsg() {
  const text = input.value.trim();
  if (!text || typing.value) return;

  messages.value.push({ role: "user", text });
  input.value = "";
  if (inputEl.value) inputEl.value.style.height = "auto";
  typing.value = true;
  scrollToBottom();

  window.setTimeout(() => {
    typing.value = false;
    messages.value.push({ role: "ai", text: getAskMeReply(text) });
    scrollToBottom();
  }, 900 + Math.random() * 600);
}
</script>
