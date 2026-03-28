# Paper Notes: *LMA driven Dynamic Audiovisuals in a Virtual Reality Live Dance Performance: Ghostdance*

**Authors:** José Siopa, Rui F. Antunes, Cecília de Lima, João Carrilho, Ana Paula B. Cláudio, Maria Beatriz Carmo  
**Venue:** MOCO '24 — 9th International Conference on Movement and Computing, Utrecht, Netherlands  
**DOI:** [10.1145/3658852.3659081](https://doi.org/10.1145/3658852.3659081)

---

## What the Paper Is About

Ghostdance is a live VR dance performance in which a human dancer interacts with a virtual avatar of their absent partner. The system consists of three layers: (a) a dancer–avatar duet, (b) a particle swarm visualization of the dancer's body driven by Laban Effort classification, and (c) spatial audio sonification of movement. In real time, a pretrained LSTM neural network identifies the eight LMA Action Drives — Punch, Slash, Dab, Flick, Press, Wring, Glide, and Float — based on the dancer's live movements. The classifications are then used to change the color, frequency, and amplitude of sound particles.

---

## System Architecture

| Layer | Technology | LMA Input |
|---|---|---|
| Motion capture | XSens Awinda IMU suit (17 body points) | Raw skeletal data |
| Effort classification | LSTM neural network (1350 training samples) | 8 Action Drive classes |
| Visuals | Unity Visual Effect Graphs (particle swarm on avatar mesh) | Action Drive → color, lifetime, velocity |
| Audio | FAUST plugin in Unity3D (per-limb audio grains) | Action Drive → frequency, amplitude, envelope |
| VR performance | Meta Quest / HTC Vive | Dancer sees absent partner's avatar |

---

## Connections to Embodied Interaction

### 1. The Body as Computational Site

The entire system's input interface is the dancer's physical body — not a controller, but the expressive material from which audiovisual meaning is generated. This is a direct reflection of Dourish's embodied interaction: the system's significance is inextricably linked to the bodily act that generates it. The body is the generative substrate, with the particle visualization literally growing from the surface of the performer's skin mesh.

### 2. Phenomenology of Absence and Presence

The core performance question — *"What happens when one of the bodies in a duet is physically absent yet visually present?"* — is fundamentally phenomenological. It directly addresses Merleau-Ponty's body schema and intercorporeality: how does the body align itself with a partner it can see but not touch or feel? Framing this as a "ghostly entity" renders it a live experiment in virtual co-presence.

### 3. Effort as Expressive Meaning

By employing LMA Action Drives as the classification unit, the system approaches movement as *expressive quality* rather than functional input (position, velocity). This is the computational embodiment of Laban's own phenomenological claim: that Effort qualities are the affective dimension of movement and cannot be reduced to kinematics alone.

### 4. Real-Time Feedback Loop

The audiovisual response to movement forms a closed feedback loop between the dancer's body and its virtual representation. The performer shapes the swarm; the swarm shapes the space the performer inhabits. This bidirectional coupling — where agent and environment co-constitute each other — is characteristic of enactive systems.