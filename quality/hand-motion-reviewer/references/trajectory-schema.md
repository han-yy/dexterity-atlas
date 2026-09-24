# Numerical review input

The CLI accepts JSON:

```json
{
  "angle_unit": "deg",
  "handedness": "right",
  "frame_convention": "palm-local, right-handed, x radial, y distal, z palmar",
  "joint_limits": {"index_mcp": [0, 80]},
  "max_joint_speed": {"index_mcp": 120},
  "bone_length_tolerance": 0.02,
  "frames": [
    {"t": 0, "joints": {"index_mcp": 0}, "bone_lengths": {"index_proximal": 0.04}, "object_quaternion_wxyz": [1,0,0,0]},
    {"t": 1, "joints": {"index_mcp": 40}, "bone_lengths": {"index_proximal": 0.04}, "object_quaternion_wxyz": [1,0,0,0]}
  ]
}
```

The values above are an input example, not universal anatomical limits. `t` is seconds. Joint speeds use angle_unit per second. Bone lengths must use one consistent length unit; tolerance is relative to the first frame. Limits and speeds are optional; absent limits produce unknown joint-limit status. When supplied, all named limit joints must exist in every frame. Additional joints without limits remain unknown.

At least two frames are needed for temporal checks. Quaternion fields and bone lengths are optional; missing measurements produce unknown results, not a pass. This schema does not include contact forces or a collision engine, so physical feasibility is always unknown. Sparse samples cannot rule out discontinuities between frames.
