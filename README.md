# tldrwl (too long, didn't read/watch/listen)

## About

- [x] Summarize text with a single API call
- [ ] Summarize video with a single API call
- [ ] Summarize audio with a single API call
- [x] Sync APIs
- [x] Async APIs

## Install

```
pip install tldrwl
```

## Examples

### Text

```python3
#!/usr/bin/env python3
# my_script.py

from tldrwl.summarize_text import TextSummarizer

text = "<my text to summarize here>"
summary = TextSummarizer().summarize_text(text)
print(summary.final_summary)
```

```bash
OPENAI_API_KEY="..." python3 my_script.py
```
