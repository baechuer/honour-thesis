# V7 Machine B microbatch 012 format-repair preservation

This archive preserves the exact pre-normalisation bytes of twelve Reviewer-B target-blind returns. Each original is base64 encoded, then hash-replayed. The repair removes only a terminal literal `\n` outside the closing JSON object and writes one terminal newline, making the already-complete JSON object parseable. No assessment, packet binding, token, source anchor, or reviewer-output canonical digest changed.
