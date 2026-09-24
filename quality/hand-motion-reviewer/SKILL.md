---
name: hand-motion-reviewer
description: Review human or dexterous robot hand animations and recorded trajectories for action fidelity, joint geometry, coordinate conventions, contact plausibility, and source provenance. Use when checking hand motion demos, retargeted poses, or capture-action definitions; not as a substitute for a physics simulation or a clinical assessment.
---

# Hand motion reviewer

Check what the evidence supports. A smooth animation can be semantically wrong; a correct hand shape can still have impossible contacts. Report these separately.

## Inputs and claim boundaries

Read the requested action, initial state, goal, hand type, object, and cited reference. Identify whether the target is a static grasp, continuous rotation, goal orientation, palm-relative 6D goal, articulated-object change, or deformable-object change. Do not change the task to one the current renderer happens to support.

Identify the evidence: generated illustration, kinematic template, recorded trajectory, image/video reference, or simulated dynamics. Distinguish a task-specific demonstration from a project montage or analogous task. Mark authored combinations as proposals rather than literature tasks.

Use the model's own handedness, dimensions, joint limits, units, and frame transforms. Never silently assume degrees versus radians, quaternion order, robot limits, subject ROM, or the frame in which a goal was specified. If missing information prevents a conclusion, label that check **unknown** while continuing checks that do not require it.

## Review

1. **Task fidelity:** compare the beginning, contact transition, execution midpoint, endpoint, and release against the original reference. Check participating digits, thumb opposition, contact surface, active/supporting roles, and object change. For periodic motion, inspect at least four phases of a cycle. For non-periodic motion, inspect the full transition, not just the final frame.
2. **Geometry:** inspect palm, dorsal and oblique/side views of the same frames. Check digit order, thumb side, bone connectivity and lengths, flexion direction, joint limits, and trajectory continuity. Flag material intersections; distinguish intended skin contact from interpenetration. A camera rotation must not alter the pose.
3. **Motion attribution:** measure object pose relative to the palm using `T_palm_object = inverse(T_world_palm) * T_world_object`. Rotating the wrist with an object rigidly attached is transport, not in-hand reorientation. For normalized quaternions, use `2*acos(clamp(abs(dot(q,q_goal)),0,1))`; account for object symmetries only when the task specifies equivalence. Report translation and rotation separately.
4. **Contact and physics:** examine whether support persists while fingers change contacts; whether objects move before causal contact; whether articulated parts rotate around the declared joint; and whether apparent motion relies on ghost forces. Images alone cannot prove force closure, friction, torque, or stability. Require collision geometry and simulation/contact measurements before calling physics **validated**. A kinematic render can at most be **visually plausible**.
5. **Evidence and UI:** verify original source and locator; make extension/reference limitations visible beside the media. Check that playback, pause, scrub, camera controls, and unavailable-media fallbacks work. Remove or disable controls when the shown fallback cannot use them.

For structured motion data, run `scripts/check_motion.py INPUT.json` after reading [the input schema](references/trajectory-schema.md). This script checks supplied numerical constraints only. It must not infer missing physical evidence or produce a global physical pass.

## Output

Give separate `pass`, `fail`, or `unknown` for:

- source/action correspondence;
- geometry and kinematics;
- temporal/action fidelity;
- contact plausibility;
- physical feasibility.

For each failure provide frame/time, view, observed problem, likely cause, and the smallest useful correction. Attach representative frame references when available. State exactly which frames and views were examined and which checks were automated. Avoid claiming the whole action library is visually validated after inspecting only a representative action.

When a template fails to match a requested action, keep the correct source image/video available and label the template unsupported until repaired. Correct labels do not fix incorrect geometry. Do not invent a success rate or report unrun simulation as passed.
