# 0003. Build hard text by decorating random words

- Status: accepted
- Date: 2026-11-21
- Round: 3 (requirement R3.1, medium and hard difficulty)

## Y-statement

In the context of **generating the text for a hard standard typing test (R3.1)**,
facing **the user's choice that hard means long words plus capital letters,
punctuation (, . ? !) and numbers, while tests must be able to check the
result and Retry must give new text each time**,
we decided **to pick random words from a `HARD_WORDS` list and decorate them by
chance: about 10% become a number from 0 to 999, about 15% end a sentence with
`.`, `?` or `!`, and about 15% get a comma, with every sentence starting with a
capital and the last word always ending a sentence**,
and neglected **a fixed bank of hand-written hard sentences, and adding random
punctuation or capitals to any word with no sentence structure**,
to achieve **text that reads like (nonsense) sentences, so capitals appear where
a typist expects them, is different on every Retry, and can be checked rule by
rule in unit tests using a seeded random generator**,
accepting **that the sentences don't mean anything, that a given test's exact
mix of numbers and punctuation varies by chance, and that the chances are
tuning knobs (`HARD_*_CHANCE` in `logic.py`) we may want to adjust after
playing.**

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Bank of hand-written sentences | Reads naturally, but players would memorize them after a few retries, and writing enough of them is a lot of content work. |
| Random punctuation/capitals on any word | Simplest, but a capital in the middle of a "sentence" or a comma right before a period feels random and unfair rather than hard. |

## Where it lives

`logic.generate_text(..., difficulty=logic.HARD)` and `logic._hard_text()`,
tested by the `test_R3_1_hard_*` tests.
