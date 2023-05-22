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

import asyncio
from tldrwl.summarize_text import TextSummarizer

text = "<my really long text>"

def main_sync() -> None:
    summary = TextSummarizer().summarize_text(text)

    print(summary)
    print(summary.estimated_cost_usd)

async def main_async() -> None:
    summary = await TextSummarizer().summarize_text_async(text)

    print(summary)
    print(summary.estimated_cost_usd)


async def main() -> None:
    await main_async()
    main_sync()

if __name__ == "__main__":
    asyncio.run(main())
```

```bash
OPENAI_API_KEY="..." python3 my_script.py
```
