## Buttons to add
- x->y
- ->25
- add-coins
- cut
- reverse
- near (adds min(distance2target, 10))
- prepend X (number = int(f"{X}{number}"))
- append X (number = int(f"{number}{X}"))
- RENAME "switch" to "swap"
- X to Y (number = int(str(number).replace(X, Y)))

## other features
### bossfights
- every press takes 2 uses

## misc improvements
- remove "replicas" ("add 1 add 2" = "add 2 add 1")
- remove processing invalid replicas (if "div 0" is invalid, "div 0 sq" does not have to be processed)
