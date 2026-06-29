<template>
  <section class="inquiry-page">
    <PageHeader
      eyebrow="Inquiry History"
      title="历史询盘"
      :description="manageMode ? '勾选记录后可批量删除，点击「完成」退出管理。' : '查看已分析的询盘记录，点击行可回到详情。'"
    />

    <div class="inquiry-toolbar">
      <button class="ghost-btn" @click="router.push('/enterprise/inquiry')">返回询盘分析</button>
      <button class="ghost-btn" :disabled="loading || deleting" @click="loadHistory">刷新</button>
      <button
        v-if="!manageMode"
        class="ghost-btn"
        :disabled="loading || deleting || !items.length"
        @click="enterManageMode"
      >
        管理
      </button>
      <template v-else>
        <button class="ghost-btn" :disabled="deleting" @click="exitManageMode">完成</button>
        <button
          class="danger-btn"
          :disabled="loading || deleting || !selectedIds.length"
          @click="removeSelected"
        >
          {{ deleting ? "正在删除…" : `删除所选${selectedIds.length ? ` (${selectedIds.length})` : ""}` }}
        </button>
      </template>
    </div>

    <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

    <div class="inquiry-input-card" :class="{ 'inquiry-history-manage': manageMode }">
      <div class="table-wrap">
        <table class="inquiry-history-table">
          <thead>
            <tr>
              <th v-if="manageMode" class="inquiry-history-check">
                <input
                  type="checkbox"
                  :checked="allSelected"
                  :disabled="!items.length || loading || deleting"
                  @change="toggleSelectAll"
                >
              </th>
              <th>时间</th>
              <th>来源</th>
              <th>意图</th>
              <th>语言</th>
              <th>紧急度</th>
              <th>状态</th>
              <th>询盘摘要</th>
              <th v-if="manageMode">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in items"
              :key="item.id"
              :class="{ selected: manageMode && selectedIds.includes(item.id) }"
              @click="handleRowClick(item)"
            >
              <td v-if="manageMode" class="inquiry-history-check" @click.stop>
                <input
                  type="checkbox"
                  :checked="selectedIds.includes(item.id)"
                  :disabled="loading || deleting"
                  @change="toggleSelect(item.id)"
                >
              </td>
              <td>{{ formatDate(item.createdAt) }}</td>
              <td>{{ item.source }}</td>
              <td>{{ intentLabels[item.summary?.intent] || item.summary?.intent || "-" }}</td>
              <td>{{ item.summary?.language || "-" }}</td>
              <td>{{ item.summary?.urgency || "-" }}</td>
              <td>{{ item.status === "done" ? "完成" : item.status }}</td>
              <td>{{ item.summary?.briefSummary || truncate(item.inquiryText) }}</td>
              <td v-if="manageMode" @click.stop>
                <button
                  class="danger-btn tiny-btn"
                  :disabled="loading || deleting"
                  @click="removeOne(item)"
                >
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="!items.length && !loading">
              <td :colspan="manageMode ? 9 : 7">
                <div class="empty-state">暂无历史询盘，请先在分析页运行一次。</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import PageHeader from "../../../../components/PageHeader.vue";
import { inquiryApi } from "../api/index.js";
import { intentLabels } from "../samples.js";
import "../inquiry.css";

const router = useRouter();
const items = ref([]);
const selectedIds = ref([]);
const manageMode = ref(false);
const loading = ref(false);
const deleting = ref(false);
const errorMessage = ref("");

const allSelected = computed(
  () => items.value.length > 0 && selectedIds.value.length === items.value.length
);

function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}

function truncate(text) {
  if (!text) return "-";
  return text.length > 48 ? `${text.slice(0, 48)}…` : text;
}

function enterManageMode() {
  manageMode.value = true;
  selectedIds.value = [];
}

function exitManageMode() {
  manageMode.value = false;
  selectedIds.value = [];
}

function toggleSelect(id) {
  if (selectedIds.value.includes(id)) {
    selectedIds.value = selectedIds.value.filter((item) => item !== id);
    return;
  }
  selectedIds.value = [...selectedIds.value, id];
}

function toggleSelectAll(event) {
  selectedIds.value = event.target.checked ? items.value.map((item) => item.id) : [];
}

function handleRowClick(item) {
  if (manageMode.value) {
    toggleSelect(item.id);
    return;
  }
  openRecord(item.id);
}

async function loadHistory() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const response = await inquiryApi.listHistory();
    items.value = response.data?.items || [];
    selectedIds.value = selectedIds.value.filter((id) =>
      items.value.some((item) => item.id === id)
    );
    if (!items.value.length) {
      manageMode.value = false;
      selectedIds.value = [];
    }
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
}

function openRecord(id) {
  router.push({ path: "/enterprise/inquiry", query: { id } });
}

async function removeOne(item) {
  if (!window.confirm(`确定删除这条历史询盘吗？\n\n${truncate(item.inquiryText)}`)) return;
  deleting.value = true;
  errorMessage.value = "";
  try {
    await inquiryApi.deleteHistory(item.id);
    selectedIds.value = selectedIds.value.filter((id) => id !== item.id);
    await loadHistory();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    deleting.value = false;
  }
}

async function removeSelected() {
  if (!selectedIds.value.length) return;
  const count = selectedIds.value.length;
  if (!window.confirm(`确定删除选中的 ${count} 条历史询盘吗？此操作无法撤销。`)) return;

  deleting.value = true;
  errorMessage.value = "";
  try {
    await inquiryApi.deleteHistoryBatch(selectedIds.value);
    selectedIds.value = [];
    await loadHistory();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    deleting.value = false;
  }
}

onMounted(loadHistory);
</script>

<style scoped></style>
