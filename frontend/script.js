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

  function renderAPIReference() {
    if (!selectedEntry?.title) {
      container.textContent = "No API section selected.";
      return;
    }

    const entrySlug = selectedEntry.title.toLowerCase().replace(/\s+/g, "-");
    const matches = (publicData?.tags || []).filter(t =>
      t.name?.toLowerCase()?.includes(entrySlug)
    );

    if (matches.length === 0) {
      container.innerHTML = "<p class='text-gray-500'>No API Reference found for this section.</p>";
      return;
    }

    const apis = publicData.paths || {};
    let html = "";

    for (const [endpoint, methods] of Object.entries(apis)) {
      for (const [method, obj] of Object.entries(methods)) {
        const tags = obj.tags?.map(t => t.toLowerCase()) || [];
        if (!tags.some(tag => tag.includes(entrySlug))) continue;

        html += `
          <div class="mb-6 border-b pb-4">
            <div class="text-sm font-mono bg-gray-100 px-2 py-1 rounded inline-block text-blue-600">${method.toUpperCase()}</div>
            <code class="ml-2 text-sm font-mono">${endpoint}</code>
            <p class="mt-1 text-gray-700 text-sm">${obj.summary ?? ""}</p>
        `;

        if (obj.parameters?.length) {
          html += `<h4 class="mt-2 font-semibold text-sm">Parameters</h4><table class="table-auto w-full text-sm mt-1 mb-2"><thead><tr><th class="text-left">Name</th><th>In</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody>`;
          obj.parameters.forEach(param => {
            html += `<tr class="border-t"><td>${param.name}</td><td>${param.in}</td><td>${param.schema?.type ?? ''}</td><td>${param.required}</td><td>${param.description ?? ''}</td></tr>`;
          });
          html += `</tbody></table>`;
        }

        if (obj.requestBody?.content) {
          html += `<h4 class="font-semibold text-sm mt-2">Request Body</h4>`;
          const appJson = obj.requestBody.content["application/json"];
          if (appJson?.example) {
            html += `<pre class="bg-gray-50 p-2 rounded text-xs overflow-auto">${JSON.stringify(appJson.example, null, 2)}</pre>`;
          } else if (appJson?.schema) {
            html += `<pre class="bg-gray-50 p-2 rounded text-xs overflow-auto">${JSON.stringify(appJson.schema, null, 2)}</pre>`;
          }
        }

        if (obj.responses) {
          html += `<h4 class="font-semibold text-sm mt-2">Responses</h4>`;
          for (const [code, res] of Object.entries(obj.responses)) {
            html += `<div class="mb-1"><span class="inline-block bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded">${code}</span> ${res.description || ''}</div>`;
          }
        }

        html += "</div>";
      }
    }

    container.innerHTML = html || "<p class='text-gray-500'>No matching API endpoints found.</p>";
  }
}

// ✅ Wait for DOM and JSON before init
Promise.all([
  new Promise(res => document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', res)
    : res()),
  fetch('./public.json').then(res => res.json()).then(data => (publicData = data))
]).then(init);