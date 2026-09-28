---
name: hand-anatomy-reviewer
description: Review generated hand illustrations or hand-motion frames for digit count, finger proportions, anatomical connectivity, handedness and frame consistency. Use for visual hand QA before publishing; report occlusion and perspective uncertainty rather than certifying hidden anatomy or physical validity.
---

# Hand anatomy reviewer

Act as an independent visual reviewer. Open the actual image at full resolution; a prompt, filename, landmark detector or previous approval is not evidence. For a teaching plate inspect **every panel and every hand**, including the supporting hand. Do not change the action to fit a flawed image. Use the supplied intended hand type; this project's generated human examples require five digits. Do not apply the five-digit assumption to a robot whose actual design differs.

Read [the report format](references/report-format.md) before writing a review. Use the source/action description to identify the expected number of hands and panels. For a single image, annotate normalized panel and hand bounding boxes so every finding is locatable. Inspect the full hand and wrist, then zoom the image if a contact or digit is ambiguous. Do not use a generated replacement as evidence of the original.

## Required visual checks

1. **Count and trace digits separately.** Trace thumb, index, middle, ring and little finger from a unique base through the visible chain to its tip. Count neither nails nor silhouette bumps as independent proof. Record a short visual trace for each digit and whether it is visible, traceable across a small occlusion, or unresolvable. Catch four/six digits, duplicated fingertips, two thumbs, a finger branching into two, merged digits, floating fingertips and a digit borrowed from the other hand. If a fully hidden finger cannot be distinguished, use `unknown`; never invent it to reach five.
2. **Connectivity and joints.** Four fingers originate in an ordered row across the distal palm; the thumb arises from the radial side and opposes the fingers. Human finger phalanges follow three segments, thumb two; don't mistake palm creases or shading for joints. Check continuity, plausible bends, misplaced nails, inversions, impossible bone elongation and finger–finger/object intersections. Do not infer exact joint angles from a single view.
3. **Length relationships — mandatory for every hand.** Follow a finger's curved centerline from its anatomical base, not a straight wrist-to-tip distance. Compare comparable, similarly posed fingers; explicitly account for flexion and foreshortening. Flag obvious stub fingers, an implausibly long little finger, a stretched thumb, extra-long middle segments or lengths changing between frames. The middle finger is usually longest and the little finger usually shorter, but these are plausibility cues, not rigid numeric laws. Index versus ring length varies normally: **never enforce a fixed ordering or ratio**. If a view cannot resolve a suspicious relationship, mark `unknown` and request a clearer view/redraw. Do not invent millimetres, ratios or clinical thresholds. A qualitative pass means the visible proportions are plausible, not measured anatomical accuracy.
4. **Handedness.** Determine palm/dorsal view and trace thumb origin before naming left/right; image-left thumb alone is insufficient for oblique/dorsal views. Across a sequence the same hand must retain its side and identity unless the task explicitly uses two hands. Catch left/right swaps even when each panel separately has five plausible digits.
5. **Completeness and continuity.** Fingertips, palm, wrist and a short forearm must fit in every teaching panel. A finger hidden by its own grip is an occlusion, not a crop, but unresolved anatomy still cannot pass. Check a consistent number of hands, no detached wrist, no digit birth/disappearance or implausible length change across frames. For video report exactly the timestamps inspected; sampled-frame review does not approve uninspected frames.

## Decision and repair

- `reject`: any required check fails. Record panel, hand, digit, visible evidence, issue code and the smallest useful correction.
- `needs_review`: no explicit failure, but a required anatomical check is `unknown`. Keep it out of the site's approved illustration set until resolved.
- `approve`: every required check is a visually supported `pass`, with per-digit traces and a separate length observation for every hand. Do not say "physically validated" or "guaranteed anatomically correct".

Write a structured JSON report bound to the exact file's SHA-256. Run `scripts/check_report.py REPORT.json --asset IMAGE.png`; this checks report completeness, image binding and the publication decision. **The script does not see or count fingers**; those judgments must come from actual visual examination. Regenerated images require new inspection and a new hash-bound report. Do not copy a previous pass to a new version.

For this atlas, the catalog builder must publish only records with both action-fidelity approval and an `approve` anatomy report. Record rejected variants separately, preserving the original reference video/image. Correct anatomy does not prove that a hand performs the intended action; run hand-motion-reviewer separately for semantic/contact checks.

## Reference boundaries

- [Gillam et al., human digit lengths](https://onlinelibrary.wiley.com/doi/10.1111/j.1469-7580.2008.00940.x): primary study on digit lengths and variation; supports avoiding a fixed index/ring ordering, not universal model thresholds.

This is QA for generated teaching assets, not an assessment of a real person's health or a detector with a measured recall rate. Never claim it catches every possible deformation.
