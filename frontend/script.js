let publicData = {};

function init() {
  const tocEl = document.getElementById("toc");
  const container = document.getElementById("markdownContainer");
  const titleEl = document.getElementById("title");
  const timestampEl = document.getElementById("timestamp");
  const originalLink = document.getElementById("originalLink");
  const tabsEl = document.getElementById("versionTabs");

  let selectedEntry = null;

  fetch('./toc_updated.json')
    .then(res => res.json())
    .then(data => {
      data.forEach((entry, i) => {
        const li = document.createElement("li");
        li.textContent = entry.title;
        li.className = `pl-${(entry.level ?? 1) * 2} cursor-pointer text-blue-600 hover:underline`;
        li.onclick = () => {
          selectedEntry = entry;
          titleEl.textContent = entry.title;
          timestampEl.textContent = entry.timestamp ? `Last scraped: ${entry.timestamp}` : "";
          originalLink.href = entry.url ?? "#";
          originalLink.style.display = entry.url ? "inline" : "none";
          renderTabs(entry);
        };
        tocEl.appendChild(li);
      });
    });

  function renderTabs(entry) {
    tabsEl.innerHTML = "";
    container.innerHTML = "";
    const versions = entry.versions || {};
    const versionNames = Object.keys(versions);

    versionNames.forEach((ver, idx) => {
      const tab = document.createElement("button");
      tab.textContent = ver === "default" ? "Default" : ver;
      tab.className = "tab px-3 py-1 rounded bg-gray-100 hover:bg-gray-200 text-sm";
      if (idx === 0) tab.classList.add("active");

      tab.addEventListener("click", () => {
        setActiveTab(tab);
        renderMarkdown(versions[ver]);
      });

      tabsEl.appendChild(tab);
    });

    // const apiTab = document.createElement("button");
    // apiTab.textContent = "API Reference";
    // apiTab.className = "tab px-3 py-1 rounded bg-gray-100 hover:bg-gray-200 text-sm";
    // apiTab.addEventListener("click", () => {
    //   setActiveTab(apiTab);
    //   renderAPIReference();
    // });
    // tabsEl.appendChild(apiTab);

    renderMarkdown(versions["default"] ?? Object.values(versions)[0] ?? "(No content)");
  }

  function setActiveTab(selected) {
    tabsEl.querySelectorAll("button").forEach(btn => {
      btn.classList.remove("bg-white", "font-bold", "border-b-2", "border-blue-500");
      btn.classList.add("bg-gray-100");
    });
    selected.classList.add("bg-white", "font-bold", "border-b-2", "border-blue-500");
    selected.classList.remove("bg-gray-100");
  }

  function renderMarkdown(markdownText) {
    if (!window.marked) {
      container.textContent = "Error: 'marked' library not loaded.";
      return;
    }
    container.innerHTML = window.marked.parse(markdownText || "(No markdown available)");
  }



}

// ✅ Wait for DOM and JSON before init
Promise.all([
  new Promise(res => document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', res)
    : res()),
  fetch('./public.json').then(res => res.json()).then(data => (publicData = data))
]).then(init);