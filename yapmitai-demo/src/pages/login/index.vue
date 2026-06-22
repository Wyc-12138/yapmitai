<template>
  <div class="yapmit-login">
    <div class="card">
      <div class="logo-row">
        <div class="logo-icon">悦</div>
        <div>
          <div class="logo-name">悦普AI产业OS</div>
          <div class="logo-sub">YAPMIT · Enterprise AI Operating System</div>
        </div>
      </div>

      <div v-if="!success">
        <div class="form-eyebrow">Enterprise Login · 企业登录</div>
        <div class="form-title">欢迎回来</div>
        <div class="form-sub">登录你的企业 AI 控制台，开始今天的 AI 工作</div>

        <form @submit.prevent="doLogin">
          <div class="field">
            <label>企业账号 / 手机号</label>
            <div class="field-wrap">
              <span class="field-icon">👤</span>
              <input
                v-model="username"
                type="text"
                placeholder="请输入企业账号或手机号"
                :class="{ err: errors.username }"
                @input="errors.username = false"
              />
            </div>
            <div v-if="errors.username" class="err-msg">请输入账号</div>
          </div>

          <div class="field">
            <label>登录密码</label>
            <div class="field-wrap">
              <span class="field-icon">🔒</span>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码"
                :class="{ err: errors.password }"
                @input="errors.password = false"
              />
              <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                {{ showPassword ? "🙈" : "👁" }}
              </button>
            </div>
            <div v-if="errors.password" class="err-msg">请输入密码</div>
          </div>

          <div class="field">
            <label>企业识别码 <span style="color: var(--text3); font-size: 11px">选填，多企业账号必填</span></label>
            <div class="field-wrap">
              <span class="field-icon">🏢</span>
              <input v-model="corpId" type="text" placeholder="如 YP-2024-001" style="padding-right: 70px" />
              <span class="corp-badge">CORP ID</span>
            </div>
          </div>

          <div class="aux-row">
            <label class="remember">
              <input v-model="remember" type="checkbox" />
              记住登录状态（7天）
            </label>
            <button type="button" class="forgot">忘记密码？</button>
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            <span v-if="loading" class="spin">⟳</span>
            <span v-else>⚡</span>
            <span>{{ loading ? "登录中…" : "登录企业控制台" }}</span>
          </button>
        </form>

        <div class="divider">其他登录方式</div>
        <div class="alt-row">
          <button type="button" class="alt-btn">💬 微信扫码登录</button>
          <button type="button" class="alt-btn">🔗 SSO 单点登录</button>
        </div>

        <div class="reg-hint">还没有企业账号？<a href="#">申请开通 →</a></div>
      </div>

      <div v-else class="success-wrap">
        <div class="success-icon">✓</div>
        <div class="success-title">登录成功</div>
        <div class="success-sub">正在跳转到你的 AI 控制台…</div>
        <div class="prog-bar"><div class="prog-fill"></div></div>
      </div>

      <div class="sec-bar">
        <div class="sec-dot"></div>
        SSL 加密传输 · 数据安全保障 · yapmit.ai
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import "./login.css";

const router = useRouter();

const username = ref("");
const password = ref("");
const corpId = ref("");
const remember = ref(false);
const showPassword = ref(false);
const loading = ref(false);
const success = ref(false);
const errors = reactive({ username: false, password: false });

function doLogin() {
  errors.username = !username.value.trim();
  errors.password = !password.value.trim();
  if (errors.username || errors.password) return;

  loading.value = true;
  window.setTimeout(() => {
    loading.value = false;
    success.value = true;
    window.setTimeout(() => {
      router.push("/enterprise/dashboard");
    }, 2000);
  }, 1300);
}
</script>
