# Anatomy review JSON

Save one report per asset under `quality/anatomy-reviews/`. Fields below are required. Do not copy the example's judgments without inspecting the image.

```json
{
  "version": "1.0",
  "asset": "assets/generated/I05-v2.png",
  "sha256": "actual lowercase SHA-256 of the image bytes",
  "action_id": "I05",
  "reviewer": "hand-anatomy-reviewer / visual model review",
  "expected_panels": 3,
  "expected_hands_per_panel": [1, 1, 1],
  "panels": [
    {
      "panel": 1,
      "bbox": [0.0, 0.0, 0.33, 1.0],
      "hands": [
        {
          "hand_id": "H1",
          "side": "left",
          "view": "palm oblique",
          "bbox": [0.01, 0.05, 0.32, 0.97],
          "digits": {
            "thumb": {"visibility": "visible", "trace": "Describe its actual base, bend and tip location."},
            "index": {"visibility": "traceable", "trace": "Describe actual visible continuity and any limited occlusion."},
            "middle": {"visibility": "visible", "trace": "..."},
            "ring": {"visibility": "visible", "trace": "..."},
            "little": {"visibility": "visible", "trace": "..."}
          },
          "count_observation": "What exactly was counted, including any extras.",
          "length_observation": "Compare actual visible finger/segment lengths while accounting for pose and perspective.",
          "joint_observation": "Observed connectivity, joints and any intersections.",
          "checks": {
            "five_digits": "pass",
            "connectivity": "pass",
            "proportions": "pass",
            "joint_structure": "pass",
            "handedness": "pass",
            "framing": "pass"
          },
          "issues": []
        }
      ]
    }
  ],
  "sequence": {"status": "pass", "observation": "Describe side, digit identity and length consistency across every panel."},
  "decision": "approve",
  "limitations": "Single-view visual assessment; hidden geometry, exact lengths and physical feasibility are not measured."
}
```

Include all panels. Boxes are `[x0,y0,x1,y1]`, normalized to the whole image; bound them to `[0,1]`. Each required check is `pass`, `fail`, or `unknown`. `visibility` is `visible`, `traceable`, or `unresolvable`. Every non-pass needs an issue with `code`, `check`, `evidence`, `correction`. Codes include `digit_count`, `duplicate_digit`, `missing_digit`, `merged_digits`, `length_ratio`, `segment_length`, `joint_topology`, `handedness_swap`, `cropped_hand`, `ambiguous_occlusion`, `interpenetration`.

For sequence failure add `issues` under `sequence`, including the affected panel numbers. A hand side may be `unknown` only with a non-pass handedness check. There is no numeric "anatomical confidence score"; qualitative evidence and uncertainty are the output.
