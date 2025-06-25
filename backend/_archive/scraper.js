const TurndownService = require('turndown');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const puppeteer = require('puppeteer');

const BASE_URL = 'https://developer.hospitable.com';
const TOC_CACHE_PATH = path.resolve(__dirname, 'toc_cache.json');
const SCRAPE_CACHE_PATH = path.resolve(__dirname, 'scrape_cache.json');
const OUTPUT_PATH = path.resolve(__dirname, 'API_DOCS_improved.md');
const turndownService = new TurndownService();

/**
 * Load the scrape cache from the file system.
 * @returns {Object} The scrape cache as a JSON object.
 */
function loadScrapeCache() {
  if (fs.existsSync(SCRAPE_CACHE_PATH)) {
    return JSON.parse(fs.readFileSync(SCRAPE_CACHE_PATH, 'utf8'));
  }
  return {};
}

/**
 * Save the scrape cache to the file system.
 * @param {Object} cache - The scrape cache to save.
 */
function saveScrapeCache(cache) {
  fs.writeFileSync(SCRAPE_CACHE_PATH, JSON.stringify(cache, null, 2));
}

/**
 * Fetch HTML content using Puppeteer.
 * @param {string} url - The URL to fetch.
 * @param {boolean} force - Whether to force fetch even if cached.
 * @returns {string} The fetched HTML content.
 */
async function fetchHtmlWithPuppeteer(url, force) {
  const scrapeCache = loadScrapeCache();
  const now = Date.now();

  if (!force && scrapeCache[url] && now - scrapeCache[url].timestamp < 48 * 60 * 60 * 1000) {
    console.log(`Using cached HTML for ${url}`);
    return scrapeCache[url].html;
  }

  console.log(`Fetching with Puppeteer: ${url}`);
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

  await page.goto(url, { waitUntil: 'networkidle2' });

  // Wait for the main content to be present
  await page.waitForSelector('.sl-elements-article', { timeout: 15000 });

  // Extract only the .sl-elements-article content
  const html = await page.evaluate(() => {
    const article = document.querySelector('.sl-elements-article');
    return article ? article.outerHTML : '';
  });

  await browser.close();

  scrapeCache[url] = { html, timestamp: now };
  saveScrapeCache(scrapeCache);

  return html;
}

/**
 * Main function to process the TOC and generate Markdown documentation.
 */
async function main() {
  const force = process.argv.includes('--force');

  if (!fs.existsSync(TOC_CACHE_PATH)) {
    console.error(`Error: ${TOC_CACHE_PATH} not found.`);
    return;
  }

  const toc = JSON.parse(fs.readFileSync(TOC_CACHE_PATH, 'utf8'));
  let markdownOutput = '# Hospitable API Documentation\n\n';

  /**
   * Process a single TOC node recursively.
   * @param {Object} node - The TOC node to process.
   * @param {number} currentLevel - The current depth level in the TOC.
   */
  async function processNode(node, currentLevel) {
    if (node.path) {
      const url = `${BASE_URL}${node.path}`;
      console.log(`Processing ${node.title} at ${url}`);

      const html = await fetchHtmlWithPuppeteer(url, force);

      if (html && html.trim()) {
        const $ = cheerio.load(html);
        const mainContent = $('.sl-elements-article').html();
        if (mainContent && mainContent.trim()) {
          const markdown = turndownService.turndown(mainContent);
          const headingPrefix = '#'.repeat(currentLevel + 1); // Adjust heading level based on TOC level
          markdownOutput += `${headingPrefix} ${node.title}\n\n${markdown}\n\n`;
        }
      }
    }

    for (const child of node.children) {
      await processNode(child, currentLevel + 1);
    }
  }

  for (const node of toc) {
    await processNode(node, node.level);
  }

  fs.writeFileSync(OUTPUT_PATH, markdownOutput);
  console.log(`Documentation saved to ${OUTPUT_PATH}`);
}

main().catch(console.error);
