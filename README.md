# Wall Painting VLA

> **Eventual goal:** Train a robotic arm to paint walls autonomously using a vision-language-action model, progressively improved through real human painting video, novel reward shaping, and few-shot adaptation to new painting styles.

---

## Project Overview

Wall painting is a deceptively complex manipulation task. It requires coordinated arm movement across a large surface, consistent stroke pressure, and spatial awareness of what has and hasn't been covered. Most robotic manipulation research focuses on tabletop pick-and-place tasks — wall painting is comparatively underexplored despite being a high-value real-world application.

This project builds a VLA (vision-language-action model) for wall painting from the ground up — starting with simulation, moving to real human painting expertise captured on video, and eventually transferring to a physical robot arm.

---

## Full Roadmap

### Phase 1 - Simulation environment (DONE)
Built a MuJoCo simulation environment with a Franka Panda arm and a wall surface. Implemented a 20x20 paint coverage grid that tracks which regions of the wall have been painted as the arm moves across it.

### Phase 2 - Demonstration data collection (DONE)
Collected 600 timesteps of demonstration data from a scripted sinusoidal policy. Each timestep stores: image, instruction, joint angles, and coverage percent.

### Phase 3 - VLA training behavioral cloning (DONE)
Trained a VLA (MobileNetV3 vision + DistilBERT language + 3-layer action head) via behavioral cloning on the 600 demos. Training loss: 0.2809 to 0.0040 over 50 epochs.

### Phase 4 - Simulation evaluation open-loop (DONE)
Fed saved demo images through the trained VLA and measured wall coverage. Result: 69.8% coverage vs 60.8% scripted baseline (+9% improvement).

### Phase 5 - Painting quality reward model (DONE)
Trained a MobileNetV3 regression model on 1,593 frames from YouTube painting videos (705 positive + 888 hard negatives). Best val loss: 0.0044. Scores frames 0-1 for painting quality. Used for real robot evaluation in Phase 8 where coverage percent is unavailable.

### Phase 6 - Reward-weighted fine-tuning (DONE)
Fine-tuned the VLA using coverage percent as a per-step reward weight. Steps with higher wall coverage receive higher loss weight, teaching the VLA to prioritize actions that led to good painting outcomes. Mean MAE reduced from 0.9456 to 0.0507 (94.6% reduction). Coverage-weighted MAE: 0.5972 to 0.0310.

### Phase 7 - Few-shot stroke adaptation (PLANNED)
Demonstrate that the trained policy can adapt to new painting styles from just 5-10 new demonstrations.

### Phase 8 - Real robot transfer (PLANNED)
Transfer the simulation-trained policy to a physical robot arm. Reward model from Phase 5 provides quality signal since coverage percent is not measurable on real hardware.

---

## Results

| Phase | Metric | Value |
|-------|--------|-------|
| Scripted oracle | Wall coverage | 60.8% |
| Phase 3 BC | Training loss | 0.2809 to 0.0040 |
| Phase 4 eval | Wall coverage | 69.8% (+9% over baseline) |
| Phase 5 reward model | Val loss | 0.0044 |
| Phase 6 fine-tuning | Mean MAE | 0.9456 to 0.0507 (-94.6%) |
| Phase 6 fine-tuning | Coverage-weighted MAE | 0.5972 to 0.0310 (-94.8%) |

---

## Model Weights (Google Drive)

| File | Description |
|------|-------------|
| best_model.pth | VLA after Phase 3 behavioral cloning |
| vla_finetuned_best.pth | VLA after Phase 6 reward-weighted fine-tuning |
| reward_model_v2_best.pt | Painting quality reward model Phase 5 |

---

## Stack

- Simulation: MuJoCo 3.x + mujoco_menagerie (Franka Panda)
- Vision encoder: MobileNetV3-Small (torchvision)
- Language encoder: DistilBERT (HuggingFace)
- Training: PyTorch, behavioral cloning + reward-weighted fine-tuning
- Reward model: MobileNetV3-Small regression, trained on YouTube painting videos
- Environment: Google Colab (A100 GPU)

---

## Setup

    git clone https://github.com/bhi0909/wall-paint-vla.git
    cd wall-paint-vla
    bash setup.sh
    pip install mujoco dm_control gymnasium torch torchvision transformers
