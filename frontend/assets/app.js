const STORAGE_KEY = "pbnAutomationSettings";

const elements = {
  apiUrl: document.getElementById("api-url"),
  apiToken: document.getElementById("api-token"),
  saveSettings: document.getElementById("save-settings"),
  refreshSites: document.getElementById("refresh-sites"),
  refreshTasks: document.getElementById("refresh-tasks"),
  sitesTableBody: document.querySelector("#sites-table tbody"),
  tasksTableBody: document.querySelector("#tasks-table tbody"),
  taskForm: document.getElementById("task-form"),
};

const state = {
  settings: {
    apiUrl: "http://localhost:8000",
    apiToken: "",
  },
};

function loadSettings() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (raw) {
    state.settings = JSON.parse(raw);
    elements.apiUrl.value = state.settings.apiUrl;
    elements.apiToken.value = state.settings.apiToken;
  }
}

function saveSettings() {
  state.settings.apiUrl = elements.apiUrl.value.trim();
  state.settings.apiToken = elements.apiToken.value.trim();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.settings));
  alert("Settings saved");
}

async function fetchJSON(path, options = {}) {
  const { apiUrl, apiToken } = state.settings;
  const headers = options.headers || {};
  headers["Content-Type"] = "application/json";
  headers["Authorization"] = `Bearer ${apiToken}`;
  const response = await fetch(`${apiUrl}${path}`, { ...options, headers });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

async function loadSites() {
  try {
    const data = await fetchJSON("/sites/");
    elements.sitesTableBody.innerHTML = data
      .map(
        (site) => `
        <tr>
          <td>${site.id}</td>
          <td>${site.name}</td>
          <td>${site.domain}</td>
          <td>${site.ux_block_id}</td>
        </tr>
      `
      )
      .join("");
  } catch (error) {
    console.error(error);
    alert("Failed to load sites");
  }
}

async function loadTasks() {
  try {
    const data = await fetchJSON("/tasks/");
    elements.tasksTableBody.innerHTML = data
      .map((task) => {
        const statusClass = `status-pill ${task.status}`;
        return `
          <tr>
            <td>${task.id}</td>
            <td>${task.site_id}</td>
            <td>${task.anchor_text}</td>
            <td><span class="${statusClass}">${task.status}</span></td>
            <td>${new Date(task.updated_at).toLocaleString()}</td>
            <td><button data-task="${task.id}" class="trigger-btn">Run</button></td>
          </tr>
        `;
      })
      .join("");
    document.querySelectorAll(".trigger-btn").forEach((btn) =>
      btn.addEventListener("click", () => triggerTask(btn.dataset.task))
    );
  } catch (error) {
    console.error(error);
    alert("Failed to load tasks");
  }
}

async function triggerTask(taskId) {
  try {
    await fetchJSON("/tasks/trigger", {
      method: "POST",
      body: JSON.stringify({ task_id: Number(taskId) }),
    });
    await loadTasks();
  } catch (error) {
    console.error(error);
    alert("Failed to trigger task\n" + error.message);
  }
}

elements.taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const payload = Object.fromEntries(formData.entries());
  payload.site_id = Number(payload.site_id);
  try {
    await fetchJSON("/tasks/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    event.target.reset();
    await loadTasks();
  } catch (error) {
    alert("Failed to create task\n" + error.message);
  }
});

elements.saveSettings.addEventListener("click", saveSettings);
elements.refreshSites.addEventListener("click", loadSites);
elements.refreshTasks.addEventListener("click", loadTasks);

loadSettings();
loadSites();
loadTasks();
