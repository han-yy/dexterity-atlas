# Dexterity Atlas · 灵巧手动作图谱


## Contents

- 198 action entries across 8 categories. Authored proposals are explicitly separate from directly sourced tasks and adaptations.
- 32 working motion primitives and 43 suggested prop/equipment entries.
- 13 references with per-action locators and provenance.
- 18 simple joint-motion templates using the same 3D scene in WebGL or CPU projection; no physics-valid grasp claim.
- 33 original GRASP figure crops and 30 NinaPro motion row crops.
- CSV/JSON collection-plan exports, prop list, recording-time calculator.

`research/build_catalog.py` regenerates `data.js` and `research/catalog.json`. `quality/check_catalog.cjs` validates links between catalogue entities, local illustration presence, and sampled joint-template numerical bounds. `quality/hand-motion-reviewer` is a reusable review skill plus a numerical trajectory checker.

## Sources and limits

Feix et al. (2016), Figure 4, printed page 70: https://www.eng.yale.edu/grablab/pubs/Feix_THMS2016.pdf

NinaPro official movement chart: https://ninapro.hevs.ch/figures/SData_Movements.png

Full source metadata and exact video URLs are in the website's References view and `research/media-provenance.json`. Source images/videos remain subject to their original rights. Do not treat authored extensions, display joint limits, default timings or suggested props as paper findings. The Three.js vendor file is under the MIT License; the full license is included beside it.

The 3D templates do not model collision, tendon coupling, friction, grasp forces or individual anatomy. The reviewer reports absent physical evidence as unknown. Successful numerical or browser checks do not establish physical feasibility.
