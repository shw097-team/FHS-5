# bounded checklist: W1-API-01

- subject: FHS-5_PLP/W1/CONTROL_PACK
- scope: W1-NF-01
- kind: POS
- requirement: W1M §09.1；B03 §07

## positive expectation
四 API 回完整 Clause/Parent/Child/NEG/Exception/span；非 heading／excerpt

## negative / first fail
只回 heading／錯 span／缺 child → `BODY_RESOLVER_UNBOUND`

- fixture_sha256: 5d94e2ddb9cce903900b66ba55e03cf434d899eab321914c0d87ce0817bf0745
- oracle_sha256: 0d3c5e3256dd4c6cfba30788c5c875222efa0fea50b5d1f842f09fd01ef97443
