# Dry etching of hBN / graphene heterostructures (Oxford RIE)

**Authors:** Bianca Turini, Neha Bhatia
**Created:** 2025-11-21
**Last modified:** 2026-02-11

## Description

Reactive ion etching (RIE) of 2D material stacks using SF6-, O2-, and CHF3-based recipes on the Oxford Plasmalab 100. Processes are tuned for small samples on Si substrate chips (~5 mm). Assumes the etch mask is already prepared; see related STEP protocols for optical or e-beam lithography.


# Oxford Plasmalab 100 — main procedure

| Step | Task | Subtask | Materials | Parameters | Warnings | Verification |
|------|------|-------|------------|----------|--------------|---------|
| 1.0 | Chip preparation | Blow dry the chip to remove possibly deposited dirt. Assumes the etching mask was prepared per your protocol and the sample is ready to etch. For lithography, see the related STEP protocol (optical / e-beam). | Nitrogen gun, tweezers. | Blow dry 5–10 s at ~45° to the surface. Gas flow setting is not critical if the jet reaches the chip and displaces debris. Angle is not critical. | Hold the chip securely. At startup, nitrogen pressure can exceed the setpoint and the flow may carry debris — avoid exposing the sample for the first few seconds. The etch mask must be thick and robust enough for the full etch; O2 in particular affects PMMA masks. | Optical inspection: substrate looks clean; no hair or dust. |
| 2.0 | Chamber inspection |  | Oxford RIE (Plasmalab 100; add exact model in lab docs). |  |  |  |
| 2.1 | Chamber inspection | Confirm the previous user ran an oxygen-based chamber clean after their process (“O2 clean”, Appendix). In Process / Log View, check the last process, parameters, and that there was no error. |  |  |  |  |
| 2.2 | Chamber inspection | Confirm the dummy Si wafer is in the loadlock and shown in System / Pumping. This wafer is for chamber cleaning only. |  |  | After “O2 clean”, the dummy can remain in the main chamber while the software thinks it is in the loadlock — contact cleanroom staff. You can check loadlock status from the loadlock window without venting. In the chamber viewport, a thin line below the upper disk indicates a wafer inside (use a flashlight if needed). |  |
| 3.0 | Select gases | Select the process gas for your etching recipe. The panel has two valves per line: upper = gas to chamber on/off; lower = flow (do not adjust — the tool sets flow). | Required gases for the recipe; He and N2 are mandatory support gases in addition to process gases. Only operate top-row valves to enable or disable delivery. |  | Do not adjust bottom-row flow-control valves. Keep He and N2 supply valves open at all times. |  |
| 4.0 | Remove dummy wafer and insert your wafer |  |  |  |  |  |
| 4.1 | Remove dummy wafer and insert your wafer | Dummy wafer removal: stop evacuation, vent the loadlock, wait until atmospheric (~300 s), remove the dummy wafer. |  |  |  |  |
| 4.2 | Remove dummy wafer and insert your wafer | Wafer insertion: place your sample wafer in the loadlock, close it, stop venting, pump down. Enter sample name or process ID when prompted after evacuation. | Dedicated Si carrier wafer per process; obtain spares from cleanroom staff or purchase as required. |  |  | Optically verify through the loadlock that the dummy was replaced correctly. |
| 5.0 | Preconditioning |  |  |  |  |  |
| 5.1 | Preconditioning | Load the preconditioning recipe (Process → Recipe → Load Recipe). Cleans the chamber; if the prior user ran O2 clean, preconditioning can be short. |  | Typical guideline: ~2 minutes per gas used in the upcoming recipe. See Supplementary for recipe edits (S1). Do not save changes to a recipe unless you created it. | Some recipes should not be preconditioned with specific gases before the first step due to residuals; for standard 1D contact recipes this is usually not an issue. |  |
| 5.2 | Preconditioning | Run the loaded recipe; monitor via Process → Chamber 1. Log parameters in the lab logbook in real time. |  | If parameters were not visible live, retrieve them later via Process → Log View using the process name you assigned. Wait until base pressure is adequate before start; the system delays until vacuum is OK. Confirm wafer transfer to the main chamber via the interface indicators. |  |  |
| 6.0 | Run your etch recipe | After preconditioning, confirm the wafer is in the loadlock. Center the sample on the carrier, keep the surface clean, assign an ID, load the process recipe, run, then unload when finished. Document everything in the logbook. | Sample as prepared for etching. |  |  | Take a micrograph before loading if possible. After the run, compare etched vs protected regions by optical contrast (contrast depends on sample and recipe). For small features, use SEM or AFM (AFM especially if the mask was e-beam resist). Dense 2D lattices may still show optical contrast. |
| 7.0 | O2 clean (handover) | Remove your sample and carrier from the loadlock, install the dummy wafer, run the O2 cleaning recipe for the next user. |  | Typically ~30 minutes O2 clean; schedule instrument time with this buffer included. |  |  |


## Supplementary Material

## Recipe tables (from STEP_RIE_Oxford_hBN_Gr)

### SF6-based selective hBN etching
| Parameter   | Value   |
|-------------|---------|
| SF6         | 40 sccm |
| Pressure    | 90 Pa   |
| RF power    | 20 W    |
| ICP power   | 0 W     |
| Table temp. | 20 °C   |
| Backside He | 10 Torr |

Note resulting bias as logged by the tool.

### O2-based selective graphene etching
| Parameter   | Value   |
|-------------|---------|
| O2          | 20 sccm |
| Pressure    | 80 Pa   |
| RF power    | 20 W    |
| ICP power   | 0 W     |
| Table temp. | 20 °C   |
| Backside He | 10 Torr |

### CHF3 / O2 non-selective etching
| Parameter   | Value   |
|-------------|---------|
| CHF3        | 40 sccm |
| O2          | 4 sccm  |
| Pressure    | 90 Pa   |
| RF power    | 60 W    |
| ICP power   | 0 W     |
| Table temp. | 20 °C   |
| Backside He | 10 Torr |

Typical DC bias ~250 V (as reported for this recipe).

### S1 — Recipe modification (software)
- Edit steps with **Edit Step** (pressure, forward power, gas flows, duration).
- **Delete Step** removes a step temporarily; if the recipe is not saved, the step remains.
- **Do not save** changes to recipes you did not create; duplicate into a new recipe instead.

### Examples (slides)
- **Example 1:** Two-step selective etch (SF6 then O2) for graphene contacts in hBN/graphene/hBN:
  control windows etch fully; contact windows leave bottom hBN (color difference resist vs etched).
- **Example 2:** Single-step CHF3/O2 etch of hBN lattices: control regions clear; dense lattices
  show contrast even below optical resolution.


## References


