# tldrwl (too long, didn't read/watch/listen)

## About

- [x] Summarize text with a single API call
- [x] Summarize Youtube video with a single API call
- [ ] Summarize audio with a single API call
- [x] Sync APIs
- [x] Async APIs

OpenAI has a limit on maximum number of tokens per requests, so the following strategy is employed to generate the summaries:

Split message into chunks
Gather summaries for each chunk
Summarize the summaries

## Install

```
pip install tldrwl
```

## Examples

### Youtube

```python3
#!/usr/bin/env python3
# www.jrodal.com

import asyncio
import time
from tldrwl.summarize_youtube import YoutubeSummarizer

import logging

logging.basicConfig(level=logging.DEBUG)

yt_video = "https://www.youtube.com/watch?v=6E3-MRnh8TQ"


def main_sync() -> None:
    summary = YoutubeSummarizer().summarize_video(yt_video)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main_async() -> None:
    summary = await YoutubeSummarizer().summarize_video_async(yt_video)

    print(summary)
    print(f"{summary.estimated_cost_usd=}")


async def main() -> None:
    start = time.time()
    print("Running async")
    await main_async()
    end = time.time()
    print(f"Finished async in {end - start}s")

    start = time.time()
    print("Running sync")
    main_sync()
    end = time.time()
    print(f"Finished sync in {end - start}s")


if __name__ == "__main__":
    asyncio.run(main())
```

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
