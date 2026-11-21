// news-image-20261121 r1 — "THE WORLD TODAY", Saturday 21 November 2026.
// Node 22, standard library only: copies the pre-rendered entry.png beside
// this file into the output directory. No network, no python, no deletion.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), outPath);
// The gate rejects an empty file: fail loudly instead of writing one.
if (statSync(outPath).size === 0) {
  throw new Error('entry.png copied but is empty');
}
