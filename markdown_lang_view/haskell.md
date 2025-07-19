# Haskell

## 0. Basics

### 0.0. Console Output

#### 0.0.0. Hello, world!

Note

> Snippet:

```hs
main :: IO ()
main = putStrLn "Hello, world!"
```

> Full:

```hs
main :: IO ()
main = putStrLn "Hello, world!"
```

> Output:

```txt
❯ Hello, world!
```

### 0.1. Primitive Types

#### 0.1.0. Boolean

Note

> Snippet:

```hs
bool1 :: Bool
bool1 = True
 
bool2 :: Bool
bool2 = False
 
main :: IO ()
main = putStrLn $ "bool1=" ++ show bool1 ++ ", bool2=" ++ show bool2
```

> Output:

```txt
❯ bool1=true, bool2=false
```

#### 0.1.1. Integer

Integer is unbounded. Int is architecture-specific, most likely 64-bit. As such, we can't
    view its internal representation the same way we can for Int.

> Snippet:

```hs
import Data.Typeable (typeOf)
import Data.Bits (testBit, FiniteBits, finiteBitSize)
import Data.Word (Word8, Word16, Word32, Word64)

integerA :: Int
integerA = 42
 
integerB :: Integer
integerB = -345
 
toBinary :: (FiniteBits a, Integral a) => a -> String
toBinary x = map (\i -> if testBit x i then '1' else '0') [finiteBitSize x - 1, finiteBitSize x - 2 .. 0]

main :: IO ()
main = putStrLn $
    "integerA=" ++ show integerA
    ++ ", integerB=" ++ show integerB
    ++ ",\ntypeOf integerA: " ++ show (typeOf integerA)
    ++ ",\ntypeOf integerB: " ++ show (typeOf integerB)
    ++ ",\nMinimum Int value: " ++ show (minBound::Int)
    ++ ",\nMaximum Int value: " ++ show (maxBound::Int)
    ++ ",\nBinary representation of integerA:\n  " ++ toBinary integerA
```

> Output:

```txt
integerA=42, integerB=-345,
typeOf integerA: Int,
typeOf integerB: Integer
Minimum Int value:-9223372036854775808,
Maximum Int value: 9223372036854775807,
Binary representation of integerA:
  0000000000000000000000000000000000000000000000000000000000101010
```
