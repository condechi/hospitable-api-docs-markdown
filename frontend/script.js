fetch('./toc_updated.json')
  .then(res => res.json())
  .then(data => {
    const tocEl = document.getElementById("toc");
    const display = document.getElementById("markdownDisplay");
    const title = document.getElementById("title");
    const timestamp = document.getElementById("timestamp");
    const link = document.getElementById("originalLink");
    const copyBtn = document.getElementById("copyBtn");
    const downloadBtn = document.getElementById("downloadBtn");

    const entries = Object.entries(data);

    entries.forEach(([url, obj], i) => {
      const li = document.createElement("li");
      li.textContent = obj.title;
      li.className = `pl-${(obj.level ?? 1) * 2}`;
      li.onclick = () => {
        title.textContent = obj.title;
        display.textContent = obj.content?.trim() || "(No markdown available)";
        timestamp.textContent = obj.timestamp ? `Last scraped: ${obj.timestamp}` : "";
        link.href = url;
        link.style.display = obj.html ? "inline" : "none";

        copyBtn.onclick = () => navigator.clipboard.writeText(display.textContent);
        downloadBtn.onclick = () => {
          const blob = new Blob([display.textContent], { type: "text/markdown" });
          const a = document.createElement("a");
          a.href = URL.createObjectURL(blob);
          a.download = `${obj.title.replace(/\s+/g, "_")}.md`;
          a.click();
        };
      };
      tocEl.appendChild(li);
    });
  });
