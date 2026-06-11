<template>
  <section>
    <div class="page-title">
      <span class="eyebrow">Model Configurations</span>
      <h1>模型配置中心</h1>
      <p>统一管理 chat 与 embedding 模型，供智能体和本地 RAG 选择使用。</p>
    </div>

    <div class="page-toolbar">
      <div class="tabs">
        <button
          v-for="item in filters"
          :key="item"
          :class="{ active: filter === item }"
          @click="changeFilter(item)"
        >
          {{ item }}
        </button>
      </div>
      <button class="primary-btn" @click="openCreate">新增模型配置</button>
    </div>

    <div class="table-wrap model-config-table">
      <table>
        <thead>
          <tr>
            <th>模型</th><th>供应商</th><th>类型</th><th>API地址</th>
            <th>Key</th><th>能力</th><th>状态</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in models" :key="item.id">
            <td><strong>{{ item.displayName }}</strong><small>{{ item.modelCode }}</small></td>
            <td>{{ item.providerName }}<small>{{ item.providerCode }}</small></td>
            <td><span class="model-type-badge" :class="item.modelType">{{ item.modelType }}</span></td>
            <td>{{ item.apiBaseUrl }}</td>
            <td>{{ item.apiKeyLast4 ? `****${item.apiKeyLast4}` : "未配置" }}</td>
            <td v-if="item.modelType === 'embedding'">
              {{ item.maxInputTokens || "-" }} tokens
              <small v-if="item.dimension">{{ item.dimension }} 维</small>
            </td>
            <td v-else>
              {{ item.contextWindowTokens || "-" }} tokens
              <small v-if="item.maxOutputTokens">最大输出 {{ item.maxOutputTokens }}</small>
            </td>
            <td>{{ item.enabled ? "启用" : "停用" }}{{ item.isDefault ? " · 默认" : "" }}</td>
            <td>
              <div class="row-actions">
                <button class="tiny-btn" @click="openEdit(item)">编辑</button>
                <button class="danger-btn" @click="remove(item)">删除</button>
              </div>
            </td>
          </tr>
          <tr v-if="!loading && !models.length">
            <td colspan="8"><div class="empty-state">暂无模型配置</div></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="drawerOpen" class="drawer-backdrop model-config-backdrop">
      <aside class="drawer model-config-drawer">
        <div class="drawer-head">
          <div>
            <h2>{{ form.id ? "编辑模型配置" : "新增模型配置" }}</h2>
            <span>{{ form.id ? form.displayName : "Model Provider" }}</span>
          </div>
          <button class="icon-btn" @click="closeDrawer">×</button>
        </div>

        <div class="drawer-form">
          <label>供应商编码<input v-model.trim="form.providerCode"></label>
          <label>供应商名称<input v-model.trim="form.providerName"></label>
          <label>API 模型名<input v-model.trim="form.modelCode"></label>
          <label>页面展示名<input v-model.trim="form.displayName"></label>
          <label>模型类型
            <select v-model="form.modelType">
              <option value="chat">chat</option>
              <option value="embedding">embedding</option>
            </select>
          </label>
          <label>API 地址<input v-model.trim="form.apiBaseUrl"></label>
          <label>API Key
            <input
              v-model="form.apiKey"
              type="password"
              :placeholder="form.id && form.apiKeyLast4 ? `留空保持 ****${form.apiKeyLast4}` : '请输入 API Key'"
            >
          </label>

          <div v-if="form.modelType === 'embedding'" class="model-specific-fields">
            <label>输出向量维度<input v-model.number="form.dimension" type="number" min="1" placeholder="例如 1536"></label>
            <label>单段文本最大输入 Token<input v-model.number="form.maxInputTokens" type="number" min="1" placeholder="例如 8191"></label>
          </div>

          <div v-else class="model-specific-fields">
            <label>上下文窗口 Token<input v-model.number="form.contextWindowTokens" type="number" min="1" placeholder="输入与输出合计，例如 128000"></label>
            <label>单次最大输出 Token<input v-model.number="form.maxOutputTokens" type="number" min="1" placeholder="例如 4096"></label>
            <label>默认生成温度<input v-model.number="form.defaultTemperature" type="number" min="0" max="2" step="0.1"></label>
          </div>

          <label>备注<textarea v-model.trim="form.remark"></textarea></label>
          <label class="drawer-check"><input v-model="form.enabled" type="checkbox"> 启用</label>
          <label class="drawer-check"><input v-model="form.isDefault" type="checkbox"> 设为该类型默认模型</label>
          <div v-if="errorMessage" class="form-error">{{ errorMessage }}</div>
        </div>
        <button class="primary-btn full model-config-submit" :disabled="saving" @click="save">
          {{ saving ? "正在保存..." : form.id ? "确认保存" : "确认新增" }}
        </button>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import {
  createModelConfig,
  deleteModelConfig,
  getModelConfigs,
  updateModelConfig
} from "./api/index.js";

const filters = ["全部", "chat", "embedding"];
const models = ref([]);
const filter = ref("全部");
const loading = ref(false);
const saving = ref(false);
const drawerOpen = ref(false);
const errorMessage = ref("");

const defaults = () => ({
  id: null,
  providerCode: "openai",
  providerName: "OpenAI",
  modelCode: "",
  displayName: "",
  modelType: "chat",
  apiBaseUrl: "https://api.openai.com/v1",
  apiKey: "",
  apiKeyLast4: "",
  dimension: null,
  maxInputTokens: null,
  contextWindowTokens: null,
  maxOutputTokens: null,
  defaultTemperature: 0.2,
  enabled: true,
  isDefault: false,
  remark: ""
});

const form = reactive(defaults());

function resetForm(value = defaults()) {
  Object.assign(form, defaults(), value, { apiKey: "" });
}

async function loadModels() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const params = filter.value === "全部" ? {} : { model_type: filter.value };
    const response = await getModelConfigs(params);
    models.value = response.data || [];
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
}

function changeFilter(value) {
  filter.value = value;
  loadModels();
}

function openCreate() {
  resetForm();
  errorMessage.value = "";
  drawerOpen.value = true;
}

function openEdit(item) {
  resetForm(item);
  errorMessage.value = "";
  drawerOpen.value = true;
}

function closeDrawer() {
  if (!window.confirm("退出后当前内容不会保存，确定退出吗？")) return;
  drawerOpen.value = false;
}

function payload() {
  const common = {
    provider_code: form.providerCode,
    provider_name: form.providerName,
    model_code: form.modelCode,
    display_name: form.displayName,
    model_type: form.modelType,
    api_base_url: form.apiBaseUrl,
    api_key: form.apiKey,
    enabled: form.enabled,
    is_default: form.isDefault,
    remark: form.remark || null
  };
  if (!form.apiKey && form.id) delete common.api_key;
  return form.modelType === "embedding"
    ? { ...common, dimension: form.dimension, max_input_tokens: form.maxInputTokens }
    : {
        ...common,
        context_window_tokens: form.contextWindowTokens,
        max_output_tokens: form.maxOutputTokens,
        default_temperature: form.defaultTemperature
      };
}

async function save() {
  if (!form.providerCode || !form.providerName || !form.modelCode || !form.displayName || !form.apiBaseUrl) {
    errorMessage.value = "请填写供应商、模型名、展示名和 API 地址。";
    return;
  }
  saving.value = true;
  try {
    form.id ? await updateModelConfig(form.id, payload()) : await createModelConfig(payload());
    drawerOpen.value = false;
    await loadModels();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    saving.value = false;
  }
}

async function remove(item) {
  if (!window.confirm(`确定删除模型配置“${item.displayName || item.modelCode}”吗？此操作无法撤销。`)) return;
  try {
    await deleteModelConfig(item.id);
    await loadModels();
  } catch (error) {
    errorMessage.value = error.message;
  }
}

onMounted(loadModels);
</script>

<style scoped>
</style>
