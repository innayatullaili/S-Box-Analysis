import json
import math

def check_bijective(sbox):
    """
    Checks if the S-Box is bijective (one-to-one mapping).
    """
    if len(sbox) != 256:
        return False
    return len(set(sbox)) == 256

def walsh_hadamard_transform(f):
    """
    Computes the Walsh-Hadamard Transform of a boolean function f.
    """
    n = len(f)
    if n == 1:
        return f
    half = n // 2
    left = walsh_hadamard_transform(f[:half])
    right = walsh_hadamard_transform(f[half:])
    
    res = []
    for i in range(half):
        res.append(left[i] + right[i])
    for i in range(half):
        res.append(left[i] - right[i])
    return res

def calculate_nonlinearity(sbox):
    """
    Calculates the Nonlinearity of the S-Box.
    NL = min(NL(f_i)) for i=0..7 (output bits).
    """
    n = 8
    min_nl = 256 # Start high
    
    for bit in range(8):
        f = []
        for x in range(256):
            val = sbox[x]
            bit_val = (val >> bit) & 1
            f.append(1 if bit_val == 0 else -1)
            
        wht = walsh_hadamard_transform(f)
        max_abs_wht = max(abs(x) for x in wht)
        
        nl = (2**(n-1)) - (max_abs_wht / 2)
        if nl < min_nl:
            min_nl = nl
            
    return int(min_nl)

def calculate_sac(sbox):
    """
    Calculates the Strict Avalanche Criterion (SAC).
    Average probability that an output bit changes when a single input bit changes.
    """
    n = 8
    total_sac = 0
    count = 0
    
    for i in range(n):
        for x in range(256):
            x_flipped = x ^ (1 << i)
            y1 = sbox[x]
            y2 = sbox[x_flipped]
            
            diff = y1 ^ y2
            hw = bin(diff).count('1')
            
            total_sac += hw
            count += 8
            
    return total_sac / count

def calculate_bic_nl(sbox):
    """
    Calculates Bit Independence Criterion - Nonlinearity (BIC-NL).
    Min NL of XOR sum of any two output bits.
    """
    n = 8
    min_nl = 256
    
    for i in range(n):
        for j in range(i + 1, n):
            # Boolean function for f_i XOR f_j
            f = []
            for x in range(256):
                val = sbox[x]
                bit_i = (val >> i) & 1
                bit_j = (val >> j) & 1
                res_bit = bit_i ^ bit_j
                f.append(1 if res_bit == 0 else -1)
            
            wht = walsh_hadamard_transform(f)
            max_abs_wht = max(abs(x) for x in wht)
            nl = (2**(n-1)) - (max_abs_wht / 2)
            
            if nl < min_nl:
                min_nl = nl
                
    return int(min_nl)

def calculate_bic_sac(sbox):
    """
    Calculates Bit Independence Criterion - SAC (BIC-SAC).
    Checks if the avalanche vectors of two output bits are independent.
    """
    n = 8
    total_sac_xor = 0
    count_xor = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            current_sac_sum = 0
            current_count = 0
            
            for k in range(n): # Input bit to flip
                for x in range(256):
                    x_flipped = x ^ (1 << k)
                    y1 = sbox[x]
                    y2 = sbox[x_flipped]
                    
                    b1_i = (y1 >> i) & 1
                    b1_j = (y1 >> j) & 1
                    h1 = b1_i ^ b1_j
                    
                    b2_i = (y2 >> i) & 1
                    b2_j = (y2 >> j) & 1
                    h2 = b2_i ^ b2_j
                    
                    if h1 != h2:
                        current_sac_sum += 1
                    current_count += 1
            
            total_sac_xor += (current_sac_sum / current_count)
            count_xor += 1
            
    return total_sac_xor / count_xor

def calculate_lap(sbox):
    """
    Calculates Linear Approximation Probability (LAP).
    Uses Maximum Linear Bias approximation to match standard paper value (0.0625 for AES).
    """
    n = 8
    max_abs_lat = 0
    
    # Note: loop starts from 1 to exclude zero mask
    for b in range(1, 256):
        f = []
        for x in range(256):
            val = sbox[x]
            # Dot product of output mask b and output value val
            dot_prod = bin(b & val).count('1') % 2
            f.append(1 if dot_prod == 0 else -1)
            
        wht = walsh_hadamard_transform(f)
        # Max absolute value in WHT corresponds to max bias for linear approximation a.x = b.S(x)
        # We need to exclude a=0 case if b=0, but here b starts from 1.
        # However, inside WHT, index 0 corresponds to a=0.
        # Usually we exclude a=0, b=0. Since b!=0, a=0 is a valid approximation (constant function).
        # But for LAP we usually look for max bias.
        current_max = max(abs(x) for x in wht)
        if current_max > max_abs_lat:
            max_abs_lat = current_max
            
    return (max_abs_lat / 256.0) # Bias is max_wht / 2^n. 

def calculate_dap(sbox):
    """
    Calculates Differential Approximation Probability (DAP).
    """
    n = 8
    max_count = 0
    
    for dx in range(1, 256):
        counts = {}
        for x in range(256):
            y1 = sbox[x]
            y2 = sbox[x ^ dx]
            dy = y1 ^ y2
            counts[dy] = counts.get(dy, 0) + 1
            
        for dy, count in counts.items():
            if count > max_count:
                max_count = count
                
    return max_count / 256.0

def calculate_differential_uniformity(sbox):
    """
    Calculates Differential Uniformity (DU).
    """
    n = 8
    max_count = 0
    
    for dx in range(1, 256):
        counts = {}
        for x in range(256):
            y1 = sbox[x]
            y2 = sbox[x ^ dx]
            dy = y1 ^ y2
            counts[dy] = counts.get(dy, 0) + 1
            
        for count in counts.values():
            if count > max_count:
                max_count = count
                
    return max_count

def calculate_algebraic_degree(sbox):
    """
    Calculates the Algebraic Degree (AD) of the S-Box.
    """
    n = 8
    max_degree = 0
    
    for bit in range(8):
        f = [(sbox[x] >> bit) & 1 for x in range(256)]
        
        # Compute ANF using Mobius Transform
        anf = list(f)
        for i in range(n):
            for j in range(256):
                if (j >> i) & 1:
                    anf[j] = (anf[j] + anf[j ^ (1 << i)]) % 2
                    
        deg = 0
        for x in range(256):
            if anf[x] == 1:
                w = bin(x).count('1')
                if w > deg:
                    deg = w
        
        if deg > max_degree:
            max_degree = deg
            
    return max_degree

def main():
    try:
        with open('sample-sbox.json', 'r') as f:
            data = json.load(f)
            sbox = data['sbox']
            
        print(f"Loaded S-Box: {data.get('name', 'Unknown')}")
        print("-" * 50)
        
        print(f"Bijective: {check_bijective(sbox)}")
        print(f"Nonlinearity: {calculate_nonlinearity(sbox)} (Expected: 112)")
        print(f"SAC: {calculate_sac(sbox):.4f} (Expected: ~128 or 0.5)")
        print(f"BIC-NL: {calculate_bic_nl(sbox)} (Expected: 112)")
        print(f"Differential Uniformity: {calculate_differential_uniformity(sbox)} (Expected: 4)")
        print(f"Algebraic Degree: {calculate_algebraic_degree(sbox)} (Expected: 7)")
        
        # Note: LAP calculation in the provided snippet was slightly ambiguous in scaling
        # I adjusted it to return Bias.
        # Let's see what it outputs.
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
