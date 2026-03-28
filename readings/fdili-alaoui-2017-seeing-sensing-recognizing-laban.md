# Paper Notes: *Seeing, Sensing and Recognizing Laban Movement Qualities*

**Authors:** Sarah Fdili Alaoui, Baptiste Caramiaux, Marcos Serrano, Frédéric Bevilacqua
**Venue:** CHI '17 - ACM Conference on Human Factors in Computing Systems, Denver, USA
**DOI:** [10.1145/3025453.3025530](https://doi.org/10.1145/3025453.3025530)

---

## What the Paper Is About

This paper investigates how Laban Movement Analysis (LMA) qualities - specifically Effort and Shape - can be perceived, sensed, and computationally recognized. The study combines a perceptual user study with a machine learning recognition system to explore the relationship between human observation of movement qualities and sensor-based classification. Participants evaluated video clips of dancers performing distinct LMA qualities, while accelerometer data from the same performances was used to train a gesture recognition model. The work bridges the subjective, phenomenological nature of LMA with quantitative signal processing, asking how much of what a trained observer *sees* in expressive movement can be *captured* by a sensor.

---

## System Architecture

| Layer | Technology | LMA Input |
|---|---|---|
| Motion capture | Accelerometers (wrist-worn) | Raw inertial signal |
| LMA focus | Effort (Weight, Space, Time, Flow) and Shape | Qualitative movement descriptors |
| Recognition model | Hidden Markov Models (HMMs) | LMA quality classes |
| Perceptual study | Video-based observer ratings | Human annotation of Effort qualities |
| Evaluation | Cross-comparison of human perception vs. sensor recognition | Agreement metrics |

---

## Connections to Embodied Interaction

### 1. The Observer as Epistemic Agent

The paper positions human perception of movement quality as an expert act - observers with LMA training reliably identify Effort qualities that untrained observers miss. This foregrounds the role of the *attuned body* in making sense of another body's expression, echoing Merleau-Ponty's intercorporeality: we perceive another's movement quality partly through resonance with our own motor repertoire.

### 2. The Gap Between Sensing and Meaning

A central tension in the paper is whether a wrist-worn accelerometer can capture what a trained human perceiver recognizes. This maps directly onto the embodied interaction critique of disembodied computation: reducing expressive movement to a signal risks losing the affective and intentional content that *constitutes* LMA Effort. The paper does not paper over this gap - it foregrounds it as a research problem.

### 3. LMA as a Bridge Vocabulary

By grounding both the human study and the computational model in LMA, the authors use Laban's framework as a shared ontology between movement practitioners and machine learning. This treats LMA not merely as a labeling scheme but as a theoretically motivated vocabulary for expressive qualities - consistent with Laban's own claim that Effort reflects the mover's inner attitude toward the four motion factors.

### 4. Implications for Interactive Systems

The recognition results inform the design of movement-responsive systems: if certain Effort qualities (e.g., Flow) are harder to classify from a single peripheral sensor, system designers must either use richer sensing or accept coarser expressivity mappings. This has direct practical relevance for any LMA-driven interactive system where the fidelity of the quality-to-output mapping depends entirely on classification accuracy.