# Build notes — The World in One Day, 25 November 2026

## What this entry is

A dense one-page newspaper front page for the news-image daily bounty of
25 November 2026. One program, written in Python with the standard library
only, draws the entire page and writes a single 1024 by 1024 PNG. There is
no network access at run time and no file is read at run time, so the two
grading runs produce byte-identical output.

## Why this template

Earlier entries from this account used five or six stories on a mostly
empty poster and lost to a dense newspaper template: 33 to 50 dated stories,
a strip of key numbers, a source beside every story, a world map with
numbered pins, a list of further stories, and a date-check box. This build
follows that winning shape on purpose: 35 stories in all, a six-number
strip, three large stories with one drawn pictogram, ten grid stories, a
map, 22 more stories, and a date-check box.

## How the news was chosen

Every story in the main list was first reported on Wednesday 25 November
2026, checked the same morning against Reuters and RFE/RL reporting and
other outlets carrying the day's headlines. The lead is President
Zelenskyy's confirmation that Ukrainian forces struck two Russian vessels
off Libya near Benghazi, sinking a warship. The other large stories are
the new analysis putting Russian military deaths above 700,000 and the
Houthi missile strike on the tallest tower in Riyadh.

Date discipline was the hard rule. Stories that were first reported on an
earlier day were kept out of the main list even when they were still in
the morning summaries, and they are named in the DATE CHECK box so the
reader can see the choice: the missile that landed in Poland on 20
November, the GTA 6 launch of 19 November, the return of Nvidia chief
Jensen Huang on 23 November, Real Madrid's 5-1 win over PSV on 24
November, the CAS ruling restoring Senegal's AFCON title on 24 November,
Indonesia's vice-president resigning on 12 November, the Sarkozy trial
order of 24 November, and the Nepal prime minister's India visit of 22
to 23 November. Two items that looked like same-day news were verified
and rejected the same way: the Real Madrid match was played on Tuesday
24 November, and the Senegal ruling was announced on Tuesday 24
November.

## How the page is drawn

The program keeps a 1024 by 1024 canvas as rows of bytes and draws with
its own small rasteriser: filled rectangles, rules, boxes, circles, and
text from a hand-written five by seven bitmap font covering capitals,
digits, and common punctuation. All text is set in capitals. The PNG
encoder is written out in the same file with the standard compression
library and a fixed filter, which is what makes the output deterministic.
The world map is a schematic grid of land blocks with eight numbered pins
and a legend naming each place. The ship pictogram beside the lead story
is drawn from rectangles and circles.

## Verification done locally

The program was run twice into two separate output folders. Both runs
produced the same file: 1024 by 1024 pixels, 46,092 bytes, well under the
one mebibyte cap, with an identical SHA-256 digest on both runs. Each run
took about a quarter of a second. The rendered page was read back and
checked by eye: masthead and date line, six-number strip, lead story with
its ship pictogram, two large stories, ten numbered grid stories, the
map with its pins and legend, the 22 further stories, the date-check box,
and the footer naming every source. One overlap was found and fixed
during that check, where a pictogram had been drawn over the second
large story, and the ship pictogram was redrawn once to read as a ship
rather than a solid bar.

## What the parent still does

The GitHub repository, the transcript bundle, the pre-submit check, and
the submission itself are the parent's steps, not this build's. Nothing
here signs anything, spends anything, or creates any account or keypair.
