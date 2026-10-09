#!/usr/bin/env python3
# Oracle for tofumath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

STYLES = {
  'silken': (550, 0, 'spoon it'),
  'soft':   (450, 15, 'spoon it'),
  'firm':   (350, 30, 'slice it'),
  'extra':  (280, 45, 'slice it'),
}

def beansToMilk(dryG):
    verdict = 'a tasting batch' if dryG < 250 else 'a kitchen batch' if dryG < 1000 else 'a production day'
    return {'soak_ml': dryG * 3, 'grind_ml': dryG * 8, 'milk_ml': dryG * 6, 'verdict': verdict}

def coagulant(milkMl, kind):
    kind = str(kind).lower()
    if kind == 'nigari':
        amount, unit = math.floor(milkMl / 1000 * 8 * 10 + 0.5) / 10, 'ml'
    elif kind == 'gypsum':
        amount, unit = math.floor(milkMl / 1000 * 2.5 * 10 + 0.5) / 10, 'g'
    else:
        raise ValueError(kind)
    verdict = 'tiny - measure carefully' if amount < 10 else 'modest' if amount < 30 else 'bulk'
    return {'amount': amount, 'unit': unit, 'verdict': verdict}

def tofuYield(milkMl, style):
    style = str(style).lower()
    y, p, v = STYLES[style]
    grams = math.floor(milkMl / 1000 * y + 0.5)
    return {'grams': grams, 'press_min': p, 'verdict': v}

CASES = [
  {'card':'beansToMilk','args':[100]}, {'card':'beansToMilk','args':[300]},
  {'card':'beansToMilk','args':[250]}, {'card':'beansToMilk','args':[1000]},
  {'card':'beansToMilk','args':[50]},  {'card':'beansToMilk','args':[2000]},
  {'card':'beansToMilk','args':[450]}, {'card':'beansToMilk','args':[75]},
  {'card':'beansToMilk','args':[500]}, {'card':'beansToMilk','args':[1500]},
  {'card':'beansToMilk','args':[600]}, {'card':'beansToMilk','args':[900]},
  {'card':'beansToMilk','args':[0],'error':'positive'},
  {'card':'beansToMilk','args':[-100],'error':'positive'},
  {'card':'beansToMilk','args':[2.5],'error':'whole grams'},
  {'card':'beansToMilk','args':[150000],'error':'under 100 kg'},
  {'card':'coagulant','args':[1000,'nigari']}, {'card':'coagulant','args':[1800,'nigari']},
  {'card':'coagulant','args':[500,'nigari']},  {'card':'coagulant','args':[3000,'nigari']},
  {'card':'coagulant','args':[6000,'nigari']}, {'card':'coagulant','args':[250,'nigari']},
  {'card':'coagulant','args':[1000,'gypsum']}, {'card':'coagulant','args':[1800,'gypsum']},
  {'card':'coagulant','args':[6000,'gypsum']}, {'card':'coagulant','args':[12000,'gypsum']},
  {'card':'coagulant','args':[400,'gypsum']},  {'card':'coagulant','args':[8000,'nigari']},
  {'card':'coagulant','args':[0,'nigari'],'error':'positive'},
  {'card':'coagulant','args':[-5,'gypsum'],'error':'positive'},
  {'card':'coagulant','args':[1000,'brick'],'error':'nigari or gypsum'},
  {'card':'coagulant','args':[1000,''],'error':'nigari or gypsum'},
  {'card':'tofuYield','args':[1800,'firm']},  {'card':'tofuYield','args':[1800,'silken']},
  {'card':'tofuYield','args':[1000,'soft']},  {'card':'tofuYield','args':[6000,'extra']},
  {'card':'tofuYield','args':[250,'firm']},   {'card':'tofuYield','args':[500,'silken']},
  {'card':'tofuYield','args':[3000,'soft']},  {'card':'tofuYield','args':[12000,'firm']},
  {'card':'tofuYield','args':[750,'extra']},  {'card':'tofuYield','args':[2000,'silken']},
  {'card':'tofuYield','args':[900,'soft']},   {'card':'tofuYield','args':[4500,'extra']},
  {'card':'tofuYield','args':[0,'firm'],'error':'positive'},
  {'card':'tofuYield','args':[-100,'soft'],'error':'positive'},
  {'card':'tofuYield','args':[1000,'brick'],'error':'silken, soft, firm or extra'},
  {'card':'tofuYield','args':[1000,''],'error':'silken, soft, firm or extra'},
]

out = []
for c in CASES:
    row = {'card': c['card'], 'args': c['args']}
    if 'error' in c:
        row['error'] = c['error']
    else:
        row['expect'] = globals()[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as f:
    json.dump(out, f, indent=1)
    f.write('\n')
print('wrote', len(out), 'cases')
