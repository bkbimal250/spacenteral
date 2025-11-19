# Spa Code Sorting - Test Cases

## Spa Code Range: 101 - 1000

### Example Data
```
101 - Green Spa
102 - Blue Spa
150 - Red Spa
200 - Yellow Spa
612 - Unicorn Spa
750 - Ocean Spa
999 - Mountain Spa
1000 - Sky Spa
```

### Sorting Results

#### Spa Code (0-9) - Ascending
```
✓ 101 - Green Spa
✓ 102 - Blue Spa
✓ 150 - Red Spa
✓ 200 - Yellow Spa
✓ 612 - Unicorn Spa
✓ 750 - Ocean Spa
✓ 999 - Mountain Spa
✓ 1000 - Sky Spa
```

#### Spa Code (9-0) - Descending
```
✓ 1000 - Sky Spa
✓ 999 - Mountain Spa
✓ 750 - Ocean Spa
✓ 612 - Unicorn Spa
✓ 200 - Yellow Spa
✓ 150 - Red Spa
✓ 102 - Blue Spa
✓ 101 - Green Spa
```

## Comparison: String vs Numeric Sorting

### ❌ Wrong (String/Alphabetical Sorting)
If we used string comparison:
```
1000, 101, 102, 150, 200, 612, 750, 999
```
This is wrong because strings compare character by character:
- "1000" < "101" (because "1" == "1", "0" < "0", but "0" < "1" at position 2)

### ✅ Correct (Numeric Sorting)
With our implementation using `parseInt()`:
```
101, 102, 150, 200, 612, 750, 999, 1000
```
This is correct because we compare actual numbers:
- 101 < 102 < 150 < 200 < 612 < 750 < 999 < 1000

## Code Implementation

```javascript
case 'spa_code_asc':
  const aCode = parseInt(a.spaCode) || 0;  // "101" → 101
  const bCode = parseInt(b.spaCode) || 0;  // "102" → 102
  return aCode - bCode;                     // 101 - 102 = -1 (negative = a before b)
```

## Edge Cases Handled

1. **Leading Zeros**: `parseInt("0101")` = `101` ✓
2. **Non-numeric**: `parseInt("ABC")` = `NaN` → fallback to `0` ✓
3. **Null/Undefined**: `parseInt(null)` = `NaN` → fallback to `0` ✓
4. **Mixed Format**: `parseInt("612-A")` = `612` (stops at first non-digit) ✓

## Date: October 26, 2025

