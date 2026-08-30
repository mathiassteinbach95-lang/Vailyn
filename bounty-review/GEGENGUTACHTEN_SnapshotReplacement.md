# Gegengutachten: „Permissionless Snapshot Replacement → Permanent DoS" (Origin Protocol)

**Gegenstand:** Immunefi-Report gegen `CompoundingStakingStrategy` / `OETHVaultLens`
**Ziel-Commit:** `ab0e85f2ada41a00d0cf6f5e6acceae2d110deb3` (OriginProtocol/origin-dollar)
**Prüfmethode:** Verifikation gegen den **echten** On-Chain- **und Off-Chain**-Code des
Ziel-Commits (nicht gegen die Python-Simulation des Reports).

**Ergebnis: Die Bounty ist NICHT gerechtfertigt.** Die beiden tragenden Annahmen des
Reports sind durch den realen Code widerlegt.

---

## 1. Die zwei Annahmen, an denen der Report hängt

Der Report behauptet einen *permanenten* DoS. Damit dieser eintritt, müssen **beide**
folgenden Annahmen wahr sein:

- **(A) Latenz-Annahme:** Die reale Proof-Generierung + Submission des Origin-Betreibers
  dauert *zuverlässig* länger als 421 s (das Snap-Delay), sodass der Angreifer den Snapshot
  immer vor dem Betreiber ersetzen kann.
- **(B) Fixierungs-Annahme:** Der Betreiber ist an die Proofs für einen *bestimmten alten*
  Snapshot (S₀) gebunden; nach einem Re-Snap sind diese Proofs *dauerhaft* wertlos, und der
  Betreiber kann nicht einfach gegen den *neuesten* Snapshot neu verifizieren.

Der Report belegt keine der beiden. Der reale Code widerlegt beide.

---

## 2. Annahme (B) ist FALSCH — der Betreiber verifiziert gegen den neuesten Snapshot

Der Off-Chain-Task `verifyBalances` liest den zu beweisenden Snapshot per Default **live von
der Chain** aus, und zwar bei *jedem* Lauf neu:

`contracts/tasks/beacon.js`, Funktion `verifyBalances(...)`:

```js
if (!slot) {
  if (!test) {
    const { blockRoot } = await strategy.snappedBalance(); // <-- aktueller On-Chain-Snapshot
    slot = blockRoot;
    log(`Using slot with block root ${slot} for verifying balances`);
  }
}
// ...
const { blockView, blockTree, stateView } = await getBeaconBlock(slot, networkName);
// Proofs werden gegen genau diesen blockRoot erzeugt und eingereicht.
```

Und der Task-Parameter selbst dokumentiert das Default-Verhalten
(`contracts/tasks/actions/verifyBalances.ts`):

> `"slot"` — *"The slot snapBalances was executed. **Default: last balances snapshot**"*

**Konsequenz:** Es gibt keine „verwaisten Proofs für S₀". Ersetzt ein Angreifer den Snapshot
(S₀ → S₁), liest der Betreiber-Bot im nächsten Durchlauf schlicht `snappedBalance()` = S₁ und
erzeugt die Proofs gegen S₁. Das im Report gezeichnete Szenario „Bot bereitet minutenlang
Proofs für S₀ vor, die dann für immer ungültig werden" existiert im realen Betrieb nicht —
der Bot bindet sich nie an einen veralteten Root.

Damit ist die zentrale Kausalkette des Reports (Zeile 1010 des Contracts „Proofs gegen
mutable Snapshot" → „in-flight Proofs sterben" → „Timestamp bleibt stale") bereits
durchbrochen: Der Contract liest zwar tatsächlich den aktuellen `snappedBalance` (das stimmt),
aber genau deshalb erzeugt auch der Betreiber seine Proofs gegen eben diesen aktuellen Wert.

---

## 3. Annahme (A) ist FALSCH — Proof-Generierung dauert Sekunden, nicht Minuten

Der Report *behauptet* „Proof-Vorbereitung dauert typischerweise 5–30 Minuten" — ohne jeden
Beleg. Der reale Code liefert die tatsächlichen Betriebszahlen. Die gesamte Proof-Erzeugung
ist **lokale Berechnung** über eine einmal geladene Beacon-State-View; der einzige nennenswerte
I/O ist der einmalige Download des Beacon-State.

`contracts/utils/beacon.js`, `getBeaconBlock()` → `fetchStateSsz()` (Kommentare der
Origin-Entwickler, aus dem realen Betrieb):

```
// ... Lighthouse gzip the ~330MB state and drop content-length. Inflating that
// on the main thread backpressures the socket down to ~2 Mbps (a 15min
// download that hits the abort below) ... Asking for identity doubles the
// wire bytes but the transfer takes ~2s.
```

Belegte reale Kosten eines Verifikationszyklus:

| Schritt | Reale Kosten (aus dem Code/Betrieb) |
|---|---|
| Beacon-State laden (~330 MB, `Accept-Encoding: identity`) | **~2 s** |
| Merkle-Proofs erzeugen (lokal, ≤ 48 Validatoren; `MAX_VERIFIED_VALIDATORS = 48`) | Millisekunden–wenige Sek. |
| `verifyBalances`-TX-Inklusion | ~1 Slot ≈ **12 s** |
| **Summe realistisch** | **≪ 60 s** |

Das ist **weit unter dem 421-s-Fenster**. Der 15-Minuten-Wert
(`BEACON_STATE_FETCH_TIMEOUT_MS`) ist *kein* Normalfall, sondern der Abort-Deckel für einen
pathologischen gzip-Pfad, den die Entwickler bereits **behoben** haben (siehe Kommentar). Der
Normalfall ist ~2 s.

Damit ist die einzige quantitative Stütze des Reports (Latenz > 421 s) widerlegt.

---

## 4. Die Race-Analyse, korrekt gerechnet

Der PoC des Reports modelliert einen Betreiber, der sich an S₀ fesselt und deshalb *immer*
verliert. Mit dem realen Verhalten (Abschnitt 2 + 3) sieht das Spiel so aus:

- **Angreifer-Budget:** Wegen `require(snappedBalance.timestamp + 420 < now)` kann *irgendjemand*
  höchstens **einmal pro 421 s** snappen. Ein Angreifer-Snap „verbraucht" das Fenster für 421 s.
- **Betreiber-Bedarf:** Der Betreiber muss innerhalb von 24 h **ein einziges** `verifyBalances`
  landen, um `lastVerifiedBalanceTimestamp` zu erneuern. 24 h ≈ **205** solcher 421-s-Fenster.
- **Zykluszeit Betreiber:** ≪ 60 s (Abschnitt 3).

Ablauf in *einem* Fenster: Sobald ein Snapshot existiert (egal ob vom Betreiber oder Angreifer
gesetzt), liest der Bot den aktuellen `blockRoot`, erzeugt in < 60 s die Proofs und reicht ein.
Der Angreifer kann in diesem Fenster **nicht erneut snappen** (Budget verbraucht), also bleibt
der Root während der ~60 s stabil → die Verifikation **landet**.

Für einen *permanenten* DoS müsste der Angreifer den Betreiber über **205 aufeinanderfolgende
Fenster (= volle 24 h)** in *jedem* Fenster schlagen, obwohl der Betreiber pro Fenster ~7×
schneller ist. Das ist mit dem Snap-Delay strukturell unmöglich, solange der Betreiber
überhaupt aktiv ist. Der einzige Weg zum „24-h-Stale" ist ein **24-stündiger Ausfall des
Betreiber-Bots** — das ist ein Betriebsvorfall, keine On-Chain-Schwachstelle.

Front-Running-Variante (Report 2.2.2 „Variation B"): Der Angreifer front-runt *eine*
`verifyBalances`-TX mit einem Snap. Damit ist sein 421-s-Budget verbraucht; der Betreiber liest
sofort den neuen Root und reicht im selben Fenster erneut ein → landet. Ergebnis: maximal eine
kurze Verzögerung + etwas Betreiber-Gas, kein Funktions- oder Mittelverlust.

Genau diese Überlegung steht als bewusste Designentscheidung im Contract selbst
(`CompoundingStakingStrategy.sol`, direkt über `snapBalances`):

```
/// This function is permissionless. The delay prevents callers from continually replacing
/// snapshots before their balance proofs can be submitted.
```

„Permissionless + Delay" ist also *known/by-design* — auf Immunefi typischerweise
Informational / Out-of-Scope, keine belohnbare HIGH-Finding.

---

## 5. Impact ist zusätzlich massiv überzeichnet

Selbst *wenn* `lastVerifiedBalanceTimestamp` stale würde, reverted **nur** der read-only
`OETHVaultLens.getRate()` — ein separater NAV-Reporter, den der Vault selbst nie aufruft.

Die Vault-Bewertung läuft über `checkBalance()`, und die kennt **keinen** Staleness-Check:

`CompoundingStakingStrategy.sol`, `checkBalance()`:

```solidity
balance = lastVerifiedEthBalance + IWETH9(WETH).balanceOf(address(this));
```

Also: `deposit()`, `withdraw()`, `rebase()`, `Vault.totalValue()` hängen **nicht** am Timestamp
und reverten **nicht**. Die Report-Behauptungen „Rebase blockiert / Deposits & Withdrawals
kaputt / protokollweite Preis-Feeds gebrochen" sind nicht gedeckt (der Report hedged in seiner
eigenen Tabelle selbst mit „may"). Und „permanent" ist falsch: ein einziges erfolgreiches
`verifyBalances` stellt alles wieder her; der Zustand ist vollständig reversibel.

---

## 6. Warum der Original-PoC nichts beweist

Der „7/7 Tests bestanden"-PoC ist eine **Python-Nachbildung der vom Autor angenommenen Logik**.
Er modelliert weder (a) den realen Betreiber, der pro Lauf `snappedBalance()` neu liest, noch
(b) die reale Latenz (~Sekunden statt „5–30 min"), noch (c) das Snap-Delay als Angreifer-Budget-
Grenze gegen einen schnelleren Betreiber. Er zeigt lediglich, dass das *Modell des Autors* in
sich konsistent ist — nicht, dass das reale System ausnutzbar ist. Er hat den echten Contract
nie berührt.

---

## 7. Fazit

| Prüfpunkt | Ergebnis |
|---|---|
| `snapBalances()` permissionless + 420-s-Delay | wahr (verifiziert) |
| `getRate()` reverted bei stale Timestamp | wahr (verifiziert) |
| **(A)** Proof-Latenz > 421 s | **widerlegt** (~Sekunden, Beleg im Code) |
| **(B)** Betreiber an alten Snapshot gefesselt | **widerlegt** (liest `snappedBalance()` live) |
| Permanenter DoS | **nicht gegeben** (Betreiber gewinnt jedes Fenster; nur 24-h-Ausfall wäre nötig) |
| Impact auf Vault (deposit/withdraw/rebase) | **keiner** (`checkBalance` ohne Staleness-Check) |
| Status | bewusstes **by-design** (Contract-Kommentar) |

**Belastbare Einordnung:** bestenfalls **Low / Informational** (theoretisches Griefing gegen
einen bewusst permissionlosen, verzögerten Mechanismus). Die im Report angesetzten
**$75k–150k (HIGH)** sind nicht haltbar. Die Einreichung trägt in dieser Form nicht.

**Was sie tragfähig machen würde (und was der Report schuldig bleibt):** ein empirischer
Nachweis, dass die reale Betreiber-Latenz (State-Fetch + Proof-Gen + Inklusion) *zuverlässig*
> 421 s liegt **und** dass der Betreiber nicht gegen den neuesten Snapshot neu verifizieren
kann. Beides ist durch den realen Code hier positiv **widerlegt** — der Nachweis ist also nicht
nur „nicht erbracht", sondern nicht erbringbar.
