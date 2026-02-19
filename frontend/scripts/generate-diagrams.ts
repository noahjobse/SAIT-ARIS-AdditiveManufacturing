import { renderMermaid, THEMES } from 'beautiful-mermaid';
import { writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { diagrams } from './diagrams.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const OUTPUT_DIR = join(__dirname, '../../docs/diagrams');
const THEME = THEMES['github-light']; // Clean, professional look

async function generateDiagrams() {
  // Ensure output directory exists
  mkdirSync(OUTPUT_DIR, { recursive: true });

  console.log('Generating diagrams...\n');

  for (const [name, source] of Object.entries(diagrams)) {
    try {
      const svg = await renderMermaid(source, THEME);
      const outputPath = join(OUTPUT_DIR, `${name}.svg`);

      writeFileSync(outputPath, svg);
      console.log(`✓ Generated: ${name}.svg`);
    } catch (error) {
      console.error(`✗ Failed to generate ${name}:`, error);
      process.exit(1);
    }
  }

  console.log('\n✓ All diagrams generated successfully!');
}

generateDiagrams();
