fetch('./toc_updated.json')
  .then(res => res.json())
  .then(data => {
    const tocEl = document.getElementById("toc");
    const title = document.getElementById("title");
    const timestamp = document.getElementById("timestamp");
    const link = document.getElementById("originalLink");
    const copyBtn = document.getElementById("copyBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const tabContainer = document.getElementById("versionTabs");
    const markdownContainer = document.getElementById("markdownContainer");

    data.forEach((entry, i) => {
      const li = document.createElement("li");
      li.textContent = entry.title;
      li.className = `pl-${(entry.level ?? 1) * 4}`;
      li.onclick = () => {
        title.textContent = entry.title;
        timestamp.textContent = entry.timestamp ? `Last scraped: ${entry.timestamp}` : "";
        link.href = entry.url ?? "#";
        link.style.display = entry.html ? "inline" : "none";

        // Clear previous tabs/content
        tabContainer.innerHTML = "";
        markdownContainer.innerHTML = "";

        const versions = entry.versions ?? { default: entry.content };

        Object.entries(versions).forEach(([versionKey, markdown], idx) => {
          // Create tab
          const tab = document.createElement("button");
          tab.className = `tab px-4 py-1 border border-gray-300 rounded-t ${idx === 0 ? 'bg-white font-bold' : 'bg-gray-200'}`;
          tab.textContent = versionKey;
          tab.dataset.version = versionKey;
          tab.onclick = () => {
            [...tabContainer.children].forEach(t => t.classList.remove("bg-white", "font-bold"));
            tab.classList.add("bg-white", "font-bold");
            markdownContainer.innerHTML = marked.parse(markdown || "(No markdown available)");
          };
          tabContainer.appendChild(tab);

          // Auto-load first tab
          if (idx === 0) {
            tab.click();
          }
        });

        // Copy and Download functionality
        copyBtn.onclick = () => navigator.clipboard.writeText(markdownContainer.textContent);
        downloadBtn.onclick = () => {
          const blob = new Blob([markdownContainer.textContent], { type: "text/markdown" });
          const a = document.createElement("a");
          a.href = URL.createObjectURL(blob);
          a.download = `${entry.title.replace(/\s+/g, "_")}.md`;
          a.click();
        };
      };
      tocEl.appendChild(li);
    });
  });

