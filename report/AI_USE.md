# AI Systems Use Disclosure

**Project:** Metamorphic Efforts: Visualising Laban Movement Qualities from Kafka's *The Metamorphosis*
**Author:** Steffen Møgelmose (smogel22@student.aau.dk)
**Course:** MED8 Embodied Interaction, Aalborg University Copenhagen, Spring 2026

In accordance with Aalborg University's guidelines on the responsible use of AI in academic work, this document discloses the use of AI-assisted tools and generative AI in the development of *Metamorphic Efforts*. The disclosure adheres to the principle that any AI use that materially influences the academic output should be disclosed, while routine assistance, such as spell-checking, code completion, or web search, does not require inclusion.

## Tools used

### Anthropic Claude (LLM)

**Used for:** general project organization (Notion sub-pages, Obsidian vault structure), code review and debugging support for the JavaScript and TouchDesigner Python callbacks, and structuring and editing sections of the portfolio report.

**Not used for:** the close reading and BESS annotation of *The Metamorphosis*, the theoretical framing and foundation of the project, the choice of Laban Movement Analysis as the descriptive system, the design of the cross-modal mappings, or the methodological decisions documented in the report.

### ElevenLabs (text-to-speech, music generation, sound effects generation)

**Used for:** generating the audio assets that constitute four of the five output layers of the running system: narration (v3 TTS, Bradford voice), body vocalisation (v3 TTS, Bradford voice), drone textures (Music Generation, 60-second loops per Action Drive), sound effects (SFX Generation), and the mother's voice in Passage 4 (v3 TTS, Jane voice). The v3 audio tag selection per passage follows interpretive emotional correlates of Laban Action Drives derived from de Meijer (1989), as documented in the report.

**Tier and rights:** generation was performed on a paid Creator/Pro subscription, which grants commercial rights to the output. The voices used are ElevenLabs library voices, not custom clones.

**Not used for:** the choice of which audio tags map to which Action Drive (this is the author's interpretive application of de Meijer's regression findings), the polyphonic mixing arrangement, or the per-passage default mix levels.

### Cursor (IDE) or comparable code-completion tools

**Used for:** routine code completion during JavaScript and Python development, in a manner equivalent to standard IDE autocompletion.

**Not used for:** the architectural decisions in the system (single-window Twine integration, WebSocket-based TD streaming, sliding-window descriptor computation, the Render relay pattern for deployment).

## Statement of responsibility

The author acknowledges that the academic claims, theoretical arguments, methodological decisions, and final form of the work are their own.

---

*Last updated: 2026-04-29*
