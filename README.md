# Wall Painting VLA

> **Eventual goal:** Train a robotic arm to paint walls autonomously using a vision-language-action model, progressively improved through real human painting video, novel reward shaping, and few-shot adaptation to new painting styles.

---

## Project Overview

Wall painting is a deceptively complex manipulation task. It requires coordinated arm movement across a large surface, consistent stroke pressure, and spatial awareness of what has and hasn't been covered. Most robotic manipulation research focuses on tabletop pick-and-place tasks — wall painting is comparatively underexplored despite being a high-value real-world application.

This project builds a VLA (vision-language-action model) for wall painting from the ground up — starting with simulation, moving to real human painting expertise captured on video, and eventually transferring to a physical robot arm.

---

## Full Roadmap

### Phase 1 - Simulation environment (COMPLETE)
Built a MuJoCo simulation environment with a Franka Panda arm and a wall surface. Implemented a 20x20 paint coverage grid. A scripted oracle policy achieves ~60% wall coverage per episode.

### Phase 2 - Demonstration data collection (COMPLETE)
Collected 600 timesteps of demonstration data. Each timestep: camera image (128x128 RGB), language instruction, robot joint positions (7-DOF), paint coverage percentage.

### Phase 3 - VLA training (COMPLETE)
Built a custom VLA: MobileNetV3 (vision) + DistilBERT (language) + MLP action head. Trained 50 epochs, loss 0.28 to 0.004, joint error under 1 degree.

### Phase 4 - Sim evaluation (COMPLETE)
Open-loop evaluation achieved 69.8% wall coverage vs 60.8% scripted baseline.

### Phase 5 - Painting quality scorer (PLANNED)
Train a quality classifier on real human painting footage using SAM2 + DINOv2 (Meta FAIR).

### Phase 6 - Policy improvement (PLANNED)
Use quality scorer as reward signal to fine-tune VLA beyond behavioral cloning.

### Phase 7 - Few-shot stroke adaptation (PLANNED)
Adapt to new painting styles from just 5-10 demonstrations.

### Phase 8 - Real robot transfer (PLANNED)
Transfer to a physical robot arm.

---

## Results

| Metric | Value |
|---|---|
| Scripted policy coverage | 60.8% |
| VLA coverage (open-loop) | 69.8% |
| Improvement over baseline | +9% |
| Training loss (epoch 0) | 0.2809 |
| Training loss (epoch 50) | 0.0040 |
| Mean joint error | <1 degree |

---

## Stack

- Simulation: MuJoCo 3.x + mujoco_menagerie (Franka Panda)
- Vision encoder: MobileNetV3 (torchvision)
- Language encoder: DistilBERT (HuggingFace)
- Training: PyTorch, behavioral cloning
- Environment: Google Colab (A100 GPU)

---

## Setup

git clone https://github.com/bhi0909/wall-paint-vla.git
cd wall-paint-vla
bash setup.sh
pip install mujoco dm_control gymnasium torch torchvision transformers
