const fs = require('fs');
const path = require('path');
const SBoxAnalyzer = require('./analyzer.js');

function run() {
    const jsonPath = path.join(__dirname, 'sample-sbox.json');
    console.log(`Reading S-Box from ${jsonPath}...`);
    
    try {
        const content = fs.readFileSync(jsonPath, 'utf8');
        const data = JSON.parse(content);
        const sbox = data.sbox;
        
        console.log(`Loaded ${sbox.length} values.`);
        
        if (sbox.length !== 256) {
            console.error('Error: S-Box must have exactly 256 values.');
            return;
        }

        const analyzer = new SBoxAnalyzer(sbox);
        
        console.log('\nRunning Analysis on AES S-Box...');
        
        // 1. Nonlinearity
        const nl = analyzer.calculateNonlinearity();
        console.log(`1. Nonlinearity: ${nl} (Expected: 112)`);
        
        // 2. SAC
        const sac = analyzer.calculateSAC();
        console.log(`2. SAC Score: ${sac.score.toFixed(4)} (Ideal: ~0.5)`);
        
        // 3. BIC-NL
        const bicNL = analyzer.calculateBIC_NL();
        console.log(`3. BIC-NL Min: ${bicNL.minNonlinearity} (Expected: 112)`);
        
        // 4. BIC-SAC
        const bicSAC = analyzer.calculateBIC_SAC();
        console.log(`4. BIC-SAC Avg (SAC of XOR): ${bicSAC.averageSAC.toFixed(4)} (Ideal: ~0.5)`);
        
        // 5. LAP
        const lap = analyzer.calculateLAP();
        console.log(`5. LAP Max Probability: ${lap.maxLAP.toFixed(4)} (Expected: 0.0625)`);
        
        // 6. DAP & DU
        const dap = analyzer.calculateDAP();
        console.log(`6. Differential Uniformity: ${dap.maxDifferential} (Expected: 4)`);
        
        // 7. Algebraic Degree
        const ad = analyzer.calculateAlgebraicDegree();
        console.log(`7. Algebraic Degree: ${ad} (Expected: 7)`);

        // 8. Correlation Immunity
        const ci = analyzer.calculateCorrelationImmunity();
        console.log(`8. Correlation Immunity: ${ci} (Expected: 0)`);

    } catch (err) {
        console.error('Error running analysis:', err);
    }
}

run();
