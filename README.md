# Metamorphic Efforts: Visualizing Laban Movement Qualities from Kafka's *The Metamorphosis*

**Steffen Møgelmose**
smogel22@student.aau.dk
Department of Architecture, Design and Media Technology, Aalborg University Copenhagen, Denmark

*Embodied Interaction Mini-Project, MED8, Spring 2026*

![Figure 1: Running piece on Passage 1 (Press), showing the topographic visual texture, LMA annotation overlay (red "Strong Weight" tooltip), and the polyphonic voices mixer panel.](report/running_piece_p1.png)

**Figure 1:** Running piece on Passage 1 (Press), showing the topographic visual texture, LMA annotation overlay, and the polyphonic voices mixer panel.

## Abstract

This project presents *Metamorphic Efforts*, a generative audiovisual system that translates the opening section of Kafka's *The Metamorphosis* (10 passages) into a real-time embodied interaction experience driven by Laban Movement Analysis (LMA) Effort qualities. Conventional LMA-driven systems run from a moving body through sensors to Effort classification; this project locates the moving body in literary prose through close reading and Body, Effort, Shape, Space (BESS) annotation, then renders the resulting Effort trajectory as coordinated visual texture (TouchDesigner) and five-layer polyphonic audio (Web Audio API in the browser). The viewer reads at their own pace; passage transitions trigger BESS payloads sent over WebSocket, including four computable Effort descriptors after Larboulette and Gibet [6]. Action Drive labels select coordinated visual presets and per-passage ElevenLabs v3 audio tags grounded in de Meijer's [7] Effort-to-emotion regression findings. The system runs in two configurations: locally with a direct WebSocket between TouchDesigner and the browser, and deployed via a Node relay on Render so a public browser can connect to TouchDesigner remotely. The contribution is a demonstration that kinesthetically dense literary text can serve as annotation substrate for Effort-driven generative systems, broadening the input modality for embodied interaction beyond performed movement.

## Keywords

Laban Movement Analysis, Effort, BESS, embodied interaction, motor simulation, generative audiovisual, TouchDesigner, ElevenLabs, Twine, Kafka.

## 1. Introduction

Most embodied-interaction systems treat embodiment as gross motor movement, gesture, or physiological sensing. The user does something physical and the system responds. This project starts from a different premise: that reading literary prose about embodied experience is itself an embodied act, and that prose with sufficient kinesthetic density can serve as an Effort data source comparable to a moving body.

Cognitive linguistics provides the empirical grounding. Reading action-related sentences activates the reader's sensorimotor system through motor simulation. Tettamanti et al. [11] showed that listening to action-related sentences activates the premotor cortex somatotopically, with mouth-, hand-, and leg-related sentences producing distinct activations in the corresponding motor regions. Gallese and Lakoff [4] and Zwaan [12] extend this to a general theory of language comprehension as embodied simulation. When Kafka writes that Gregor's legs "waved about helplessly," the reader does not simply decode semantic content; their motor system partially reproduces the helpless limb movement.

Kafka's *The Metamorphosis* is unusually well suited to this approach. Every paragraph foregrounds bodily struggle. The transformation makes ordinary actions (lifting a head, rolling, opening a door) into described kinesthetic events. Beck [1] and Pawel [9] trace Kafka's interest in Yiddish theatre as a union of spoken and gestural language, supporting a sensibility already oriented toward the expressive body as a source of meaning.

The project proposes three claims. First, motor simulation is triggered in the reader's sensorimotor system by the act of reading literary prose related to embodied experience, resulting in bodily activation rather than pure semantic decoding. Second, the system is determined by the viewer's temporal and attentional engagement with the text; this is the "interaction" that initiates BESS transitions and audio events. Third, the motor simulation that is continuously in progress during reading is extended by the multi-modal output, which builds on the same Effort qualities that the text encodes. Readers read about heaviness, the visual field enacts heaviness, and the voice performs heaviness; perception, text, and body are coupled because all three channels are powered by the same Effort analysis.

A walkthrough recording is available at https://vimeo.com/1187075793.

## 2. Related Work

The project is anchored in four prior works. The first establishes the pipeline structure and is treated as the main reference; the others provide computable formulas, empirical grounding for the emotion mapping, and a structural comparator.

### 2.1 Main reference: Fdili Alaoui et al. [3]

Fdili Alaoui et al. investigate how LMA can be computationally modeled by incorporating movement expertise into multimodal sensing. Working with certified LMA practitioners, the authors create feature sets from positional, dynamic, and physiological sensor data that correlate with how experts perceive the four Effort factors (Weight, Time, Space, Flow). Their main finding is that integrating multiple data modalities yields significantly better characterization of Effort than any single channel. The paper is grounded phenomenologically in Merleau-Ponty [8] and Dourish [2]: computational systems should engage with movement as a lived, expressive phenomenon rather than functional input.

This project takes the pipeline structure (BESS annotation as structured input, Effort factors as the central parameterization, generative output as the rendering target) and changes the input modality from physical performance to literary prose. The multi-modal principle motivates the five-layer audio design and the integrated visual field described in Section 5.

### 2.2 Computable Effort descriptors: Larboulette and Gibet [6]

Larboulette and Gibet formalize the Effort descriptors as computable functions: Weight as max kinetic energy over a window, Time as summed acceleration, Space as path-to-displacement ratio, Flow as aggregated jerk. These are the formulas typically applied to motion-capture data; this project applies them to the BESS annotation trajectory, computed in JavaScript on a sliding window of the last five passages and sent to TouchDesigner alongside the raw BESS payload. The descriptor implementation is documented and reproducible via the Python script `generate_report_figures.py` in the repository, which produces bit-identical output to the JavaScript runtime.

### 2.3 Effort-to-emotion attribution: de Meijer [7]

De Meijer ran 85 naive observers rating 96 systematically varied body movements. Three of his seven dimensions (force, velocity, directness) correspond to Laban's Weight, Time, and Space. Regression analysis predicted emotion categories from feature combinations; factor analysis extracted three underlying factors: Rejection-Acceptance, Withdrawal-Approach, and Preparation-Defeatedness. De Meijer did not test Action Drives directly, so the Drive-level emotional correlates used in this project (Press to determination, Wring to grief, Glide to calm focus, Slash to fear) are interpretive applications of his regression findings, not direct empirical mappings. This honest distinction is preserved throughout the report and is one of the limitations discussed in Section 9.

### 2.4 Structural comparator: Ghostdance [10]

Siopa et al. provide the closest structural comparator. Ghostdance uses an LSTM classifier to identify Action Drives from a live dancer's IMU data and routes them to Unity particle presets and spatial audio in VR. Both projects use Action Drives as preset selectors that change the state of all output modalities at once. The central distinction is the input channel: Ghostdance uses a live body, this project uses literary prose. The two projects arrive at the same parametric framework from opposite directions: body-first and text-first.

| | Ghostdance | Metamorphic Efforts |
|---|---|---|
| Movement input | Live dancer (IMU sensors) | Literary prose (close reading) |
| Effort extraction | Real-time LSTM classification | Manual BESS annotation |
| Output medium | Unity particles in VR | TouchDesigner + ElevenLabs in browser |
| Interaction model | Dancer performs, audience watches | Viewer reads, system responds |
| Temporal control | Continuous, dancer-driven | Hybrid, viewer-paced |

## 3. Theoretical Framework

The phenomenological foundation comes from Merleau-Ponty [8], for whom perception is active bodily engagement with the world rather than passive registration of stimuli. Perception and action are co-constitutive: there is no seeing without the body that sees. Dourish [2] translates this into interaction design with the principles of embodied interaction: systems should engage with the full range of human skills and capacities for action, including the qualitative, expressive, and improvisational dimensions of bodily experience.

LMA provides the descriptive system through which the project parameterizes movement quality. LMA breaks down movement observation into four categories known as BESS: Body, Effort, Shape, and Space. Effort describes the dynamic, qualitative structure of movement through four factors: Weight (Strong/Light), Time (Sudden/Sustained), Space (Direct/Indirect), and Flow (Bound/Free). The three factors excluding Flow combine in pairs to produce Laban's eight Action Drives: Press, Flick, Punch, Float, Wring, Dab, Slash, Glide. Shape describes how the body changes form in three-dimensional space (growing/shrinking, rising/sinking, advancing/retreating). Body describes the structural organization of the mover (which parts lead and follow, how movement sequences). Space describes the mover's relationship to the spatial environment (kinesphere, dominant plane, attentional focus).

The central principle is that these categories co-constitute a single embodied experience. A Press is not three separate constructs (Strong + Sustained + Direct) but one felt quality. The project highlights this integration by rendering all BESS parameters through a single visual field rather than separate layers, and by routing the same annotation to multiple polyphonic audio voices.

The project also draws on Bakhtin's polyphony [12] as structural metaphor. Kafka's prose contains multiple simultaneous movement voices: Gregor's heavy Pressing body, the clock's metronomic ticking, the mother's ambiguous knock, the rain on the window. These do not resolve into a single Effort; they form a polyphonic texture. This is metaphorical use rather than strict Bakhtinian application, and it operates at three levels: the source text (multiple movement voices per passage), the system output (five simultaneous audio channels sharing a harmonic ground), and the methodology (single-analyst annotation as one instructive narrative voice among others).

## 4. Method

### 4.1 Pipeline

The system runs the following pipeline:

```
text → close reading → BESS annotation → Action Drive + descriptors
                                            ↓
                     TouchDesigner ←─── BESS payload (WebSocket)
                                            ↓
            browser canvas ←─── JPEG frames (WebSocket)
                                            ↓
       5 audio layers (Web Audio API): narration · body vox · drone · SFX · characters
```

Each passage is annotated for Body, Effort, Shape, and Space using normalized 0-1 values. The three Effort factors excluding Flow combine to one of Laban's eight Action Drives. Flow modulates as a continuous overlay. Across the 10 passages four Drives are used: Press (P1-4, P6), Wring (P5, P7), Glide (P8-9), Slash (P10).

### 4.2 BESS annotation

A custom browser tool (`bess_author.html`, Figure 2) was built to author the 53 annotation spans in the source. The tool loads the Twine `.twee` source, lets the analyst select text spans and tag them with BESS category, set the Action Drive and BESS slider values per passage, and outputs Twine-ready markup or JSON. Annotation is structured expert judgment rather than ground truth; the limitations of this approach are discussed in Section 9.

![Figure 2: BESS Author tool, showing Passage 1 annotation: span tagging in the text body, Action Drive selector ("press"), BESS sliders for Effort, Shape, Body, and Space, and JSON output.](report/bess_author.png)

**Figure 2:** BESS Author tool, showing Passage 1 annotation: span tagging in the text body, Action Drive selector, BESS sliders, and JSON output.

### 4.3 Worked example: Passage 1

Passage 1 (Gregor waking, transformed) is annotated as follows:

- action_drive: `press`
- flow: 0.15 (tightly Bound)
- intensity: 0.40 (moderate)
- shape_grow: 0.10, shape_rise: 0.00, shape_advance: 0.00
- body_connectivity: 0.50, body_sequencing: 0.30
- kinesphere: 0.30, space_approach: 0.90 (highly Direct), space_plane: 0.20

The Action Drive Press follows from Strong Weight (the armour-like back, the inability to move freely), Sustained Time (he *lay*, he *lifted* slowly), and Direct Space (attention focused on his own transformed body). Flow is tightly Bound: every described action can be started and stopped. The interpretive emotional correlate after de Meijer [7] is determination and heaviness. The full annotation methodology and per-passage values are documented in `report/full_report.md`.

## 5. System Architecture

Twine (SugarCube) serves as the single browser interface: text, audio, and visuals integrate in one display. TouchDesigner runs as a headless visual generator that receives BESS payloads and streams JPEG frames back via WebSocket. Audio plays from the browser via Web Audio API with five polyphonic layers, each with an independent volume slider visible to the viewer. Figure 3 shows the TouchDesigner network in the deployed configuration.

![Figure 3: TouchDesigner network with the WebSocket DAT (ws_render) connected to embodied-interaction.onrender.com:443. Live BESS values for Passage 1 visible in the right column, the noise/feedback/color processing chain in the centre, and the frame_sender Execute DAT streaming JPEGs.](report/touchdesigner_network.png)

**Figure 3:** TouchDesigner network with the WebSocket DAT connected to the Render relay. Live BESS values for Passage 1 visible in the right column, noise/feedback/color processing chain in the centre, frame_sender Execute DAT streaming JPEGs.

The system runs in two configurations.

**Local development.** TouchDesigner and browser on the same machine. Direct WebSocket on `ws://localhost:9980`. Used during development:

```
TWINE (browser, localhost:8080)
  |  Kafka text + LMA annotation overlay
  |  5 audio layers (Web Audio API)
  |  Canvas shows TD visual frames
  |
  |  ws://localhost:9980  (BESS JSON --->)
  |  (<--- JPEG frames)
  |
TOUCHDESIGNER (same machine, headless)
```

**Deployed.** Browser hosted on GitHub Pages at `mogelmose.org/Embodied-interaction/`. TouchDesigner runs on the artist's machine. A small Node relay on Render at `embodied-interaction.onrender.com/ws` matches them by `?role=browser` and `?role=td` query parameters:

```
TWINE (browser, role=browser)
        |
        |  wss://embodied-interaction.onrender.com/ws
        v
RENDER RELAY (Node, backend/)
        ^
        |  wss://embodied-interaction.onrender.com/ws
        |
TOUCHDESIGNER (artist's machine, role=td)
```

Both ends dial out to Render; neither accepts inbound connections. Application logic on both sides is identical to the local configuration; only the transport changes. This allows the piece to be experienced from any modern browser without the viewer needing to install TouchDesigner.

## 6. Mappings

The system contains seven cross-modal mappings, each grounded in a specific source contribution:

| Source | Contribution | Where it appears |
|---|---|---|
| Fdili Alaoui et al. [3] | Pipeline structure; multi-modal Effort principle | Overall architecture; 5 audio layers + visual field |
| Larboulette and Gibet [6] | Computable Effort-to-parameter formulas | Visual preset; runtime descriptor modulation |
| de Meijer [7] | Effort-to-emotion regression findings | TTS audio tag selection per passage |
| Siopa et al. [10] | Action Drive preset-selector architecture | Visual preset switching; cross-modal state |

### 6.1 Visual field

Rather than rendering each BESS category as a separate visual layer, TouchDesigner modulates a single continuous noise/feedback/color texture. Each Effort factor maps to a noise parameter following Larboulette and Gibet's computable definitions: Weight to noise amplitude and period; Time to animation speed; Space to blur and zoom; Flow to feedback decay. Each Action Drive has a stored visual preset; on Drive transition the preset is loaded and `value_lag` smooths toward the new target. The four computed descriptors (`ld_weight`, `ld_time`, `ld_space`, `ld_flow`) modulate transition behaviour continuously.

### 6.2 Polyphonic audio

The five audio layers express different movement voices:

- **Narration**: Kafka's text via ElevenLabs v3 TTS (Bradford voice). Per-passage audio tags follow de Meijer-derived emotional correlates. For Wring at P7: `[desperate, frantic], [panicked]`. For Glide at P8: `[calm, measured], [quiet, deliberate]`. For Slash at P10: `[aggressive, urgent], [exhausted, defeated], [flatly, final]`.
- **Body vocalisation**: Gregor's somatic voice as non-verbal breath, gasps, strain. Strong+Sustained yields heavy exhales; Sudden yields gasps; Bound yields constricted throat.
- **Drones**: per-Drive 60-second loops generated via ElevenLabs Music Generation, providing a sustained atmospheric ground.
- **SFX**: clock ticks (Sustained, Bound), knocks (Sudden, Direct), body scraping (Strong, Sustained), door slams (Sudden, Strong).
- **Characters**: external movement voices from P4 onward (mother's call, manager's footsteps, father's hissing, stomping, weeping). Each character has its own assigned Effort quality.

A default mix per passage authored by the analyst sets opening volumes; viewers can override any layer with the on-screen sliders, making the polyphonic structure tangible by lifting or muting voices.

## 7. Results

The BESS annotation produces a trajectory of six informative channels across the 10 passages (Figure 4). Flow rises from 0.15 (tightly Bound at P1-2) to a peak of 0.75 at P8 (the coordinated jaw-to-door effort), drops to 0.4 at P9 (the held door-opening moment), and ends at 0.65 at P10. Intensity climbs from 0.35 to a double peak of 0.8 at P6-P7, dips to 0.6 at P8, surges to 0.85 at P9, holds at 0.8 for Slash. Shape_advance climbs from 0.0 through 0.5 (getting out of bed) to 0.8 (reaching through the open door) and crashes to 0.0. Space_approach starts very high (0.9) and trends downward to 0.35 by P10.

![Figure 4: BESS value trajectory across the 10-passage arc. Six channels shown: flow, intensity, shape_advance, body_connectivity, body_sequencing, space_approach. Action Drive labels above each passage.](report/bess_trajectory.png)

**Figure 4:** BESS value trajectory across the 10-passage arc.

The four Larboulette and Gibet descriptors computed on the BESS trajectory using a five-passage sliding window are shown in Figure 5. `ld_weight` rises steadily as the piece builds toward the confrontation. `ld_time` peaks sharply at P9-P10 where intensity reaches its peak and Effort quality shifts most abruptly. `ld_flow` rises as annotated Flow values become less smooth from P5 onward. `ld_space` drops to 0 through the middle of the piece and recovers near the end. The descriptor logic is implemented identically in JavaScript at runtime and in `generate_report_figures.py` for reproducible documentation.

![Figure 5: Larboulette and Gibet descriptors computed on the BESS trajectory using a sliding window of five passages. Four channels: ld_weight (max kinetic energy), ld_time (summed acceleration), ld_space (path/displacement), ld_flow (aggregated jerk).](report/descriptors_computed.png)

**Figure 5:** Larboulette and Gibet descriptors computed on the BESS trajectory using a five-passage sliding window.

## 8. Discussion

The system demonstrates that kinesthetically dense literary text can serve as annotation substrate for Effort-driven generative systems. The Larboulette and Gibet formulas that ground the visual parameterisation are the same formulas typically applied to motion capture data; only the data source differs. This extends the input set for Effort-driven embodied-interaction systems beyond performed movement.

Three further observations emerge from running the piece. First, the polyphonic audio architecture made the multi-voice character of Kafka's prose audible in a way that the text alone cannot make explicit; lifting and muting individual layers reveals which voices carry which Effort qualities at each passage. Second, the use of de Meijer-derived emotional correlates of Effort constellations to direct ElevenLabs v3 TTS via audio tags is, to the author's knowledge, novel; the voice does not merely read the text, it performs the Effort quality of the text. Third, the deployed configuration via the Render relay shows that an embodied-interaction piece anchored in a desktop application (TouchDesigner) can be made publicly accessible without exposing the artist's machine, by using a small public relay between the local renderer and the public browser.

The proposed text-as-movement-substrate claim is bounded. Not all prose qualifies. Kafka works because every paragraph foregrounds physical struggle; texts dominated by interior monologue or psychological abstraction would not allow comparable Effort traceability. Beckett, Bernhard, and Kleist are candidates that share kinesthetic density and would be productive next tests.

## 9. Limitations

The annotation is single-analyst; there is no inter-rater reliability check. Fdili Alaoui et al. [3] used certified LMA practitioner annotation as ground truth for training their computational models; this project would be strengthened by replacing the author's annotation with a certified practitioner's, ideally with multiple annotators to enable inter-rater agreement.

The de Meijer Drive-to-emotion mapping is interpretive, not direct empirical. De Meijer tested Effort feature combinations, not Action Drives. The associations used here are plausible because Drives are constructed from the exact dimensions de Meijer measured, but the routing is interpretation, not measurement.

The `ld_flow` descriptor is computed from the jerk of the annotated flow channel itself, so it measures meta-variability of that channel rather than the Flow Effort of the described movement directly. In a sensor-based implementation, `ld_flow` would be computed from jerk of position data across all axes.

Audio uses Effort as a design-time curation principle for asset selection (which audio tags, which body vox file, which drone loop), not as a runtime control signal. Only the visual layer is continuously runtime-modulated by descriptors. Symmetry between visual and audio modulation is a worthwhile future direction.

The system is a forward chain, not a closed loop: the viewer's body state does not influence the system. A version that closes this loop through psychophysiological measurements would more fully realize Dourish's [2] embodied-interaction principle.

A planned listener evaluation was not conducted within the scope of this mini-project.

## 10. Future Work

Three directions:

**Listener evaluation.** A protocol for an N=12-15 study is drafted. Listeners would experience the piece in two conditions (visual+audio, audio only) and rate perceived Effort and emotional correlates per passage. This would test whether the Effort qualities encoded by the system are received by the listener as designed.

**Multi-text generalization.** The text-as-movement-substrate claim is bounded to kinesthetically dense prose. Testing the same pipeline on other works of art would establish whether the annotation method transfers across kinesthetically dense texts of different periods and styles.

**Closing the audio/visual asymmetry.** Currently visuals respond to descriptors at runtime while audio uses Effort only at design time. A future version could modulate granular synthesis or live audio processing parameters (filter cutoff, grain density, spatial position) directly from the descriptor stream, making the audio modulation symmetric with the visual modulation.

## 11. AI Use

The author used Anthropic Claude (LLM) for general project organization, code review, and editing of supporting documents. ElevenLabs (paid Pro tier, commercial rights) was used to generate the audio assets for narration, body vocalization, drones, and sound effects. Cursor (IDE) provided routine code completion. None of these tools were used for BESS annotation, theoretical framing, or methodological decisions of the project.

## 12. Conclusion

This project presents *Metamorphic Efforts*, a generative audiovisual system that translates the opening section of Kafka's *The Metamorphosis* into a real-time embodied interaction experience driven by Laban Movement Analysis Effort qualities. By inverting the conventional LMA pipeline and locating the moving body in literary prose rather than in a performed body, the project demonstrates that kinesthetically dense literary text can serve as annotation substrate for Effort-driven generative systems. The five-layer polyphonic audio and the integrated visual field together render the same Effort trajectory across multiple modalities, and the deployed configuration via a Render relay makes the piece publicly accessible without exposing the artist's machine. The main limitation is that the system is a forward chain rather than a closed loop, and that the annotation is single-analyst; both are addressable in future work. The contribution is methodological: extending the input set for Effort-driven embodied-interaction systems beyond performed movement to include kinesthetically dense literary prose.

## References

[1] Beck, E. T. (1971). *Kafka and the Yiddish Theater: Its Impact on His Work.* University of Wisconsin Press.

[2] Dourish, P. (2004). *Where the Action Is: The Foundations of Embodied Interaction.* MIT Press.

[3] Fdili Alaoui, S., Francoise, J., Schiphorst, T., Studd, K., & Bevilacqua, F. (2017). Seeing, Sensing and Recognizing Laban Movement Qualities. In *Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems* (CHI '17), 4009-4020.

[4] Gallese, V., & Lakoff, G. (2005). The brain's concepts: The role of the sensory-motor system in conceptual knowledge. *Cognitive Neuropsychology*, 22(3-4), 455-479.

[5] Kafka, F. (1915). *The Metamorphosis.* (D. Wyllie, Trans., Project Gutenberg edition).

[6] Larboulette, C., & Gibet, S. (2015). A Review of Computable Expressive Descriptors of Human Motion. In *Proceedings of MOCO '15*.

[7] de Meijer, M. (1989). The contribution of general features of body movement to the attribution of emotions. *Journal of Nonverbal Behavior*, 13(4), 247-268.

[8] Merleau-Ponty, M. (1945/2002). *Phenomenology of Perception.* Routledge.

[9] Pawel, E. (1984). *The Nightmare of Reason: A Life of Franz Kafka.* Farrar, Straus and Giroux.

[10] Siopa, A. et al. (2024). Ghostdance. In *Proceedings of MOCO '24*.

[11] Tettamanti, M. et al. (2005). Listening to action-related sentences activates fronto-parietal motor circuits. *Journal of Cognitive Neuroscience*, 17(2), 273-281.

[12] Zwaan, R. A. (2004). The immersed experiencer: Toward an embodied theory of language comprehension. *Psychology of Learning and Motivation*, 44, 35-62.

---

## Appendix: Installation and Running

### Requirements

- **Python 3.8+** for the local HTTP server
- **TouchDesigner 2023.x or later** (free non-commercial licence sufficient): https://derivative.ca/download
- **A modern browser** with Web Audio API and WebSocket support

### Setup

```
git clone https://github.com/smogelmose/Embodied-interaction.git
cd Embodied-interaction
```

### Running locally

The system requires three components running simultaneously: TouchDesigner (visual generator), a local HTTP server (browser host), and the browser tab itself.

1. **Start TouchDesigner.** Open `Metamorphic_Efforts.toe`. The Web Server DAT starts the WebSocket server automatically on port 9980, and the Execute DAT named `frame_sender` begins streaming JPEG frames at approximately 15 fps once a browser client connects.

2. **Start the local HTTP server** from the project root:

   macOS/Linux: `python3 -m http.server 8080`
   Windows: `start_server.bat` or `python -m http.server 8080`

3. **Open the browser** at `http://localhost:8080/Metamorphic_Efforts.html`.

### Running deployed

The deployed configuration uses GitHub Pages for the frontend (`docs/` folder, served at `mogelmose.org/Embodied-interaction/`) and a Render Node service (`backend/`) as the WebSocket relay. The frontend defaults to `wss://embodied-interaction.onrender.com/ws?role=browser`. TouchDesigner connects to the same URL with `?role=td`. The relay matches the two by role and forwards messages between them. No inbound port on the artist's machine is required.

### Optional tooling

`bess_author.html` is a self-contained browser tool for creating and editing BESS annotations on passage text. Open directly in any modern browser; no server required. It loads a `.twee` or `.txt` file, allows span tagging with BESS category and LMA label, supports per-passage Action Drive and ElevenLabs v3 voice tags, and outputs Twine-ready markup.

### License

Code is licensed under MIT. Creative content (BESS annotations, report, figures, generated audio, walkthrough video, system design) is licensed under CC BY-NC 4.0. The source text of *The Metamorphosis* (Wyllie translation, Project Gutenberg) is in the public domain.

### Repository

https://github.com/smogelmose/Embodied-interaction
