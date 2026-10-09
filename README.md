# Tofu math

Three tofu-making calculators as a small static site - exact arithmetic, every
borrowed number labeled:

- **Bean to milk** - dry soybeans -> soak water (3x), grind water (8x) and soy milk
  (6 mL per g) at labeled norms, with a batch-size band.
- **Coagulant** - soy milk -> nigari (8 mL/L) or gypsum (2.5 g/L) at labeled rates.
- **Press and yield** - soy milk and style (silken/soft/firm/extra) -> block weight
  (550/450/350/280 g per L) and press time (0/15/30/45 min), all labeled.

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 48 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```
