# bounded checklist: W1-HOST-01

- subject: FHS-5_PLP/W1/CONTROL_PACK
- scope: W1-NF-01
- kind: POS
- requirement: W1M §09.1 L889–908；M §11.7 U-017

## positive expectation
CODEX（或指定 Host）同 scope 真 `Consumed` raw：consumer_id、consumed_sha256、readback_at

## negative / first fail
無 raw 宣 consumed → `HOST_PENDING`；只讀 H0／briefcheck 不計

- fixture_sha256: 168aa72567745ebce907c951076323fd2db527e35502ec1ed912f309632a3fda
- oracle_sha256: c92846be150cfcfbd9400e5bf23d50ad73b1ca897d10e921ad3120e387573e68
