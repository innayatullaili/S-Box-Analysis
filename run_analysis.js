const fs = require('fs');
const path = require('path');
const SBoxAnalyzer = require('./analyzer.js');

function parseCSV(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const values = [];
    const lines = content.split('\n');
    
    for (const line of lines) {
        if (!line.trim()) continue;
        const parts = line.split(',');
        for (const part of parts) {
            const val = parseInt(part.trim());
            if (!isNaN(val)) {
                values.push(val);
            }
        }
    }
    return values;
}

function run() {
    const csvPath = path.join(__dirname, 'test-sbox.csv');
    console.log(`Reading S-Box from ${csvPath}...`);
    
    try {
        const sbox = parseCSV(csvPath);
        console.log(`Loaded ${sbox.length} values.`);
        
        if (sbox.length !== 256) {
            console.error('Error: S-Box must have exactly 256 values.');
            return;
        }

        const analyzer = new SBoxAnalyzer(sbox);
        
        console.log('\nRunning Analysis...');
        
        // 1. Nonlinearity
        const nl = analyzer.calculateNonlinearity();
        console.log(`1. Nonlinearity: ${nl}`);
        
        // 2. SAC
        const sac = analyzer.calculateSAC();
        console.log(`2. SAC Score: ${sac.score.toFixed(4)}`);
        console.log(`   SAC Max Deviation: ${sac.maxDeviation.toFixed(4)}`);
        
        // 3. BIC-NL
        const bicNL = analyzer.calculateBIC_NL();
        console.log(`3. BIC-NL Min: ${bicNL.minNonlinearity}`);
        console.log(`   BIC-NL Avg: ${bicNL.averageNonlinearity.toFixed(4)}`);
        
        // 4. BIC-SAC
        const bicSAC = analyzer.calculateBIC_SAC();
        console.log(`4. BIC-SAC Max Correlation: ${bicSAC.maxCorrelation.toFixed(4)}`);
        console.log(`   BIC-SAC Avg Correlation: ${bicSAC.averageCorrelation.toFixed(4)}`);
        
        // 5. LAP
        const lap = analyzer.calculateLAP();
        console.log(`5. LAP Max Bias: ${lap.maxBias}`);
        console.log(`   LAP Max Probability: ${lap.maxLAP.toFixed(6)}`);
        
        // 6. DAP & DU
        const dap = analyzer.calculateDAP();
        console.log(`6. Differential Uniformity: ${dap.maxDifferential}`);
        console.log(`   Max DAP: ${dap.maxDAP.toFixed(6)}`);
        
        // 7. Algebraic Degree
        const ad = analyzer.calculateAlgebraicDegree();
        console.log(`7. Algebraic Degree: ${ad}`);

    } catch (err) {
        console.error('Error running analysis:', err);
    }
}

run();
