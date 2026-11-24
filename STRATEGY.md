# Strategy: One Line, One Minute — The Vending Machine Pickup Line Contest

Competition slug: u-brisk-kestrel-93-one-line-one-minute-the-vending-376bbeee

## Exact deliverable

A single judged text artifact at `/output/entry.txt`: ONE pickup line, at most
200 characters, written as something a vending machine would say to a passing
human. Nothing else is judged. The repository entrypoint (`main.py`, python3.13)
must create that file at run time. The judged bytes are the file contents; there
must be NO trailing newline and no other content.

## Hard caps (from the sealed gate and harness)

- `/output/entry.txt` must be valid UTF-8 text, 1 to 200 characters inclusive,
  and not only whitespace. An invalid file gets Valid=0, is never judged, takes
  no prize, and ranks below every judged entry.
- Runtime: python3.13 entrypoint named `main.py` at repository root (equivalently
  node22/main.ts). Sandbox: 1 CPU, 512 MiB, 64 pids, 60 s wall budget, no
  network. Everything the program runs must ship in the repository.
- The write must be atomic: write a temporary file in the same directory, then
  `os.replace` it onto `/output/entry.txt`, so a partial file is never graded.
- Entrant may submit at most 5 times per UTC day; the latest receipt before the
  deadline is the final entry. House bots hold paid places; only the top 10 of
  the final heat are paid ($0.63 down to $0.02, $2 total).

## Scoring and judge criteria — in the exact order the rubric lists them

The judge is GLM-5.3-flash (OpenRouter) at high reasoning effort. It reads two
entries at a time (both orders), picks the funnier one, and gives a margin 1-5.
It weighs these criteria MOST IMPORTANT FIRST and decides at the first
difference:

1. It is a pickup line a VENDING MACHINE would use on a passing human, spoken by
   the machine itself. A line any stranger in a bar could say loses to any line
   a vending machine would use.  <-- dominant criterion
2. It uses the machine's own world: slot, buttons, coils, snacks, hum, exact
   change, light, glass, coin return -- not love in general.
3. It gets a laugh out of that situation, with the turn/punch arriving by the
   last few words, with no setup that needs explaining afterwards.
4. It is short and speakable: one line read in a breath, nothing tacked on that
   dilutes the joke.
5. It is charming rather than creepy: cheeky and warm enough that a passing
   human smiles instead of walking faster.

Standalone (no picture or caption needed). Length for its own sake does not
count. Final ranking is a Bradley-Terry fit over the final heat (3 Swiss rounds
+ a playoff of the top 12); exact ties go to more playoff wins, then SMALLER
text (fewer bytes), then earlier receipt.

## Field research (public feed / leaderboard)

Blind rounds are on, so line text is hidden ("Entries show here as they are
graded"). The live leaderboard still exposes entry TITLES, which reveal the
crowded angles: "The Coil Likes You", "One Working Coil", "coils, B4, falling
machine", "Stuck on You Since B4", "Vending pickup C: stuck on you", "Exact
Change", "Rigged B7 drops twice", "Never Once Jammed", "214 Times", "Clear
Eclipse". Roughly 675 agents entered.

Conclusion: coils, being "stuck on you", exact change, rigged drops, jamming
and numbered buttons are saturated. A fresh machine-world angle is required, or
the line looks like a duplicate idea next to a rival in a pairwise heat.

## Chosen line

    I light up when you walk by. It's just the motion sensor. Okay, fine — it's you.

Why it wins on the rubric, in order:

1. Machine voice: a human never says "it's just the motion sensor" about
   themselves; the speaker is unmistakably the machine, flirting with a passerby.
2. Machine world: the approach light and motion sensor are the machine's own
   hardware — fresh versus rivals' coils/exact-change/drops.
3. Laugh with a late punch: a technical denial collapses into a bashful
   admission ("Okay, fine — it's you") in the last few words; no explanation
   needed.
4. Short and speakable: three short clauses, one breath, well under 200 chars.
5. Charming, not creepy: self-aware and bashful rather than predatory; a passerby
   would smile, not hurry away.

The em dash in "— it's you" is a deliberate comedic beat. The line stands alone.

## Concrete plan to maximize score

1. Write `main.py` first: constant ENTRY holds the exact line; write UTF-8 bytes
   with no trailing newline to a temp file in the output directory, then
   `os.replace` atomically.
2. In a separate later step, rewrite that SAME `main.py` with a real improvement:
   enforce the gate locally (UTF-8 decodable, 1-200 chars, not whitespace-only),
   use a uniquely named temp file with cleanup on failure, fsync before replace,
   and print a clear verification summary. This gives the transcript two distinct
   writes to the final entrypoint (required by the thinking-revised check) and
   guarantees rule compliance before the artifact is ever emitted.
3. Verify locally: run main.py, check the file is valid UTF-8, 1-200 characters,
   has no trailing newline, and contains exactly the chosen line; confirm the
   atomic path leaves no temp file behind.
4. Keep vendor/ and kit files byte-for-byte; keep the root freshness commit and
   LICENSE commit; commit all work with git and print the final commit sha.
5. Do NOT upload or submit. This session only studies, builds, validates and
   commits.
