# GitHub auth walkthrough (for non-technical founders)

You need two things: a free GitHub account and the `gh` command-line tool logged
in. This takes about four minutes and you do it once, ever. Follow the steps in
order. If any step fails, the fix is right underneath it.

## Step 0: do you already have an account?

If you have ever pushed code or opened an issue on github.com, you have an
account. Skip to Step 2. If not, do Step 1.

## Step 1: create a free GitHub account (2 minutes)

1. Go to https://github.com/signup in your browser.
2. Enter your email, a password and a username. Your username becomes part of
   your repo URLs, so keep it clean and professional. Your name or your firm's
   name is fine.
3. Verify your email when GitHub sends the code.

That is it. The free plan gives you unlimited private repositories, which is all
you need this week.

## Step 2: install the gh command-line tool

`gh` is GitHub's official tool. It lets this skill create the repo and issues for
you instead of clicking around.

- **macOS:** open Terminal and run `brew install gh`. No Homebrew? Install it
  first from https://brew.sh, then run the command.
- **Windows:** open PowerShell and run `winget install --id GitHub.cli`.
- **Linux:** follow https://github.com/cli/cli#installation for your distro, or
  run `sudo apt install gh` on Debian or Ubuntu.

Check it worked:

```
gh --version
```

You should see a version number. If you see "command not found", close the
terminal, open a fresh one, and try again. A new terminal picks up the new tool.

## Step 3: log gh in to your account (1 minute)

Run:

```
gh auth login
```

It asks a few questions. Answer like this:

1. "What account do you want to log into?" Choose **GitHub.com**.
2. "What is your preferred protocol?" Choose **HTTPS**.
3. "Authenticate Git with your GitHub credentials?" Choose **Yes**.
4. "How would you like to authenticate?" Choose **Login with a web browser**.
5. It shows an eight-character code (for example `AB12-CD34`). Copy it. Press
   Enter. Your browser opens. Paste the code, click through, click Authorise.

Back in the terminal you will see a green tick and "Logged in as <you>".

## Step 4: confirm

```
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-github.py --check
```

You want the line `ready: gh installed and authenticated as <you>.` Once you see
it, go back to the skill and run `--create`.

## Common snags

- **"gh not found" after installing.** Open a brand-new terminal window. The old
  one does not know about the tool yet.
- **Locked-down work laptop that blocks installs.** Use your own machine, or use
  the browser fallback in the skill's "If it goes wrong" section. You can create
  the repo and issues by hand at github.com; it is slower, same result.
- **Corporate network blocks the browser login.** Run `gh auth login` and choose
  "Paste an authentication token" instead. Create a token at
  https://github.com/settings/tokens with the `repo` scope, paste it in.
- **Two-factor prompts.** Approve them. Two-factor on your GitHub account is a
  good thing, especially for a regulated-sector founder. Keep it on.
