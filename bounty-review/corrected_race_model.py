#!/usr/bin/env python3
"""
Korrigiertes Race-Modell fuer den behaupteten "Snapshot Replacement DoS".

Unterschied zum Original-PoC: der Betreiber-Bot liest bei JEDEM Lauf den
aktuellen On-Chain-Snapshot (snappedBalance()) neu und beweist gegen dessen
blockRoot -- so wie es der reale Off-Chain-Task tut
(contracts/tasks/beacon.js: `const { blockRoot } = await strategy.snappedBalance()`).

Reale Konstanten (Ziel-Commit ab0e85f):
  SNAP_BALANCES_DELAY   = 420 s  -> min. Re-Snap-Abstand 421 s
  MAX_VERIFIED_BAL_AGE  = 24 h
Reale Betreiber-Latenz (aus utils/beacon.js-Kommentaren): State-Fetch ~2 s,
Proof-Gen lokal, TX-Inklusion ~12 s  -> Zyklus << 60 s.
"""
SNAP_DELAY = 420          # s
MIN_RESNAP = SNAP_DELAY+1 # 421 s: strikte Ungleichung im Contract
MAX_AGE    = 24*3600      # 86400 s

def simulate(op_cycle_s, attacker=True, horizon_s=7*24*3600):
    """Diskrete Sekunden-Simulation. Rueckgabe: (max_staleness, dos)."""
    t = 0
    snap_ts = 0            # snappedBalance.timestamp (0 = keiner)
    last_snap_by_attacker_at = -10**9
    last_verified = 0      # lastVerifiedBalanceTimestamp
    # Betreiber startet einen Verify-Zyklus, sobald ein Snapshot existiert.
    op_busy_until = None
    op_target_root = None  # der Root, den der Betreiber gerade beweist
    def cur_root():        # Root ist eindeutig durch snap_ts identifiziert
        return snap_ts
    max_stale = 0
    while t < horizon_s:
        # 1) Angreifer snappt, sobald erlaubt (max. 1x pro 421 s)
        if attacker and (snap_ts + SNAP_DELAY < t):
            snap_ts = t
            last_snap_by_attacker_at = t
            # Ein Re-Snap invalidiert einen laufenden Betreiber-Zyklus NUR,
            # wenn er gegen den alten Root laeuft:
            if op_busy_until is not None and op_target_root != snap_ts:
                op_busy_until = None   # Betreiber merkt es, startet neu
                op_target_root = None
        # 2) Betreiber: wenn frei und Snapshot vorhanden -> Zyklus starten
        if op_busy_until is None and snap_ts != 0 and snap_ts != last_verified:
            op_target_root = cur_root()
            op_busy_until = t + op_cycle_s
        # 3) Betreiber: Zyklus fertig -> verifyBalances landet, falls Root noch aktuell
        if op_busy_until is not None and t >= op_busy_until:
            if op_target_root == cur_root():   # kein Re-Snap dazwischen
                last_verified = snap_ts
                snap_ts = 0                    # Contract setzt timestamp=0
            op_busy_until = None
            op_target_root = None
        # 4) Staleness der getRate()-Sicht messen
        stale = t - last_verified
        if stale > max_stale:
            max_stale = stale
        t += 1
    dos = max_stale > MAX_AGE
    return max_stale, dos

if __name__ == "__main__":
    print(f"{'Betreiber-Zyklus':>18} | {'Angreifer':>9} | {'max Staleness':>13} | {'24h-DoS?':>8}")
    print("-"*60)
    for cyc in (15, 30, 60, 120, 300, 420):
        for atk in (True,):
            ms, dos = simulate(cyc, attacker=atk)
            print(f"{cyc:>16}s | {'ja' if atk else 'nein':>9} | {ms:>11}s | {'JA' if dos else 'NEIN':>8}")
    print()
    # Gegenprobe: was der Original-PoC implizit annimmt -- Betreiber langsamer
    # als das Re-Snap-Fenster UND an alten Root gefesselt -> nur DANN DoS:
    ms, dos = simulate(op_cycle_s=1000, attacker=True)
    print(f"Kontrollfall (unrealistischer 1000s-Zyklus > 421s): max Staleness {ms}s, DoS={dos}")
    print()
    print("Kernaussage: Solange der Betreiber-Zyklus < 421s ist (real ~<60s),")
    print("landet in jedem 421s-Fenster eine Verifikation -> KEIN DoS.")
    print("Ein 24h-Stale erfordert einen 24h-Ausfall des Betreibers, keine On-Chain-Luecke.")
