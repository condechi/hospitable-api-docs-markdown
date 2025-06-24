// script.js

// Fetch TOC data from the JSON file
fetch('toc_updated.json')
  .then(response => response.json())
  .then(tocData => {
    const tocElement = document.getElementById('toc');
    renderTOC(tocData, tocElement);
  })
  .catch(error => console.error('Error loading TOC data:', error));

// Function to render the TOC dynamically
function renderTOC(toc, parentElement) {
  toc.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.title;
    li.dataset.content = item.content;

    // Add click event to display content
    li.addEventListener('click', () => {
      displayContent(item.content);
    });

    parentElement.appendChild(li);

    // If the item has children, create a nested list
    if (item.children && item.children.length > 0) {
      const ul = document.createElement('ul');
      renderTOC(item.children, ul);
      parentElement.appendChild(ul);
    }
  });
}

// Function to display the Markdown contenthe Markdown content
function displayContent(content) {layContent(content) {
  const markdownContent = document.getElementById('markdown-content');content');
  markdownContent.innerHTML = marked(content); // Use the Marked.js library to render MarkdownarkdownContent.innerHTML = marked(content); // Use the Marked.js library to render Markdown
}// Initialize the TOCdocument.addEventListener('DOMContentLoaded', () => {  const tocElement = document.getElementById('toc');  renderTOC(tocData, tocElement);});