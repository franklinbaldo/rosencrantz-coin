============================================================
ROSENCRANTZ'S COIN: Minesweeper Substrate Invariance Test
============================================================
Model: gpt-4o-mini
Samples/cell: 50
Boards: 3 (5x5, 4 mines)
Families: A, C, D

────────────────────────────────────────────────────────────
BOARD 1 (seed=42)
────────────────────────────────────────────────────────────

Board state:
. . . . .
. 1 1 1 1
.       .
1 1 1 . 1
. 1 . . .

Computing ground truth...
  Valid configurations: 2
  Target cells: [(0, 0), (0, 1), (0, 3), (0, 2)]
    (0,0): P*=0.500 [AMBIGUOUS]
    (0,1): P*=0.500 [AMBIGUOUS]
    (0,3): P*=0.500 [AMBIGUOUS]
    (0,2): P*=0.000 [SAFE]

--- Universe 2: External RNG ---
  U2 (0,0): n=50, P_hat=0.440, P*=0.500
  U2 (0,1): n=50, P_hat=0.420, P*=0.500
  U2 (0,3): n=50, P_hat=0.580, P*=0.500
  U2 (0,2): n=50, P_hat=0.460, P*=0.000

--- Universe 1: Homogeneous Substrate (Family A) ---
  U1-A (0,0): n=50, P_hat=0.520, P*=0.500, KL=0.0008
  U1-A (0,1): n=50, P_hat=0.600, P*=0.500, KL=0.0204
  U1-A (0,3): n=50, P_hat=0.460, P*=0.500, KL=0.0032
  U1-A (0,2): n=50, P_hat=0.580, P*=0.000, KL=0.8675

--- Universe 1: Homogeneous Substrate (Family C) ---
  U1-C (0,0): n=50, P_hat=0.580, P*=0.500, KL=0.0130
  U1-C (0,1): n=50, P_hat=0.520, P*=0.500, KL=0.0008
  U1-C (0,3): n=50, P_hat=0.440, P*=0.500, KL=0.0073
  U1-C (0,2): n=50, P_hat=0.540, P*=0.000, KL=0.7765

--- Universe 1: Homogeneous Substrate (Family D) ---
  U1-D (0,0): n=50, P_hat=0.480, P*=0.500, KL=0.0008
  U1-D (0,1): n=50, P_hat=0.420, P*=0.500, KL=0.0130
  U1-D (0,3): n=50, P_hat=0.560, P*=0.500, KL=0.0073
  U1-D (0,2): n=50, P_hat=0.560, P*=0.000, KL=0.8210

--- Universe 3: Decoupled Oracle ---
  U3 (0,0): n=50, P_hat=0.480, P*=0.500, KL=0.0008
  U3 (0,1): n=50, P_hat=0.460, P*=0.500, KL=0.0032
  U3 (0,3): n=50, P_hat=0.480, P*=0.500, KL=0.0008
  U3 (0,2): n=50, P_hat=0.380, P*=0.000, KL=0.4780

────────────────────────────────────────
BOARD 1 SUMMARY
────────────────────────────────────────
  U1-A vs GT:  mean_KL=0.2230  mean_Brier=0.0871  mean_|err|=0.1850
  U1-C vs GT:  mean_KL=0.1994  mean_Brier=0.0755  mean_|err|=0.1750
  U1-D vs GT:  mean_KL=0.2105  mean_Brier=0.0810  mean_|err|=0.1800
  U3 vs GT:    mean_KL=0.1207  mean_Brier=0.0367  mean_|err|=0.1150
  U2 vs GT:    mean_KL=0.1623  mean_Brier=0.0570  mean_|err|=0.1700
  Δ(U1-A, U3)=0.0313  Δ(U1-A, U2)=0.0341
  Δ(U1-C, U3)=0.0207  Δ(U1-C, U2)=0.0280
  Δ(U1-D, U3)=0.0206  Δ(U1-D, U2)=0.0060

────────────────────────────────────────────────────────────
BOARD 2 (seed=1042)
────────────────────────────────────────────────────────────

Board state:
. . 2 . .
. . . . .
. . 2 1
1 . 1   .


Computing ground truth...
  Valid configurations: 6
  Target cells: [(0, 0), (0, 1), (0, 3), (1, 1)]
    (0,0): P*=0.333 [AMBIGUOUS]
    (0,1): P*=0.500 [AMBIGUOUS]
    (0,3): P*=0.500 [AMBIGUOUS]
    (1,1): P*=0.000 [SAFE]

--- Universe 2: External RNG ---
  U2 (0,0): n=50, P_hat=0.400, P*=0.333
  U2 (0,1): n=50, P_hat=0.540, P*=0.500
  U2 (0,3): n=50, P_hat=0.520, P*=0.500
  U2 (1,1): n=50, P_hat=0.500, P*=0.000

--- Universe 1: Homogeneous Substrate (Family A) ---
  U1-A (0,0): n=50, P_hat=0.480, P*=0.333, KL=0.0441
  U1-A (0,1): n=50, P_hat=0.380, P*=0.500, KL=0.0297
  U1-A (0,3): n=50, P_hat=0.560, P*=0.500, KL=0.0073
  U1-A (1,1): n=50, P_hat=0.460, P*=0.000, KL=0.6162

--- Universe 1: Homogeneous Substrate (Family C) ---
  U1-C (0,0): n=50, P_hat=0.500, P*=0.333, KL=0.0566
  U1-C (0,1): n=50, P_hat=0.640, P*=0.500, KL=0.0408
  U1-C (0,3): n=50, P_hat=0.440, P*=0.500, KL=0.0073
  U1-C (1,1): n=50, P_hat=0.400, P*=0.000, KL=0.5108

--- Universe 1: Homogeneous Substrate (Family D) ---
  U1-D (0,0): n=50, P_hat=0.500, P*=0.333, KL=0.0566
  U1-D (0,1): n=50, P_hat=0.560, P*=0.500, KL=0.0073
  U1-D (0,3): n=50, P_hat=0.540, P*=0.500, KL=0.0032
  U1-D (1,1): n=50, P_hat=0.480, P*=0.000, KL=0.6539

--- Universe 3: Decoupled Oracle ---
  U3 (0,0): n=50, P_hat=0.460, P*=0.333, KL=0.0331
  U3 (0,1): n=50, P_hat=0.540, P*=0.500, KL=0.0032
  U3 (0,3): n=50, P_hat=0.520, P*=0.500, KL=0.0008
  U3 (1,1): n=50, P_hat=0.500, P*=0.000, KL=0.6931

────────────────────────────────────────
BOARD 2 SUMMARY
────────────────────────────────────────
  U1-A vs GT:  mean_KL=0.1743  mean_Brier=0.0628  mean_|err|=0.1967
  U1-C vs GT:  mean_KL=0.1539  mean_Brier=0.0527  mean_|err|=0.1917
  U1-D vs GT:  mean_KL=0.1803  mean_Brier=0.0658  mean_|err|=0.1867
  U3 vs GT:    mean_KL=0.1826  mean_Brier=0.0670  mean_|err|=0.1717
  U2 vs GT:    mean_KL=0.1767  mean_Brier=0.0641  mean_|err|=0.1567
  Δ(U1-A, U3)=0.0147  Δ(U1-A, U2)=0.0178
  Δ(U1-C, U3)=0.0142  Δ(U1-C, U2)=0.0185
  Δ(U1-D, U3)=0.0014  Δ(U1-D, U2)=0.0057

────────────────────────────────────────────────────────────
BOARD 3 (seed=2042)
────────────────────────────────────────────────────────────

Board state:
. . . . .
. . . . .
. . 1 2 .
1 1   2 .
.     2 .

Computing ground truth...
  Valid configurations: 2
  Target cells: [(1, 2), (1, 3), (0, 0)]
    (1,2): P*=0.500 [AMBIGUOUS]
    (1,3): P*=0.500 [AMBIGUOUS]
    (0,0): P*=0.000 [SAFE]

--- Universe 2: External RNG ---
  U2 (1,2): n=50, P_hat=0.380, P*=0.500
  U2 (1,3): n=50, P_hat=0.420, P*=0.500
  U2 (0,0): n=50, P_hat=0.420, P*=0.000

--- Universe 1: Homogeneous Substrate (Family A) ---
  U1-A (1,2): n=50, P_hat=0.460, P*=0.500, KL=0.0032
  U1-A (1,3): n=50, P_hat=0.400, P*=0.500, KL=0.0204
  U1-A (0,0): n=50, P_hat=0.480, P*=0.000, KL=0.6539

--- Universe 1: Homogeneous Substrate (Family C) ---
  U1-C (1,2): n=50, P_hat=0.420, P*=0.500, KL=0.0130
  U1-C (1,3): n=50, P_hat=0.440, P*=0.500, KL=0.0073
  U1-C (0,0): n=50, P_hat=0.460, P*=0.000, KL=0.6162

--- Universe 1: Homogeneous Substrate (Family D) ---
  U1-D (1,2): n=50, P_hat=0.460, P*=0.500, KL=0.0032
  U1-D (1,3): n=50, P_hat=0.440, P*=0.500, KL=0.0073
  U1-D (0,0): n=50, P_hat=0.540, P*=0.000, KL=0.7765

--- Universe 3: Decoupled Oracle ---
  U3 (1,2): n=50, P_hat=0.540, P*=0.500, KL=0.0032
  U3 (1,3): n=50, P_hat=0.380, P*=0.500, KL=0.0297
  U3 (0,0): n=50, P_hat=0.480, P*=0.000, KL=0.6539

────────────────────────────────────────
BOARD 3 SUMMARY
────────────────────────────────────────
  U1-A vs GT:  mean_KL=0.2258  mean_Brier=0.0807  mean_|err|=0.2067
  U1-C vs GT:  mean_KL=0.2121  mean_Brier=0.0739  mean_|err|=0.2000
  U1-D vs GT:  mean_KL=0.2623  mean_Brier=0.0989  mean_|err|=0.2133
  U3 vs GT:    mean_KL=0.2289  mean_Brier=0.0821  mean_|err|=0.2133
  U2 vs GT:    mean_KL=0.1958  mean_Brier=0.0657  mean_|err|=0.2067
  Δ(U1-A, U3)=0.0046  Δ(U1-A, U2)=0.0071
  Δ(U1-C, U3)=0.0124  Δ(U1-C, U2)=0.0025
  Δ(U1-D, U3)=0.0092  Δ(U1-D, U2)=0.0144

Results saved to /app/experiments/../results/minesweeper_20260304_125818.json
