# Integer

## Python

Note to come...

> Snippet:

```py
int_a = 5
int_b = -112
```

> Output:

```txt

```

## Haskell

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

## Rust

Note

> Snippet:

```rs
let signed_8bit: i8 = 27;
let signed_16bit: i16 = -3;
let signed_32bit: i32 = -666;
let signed_64bit: i64 = 42;
let signed_128bit: i128 = 999999;

let unsigned_8bit: u8 = 56;
let unsigned_16bit: u16 = 1;
let unsigned_32bit: u32 = 0;
let unsigned_64bit: u64 = 1234567;
let unsigned_128bit: u128 = 123456789;
```

> Full:

```rs
use std::any::type_name;
use std::fmt::Binary;
use std::fmt::Display;
use std::mem::size_of;

fn get_type<T>(_: &T) -> &str {
    type_name::<T>()
}

fn print_info<T: Binary + Copy + Display>(varname: &str, variable: T) {
    let bit_width = size_of::<T>() * 8;
    println!("{varname}: type '{vartype}'", vartype = get_type(&variable));
    println!("  decimal: {}", variable);
    println!("  stored as: {:0bit_width$b} binary\n", variable, bit_width = bit_width);
}

fn main() {
    let signed_8bit: i8 = 27;
    let signed_16bit: i16 = -3;
    let signed_32bit: i32 = -666;
    let signed_64bit: i64 = 42;
    let signed_128bit: i128 = 999999;

    let unsigned_8bit: u8 = 56;
    let unsigned_16bit: u16 = 1;
    let unsigned_32bit: u32 = 0;
    let unsigned_64bit: u64 = 1234567;
    let unsigned_128bit: u128 = 123456789;

    print_info("signed_8bit", signed_8bit);
    print_info("signed_16bit", signed_16bit);
    print_info("signed_32bit", signed_32bit);
    print_info("signed_64bit", signed_64bit);
    print_info("signed_128bit", signed_128bit);

    print_info("unsigned_8bit", unsigned_8bit);
    print_info("unsigned_16bit", unsigned_16bit);
    print_info("unsigned_32bit", unsigned_32bit);
    print_info("unsigned_64bit", unsigned_64bit);
    print_info("unsigned_128bit", unsigned_128bit);
}
```

> Output:

```txt
signed_16bit: type 'i16'
  decimal: -3
  stored as: 1111111111111101 binary

signed_32bit: type 'i32'
  decimal: -666
  stored as: 11111111111111111111110101100110 binary

signed_64bit: type 'i64'
  decimal: 42
  stored as: 0000000000000000000000000000000000000000000000000000000000101010 binary

signed_128bit: type 'i128'
  decimal: 999999
  stored as: 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011110100001000111111 binary

unsigned_8bit: type 'u8'
  decimal: 56
  stored as: 00111000 binary

unsigned_16bit: type 'u16'
  decimal: 1
  stored as: 0000000000000001 binary

unsigned_32bit: type 'u32'
  decimal: 0
  stored as: 00000000000000000000000000000000 binary

unsigned_64bit: type 'u64'
  decimal: 1234567
  stored as: 0000000000000000000000000000000000000000000100101101011010000111 binary

unsigned_128bit: type 'u128'
  decimal: 123456789
  stored as: 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111010110111100110100010101 binary

```
