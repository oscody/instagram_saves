#!/usr/bin/env python3
"""Read the posts shared in one Instagram DM chat through headless Firefox.

Fallback for export_chat_links.py when the app API fails; run that script with --browser to use it.
It opens the chat on a throwaway copy of the Firefox profile (so the real profile and its login are
never touched) and reads Instagram's own in page data store (Relay): each SlideMessage links to
content, then xma, which holds the post URL (target_url) and author (header_title_text). Shared
posts on screen are cards without links, so the page HTML alone has no URLs.

A page load holds the newest 20 messages. Setting scrollTop from JavaScript loads nothing; real
mouse wheel scrolling over the message pane loads 20 older messages per step.
"""

import logging
import shutil
import tempfile
import time
from pathlib import Path

logger = logging.getLogger("ig_chat_export")

FIREFOX_BINARY = "/usr/bin/firefox-esr"
INBOX_URL = "https://www.instagram.com/direct/inbox/"
SCROLL_PAUSE = 3.0  # seconds for a wheel step's older messages to arrive
MAX_STALLED_STEPS = 4  # wheel steps with no new messages before giving up (top of chat, or loading broke)
MAX_STEPS = 300  # about 6,000 messages

# Find the Relay environment through React's fiber tree once, then list this chat's messages.
READ_MESSAGES_JS = r"""
const threadId = arguments[0];
let env = window.__igRelayEnv;
if (!env) {
  for (const el of document.querySelectorAll('div')) {
    for (const key of Object.keys(el)) {
      if (!key.startsWith('__reactFiber')) continue;
      let fiber = el[key];
      for (let i = 0; i < 60 && fiber && !env; i++) {
        const props = fiber.memoizedProps;
        if (props && props.environment && props.environment.getStore) env = props.environment;
        fiber = fiber.return;
      }
    }
    if (env) break;
  }
  window.__igRelayEnv = env;
}
if (!env) return null;
const source = env.getStore().getSource();
const out = [];
for (const id of source.getRecordIDs()) {
  const msg = source.get(id);
  if (!msg || msg.__typename !== 'SlideMessage' || msg.thread_fbid !== threadId) continue;
  const content = msg.content && source.get(msg.content.__ref);
  const xma = content && content.xma && source.get(content.xma.__ref);
  out.push({
    timestamp_ms: Number(msg.timestamp_ms),
    xma_type: xma ? xma.__typename : null,
    target_url: xma ? xma.target_url || '' : '',
    author: xma ? xma.header_title_text : null,
    title: xma ? xma.title_text || '' : '',
  });
}
return out;
"""

# SlideMessagePortraitXMA cards are reels, SlideMessageStandardXMA cards are posts.
XMA_ITEM_TYPES = {"SlideMessagePortraitXMA": "xma_clip", "SlideMessageStandardXMA": "xma_media_share"}


def to_item(message: dict) -> dict:
    """Shape a message like an app API item, so extract_links() and build_record() take it as is."""
    item_type = XMA_ITEM_TYPES.get(message["xma_type"], "xma_other")
    return {
        "item_type": item_type,
        "timestamp": message["timestamp_ms"] * 1000,
        item_type: [{"target_url": message["target_url"], "header_title_text": message["author"], "title_text": message["title"]}],
    }


def open_firefox(profile: str):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options

    workdir = Path(tempfile.mkdtemp(prefix="ig-firefox-"))
    copy = workdir / "profile"
    shutil.copytree(profile, copy, ignore=shutil.ignore_patterns("lock", ".parentlock", "cache2", "startupCache"))
    options = Options()
    options.binary_location = FIREFOX_BINARY
    for arg in ("-headless", "-profile", str(copy)):
        options.add_argument(arg)
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1280, 1000)
    return driver, workdir


def wait_for_messages(driver, thread_v2_id: str, timeout: float = 40) -> list:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        messages = driver.execute_script(READ_MESSAGES_JS, thread_v2_id)
        if messages:
            return messages
        time.sleep(2)
    raise RuntimeError("The chat opened but no messages showed up in the page data")


def read_chat(profile: str, thread_title: str, thread_v2_id: str, stop_at_us: int) -> tuple[list, bool]:
    """Scroll the chat back until a message at or before stop_at_us is loaded.

    Returns (items newest first, reached) where reached is False when scrolling stalled first.
    """
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
    from selenium.webdriver.common.by import By

    logger.info(f"Opening '{thread_title}' in headless Firefox")
    driver, workdir = open_firefox(profile)
    try:
        driver.get(INBOX_URL)
        time.sleep(8)
        if "/accounts/login" in driver.current_url:
            raise RuntimeError("Firefox is not logged into Instagram")
        # The web chat URL uses an id the app API does not return, so open the chat from the inbox.
        driver.find_element(By.XPATH, f"//span[text()='{thread_title}']").click()
        messages = wait_for_messages(driver, thread_v2_id)

        body = driver.find_element(By.TAG_NAME, "body")
        stalled = 0
        for step in range(MAX_STEPS):
            oldest_us = min(m["timestamp_ms"] for m in messages) * 1000
            if oldest_us <= stop_at_us:
                break
            # 230 px right of the page centre is over the message pane.
            for _ in range(6):
                ActionChains(driver).scroll_from_origin(ScrollOrigin.from_element(body, 230, 0), 0, -1500).perform()
                time.sleep(0.7)
            time.sleep(SCROLL_PAUSE)
            loaded = driver.execute_script(READ_MESSAGES_JS, thread_v2_id)
            stalled = stalled + 1 if len(loaded) <= len(messages) else 0
            messages = loaded
            if stalled >= MAX_STALLED_STEPS:
                logger.warning(f"Scrolling stopped loading older messages after {step + 1} steps")
                break
        reached = min(m["timestamp_ms"] for m in messages) * 1000 <= stop_at_us
        logger.info(f"  browser: {len(messages)} messages loaded, reached the last scanned message: {reached}")
        shared = [m for m in messages if m["xma_type"]]
        return [to_item(m) for m in sorted(shared, key=lambda m: m["timestamp_ms"], reverse=True)], reached
    finally:
        driver.quit()
        shutil.rmtree(workdir, ignore_errors=True)
