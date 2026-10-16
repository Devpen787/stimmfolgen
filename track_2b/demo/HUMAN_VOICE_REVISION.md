# Participant audio revision - 16 October 2026

The participant requested replacing synthetic narration with their own recorded audio at the existing submitted video URL. The requested Downloads/StimmFolgen-voice.m4a was absent. A project recording saved moments before the request was found at Desktop/Hackathon_StimmFolgen.mov (124.864209 seconds). Its audio was used; its screen video was not published. The raw recording remains local.

The existing genuine browser-capture footage was retained and globally retimed by 1.038285. Audio was sped up by 1.044889 using pitch-preserving atempo and normalised with loudnorm I=-16:TP=-1.5:LRA=11. Speech was not trimmed. Output: 119.500 seconds, 1280x720 H.264, AAC, faststart. Representative frames and signal levels were checked. No claim of a verified verbatim transcription or perceptual listening review is made. Prior synthetic-cut captions are not attached to the new audio.

The original submitted synthetic-narration cut is preserved byte-for-byte as StimmFolgen_Live_Demo_Submitted.mp4 and publicly at /demo-submitted.mp4. Its SHA-256 remains 90d17cec0ce8bd6f3d2de3d6768287b96111a0aa05e19894337041f257005027. The original tested submission commit 9e1c608 remains unchanged.

**This voice-only revision was prepared/published after the 16 October noon CEST deadline.** The public player explicitly discloses that timing and links the original. Organiser acceptance of the revision is not established. No duplicate submission or false pre-deadline claim was made. No model/runtime, source wordings, private vaults, quotas or submitted PDF were changed.

The replacement audio is participant-supplied; development never synthesised or cloned the participant's voice. The exact file/source hashes are in StimmFolgen_Live_Demo-metadata.json. Reproduction uses the participant's private local input and must not assume it is part of this public repository.


Deployment verified: Worker f00684cc-68fb-477a-b7b4-5792fd77cae5. Production /demo.mp4 returned HTTP 200 and matched SHA-256 811346e933e863a2c6011de9117ae734c9b6f7ab7a0885a4969f8dc5eb8c07e7. The original /demo-submitted.mp4 also matched its preserved SHA. The browser player loaded 119.5 seconds with readyState 4 and no media error. Upload initially retried EPIPE/connect-timeout failures, then completed. These were transport failures, not an altered deadline timestamp.

The participant subsequently reported distracting background noise. A local-only speech-denoised comparison and full draft were prepared for listening review, using FFmpeg arnndn and the GregorR/rnnoise-models somnolent-hogwash model. Audio remains local during processing; no voice cloning or paid service is used. This denoised draft is **not published** by this commit; the current public video remains the first participant-audio mix. The assistant cannot perform a perceptual listening review in this session, so no subjective audio-quality pass is claimed.
