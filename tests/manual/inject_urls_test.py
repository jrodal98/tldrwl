#!/usr/bin/env python3
# www.jrodal.com

from tests.manual.test_helper import run_tests

text = "This is my website: https://www.jrodal.com/ and this is one of my posts: https://www.jrodal.com/posts/how-to-deploy-rocket-rust-web-app-on-vps/ and this is a yt video: https://www.youtube.com/watch?v=--khbXchTeE"  # noqa

if __name__ == "__main__":
    run_tests(text)
