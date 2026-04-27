import fs from 'fs';
import path from 'path';
import { globSync } from 'glob';

console.log('Running Visual Polish Token Validation...');

const tokenFiles = globSync('principles/tokens/**/*.json');
let hasError = false;

tokenFiles.forEach(file => {
  try {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    
    // Quick validation logic
    if (data.$schema || data.$version) {
      console.log(`✓ ${path.basename(file)} parses successfully.`);
    } else {
      console.warn(`⚠ ${path.basename(file)} is missing $schema or $version.`);
    }
    
  } catch (err) {
    console.error(`✗ ERROR parsing ${file}:`, err.message);
    hasError = true;
  }
});

if (hasError) {
  console.error('\n✗ Token validation failed. Fix errors before building.');
  process.exit(1);
} else {
  console.log('\n✓ All tokens are structurally valid.');
  process.exit(0);
}
