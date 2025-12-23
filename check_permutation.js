const fs = require('fs');
const path = require('path');

const jsonPath = path.join(__dirname, 'sample-sbox.json');
const content = fs.readFileSync(jsonPath, 'utf8');
const data = JSON.parse(content);
const sbox = data.sbox;

const counts = new Array(256).fill(0);
let duplicates = 0;
let missing = 0;

for (const val of sbox) {
    counts[val]++;
}

for (let i = 0; i < 256; i++) {
    if (counts[i] === 0) {
        missing++;
        console.log(`Missing value: ${i}`);
    }
    if (counts[i] > 1) {
        duplicates++;
        console.log(`Duplicate value: ${i} (Count: ${counts[i]})`);
    }
}

console.log(`Size: ${sbox.length}`);
console.log(`Missing values: ${missing}`);
console.log(`Duplicate values: ${duplicates}`);

if (missing > 0) {
    console.log('S-Box is NOT a permutation.');
} else {
    console.log('S-Box IS a permutation.');
}
