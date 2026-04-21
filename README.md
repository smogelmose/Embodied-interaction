# Embodied Interaction

Repository for the Embodied Interaction course at AAU Copenhagen - exploring bodily presence, movement quality, and designing and evaluating embodied systems.

## About

This repository documents my work for the Embodied Interaction course at Aalborg University Copenhagen (MED8, Spring 2026).

# Mini-Project

## Metamorphic Efforts

**Visualizing Laban Movement Qualities from Kafka's *The Metamorphosis***

*Embodied polyphony: enacting the kinesthetic body of prose.*

Embodied Interaction Mini-Project, MED8, Aalborg University Copenhagen, Spring 2026

Website: [mogelmose.org](https://mogelmose.org) | [Full report](report/full_report.md)

---

## 1. Main Reference

**Fdili Alaoui, S., Francoise, J., Schiphorst, T., Studd, K., & Bevilacqua, F. (2017). "Seeing, Sensing and Recognizing Laban Movement Qualities." In *Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems* (CHI '17). ACM, 4009--4020.**

Fdili Alaoui et al. investigate how Laban Movement Analysis (LMA) can be computationally modeled by integrating movement expertise into multimodal sensing systems. Working with certified LMA practitioners, they design feature sets from positional, dynamic, and physiological sensor data that correlate with how experts perceive Laban Effort qualities: Weight, Time, Space, and Flow. Their evaluation shows that combining multiple data modalities characterizes Effort significantly better than any single modality alone. The paper follows a phenomenological position (Merleau-Ponty, Dourish): computational systems should engage with movement as lived, expressive experience, not reduce it to functional input.

### What I take from this paper

Two things. First, the **pipeline structure**: BESS annotation as structured input, Effort factors as the central parameterization, generative output as the rendering target. Where their work goes from physical body to sensors to Effort classification, this project locates the moving body in literary prose - Kafka's text encodes physical struggle in precise kinesthetic language. The close reading extracts Effort qualities through the same BESS framework used for physical bodies, and the generative system renders them.

Second, the **multi-modal principle**: their finding that multiple modalities characterize Effort better than any single channel motivates the five-layer audio design and the integrated visual field. Each Effort factor is expressed simultaneously across narration (vocal delivery), body vocalizations, drone timbre, sound effects, character voices, and the visual noise texture. No single channel carries the full Effort signature alone.

## 2. Supporting References

### Siopa et al. (2024). "Ghostdance." In *Proceedings of MOCO '24*.

In Ghostdance, a live VR dance performance, an LSTM classifier identifies the eight LMA Action Drives from a dancer's IMU data and routes them to Unity particle system presets and spatial audio in real time. The pipeline runs: live body to classification to audiovisuals.

**What I take:** the **Action Drive preset-selector architecture**. Each of the eight Action Drives is a discrete preset that triggers a coordinated cross-modal state change. My project adopts this pattern directly: when a Twine passage transitions, its annotated Action Drive selects a visual preset (noise amplitude, speed, blur, zoom, color) and an audio configuration simultaneously. The difference is the input stage: close reading replaces LSTM classification, and TouchDesigner noise/feedback replaces Unity particle swarm.

| | Ghostdance | Metamorphic Efforts |
|---|---|---|
| Movement input | Live dancer (IMU sensors) | Literary prose (close reading) |
| Effort extraction | Real-time LSTM classification | Manual BESS annotation |
| Output medium | Unity particles + spatial audio in VR | TouchDesigner noise/feedback + ElevenLabs TTS in browser |
| Interaction model | Dancer performs, audience watches | Viewer reads, system responds |

### Larboulette & Gibet (2015). "A Review of Computable Expressive Descriptors of Human Motion." In *Proceedings of MOCO '15*.

Provides formalized, computable definitions for each Effort descriptor: Weight as maximum kinetic energy, Time as summed acceleration, Space as path-to-displacement ratio, Flow as aggregated jerk.

**What I take:** the **parameter mappings** for the visual preset table. Each TouchDesigner parameter encodes the same physical quantity that the Effort factor measures in a moving body:

| Effort factor | Computable definition | TD parameter | Strong/Sudden/Indirect end | Light/Sustained/Direct end |
|---|---|---|---|---|
| Weight | Max kinetic energy | Noise amplitude, period | High amp, large period | Low amp, fine grain |
| Time | Summed acceleration | Noise animation speed | Fast | Slow |
| Space | Path/displacement ratio | Blur, zoom | Diffuse, wide | Sharp, tight |
| Flow | Aggregated jerk | Feedback decay | Fast decay (Bound) | Slow decay (Free) |

### De Meijer (1989). "The contribution of general features of body movement to the attribution of emotions." *Journal of Nonverbal Behavior*, 13(4), 247--268.

Demonstrates that naive viewers attribute stable, predictable emotions to movement sequences based on their Effort constellations alone, without knowing any context.

**What I take:** **validation that the emotional arc is predicted by the Effort data**, not imposed by interpretation. The passage sequence (Press to Wring to Glide to Slash) carries measurable emotional signatures (determination to anguish to calm to shock). This also grounds the ElevenLabs TTS vocal direction: tag selection per passage (e.g., breathless/strained for Wring, calm/flowing for Glide) follows de Meijer's empirical correlates.

## 3. Implementation

The project extracts Effort Action Drives from the opening section of Kafka's *The Metamorphosis* (10 passages) through close reading and full BESS annotation, then renders them as a generative audiovisual experience.

### System architecture (v2)

Twine (SugarCube) is the single browser interface: text, audio, and visuals all appear in one window. TouchDesigner runs headless on the same machine, generating visuals and streaming JPEG frames to the browser via WebSocket. Audio plays from the browser using Web Audio API with five polyphonic layers (narration, body vocalizations, drones, SFX, character voices) under optional viewer volume control.

```
TWINE (browser, single interface)
  |  Kafka text + LMA annotation overlay
  |  5 audio layers (Web Audio API)
  |  Canvas shows TD visual frames
  |
  |  WebSocket text: BESS JSON --->
  |  <--- WebSocket binary: JPEG frames
  |
TOUCHDESIGNER (headless, same machine)
  |  Receives BESS, updates noise/feedback/color chain
  |  Encodes final_out as JPEG
```

### Mapping derivations summary

| Source | What it contributes | Where it appears |
|---|---|---|
| Fdili Alaoui et al. (2017) | Pipeline structure; multi-modal Effort expression | Overall architecture; 5 audio layers + visual field |
| Larboulette & Gibet (2015) | Computable Effort-to-parameter formulas | Visual preset table (amp, period, speed, blur, zoom, feedback) |
| De Meijer (1989) | Empirical Effort-to-emotion mapping | Emotional arc validation; TTS vocal tag selection |
| Siopa et al. (2024) | Action Drive preset-selector architecture | TD preset lookup; coordinated cross-modal state changes |

### Embodied interaction argument

The theoretical grounding is Merleau-Ponty's phenomenology of perception, channeled through Dourish's (2004) embodied interaction framework. Perception is active bodily engagement, not passive reception. Reading Kafka's kinesthetic prose activates motor simulation (Gallese & Lakoff, 2005; Zwaan, 2004), making the act of reading a site of embodied experience. The system treats this literary movement data as computationally legible through the same BESS framework used for physical bodies, and the viewer's temporal engagement with the piece (pacing, attending, progressing) is itself a form of bodily participation in the unfolding Effort arc.

This extends the concept of "embodied interaction" beyond gross motor movement, gesture, and touch to include the kinesthetic imagination activated by literary reading.

## 4. Additional References

- Dourish, P. (2004). *Where the Action Is: The Foundations of Embodied Interaction.* MIT Press.
- Gallese, V. & Lakoff, G. (2005). "The brain's concepts: The role of the sensory-motor system in conceptual knowledge." *Cognitive Neuropsychology*, 22(3-4), 455--479.
- Larboulette, C. & Gibet, S. (2015). "A Review of Computable Expressive Descriptors of Human Motion." *Proceedings of MOCO '15*.
- Merleau-Ponty, M. (1945/2002). *Phenomenology of Perception.* Routledge.
- Subyen, P. et al. (2011). "EMVIZ: The Poetics of Movement Quality Visualization." *Eurographics Workshop on Computational Aesthetics*, 121--128.
- Zwaan, R. A. (2004). "The immersed experiencer: Toward an embodied theory of language comprehension." *Psychology of Learning and Motivation*, 44, 35--62.

## Course

**Aalborg University Copenhagen**  
MED8 – Embodied Interaction  
Spring 2026

## License

MIT License — see [LICENSE](LICENSE) for details.
