<template>
  <section>
    <PageHeader eyebrow="AI Skills Center" title="AI工具中心" description="一个账号，使用全部AI能力。" />
    <div class="page-toolbar"><div class="tabs"><button v-for="item in categories" :key="item" :class="{ active: filter === item }" @click="filter = item; loadTools()">{{ item }}</button></div><button class="primary-btn" @click="openDrawer()">新增AI工具</button></div>
    <div v-if="errorMessage" class="form-error">{{ errorMessage }}</div>
    <div class="tool-grid">
      <article v-for="tool in visible" :key="tool.id" class="tool-card skill-card">
        <div class="tool-icon">{{ tool.icon || tool.name?.slice(0, 1) || "技" }}</div>
        <div><strong>{{ tool.name }}</strong><small>{{ tool.nameEn || tool.code }}</small></div>
        <p>{{ tool.description || "" }}</p><div class="tool-meta"><span>{{ tool.category }}</span><span>{{ tool.callCount || 0 }} 次调用</span></div>
        <div class="skill-card-actions"><template v-if="!tool.type"><button class="ghost-btn" @click="openDrawer(tool)">编辑</button><button class="danger-btn" @click="removeTool(tool)">删除</button></template><button class="primary-btn" @click="openRun(tool)">{{ tool.type ? "立即生成" : "立即使用" }}</button></div>
      </article>
      <div v-if="!visible.length" class="empty-state">暂无AI工具</div>
    </div>

    <div v-if="activeTool" class="modal-backdrop skill-modal-backdrop">
      <div class="skill-run-modal">
        <button class="icon-btn skill-close" @click="activeTool = null">×</button><h2>{{ activeTool.name }}</h2><p>{{ activeTool.nameEn || activeTool.code }} · {{ activeTool.description || "" }}</p>
        <label>使用模型<select v-model.number="runForm.modelConfigId"><option v-for="model in chatModels" :key="model.id" :value="model.id">{{ model.displayName }} · {{ model.providerName }}</option></select></label>
        <label>任务简报<textarea v-model.trim="runForm.task" required placeholder="例如：为海南椰子零食生成TikTok短视频脚本和英文Listing"></textarea></label>
        <div v-if="runError" class="form-error">{{ runError }}</div><button class="primary-btn full" :disabled="running" @click="runTool">{{ running ? "Running..." : "Run tool" }}</button>
        <h3>RECENT OUTPUTS</h3><div class="skill-record-list"><article v-for="record in activeTool.recentRecords || []" :key="record.id" class="skill-record"><h4>{{ record.title }}</h4><time>{{ record.createdAt }}</time><p>目标：{{ record.target || "-" }}</p><p>建议动作：{{ record.suggestedAction || "-" }}</p><p>交付物：{{ record.deliverables || "-" }}</p></article><div v-if="!(activeTool.recentRecords || []).length" class="empty-state">暂无历史输出</div></div>
      </div>
    </div>

    <!-- ── Media demo modal (text-to-image / text-to-video) ── -->
    <div v-if="mediaOpen" class="modal-backdrop skill-modal-backdrop" @click.self="closeMediaModal">
      <div class="skill-run-modal media-demo-modal">
        <button class="icon-btn skill-close" @click="closeMediaModal">×</button>
        <h2>{{ mediaType === "image" ? "AI文生图" : "AI文生视频" }}</h2>
        <p>{{ mediaType === "image" ? "输入提示词，选择尺寸和风格，AI 为你生成图片。" : "输入提示词，选择比例和时长，AI 为你生成视频。" }}</p>

        <label>提示词<textarea v-model.trim="mediaForm.prompt" required :placeholder="mediaType === 'image' ? '例如：A futuristic city skyline at sunset, cyberpunk style, 8K' : '例如：A drone flyover of a tropical beach resort at golden hour'"></textarea></label>

        <template v-if="mediaType === 'image'">
          <div class="media-form-row">
            <label>尺寸<select v-model="mediaForm.size"><option>1024x1024</option><option>1792x1024</option><option>1024x1792</option></select></label>
            <label>风格<select v-model="mediaForm.style"><option>natural</option><option>vivid</option></select></label>
            <label>数量<select v-model.number="mediaForm.quantity"><option>1</option><option>2</option><option>3</option><option>4</option></select></label>
          </div>
        </template>
        <template v-else>
          <div class="media-form-row">
            <label>比例<select v-model="mediaForm.ratio"><option>16:9</option><option>9:16</option><option>1:1</option></select></label>
            <label>时长(秒)<input v-model.number="mediaForm.duration" type="number" min="3" max="30"></label>
            <label>风格<select v-model="mediaForm.style"><option>cinematic</option><option>anime</option><option>realistic</option></select></label>
          </div>
        </template>

        <div v-if="mediaError" class="form-error">{{ mediaError }}</div>

        <!-- Loading -->
        <div v-if="mediaLoading" class="media-loading">
          <span class="media-spinner"></span>
          <span>{{ mediaType === "video" ? "正在创建生成任务..." : "正在生成..." }}</span>
        </div>

        <!-- Video polling status -->
        <div v-if="mediaType === 'video' && mediaTaskStatus && !mediaLoading && !mediaResults.length" class="media-status">
          <span class="media-spinner"></span>
          <span>{{ mediaTaskStatus === "pending" ? "任务排队中..." : mediaTaskStatus === "running" ? "视频生成中，请稍候..." : mediaTaskStatus === "failed" ? "生成失败" : mediaTaskStatus }}</span>
        </div>

        <!-- Results -->
        <template v-if="mediaResults.length">
          <div v-if="mediaType === 'image'" class="media-image-grid">
            <div v-for="(r, i) in mediaResults" :key="i" class="media-image-card">
              <img :src="r.url" :alt="mediaForm.prompt" loading="lazy">
              <a :href="r.url" :download="r.filename" class="primary-btn tiny-btn">下载</a>
            </div>
          </div>
          <div v-else class="media-video-result">
            <video :src="mediaResults[0].url" controls style="width:100%;max-height:360px;border-radius:8px"></video>
            <a :href="mediaResults[0].url" :download="mediaResults[0].filename" class="primary-btn">下载视频</a>
          </div>
        </template>

        <button v-if="!mediaLoading && (!mediaTaskStatus || mediaTaskStatus === 'failed')" class="primary-btn full" :disabled="mediaLoading" @click="runMediaGenerate">{{ mediaType === "image" ? "生成图片" : "创建视频任务" }}</button>

        <!-- Recent history -->
        <h3>最近生成记录</h3>
        <div class="media-history-list" v-if="recentMediaHistory.length">
          <article v-for="(item, i) in recentMediaHistory" :key="i" class="media-history-item">
            <span class="media-history-type">{{ item.type === "image" ? "🖼" : "🎬" }}</span>
            <span class="media-history-prompt">{{ item.prompt }}</span>
            <a :href="item.url" :download="item.filename || ''" class="ghost-btn tiny-btn">下载</a>
          </article>
        </div>
        <div v-else class="empty-state">暂无生成记录</div>
      </div>
    </div>

    <div v-if="drawerOpen" class="drawer-backdrop model-config-backdrop">
      <aside class="drawer model-config-drawer">
        <div class="drawer-head"><div><h2>{{ form.id ? "编辑AI工具" : "新增AI工具" }}</h2><span>Prompt Skill</span></div><button class="icon-btn" @click="closeDrawer">×</button></div>
        <div class="drawer-form">
          <label>技能名称<input v-model.trim="form.name"></label><label>英文名称<input v-model.trim="form.nameEn"></label><label>唯一编码<input v-model.trim="form.code"></label><label>分类<input v-model.trim="form.category"></label><label>图标<input v-model.trim="form.icon" maxlength="10"></label>
          <label>使用 Chat 模型<select v-model.number="form.modelConfigId"><option v-for="model in chatModels" :key="model.id" :value="model.id">{{ model.displayName }} · {{ model.providerName }}</option></select></label>
          <label>技能说明<textarea v-model.trim="form.description"></textarea></label><label>Prompt 模板<textarea v-model.trim="form.promptTemplate"></textarea></label><label>排序<input v-model.number="form.sortOrder" type="number"></label>
          <label class="drawer-check"><input v-model="form.enabled" type="checkbox"> 启用</label><label class="drawer-check"><input v-model="form.isSystem" type="checkbox"> 系统内置</label><div v-if="formError" class="form-error">{{ formError }}</div>
        </div><button class="primary-btn full" @click="saveTool">{{ form.id ? "确认保存" : "确认新增" }}</button>
      </aside>
    </div>
  </section>
</template>
<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from "vue";
import PageHeader from "../../../components/PageHeader.vue";
import { demoMediaApi, toolsApi } from "./api/index.js";
const categories = ["全部", "内容生成", "数据分析", "营销投放", "客户管理", "运营工具", "合规工具", "视觉生成"];
const tools = ref([]), chatModels = ref([]), filter = ref("全部"), activeTool = ref(null);
const drawerOpen = ref(false), running = ref(false), errorMessage = ref(""), runError = ref(""), formError = ref("");
const runForm = reactive({ task: "", modelConfigId: null });

// ── Demo media tools (static, not in database) ──
const DEMO_MEDIA_TOOLS = [
  { id: "demo-t2i", name: "AI文生图", nameEn: "Text to Image", code: "demo-text-to-image", category: "视觉生成",
    description: "输入提示词，AI 为你生成高质量图片。支持多种尺寸和风格。", icon: "🖼",
    type: "media-image", callCount: 0, recentRecords: [] },
  { id: "demo-t2v", name: "AI文生视频", nameEn: "Text to Video", code: "demo-text-to-video", category: "视觉生成",
    description: "输入提示词，AI 为你生成短视频。支持多种比例和时长。", icon: "🎬",
    type: "media-video", callCount: 0, recentRecords: [] }
];

// ── Media modal state ──
const mediaOpen = ref(false);
const mediaType = ref(""); // "image" | "video"
const mediaForm = reactive({ prompt: "", size: "1024x1024", style: "natural", quantity: 1, ratio: "16:9", duration: 5 });
const mediaLoading = ref(false);
const mediaError = ref("");
const mediaResults = ref([]); // image: [{url, filename}]; video: single result
const mediaTaskId = ref("");
const mediaTaskStatus = ref(""); // pending | running | completed | failed
const mediaPollTimer = ref(null);

// ── localStorage history ──
const MEDIA_HISTORY_KEY = "yapmitai-demo-media-history";
function loadMediaHistory() { try { return JSON.parse(localStorage.getItem(MEDIA_HISTORY_KEY) || "[]"); } catch { return []; } }
function saveMediaHistory(entry) { const list = [entry, ...loadMediaHistory()].slice(0, 10); localStorage.setItem(MEDIA_HISTORY_KEY, JSON.stringify(list)); }
const emptyForm = () => ({ id: null, name: "", nameEn: "", code: "", category: "内容生成", description: "", icon: "技", modelConfigId: null, promptTemplate: "请基于任务简报完成该AI工具任务：{{task}}", enabled: true, isSystem: false, sortOrder: 100 });
const form = reactive(emptyForm());
const visible = computed(() => {
  const all = [...tools.value, ...DEMO_MEDIA_TOOLS];
  return filter.value === "全部" ? all : all.filter((item) => item.category === filter.value);
});
async function loadTools() { try { const response = await toolsApi.list(filter.value === "全部" ? {} : { category: filter.value }); tools.value = response.data || []; errorMessage.value = ""; } catch (error) { errorMessage.value = error.message; } }
async function loadModels() { try { const response = await toolsApi.chatModels(); chatModels.value = response.data || []; } catch (error) { errorMessage.value = error.message; } }
function openRun(tool) {
  if (tool.type === "media-image") { openMediaModal("image"); return; }
  if (tool.type === "media-video") { openMediaModal("video"); return; }
  activeTool.value = tool; runForm.task = ""; runForm.modelConfigId = tool.modelConfigId || chatModels.value[0]?.id || null; runError.value = "";
}

// ── Media modal ──
function openMediaModal(type) {
  mediaOpen.value = true; mediaType.value = type; mediaError.value = ""; mediaResults.value = []; mediaTaskId.value = ""; mediaTaskStatus.value = "";
  Object.assign(mediaForm, { prompt: "", size: "1024x1024", style: "natural", quantity: 1, ratio: "16:9", duration: 5 });
  if (mediaPollTimer.value) { clearInterval(mediaPollTimer.value); mediaPollTimer.value = null; }
}
function closeMediaModal() { if (mediaPollTimer.value) clearInterval(mediaPollTimer.value); mediaOpen.value = false; }

async function runMediaGenerate() {
  if (!mediaForm.prompt) { mediaError.value = "请填写提示词。"; return; }
  mediaLoading.value = true; mediaError.value = "";
  try {
    if (mediaType.value === "image") {
      const resp = await demoMediaApi.textToImage({ prompt: mediaForm.prompt, size: mediaForm.size, style: mediaForm.style, quantity: mediaForm.quantity });
      mediaResults.value = resp.data || [];
      mediaResults.value.forEach(r => saveMediaHistory({ type: "image", prompt: mediaForm.prompt, url: r.url, filename: r.filename, createdAt: new Date().toISOString() }));
    } else {
      const resp = await demoMediaApi.textToVideo({ prompt: mediaForm.prompt, ratio: mediaForm.ratio, duration: mediaForm.duration, style: mediaForm.style });
      mediaTaskId.value = resp.data.task_id;
      mediaTaskStatus.value = resp.data.status;
      startVideoPolling();
    }
  } catch (e) { mediaError.value = e.message; }
  finally { mediaLoading.value = false; }
}

function startVideoPolling() {
  mediaPollTimer.value = setInterval(async () => {
    try {
      const resp = await demoMediaApi.getVideoStatus(mediaTaskId.value);
      mediaTaskStatus.value = resp.data.status;
      if (resp.data.status === "completed") {
        clearInterval(mediaPollTimer.value); mediaPollTimer.value = null;
        mediaResults.value = [{ url: resp.data.url, filename: resp.data.filename }];
        saveMediaHistory({ type: "video", prompt: mediaForm.prompt, url: resp.data.url, filename: resp.data.filename, createdAt: new Date().toISOString() });
      } else if (resp.data.status === "failed") {
        clearInterval(mediaPollTimer.value); mediaPollTimer.value = null;
        mediaError.value = resp.data.error || "视频生成失败";
      }
    } catch (e) { mediaError.value = e.message; clearInterval(mediaPollTimer.value); mediaPollTimer.value = null; }
  }, 3000);
}

onUnmounted(() => { if (mediaPollTimer.value) clearInterval(mediaPollTimer.value); });
const recentMediaHistory = ref(loadMediaHistory());
async function runTool() { if (!runForm.task) { runError.value = "请填写任务简报。"; return; } running.value = true; try { const response = await toolsApi.run(activeTool.value.id, { task: runForm.task, model_config_id: runForm.modelConfigId }); activeTool.value.recentRecords = [response.data, ...(activeTool.value.recentRecords || [])].slice(0, 3); activeTool.value.callCount = (activeTool.value.callCount || 0) + 1; } catch (error) { runError.value = error.message; } finally { running.value = false; } }
function openDrawer(tool = null) { Object.assign(form, emptyForm(), tool || {}, { modelConfigId: tool?.modelConfigId || chatModels.value[0]?.id || null }); drawerOpen.value = true; formError.value = ""; }
function closeDrawer() { if (window.confirm("退出后当前内容不会保存，确定退出吗？")) drawerOpen.value = false; }
function toolPayload() { return { name: form.name, name_en: form.nameEn || null, code: form.code, category: form.category, description: form.description || null, icon: form.icon || null, model_config_id: form.modelConfigId || null, prompt_template: form.promptTemplate, input_schema: { fields: [{ name: "task", label: "任务简报", type: "textarea" }] }, output_schema: { type: "object", fields: ["title", "target", "suggested_action", "deliverables"] }, enabled: form.enabled, is_system: form.isSystem, sort_order: form.sortOrder || 0 }; }
async function saveTool() { if (!form.name || !form.code || !form.category || !form.promptTemplate) { formError.value = "请填写技能名称、唯一编码、分类和 Prompt 模板。"; return; } try { form.id ? await toolsApi.update(form.id, toolPayload()) : await toolsApi.create(toolPayload()); drawerOpen.value = false; await loadTools(); } catch (error) { formError.value = error.message; } }
async function removeTool(tool) { if (!window.confirm(`确定删除“${tool.name}”吗？相关运行历史也会被删除。`)) return; try { await toolsApi.delete(tool.id); await loadTools(); } catch (error) { errorMessage.value = error.message; } }
onMounted(async () => { await loadModels(); await loadTools(); });
</script>
<style scoped></style>
