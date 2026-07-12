# 🗝️ The Vault

A sealed, offline-first reading PWA.

The content in this repository ships exclusively as AES-256-GCM ciphertext
(`content.enc`). The decryption key travels only in the URL fragment of the
keyholder's link — fragments never reach the server, and no key material
exists anywhere in this repo. Without the full link, there is nothing here
to read.

- **Stack:** a single HTML file, zero dependencies, WebCrypto + `DecompressionStream`
- **Offline:** service worker caches everything on first visit; installable as a PWA
- **State:** progress, streaks, XP, and highlights live in `localStorage` on the device
