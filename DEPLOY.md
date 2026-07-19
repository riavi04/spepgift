# Sharing soundbird

The repository is **private** and there is no public website. The page is
written to one person by name, so it is shared as a link rather than published.

## How Ben gets it

The built page is published as a **Claude artifact**, which is private until you
choose to share it:

<https://claude.ai/code/artifact/9b05c645-905f-474a-8e58-41155d2f3cfc>

1. Open that link.
2. Use the **share** menu on the page.
3. Send Ben the link it gives you.

Anyone with the link can open it. Nothing indexes it, and there is no public
GitHub footprint. It works on a phone.

## Updating it

Say what you want changed. Claude edits the source, rebuilds, and republishes to
**the same link**, so anything already sent to Ben keeps working and simply
shows the new version.

The underlying commands are:

```sh
python3 src/build.py dist/sound-bird.html    # rebuild
git add -A && git commit -m "..." && git push # save to the private repo
```

then republish `dist/sound-bird.html` as the artifact.

## The offline copy

`dist/standalone.html` is the same page as a single 6.4 MB file that needs no
internet once it has been opened. AirDrop it, or put it on a USB stick. Double
clicking it works.

## If you ever do want a real public URL

Three routes, in increasing effort:

- **Make this repository public** and turn on Pages: Settings → Pages → Deploy
  from a branch → `main` → `/docs`. It would then live at
  `https://riavi04.github.io/soundbird/`. Everything, including the personal
  intro cards and the whole commit history, becomes world-readable.
- **Keep the source private** and host only the built page somewhere like
  Cloudflare Pages or Netlify, both of which deploy from a private repository on
  their free tiers. The page is still public to anyone with the address.
- **Publish a neutral version** with the personal copy stripped out, and keep
  the personal one as the private link. That is a change to the source rather
  than to the hosting.

`build.py` already writes `docs/index.html`, so the first route needs no code
changes.
