# Get the GitHub Pages dashboard live

End state: `https://jeremyfeit-spec.github.io/regulatory-tracker/` shows the dashboard, login-gated to your repo's collaborators (because the repo is private). Each Friday's regulatory update auto-publishes there.

---

## Step 0 — Confirm your GitHub plan supports private-repo Pages

Pages on a **private** repo requires GitHub **Pro**, **Team**, or **Enterprise Cloud**. Free personal accounts don't include it.

1. Go to https://github.com/settings/billing/plans
2. Look for "Current plan"
3. If it says **Free** → you have three choices:
   - Upgrade your personal account to **Pro** ($4/mo) — easiest
   - Move the repo into your Intuit GH org (which has Enterprise) — best
   - Make the repo public — free, but exposes the data
4. If it says **Pro / Team / Enterprise** → keep going

---

## Step 1 — Push the local folder to GitHub

The local database lives at `~/Documents/regulatory-tracker/`. Push it to your existing repo:

```bash
cd ~/Documents/regulatory-tracker
git init
git add .
git commit -m "Initial scaffold + dashboard"
git branch -M main
git remote add origin https://github.com/jeremyfeit-spec/regulatory-tracker.git
git push -u origin main
```

If `git push` rejects your password — GitHub stopped accepting passwords from the CLI. Run `gh auth login` once (`brew install gh` if needed), then re-run the push.

If the push complains the remote already has commits, run this once first:

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

After this, https://github.com/jeremyfeit-spec/regulatory-tracker should show the `countries/`, `config/`, `docs/`, `history/` folders.

---

## Step 2 — Enable GitHub Pages from the `/docs` folder

1. Open https://github.com/jeremyfeit-spec/regulatory-tracker/settings/pages
2. Under **Build and deployment**:
   - **Source:** `Deploy from a branch`
   - **Branch:** `main` · folder: `/docs` · click **Save**
3. GitHub starts a Pages build. Refresh the page after ~30 seconds — you'll see "Your site is live at `https://jeremyfeit-spec.github.io/regulatory-tracker/`"
4. Click that URL. You'll either see the dashboard, or a GitHub login prompt (if the repo is private).

If you see a 404 for ~2 minutes after enabling Pages, that's normal — first build can be slow. Refresh.

---

## Step 3 — Confirm access controls

Because the repo is **private**, the Pages site is also access-controlled:
- You need to be signed into GitHub
- You need to have read access to `jeremyfeit-spec/regulatory-tracker`

To grant access to a teammate: repo **Settings → Collaborators → Add people**. They sign in to GitHub and can then see both the repo and the Pages site.

---

## Step 4 — How weekly updates flow to the live page

The Friday 8am PT scheduled task (`regulatory-tracker-friday-digest`) does this in order:

1. Web-searches for new regulations across all 61 countries
2. Updates `countries/<ISO>.json` files with new/changed entries
3. Writes the weekly diff to `history/diff_<DATE>.json`
4. Runs `docs/_build_data.py` to refresh `docs/data.json` (the dashboard's data feed)
5. **Tries to `git commit && git push`** — if it works, the live Pages site updates within a couple minutes
6. Posts the digest to `#international_weekly_regulatory_overview`

**Important caveat for step 5:** The Cowork sandbox runs the scheduled task in an isolated environment that may not have your GitHub auth. If the push fails silently, the local `~/Documents/regulatory-tracker/` is still up to date — you'd just need to push manually:

```bash
cd ~/Documents/regulatory-tracker
git add . && git commit -m "weekly update" && git push
```

Run this after each Friday job, or set up SSH keys / a credential helper so the sandbox can authenticate. Easiest workaround: install `gh` in a way that's available to the scheduled task, then run `gh auth login` once.

---

## Step 5 — Verify it all works end-to-end (right now, before Friday)

1. **Run the scheduled task manually** — open Cowork sidebar → **Scheduled** → `regulatory-tracker-friday-digest` → **Run now**
2. Approve any tool permission prompts (web search, Slack MCP, filesystem). These approvals are saved to the task for future runs.
3. After the run completes:
   - Open `#international_weekly_regulatory_overview` in Slack — see the digest
   - Check `~/Documents/regulatory-tracker/history/` — there should be a new `diff_*.json`
   - Check `~/Documents/regulatory-tracker/docs/data.json` — file size should be ~33-40KB
4. If the auto-push didn't happen, push manually (Step 4 caveat above)
5. Refresh `https://jeremyfeit-spec.github.io/regulatory-tracker/` — see the updated dashboard

---

## Troubleshooting

**"Pages is disabled because your plan doesn't support it"** — your GH plan doesn't include private-repo Pages. See Step 0.

**Pages site shows 404** — wait 2 minutes for first build, then check https://github.com/jeremyfeit-spec/regulatory-tracker/actions for a "pages build" workflow. If it failed, check the log.

**Pages site shows the dashboard but data is empty** — `docs/data.json` didn't get committed. Check it exists in the repo on GitHub. If missing locally, run `python3 ~/Documents/regulatory-tracker/docs/_build_data.py` and push.

**Slack post never lands** — the scheduled task likely paused waiting for tool approvals. Run it manually once (Step 5) to grant them.
