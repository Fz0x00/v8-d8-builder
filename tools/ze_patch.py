#!/usr/bin/env python3
"""Patch V8 instruction-selector.cc: add ZE_TRACE env-gated tracing to
ZeroExtendsWord32ToWord64 (top-level calls + cache hits + final results)."""
import sys
path = sys.argv[1]
s = open(path).read()
anchor = 'bool InstructionSelectorT<Adapter>::ZeroExtendsWord32ToWord64('
i = s.find(anchor)
assert i > 0, 'anchor not found'
j = s.find('{', i)
ins = '''
  const bool ze_trace = recursion_depth == 0 && getenv("ZE_TRACE") != nullptr;
  if (ze_trace) {
    PrintF("[ZE-TOP] node=%d opcode=%d cached_state=%d\\n",
           this->id(node), static_cast<int>(this->opcode(node)),
           static_cast<int>(phi_states_[this->id(node)]));
  }
'''
# also trace cache reuse return: find the 'kNotYetChecked' compare after insertion
s2 = s[:j+1] + ins + s[j+1:]
k = s2.find('if (current != Upper32BitsState::kNotYetChecked) {', j)
assert k > 0, 'cache-hit anchor not found'
hit_ins = '''
    if (ze_trace) {
      PrintF("[ZE-CACHE-HIT] node=%d state=%d\\n", this->id(node),
             static_cast<int>(current));
    }
'''
s2 = s2[:k] + hit_ins + s2[k:]
open(path, 'w').write(s2)
print('ZE patch applied to', path)
