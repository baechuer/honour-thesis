# Preserved terminal-literal format repair

The original non-parseable byte stream is retained as a base64 artifact. The canonical copy removes only the literal terminal `\\n` outside JSON, then retains one final newline. No reviewer content is changed.
