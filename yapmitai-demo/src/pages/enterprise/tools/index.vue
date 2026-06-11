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
        <div class="skill-card-actions"><button class="ghost-btn" @click="openDrawer(tool)">编辑</button><button class="danger-btn" @click="removeTool(tool)">删除</button><button class="primary-btn" @click="openRun(tool)">立即使用</button></div>
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
import { computed, onMounted, reactive, ref } from "vue";
import PageHeader from "../../../components/PageHeader.vue";
import { toolsApi } from "./api/index.js";
const categories = ["全部", "内容生成", "数据分析", "营销投放", "客户管理", "运营工具", "合规工具"];
const tools = ref([]), chatModels = ref([]), filter = ref("全部"), activeTool = ref(null);
const drawerOpen = ref(false), running = ref(false), errorMessage = ref(""), runError = ref(""), formError = ref("");
const runForm = reactive({ task: "", modelConfigId: null });
const emptyForm = () => ({ id: null, name: "", nameEn: "", code: "", category: "内容生成", description: "", icon: "技", modelConfigId: null, promptTemplate: "请基于任务简报完成该AI工具任务：{{task}}", enabled: true, isSystem: false, sortOrder: 100 });
const form = reactive(emptyForm());
const visible = computed(() => filter.value === "全部" ? tools.value : tools.value.filter((item) => item.category === filter.value));
async function loadTools() { try { const response = await toolsApi.list(filter.value === "全部" ? {} : { category: filter.value }); tools.value = response.data || []; errorMessage.value = ""; } catch (error) { errorMessage.value = error.message; } }
async function loadModels() { try { const response = await toolsApi.chatModels(); chatModels.value = response.data || []; } catch (error) { errorMessage.value = error.message; } }
function openRun(tool) { activeTool.value = tool; runForm.task = ""; runForm.modelConfigId = tool.modelConfigId || chatModels.value[0]?.id || null; runError.value = ""; }
async function runTool() { if (!runForm.task) { runError.value = "请填写任务简报。"; return; } running.value = true; try { const response = await toolsApi.run(activeTool.value.id, { task: runForm.task, model_config_id: runForm.modelConfigId }); activeTool.value.recentRecords = [response.data, ...(activeTool.value.recentRecords || [])].slice(0, 3); activeTool.value.callCount = (activeTool.value.callCount || 0) + 1; } catch (error) { runError.value = error.message; } finally { running.value = false; } }
function openDrawer(tool = null) { Object.assign(form, emptyForm(), tool || {}, { modelConfigId: tool?.modelConfigId || chatModels.value[0]?.id || null }); drawerOpen.value = true; formError.value = ""; }
function closeDrawer() { if (window.confirm("退出后当前内容不会保存，确定退出吗？")) drawerOpen.value = false; }
function toolPayload() { return { name: form.name, name_en: form.nameEn || null, code: form.code, category: form.category, description: form.description || null, icon: form.icon || null, model_config_id: form.modelConfigId || null, prompt_template: form.promptTemplate, input_schema: { fields: [{ name: "task", label: "任务简报", type: "textarea" }] }, output_schema: { type: "object", fields: ["title", "target", "suggested_action", "deliverables"] }, enabled: form.enabled, is_system: form.isSystem, sort_order: form.sortOrder || 0 }; }
async function saveTool() { if (!form.name || !form.code || !form.category || !form.promptTemplate) { formError.value = "请填写技能名称、唯一编码、分类和 Prompt 模板。"; return; } try { form.id ? await toolsApi.update(form.id, toolPayload()) : await toolsApi.create(toolPayload()); drawerOpen.value = false; await loadTools(); } catch (error) { formError.value = error.message; } }
async function removeTool(tool) { if (!window.confirm(`确定删除“${tool.name}”吗？相关运行历史也会被删除。`)) return; try { await toolsApi.delete(tool.id); await loadTools(); } catch (error) { errorMessage.value = error.message; } }
onMounted(async () => { await loadModels(); await loadTools(); });
</script>
<style scoped></style>
