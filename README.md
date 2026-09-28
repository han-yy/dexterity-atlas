# Dexterity Atlas · 灵巧手动作图谱

Open `index.html` directly, or serve this directory with `python3 -m http.server 8766` and open `http://localhost:8766`.

GitHub Pages deployment for `han-yy`: see [中文部署步骤](DEPLOY_GITHUB_PAGES.md). The upload-ready ZIP has `index.html` at its root and requires no build. Deployment has not been performed on GitHub.

The action catalogue, illustrations and 3D joint template are local. Official experiment videos, original source links and optional web fonts require internet access. The website falls back to system fonts and source links when external resources are unavailable. Personal collection lists are stored in the current browser, not synced to a server.

## Contents

- 251 action entries across 8 categories. Authored proposals are explicitly separate from directly sourced tasks and adaptations.
- 40 working motion primitives and 107 suggested prop/equipment entries.
- 25 references with per-action locators and provenance.
- 18 simple joint-motion templates using the same 3D scene in WebGL or CPU projection; no physics-valid grasp claim.
- 33 original GRASP figure crops and 30 NinaPro motion row crops.
- CSV/JSON collection-plan exports, prop list, recording-time calculator.

`research/build_catalog.py` regenerates `data.js` and `research/catalog.json`. `quality/check_catalog.cjs` validates links between catalogue entities, local illustration presence, and sampled joint-template numerical bounds. `quality/hand-motion-reviewer` is a reusable review skill plus a numerical trajectory checker.

Version 1.4 adds clearly labelled AI teaching illustrations and an independent [hand anatomy reviewer](quality/hand-anatomy-reviewer/SKILL.md). Every visible hand is checked for five distinct digits, proportions, connectivity, joint structure, handedness and framing. Unresolved occlusion requires review; any failure rejects publication. An approval is bound to the exact image hash, and action-fidelity approval is also required. [Usage and tests](quality/ANATOMY_REVIEW.md) explain what the visual agent and report validator each check. This is qualitative image QA, not a trained detector with a measured recall rate or a physics certificate.

The image campaign is incomplete. Exact generated, published and remaining counts are recorded in `research/illustration-audit.json`; the plan contains 142 actions whose previous media did not provide a sufficiently specific illustration. Rejected or pending images stay outside the public gallery and deployment ZIP. Original sources remain selectable. The full development folder retains review fixtures and failed variants for reproducibility; the deployment ZIP includes only approved generated pictures.

## Sources and limits

Feix et al. (2016), Figure 4, printed page 70: https://www.eng.yale.edu/grablab/pubs/Feix_THMS2016.pdf

NinaPro official movement chart: https://ninapro.hevs.ch/figures/SData_Movements.png

Full source metadata and exact video URLs are in the website's References view and `research/media-provenance.json`. Source images/videos remain subject to their original rights. Do not treat authored extensions, display joint limits, default timings or suggested props as paper findings. The Three.js vendor file is under the MIT License; the full license is included beside it.

The 3D templates do not model collision, tendon coupling, friction, grasp forces or individual anatomy. The reviewer reports absent physical evidence as unknown. Successful numerical or browser checks do not establish physical feasibility.

Version 1.1 adds a 14-family dexterity coverage map (50 linked core actions) and 12 source-backed entries. See [更新记录](CHANGELOG.md) for corrected navigation, new demonstrations and remaining coverage gaps.

Version 1.2 imports Play2Perfect, ADEPT, WM-Craftnet and TeleDexter: 21 new action entries, 7 enriched existing actions, 32 new props, source-specific media switching, and searchable object provenance. Task, subtask and condition entries are distinguished. Version 1.2 had 107 direct tasks, 13 adaptations and 111 proposals. See `research/project-import-audit.json`.

Version 1.3 adds the ActionSense study page (`#actionsense`): all 20 original activity labels map to 13 complete activity entries. There are 20 new entries (12 complete activities, 4 authored capture subactions, 4 calibration protocols), 5 enriched existing entries, 3 new working primitives, and 28 new props/equipment. The catalogue now has 125 direct entries, 20 adaptations and 106 proposals. Calibration is separate from the 20 kitchen labels.

`research/actionsense-mapping.json` and `research/actionsense-labels.csv` preserve original English labels, material conditions, action IDs, props and citation locators. Per-task phases are authored capture proposals, not original fine-grained ground truth. Official video is a human activity montage, not a robot rollout or individually clipped subaction demonstration.

ActionSense data/media and the atlas's translated ActionSense label mapping and derived decomposition are attributed to DelPreto et al., NeurIPS 2022 / MIT and provided under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Remote original videos/images are not edited or bundled. This attribution/license does not replace the licenses of unrelated code or other datasets. Sensor availability and hand-tracking limitations are visible on the ActionSense page.
