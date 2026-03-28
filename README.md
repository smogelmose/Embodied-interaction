# Embodied Interaction

Repository for the Embodied Interaction course at AAU Copenhagen - exploring bodily presence, movement quality, and designing and
evaluating embodied systems.

## About

This repository documents my work for the Embodied Interaction course at Aalborg University Copenhagen (MED8, Spring 2026).

## Contents

### Mini-Project

Individual implementation of an embodied interaction concept,
grounded in an academic reference and demonstrated through a
working prototype.

*Metamorphic Efforts: Visualizing Laban Movement Qualities from Kafka's The Metamorphosis*

The project extracts Laban Effort Action Drives from Kafka's *The Metamorphosis* by conducting a close reading and a full BESS (Body, Effort, Shape, Space) annotation of key passages. It then converts these qualities into generative audiovisuals using TouchDesigner. The pipeline inverts Fdili Alaoui et al. (2017): rather than body → sensors → Effort classification, the flow is text → close reading → BESS annotation → generative audiovisual output.

The claim is that Kafka's prose encodes the same movement qualities that a sensor system would capture from a moving body. Fdili Alaoui et al.'s framework for translating embodied movement expertise into computable parameters provides the theoretical bridge between literary movement description and generative media. Based on de Meijer's (1989) empirical Effort-to-emotion mapping, the passages are chosen for a five-minute prototype exploring Effort Action Drives. The TouchDesigner implementation uses a multi-layer visual architecture together with multi-layer ElevenLabs audio.

In Siopa et al.'s *Ghostdance* (MOCO '24), a live VR dance performance, an LSTM classifier picks out the same eight LMA Action Drives from a dancer's live IMU data and controls a Unity particle swarm and spatial audio system in real time. Ghostdance goes live body → classification → audiovisuals; this project flips the sensing stage so that literary prose is the sensor and close reading is the classifier.

- [Fdili Alaoui et al. (2017) — Seeing, Sensing and Recognizing Laban Movement Qualities](readings/fdili-alaoui-2017-seeing-sensing-recognizing-laban.md)
- [Siopa et al. (2024) — LMA driven Dynamic Audiovisuals in a VR Live Dance Performance: Ghostdance](readings/ghostdance-moco24-notes.md)

**Website:** [https://mogelmose.org](https://mogelmose.org)  
**GitHub:** [https://github.com/smogelmose/Embodied-interaction](https://github.com/smogelmose/Embodied-interaction)

## Course

**Aalborg University Copenhagen**  
MED8 – Embodied Interaction  
Spring 2026

## License

MIT License — see [LICENSE](LICENSE) for details.