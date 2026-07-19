# Putting soundbird online

This is set up the same way as `personal-website`: a GitHub repository with an
HTTPS remote, and your credentials already stored on this machine. Once the
repository exists, Claude can push to it on request without you doing anything
further.

There is exactly **one** step only you can do, because it involves signing in.

---

## Step 1 (you, once): sign in to GitHub from the terminal

1. Open **Terminal**. Press `Cmd` + `Space`, type `Terminal`, press `Enter`.
2. Paste this and press `Enter`:

   ```sh
   cd ~/Projects/sound-bird
   ```

3. Paste this and press `Enter`:

   ```sh
   gh auth login
   ```

4. Answer the prompts with the arrow keys and `Enter`:

   - *What account do you want to log into?* → **GitHub.com**
   - *What is your preferred protocol?* → **HTTPS**
   - *Authenticate Git with your GitHub credentials?* → **Yes**
   - *How would you like to authenticate?* → **Login with a web browser**

5. It shows a one-time code like `ABCD-1234`. Copy it, press `Enter`, and your
   browser opens. Paste the code and click through to authorize.

6. Back in Terminal you should see `✓ Logged in as riavi04`.

That is the whole of your part. You never have to do it again.

---

## Step 2 (Claude): everything else

Tell Claude *"the repo is ready, publish it"* and it will run:

```sh
gh repo create soundbird --public --source=. --remote=origin --push
echo '{"source":{"branch":"main","path":"/docs"}}' \
  | gh api -X POST repos/:owner/soundbird/pages --input -
```

Your site then lives at:

```
https://riavi04.github.io/soundbird/
```

It usually takes a minute or two to appear the first time.

---

## Afterwards

Just say what you want changed. Claude edits the source, rebuilds, and pushes,
and the live site updates within about a minute. The useful phrases are:

- *"push the latest to the site"*
- *"rebuild and deploy"*

Under the hood that is `python3 src/build.py dist/sound-bird.html` followed by a
commit and `git push`, because `build.py` writes `docs/index.html`, which is the
file GitHub Pages serves.

## If you would rather not use the terminal at all

Create the empty repository in the browser instead:

1. Go to <https://github.com/new>
2. Repository name: `soundbird`
3. Choose **Public**
4. Do **not** tick "Add a README"
5. Click **Create repository**

Then tell Claude, which will add the remote and push. You would still need to
switch Pages on once, under the repository's **Settings → Pages → Deploy from a
branch → main → /docs → Save**.

## Taking it down

```sh
gh repo delete soundbird
```

Or from the repository's Settings page, at the bottom.
