/* Tofu math - exact arithmetic, labeled norms.
   Labeled norms shown in the UI: soak water 3x dry beans, grind water 8x,
   milk yield 6 mL per g dry beans, nigari 8 mL/L, gypsum 2.5 g/L,
   tofu yield and press time by style (silken 550 g/L, soft 450, firm 350, extra 280). */
(function (root) {
  'use strict';

  var STYLES = {
    silken: { yield_g_per_l: 550, press_min: 0,  verdict: 'spoon it' },
    soft:   { yield_g_per_l: 450, press_min: 15, verdict: 'spoon it' },
    firm:   { yield_g_per_l: 350, press_min: 30, verdict: 'slice it' },
    extra:  { yield_g_per_l: 280, press_min: 45, verdict: 'slice it' }
  };

  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }

  function beansToMilk(dryG) {
    dryG = num(dryG, 'dry beans');
    if (dryG <= 0) throw new Error('dry beans must be positive');
    if (!Number.isInteger(dryG)) throw new Error('weigh dry beans in whole grams');
    if (dryG > 100000) throw new Error('keep it under 100 kg (labeled)');
    var verdict = dryG < 250 ? 'a tasting batch' : dryG < 1000 ? 'a kitchen batch' : 'a production day';
    return { soak_ml: dryG * 3, grind_ml: dryG * 8, milk_ml: dryG * 6, verdict: verdict };
  }

  function coagulant(milkMl, kind) {
    milkMl = num(milkMl, 'soy milk');
    if (milkMl <= 0) throw new Error('soy milk must be positive');
    kind = String(kind).toLowerCase();
    var amount, unit;
    if (kind === 'nigari') { amount = Math.round(milkMl / 1000 * 8 * 10) / 10; unit = 'ml'; }
    else if (kind === 'gypsum') { amount = Math.round(milkMl / 1000 * 2.5 * 10) / 10; unit = 'g'; }
    else throw new Error('kind is nigari or gypsum (labeled)');
    var verdict = amount < 10 ? 'tiny - measure carefully' : amount < 30 ? 'modest' : 'bulk';
    return { amount: amount, unit: unit, verdict: verdict };
  }

  function tofuYield(milkMl, style) {
    milkMl = num(milkMl, 'soy milk');
    if (milkMl <= 0) throw new Error('soy milk must be positive');
    style = String(style).toLowerCase();
    var s = STYLES[style];
    if (!s) throw new Error('style is silken, soft, firm or extra (labeled)');
    var grams = Math.round(milkMl / 1000 * s.yield_g_per_l);
    return { grams: grams, press_min: s.press_min, verdict: s.verdict };
  }

  var api = { beansToMilk: beansToMilk, coagulant: coagulant, tofuYield: tofuYield };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.TofuMath = api;
})(typeof window !== 'undefined' ? window : globalThis);
