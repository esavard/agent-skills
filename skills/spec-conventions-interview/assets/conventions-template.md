# CONVENTIONS.md

## 1. Architecture Style
Style: <hexagonal | layered | vertical-slice | other>
Boundaries: <folder-per-layer names, e.g. domain/ application/ infrastructure/>

## 2. Architecture Enforcement
Tool: <none yet | tool name from stack table>
Threshold: <always | above N modules/LOC>

## 3. DDD Usage
Used: <yes/no>
Ubiquitous language doc: <path, or "not yet: add when first aggregate is named">

## 4. SOLID / Clean Code Stance
Exceptions: <none | list>

## 5. Testing Rules
Required types: <unit | integration | e2e>
Location convention: <e.g. tests/ mirrors src/, or colocated *_test files>
Style: <Given/When/Then | Arrange/Act/Assert | none enforced>
Coverage gate: <none | threshold>

## 6. Reuse & Dependency Policy
New external dependency: <needs no approval | needs flagging in PR | needs approval from X>
Shared code threshold: <extract to shared/common on Nth duplication>

## 7. Process Constraints
<agent must never do X unprompted: list or "none yet">
Spec checkboxes: implementing agent checks each `docs/specs/` item the moment it is verified; unchecked items carry `(manual)` or `NOT DONE: <reason>`.

Last reviewed: <date>, <what prompted this>
