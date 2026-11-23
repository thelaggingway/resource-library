## Details

### a2ui
- Details: A2UI is an open-source generative UI framework and protocol for agentic experiences: instead of an agent replying in text alone, it streams structured UI data that native renderers turn into real widgets. The data-not-code approach keeps a strict schema between agent and renderer, so agent-generated interfaces stay within the app's capability boundaries. It ships agent SDKs in several languages, a versioned protocol spec, native renderers for React, Angular, Lit, Flutter, SwiftUI and Jetpack Compose, plus a browser-based A2UI Composer for trying compositions. It fits apps where an agent should build the flow itself — remote rendering is supported by design, and the same agent can drive UI across web and mobile without WebViews or HTML.

### wland
- Details: wland is a Wayland compositor compiled to WebAssembly (about 65 kB gzipped) that runs in a browser tab. Unmodified Wayland apps — foot, Nautilus, Chromium, even X11 apps via xwayland-satellite — talk the real wire protocol to a small relay (wlandr) on a Linux host, VM or container, which streams them over WebSocket or vsock to the compositor; typing, menus, clipboard, drag and drop, HiDPI and window controls all work, at up to 120 FPS on a Retina MacBook. A Docker demo image runs Chromium and a file manager in the page, and an npx CLI serves your own machine's apps. Note it is brand-new, announced 21 Nov 2026, so expect rough edges — the README lists known limits.

