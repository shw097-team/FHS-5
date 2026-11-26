# Design

The engine is a bounded stdlib slice. It reads the adopted pack read-only,
writes only under the isolated run root, and types every refusal. Design
fixtures are evaluated as DESIGN_ENGINE observations; product case state stays
NOT_COVERED. The Checker and Consumer are separate local processes with
disclosed limitations (same OS principal, not an original-domain principal).
