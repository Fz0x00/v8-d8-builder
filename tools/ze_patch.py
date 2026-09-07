#!/usr/bin/env python3
"""Patch V8 11.6 instruction-selector.cc: ZE_TRACE tracing for
ZeroExtendsWord32ToWord64 (11.6 API: node->id(), node->opcode())."""
import sys
path = sys.argv[1]
s = open(path).read()
anchor = 'bool InstructionSelectorT<Adapter>::ZeroExtendsWord32ToWord64('
i = s.find(anchor)
assert i > 0, 'anchor not found'
j = s.find('{', i)
ins = (
'\n  const bool ze_trace = recursion_depth == 0 && getenv("ZE_TRACE") != nullptr;'
'\n  if (ze_trace) {'
'\n    PrintF("[ZE-TOP] node=%d opcode=%d state=%d\\n",'
'\n           node->id(), static_cast<int>(node->opcode()),'
'\n           static_cast<int>(phi_states_[node->id()]));'
'\n  }'
)
s2 = s[:j+1] + ins + s[j+1:]
k = s2.find('if (current != Upper32BitsState::kNotYetChecked) {', j)
assert k > 0, 'cache-hit anchor not found'
hit = (
'\n    if (ze_trace) {'
'\n      PrintF("[ZE-CACHE-HIT] node=%d state=%d\\n", node->id(),'
'\n             static_cast<int>(current));'
'\n    }'
)
s2 = s2[:k] + hit + s2[k:]
# also trace optimistic marking and final verdicts of top call
k2 = s2.find('phi_states_[node->id()] = Upper32BitsState::kUpperBitsGuaranteedZero;', j)
mark = (
'\n    if (ze_trace) {'
'\n      PrintF("[ZE-MARK0] node=%d\\n", node->id());'
'\n    }'
)
if k2 > 0: s2 = s2[:k2] + mark + s2[k2:]
open(path, 'w').write(s2)
print('ZE patch applied (11.6 API)')
