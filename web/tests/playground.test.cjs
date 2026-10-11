const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const inputs = {
  baseColor: { value: '' },
  mood: { value: '' },
  designDesc: { value: 'Purple gradient and 24px rounded cards' },
};
const context = {
  document: {
    getElementById: (id) => inputs[id] || null,
    addEventListener: () => {},
  },
  window: {},
};

vm.createContext(context);
vm.runInContext(fs.readFileSync('web/js/main.js', 'utf8'), context);
const evaluate = (expression) => vm.runInContext(expression, context);

const fallback = evaluate('tools.palette.run()');
assert.equal(fallback.base_color, '#3b82f6');
assert.equal(fallback.colors.length, 5);

inputs.mood.value = 'calm';
const moodPalette = evaluate('tools.palette.run()');
assert.equal(moodPalette.base_color, '#70b8db');
assert.equal(moodPalette.mood, 'calm');

inputs.baseColor.value = '#123';
const explicitPalette = evaluate('tools.palette.run()');
assert.equal(explicitPalette.base_color, '#112233');
assert.equal(explicitPalette.mood, null);

inputs.mood.value = 'paper_ink';
assert.equal(evaluate('tools.palette.run()').base_color, '#112233');
inputs.baseColor.value = '';
assert.match(evaluate('tools.palette.run()').mood, /paper_ink/);

inputs.baseColor.value = '#12zz00';
assert.ok(evaluate('tools.palette.run()').error);

const critique = evaluate('tools.critique_ai.run()');
assert.equal(critique.analysis_type, 'keyword_heuristic');
assert.equal(critique.detected_ai_tropes.length, 2);

inputs.designDesc.value = 'An editorial product page with clear typography';
assert.equal(evaluate('tools.critique_ai.run()').detected_ai_tropes.length, 0);

console.log('Browser playground smoke tests passed.');
