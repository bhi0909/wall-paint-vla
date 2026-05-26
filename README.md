# Wall Painting VLA

> **Eventual goal:** Train a robotic arm to paint walls autonomously using a vision-language-action model, progressively improved through real human painting video, novel reward shaping, and few-shot adaptation to new painting styles.

---

## Project Overview

Wall painting is a deceptively complex manipulation task. It requires coordinated arm movement across a large surface, consistent stroke pressure, and spatial awareness of what has and hasn't been covered. Most robotic manipulation research focuses on tabletop pick-and-place tasks — wall painting is comparatively underexplored despite being a high-value real-world application.

This project builds a VLA (vision-language-action model) for wall painting from the ground up — starting with simulation, moving to real human painting expertise captured on video, and eventually transferring to a physical robot arm.

---

## Full Roadmap

### 🟢 Phase 1 — Simulation environment
Built a MuJoCo simulation environment with a Franka Panda arm and a wall surface. Implemented a 20×20 paint coverage grid that tracks which regions of the wall have been painted as the arm moves across it. A scripted oracle policy sweeps the arm in a sinusoidal pattern, achieving ~60% wall coverage per episode.

### 🟢 Phase 2 — Demonstration data collection
Collected 600 timesteps of demonstration data from the scripted policy. Each timestep is saved as a tuple of:
- Camera image (128×128 RGB)
- Language instruction ("paint the wall")
- Robot joint positions (7-DOF)
- Paint coverage percentage

### 🟢 Phase 3 — VLA training (behavioral cloning)
Built a custom VLA architecture combining:
- **MobileNetV3** (pretrained, frozen) as the vision encoder
- **DistilBERT** (pretrained, frozen) as the language encoder
- A 3-layer MLP action head (trainable) that maps fused visual and language features to 7 joint angles

Trained for 50 epochs using behavioral cloning (imitation learning). Loss decreased from 0.28 to 0.004. Mean joint prediction error on held-out timesteps: under 1 degree.

### ⬜ Phase 4 — Sim evaluation
Run the trained VLA in simulation, replacing the scripted policy with the model's predictions. Measure wall coverage achieved by the learned policy vs the scripted baseline.

### ⬜ Phase 5 — Painting quality scorer from human video
Train a vision-based painting quality classifier on real human painting footage (1+ hour of expert painting video). The scorer will evaluate stroke evenness, coverage uniformity, and technique — providing a reward signal that goes beyond simple coverage percentage. This is a novel approach: instead of hand-crafting a reward function, we derive it directly from human expert video.

### ⬜ Phase 6 — Policy improvement via quality reward
Use the painting quality scorer as a reward signal to further fine-tune the VLA policy beyond what behavioral cloning alone achieves. The goal is to produce a robot that paints not just by copying demonstrations, but by painting the way a skilled human would.

### ⬜ Phase 7 — Few-shot stroke adaptation
Demonstrate that the trained policy can adapt to new painting styles (horizontal strokes, vertical strokes, corner technique) from just 5–10 new demonstrations. This tests the model's ability to generalize quickly to task variations — a key requirement for practical deployment.

### ⬜ Phase 8 — Real robot transfer
Transfer the simulation-trained policy to a physical robot arm. Evaluate real-world painting performance and address the sim-to-real gap.

---

## Current Results

| Metric | Value |
|---|---|
| Scripted policy coverage | 60.8% |
| Training loss (epoch 0) | 0.2809 |
| Training loss (epoch 50) | 0.0040 |
| Mean joint error (step 0) | 0.26 degrees |
| Mean joint error (step 200) | 0.97 degrees |
| Mean joint error (step 400) | 0.35 degrees |

---

## Repository Structure

```
wall-paint-vla/
├── demo_data/
│   ├── images/          # 600 PNG frames from simulation
│   └── metadata.json    # timestep data (image path, instruction, action, coverage)
├── rlds_dataset/        # demo data in RLDS format
├── setup.sh             # clones mujoco_menagerie
└── README.md
```

---

## Stack

- **Simulation**: MuJoCo 3.x + mujoco_menagerie (Franka Panda)
- **Vision encoder**: MobileNetV3 (torchvision)
- **Language encoder**: DistilBERT (HuggingFace)
- **Training**: PyTorch, behavioral cloning
- **Environment**: Google Colab (A100 GPU)

---

## Setup

```bash
git clone https://github.com/bhi0909/wall-paint-vla.git
cd wall-paint-vla
bash setup.sh   # clones mujoco_menagerie
pip install mujoco dm_control gymnasium torch torchvision transformers
```

Demo data is included in the repository. Model weights are stored separately in Google Drive due to file size.
