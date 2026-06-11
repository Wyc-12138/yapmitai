<template>
  <section>
    <PageHeader eyebrow="Agent Gateway Config" title="Agent网关全局配置" description="统一管理外部Agent包、全局开关与连接测试。" />
    <div class="settings-grid">
      <AppPanel title="连接配置" subtitle="Connection">
        <label class="field-label">API Key</label><div class="input-row"><span>密</span><input :value="showKey ? 'yap_sk_live_demo_2026' : '••••••••••••••••••••'" readonly><button class="icon-btn" @click="showKey = !showKey">{{ showKey ? "隐" : "显" }}</button></div>
        <label class="field-label">网关地址</label><div class="input-row"><span>网</span><input value="https://gateway.yapmitai.com/api/v1" readonly></div>
        <label class="field-label">超时设置</label><div class="input-row"><span>时</span><input value="30s" readonly></div>
        <div class="switch-row"><div><strong>全局 Agent 总开关</strong><small>{{ globalEnabled ? "外部Agent优先，异常自动fallback" : "全部接口直接使用Mock fallback" }}</small></div><AppToggle v-model="globalEnabled" /></div>
        <button class="primary-btn full" @click="connected = true">连接测试</button><div v-if="connected" class="success-line">连接成功，延迟 128ms</div>
      </AppPanel>
      <AppPanel title="可用Agent包列表" subtitle="Available Agent Packages">
        <div class="agent-package-list"><div v-for="item in packages" :key="item.id" class="agent-package"><div><strong>{{ item.name }}</strong><span>{{ item.type }} · v{{ item.version }}</span></div><span class="status-badge" :class="item.enabled ? 'working' : 'offline'">{{ item.enabled ? "工作中" : "离线" }}</span><AppToggle v-model="item.enabled" /></div></div>
      </AppPanel>
    </div>
  </section>
</template>
<script setup>
import { reactive, ref, watch } from "vue";
import AppPanel from "../../../../components/AppPanel.vue";
import AppToggle from "../../../../components/AppToggle.vue";
import PageHeader from "../../../../components/PageHeader.vue";
const showKey = ref(false);
const connected = ref(false);
const globalEnabled = ref(JSON.parse(localStorage.getItem("agent-global-enabled") || "true"));
watch(globalEnabled, (value) => localStorage.setItem("agent-global-enabled", JSON.stringify(value)));
const packages = reactive([{ id: "creation-image", name: "文生图 Agent", type: "AI创作", version: "1.2.0", enabled: true }, { id: "creation-video", name: "文生视频 Agent", type: "AI创作", version: "1.0.8", enabled: true }, { id: "outreach-leads", name: "智能获客 Agent", type: "拓客", version: "2.1.1", enabled: true }, { id: "cs-personalwx", name: "个微客服 Agent", type: "客服", version: "1.4.3", enabled: false }, { id: "cs-corpwx", name: "企微客服 Agent", type: "客服", version: "1.5.0", enabled: true }, { id: "knowledge-rag", name: "RAG知识库 Agent", type: "知识库", version: "0.9.7", enabled: true }]);
</script>
<style scoped></style>
