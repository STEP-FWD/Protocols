# EBL - Raith Elphy Plus using single-layer PMMA

**Authors:** [Ediz Herkert](https://orcid.org/0000-0003-3040-8077)

---

# Description

This STEP protocol defines the process parameters for fabricating patterns up to 250 μm in size with a resolution of approximately 30 – 50 nm [[A1]](#a1-exemplary-structure). It is based on a single-layer PMMA resist and carried out using a 30 kV Raith Elphy Plus electron-beam lithography system. Although primarily developed for lift-off applications, the process can also be applied to fabricate etching masks.

---

# Protocol

| ID | Step | Sub-step | ME | PR | IWTD | VEO |
| --- | --- | --- | --- | --- | --- | --- |
| 1. | Substrate cleaning |   | • Beakers with spout for acetone <br>• Crystalizing dishes with spout for isopropanol and distilled water |   | • *WARNING*: Acetone is flammable and irritating. All following sub tasks *MUST* be carried out in a fume hood. |   |
| 1.1 | Substrate cleaning | Acetone immersion<br><br>Immerse the substrate in an acetone beaker. Close the beaker with tin foild to avoid acetone evaporation. | • Acetone (Scharlab AC0311)<br>• Tin foil<br>• Beaker with spout<br>• Sonicator (optional) | • **Temperature:** Room temperature (heating up acetone to 50ºC and longer sonication times have been tried without noticeable differences)<br>• **Time:** 15 min | • Gentle sonication improves the cleaning if your sample can withstand it<br>• The acetone beaker should be full enough to be stable in the sonication bath |   |
| 1.2 | Substrate cleaning | Isopropanol rinsing<br><br>Rinse the front and back of your substrate for ~30 s with isopropanol while holding the substrate with a tweezer. | • Isopropanol (Scharlab AL0311)<br>• Crystalizing dish with spout <br>• Tweezer | • **Time**: 15 – 30 s is the typical time required for this step | • Rinse the substrate with isopropanol before the acetone has evaporated |   |
| 1.3 | Substrate cleaning | Distilled water rinsing<br><br>Rinse the front and back of your substrate for ~30 s with distilled water while holding the substrate with a tweezer. | • Distilled water<br>• Crystalizing dish with spout <br>• Tweezer | • **Time**: 15 – 30 s is the typical time required for this step | • Rinse the substrate with water before the isopropanol has evaporated<br>• Typically, it is not recommend to rinse with water after isopropanol because it leaves water residues. However, we found that the isopropanol that we used has left some residues on the substrates. |   |
| 1.4 | Substrate cleaning | Substrate dehydration | • Hot plate | • **Time**: 3 - 5 min <br>• **Temperature**: 150 - 180°C | • Ensure good thermal contact between substrate and (clean) hot plate. | It is good practice to inspect your substrate after cleaning with the microscope. Especially, darkfield images can show any residual debris. Normally, there  should be no visible debris. Be aware that you might see debris from the microscopy slide below your (transparent) substrate. |
| 2. | Spin-coat resists |   | We use a spin coater and a micropipette (20 – 200 µl) with a fresh tip for each chemical | A 3–5 min dehydration bake at 150–180 °C improves resist adhesion if the sample was not dehydrated the same day [[1]](https://www.epfl.ch/research/facilities/cmi/equipment/ebeam-lithography/raith-ebpg5000/ebeam-resists-available-in-cmi/mma-pmma-resists/<br>). | • *WARNING*: The PMMA solvents are often corrosive, flammable, and irritating<br>• All following sub tasks MUST be carried out in a fume hood<br>• It is mandatory to use a fresh pipette tip for each coating step to prevent contamination |   |
| 2.1 | Spin-coat resists | Spin-coat PMMA<br><br>Spin coat PMMA for 60 s at 4000 rpm. | • Spin coater<br>• 20 – 200 µl micropipette<br>• PMMA (Allresist AR-P 679.04)<br><br>Using a micropipette is not strictly necessary but reduces waste and improves process controllability. | • **Spin time**: 60 s<br>• **Spin speed**: 2000 - 8000 rpm depending on the required thickness [[2]](./attachments/raith_exposure_parameters.pdf)<br>• **Volume**: 50 µl for a 10 x 10 mm^2 substrate | • Take care that there are no bubbles in the resist before spin coating<br>• Ensure that your substrate is hold in place by a good vacuum |   |

# Attachments

## A1: Exemplary structure
20 nm gold dots with about 200 nm pitch achieved using a slightly modified version of the process described here (optimized dose and cold development).

![SEM: 20 nm gold dots, ~200 nm pitch](./attachments/attachment_1.jpg)

## A2: Underexposure
The second pattern was exposed at a 50% higher dose than the first pattern. The first pattern is clearly underexposed as can be seen by badly defined edges and resist residues trapped below the deposited metal film.

![Underexposed pattern](./attachments/attachment_2a.png)
![Correctly exposed pattern](./attachments/attachment_2b.png)
