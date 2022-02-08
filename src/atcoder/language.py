import dataclasses
import typing


@dataclasses.dataclass
class Language:
    id: int
    text: str
    name: typing.Optional[str] = None
    compiler_or_runtime: typing.Optional[str] = None
    version: typing.Optional[str] = None
    compile_to: typing.Optional[str] = None
    category: typing.Optional[str] = None
    file_extensions: typing.Optional[typing.List[str]] = None


LANGUAGES_YAML_TEXT = """
- category: null
  compile_to: null
  compiler_or_runtime: GCC
  file_extensions:

    - c
    - h
  id: 4001
  name: C
  text: C (GCC 9.2.1)
  version: 9.2.1
- category: null
  compile_to: null
  compiler_or_runtime: Clang
  file_extensions:
    - c
    - h
  id: 4002
  name: C
  text: C (Clang 10.0.0)
  version: 10.0.0
- category: null
  compile_to: null
  compiler_or_runtime: GCC
  file_extensions:
    - cpp
    - hpp

  id: 4003
  name: C++
  text: C++ (GCC 9.2.1)
  version: 9.2.1
- category: null
  compile_to: null
  compiler_or_runtime: Clang
  file_extensions:
    - cpp
    - hpp
  id: 4004
  name: C++
  text: C++ (Clang 10.0.0)
  version: 10.0.0
- category: null
  compile_to: null
  compiler_or_runtime: OpenJDK
  file_extensions:
    - java
    
  id: 4005
  name: Java
  text: Java (OpenJDK 11.0.6)
  version: 11.0.6
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - py
    
  id: 4006
  name: Python
  text: Python (3.8.2)
  version: 3.8.2
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - sh
    
  id: 4007
  name: Bash
  text: Bash (5.0.11)
  version: 5.0.11
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions: 
    - bc
    
  id: 4008
  name: bc
  text: bc (1.07.1)
  version: 1.07.1
- category: null
  compile_to: null
  compiler_or_runtime: GNU Awk
  file_extensions:
    - awk
    
  id: 4009
  name: Awk
  text: Awk (GNU Awk 4.1.4)
  version: 4.1.4
- category: null
  compile_to: null
  compiler_or_runtime: .NET Core
  file_extensions:
    - cs
    
  id: 4010
  name: C#
  text: C# (.NET Core 3.1.201)
  version: 3.1.201
- category: null
  compile_to: null
  compiler_or_runtime: Mono-mcs
  file_extensions:
    - cs
    
  id: 4011
  name: C#
  text: C# (Mono-mcs 6.8.0.105)
  version: 6.8.0.105
- category: null
  compile_to: null
  compiler_or_runtime: Mono-csc
  file_extensions: 
    - cs
    
  id: 4012
  name: C#
  text: C# (Mono-csc 3.5.0)
  version: 3.5.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - clj
    - cljs
    - cljc
    - edn
  
  id: 4013
  name: Clojure
  text: Clojure (1.10.1.536)
  version: 1.10.1.536
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - cr
    
  id: 4014
  name: Crystal
  text: Crystal (0.33.0)
  version: 0.33.0
- category: null
  compile_to: null
  compiler_or_runtime: DMD
  file_extensions:
    - d
    
  id: 4015
  name: D
  text: D (DMD 2.091.0)
  version: 2.091.0
- category: null
  compile_to: null
  compiler_or_runtime: GDC
  file_extensions:
    - d
    
  id: 4016
  name: D
  text: D (GDC 9.2.1)
  version: 9.2.1
- category: null
  compile_to: null
  compiler_or_runtime: LDC
  file_extensions:
    - d
    
  id: 4017
  name: D
  text: D (LDC 1.20.1)
  version: 1.20.1
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - dart
    
  id: 4018
  name: Dart
  text: Dart (2.7.2)
  version: 2.7.2
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - dc
  id: 4019
  name: dc
  text: dc (1.4.1)
  version: 1.4.1
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - erl
    - hrl
  id: 4020
  name: Erlang
  text: Erlang (22.3)
  version: '22.3'
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - ex
    - exs
  id: 4021
  name: Elixir
  text: Elixir (1.10.2)
  version: 1.10.2
- category: null
  compile_to: null
  compiler_or_runtime: .NET Core
  file_extensions: []
  id: 4022
  name: F#
  text: F# (.NET Core 3.1.201)
  version: 3.1.201
- category: null
  compile_to: null
  compiler_or_runtime: Mono
  file_extensions:
    - fs
    - fsi
    - fsx
    - fsscript
  id: 4023
  name: F#
  text: F# (Mono 10.2.3)
  version: 10.2.3
- category: null
  compile_to: null
  compiler_or_runtime: gforth
  file_extensions:
    - fs
    - fsi
    - fsx
    - fsscript
  id: 4024
  name: Forth
  text: Forth (gforth 0.7.3)
  version: 0.7.3
- category: null
  compile_to: null
  compiler_or_runtime: GNU Fortran
  file_extensions:
    - f90
  id: 4025
  name: Fortran
  text: Fortran (GNU Fortran 9.2.1)
  version: 9.2.1
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - go
  id: 4026
  name: Go
  text: Go (1.14.1)
  version: 1.14.1
- category: null
  compile_to: null
  compiler_or_runtime: GHC
  file_extensions:
    - hs
  id: 4027
  name: Haskell
  text: Haskell (GHC 8.8.3)
  version: 8.8.3
- category: null
  compile_to: js
  compiler_or_runtime: null
  file_extensions:
    - hx
    - hxml
  id: 4028
  name: Haxe
  text: Haxe (4.0.3); js
  version: 4.0.3
- category: null
  compile_to: Java
  compiler_or_runtime: null
  file_extensions:
    - hx
    - hxml
  id: 4029
  name: Haxe
  text: Haxe (4.0.3); Java
  version: 4.0.3
- category: null
  compile_to: null
  compiler_or_runtime: Node.js
  file_extensions:
    - js

  id: 4030
  name: JavaScript
  text: JavaScript (Node.js 12.16.1)
  version: 12.16.1
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - jl
  
  id: 4031
  name: Julia
  text: Julia (1.4.0)
  version: 1.4.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - kt
  id: 4032
  name: Kotlin
  text: Kotlin (1.3.71)
  version: 1.3.71
- category: null
  compile_to: null
  compiler_or_runtime: Lua
  file_extensions:
    - lua
  id: 4033
  name: Lua
  text: Lua (Lua 5.3.5)
  version: 5.3.5
- category: null
  compile_to: null
  compiler_or_runtime: LuaJIT
  file_extensions:
    - lua
  id: 4034
  name: Lua
  text: Lua (LuaJIT 2.1.0)
  version: 2.1.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - dash
  id: 4035
  name: Dash
  text: Dash (0.5.8)
  version: 0.5.8
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - nim
    - nims
    - nimble
  id: 4036
  name: Nim
  text: Nim (1.0.6)
  version: 1.0.6
- category: null
  compile_to: null
  compiler_or_runtime: Clang
  file_extensions:
    - h
    - m
    - mm
    - M
  id: 4037
  name: Objective-C
  text: Objective-C (Clang 10.0.0)
  version: 10.0.0
- category: null
  compile_to: null
  compiler_or_runtime: SBCL
  file_extensions:
    - lisp
    - lsp
    - cl
  id: 4038
  name: Common Lisp
  text: Common Lisp (SBCL 2.0.3)
  version: 2.0.3
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - ml
  id: 4039
  name: OCaml
  text: OCaml (4.10.0)
  version: 4.10.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - m
  id: 4040
  name: Octave
  text: Octave (5.2.0)
  version: 5.2.0
- category: null
  compile_to: null
  compiler_or_runtime: FPC
  file_extensions:
    - pas
  id: 4041
  name: Pascal
  text: Pascal (FPC 3.0.4)
  version: 3.0.4
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - pl
  id: 4042
  name: Perl
  text: Perl (5.26.1)
  version: 5.26.1
- category: null
  compile_to: null
  compiler_or_runtime: Rakudo
  file_extensions:
    - raku
  id: 4043
  name: Raku
  text: Raku (Rakudo 2020.02.1)
  version: 2020.02.1
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - php
  id: 4044
  name: PHP
  text: PHP (7.4.4)
  version: 7.4.4
- category: null
  compile_to: null
  compiler_or_runtime: SWI-Prolog
  file_extensions:
    - pl
  id: 4045
  name: Prolog
  text: Prolog (SWI-Prolog 8.0.3)
  version: 8.0.3
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - py
  id: 4046
  name: PyPy2
  text: PyPy2 (7.3.0)
  version: 7.3.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - py
  id: 4047
  name: PyPy3
  text: PyPy3 (7.3.0)
  version: 7.3.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - rkt
  id: 4048
  name: Racket
  text: Racket (7.6)
  version: '7.6'
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - rb
  id: 4049
  name: Ruby
  text: Ruby (2.7.1)
  version: 2.7.1
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - rs
  id: 4050
  name: Rust
  text: Rust (1.42.0)
  version: 1.42.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - scala
    - sc
  id: 4051
  name: Scala
  text: Scala (2.13.1)
  version: 2.13.1
- category: null
  compile_to: null
  compiler_or_runtime: OpenJDK
  file_extensions:
    - java
  id: 4052
  name: Java
  text: Java (OpenJDK 1.8.0)
  version: 1.8.0
- category: null
  compile_to: null
  compiler_or_runtime: Gauche
  file_extensions:
    - ss
    - scm
    - sls
  id: 4053
  name: Scheme
  text: Scheme (Gauche 0.9.9)
  version: 0.9.9
- category: null
  compile_to: null
  compiler_or_runtime: MLton
  file_extensions:
    - sml
  id: 4054
  name: Standard ML
  text: Standard ML (MLton 20130715)
  version: '20130715'
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - swift
  id: 4055
  name: Swift
  text: Swift (5.2.1)
  version: 5.2.1
- category: null
  compile_to: null
  compiler_or_runtime: cat
  file_extensions:
    - txt
  id: 4056
  name: Text
  text: Text (cat 8.28)
  version: '8.28'
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - ts
  id: 4057
  name: TypeScript
  text: TypeScript (3.8)
  version: '3.8'
- category: null
  compile_to: null
  compiler_or_runtime: .NET Core
  file_extensions: 
    - vb
  id: 4058
  name: Visual Basic
  text: Visual Basic (.NET Core 3.1.101)
  version: 3.1.101
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - sh
  id: 4059
  name: Zsh
  text: Zsh (5.4.2)
  version: 5.4.2
- category: null
  compile_to: null
  compiler_or_runtime: OpenCOBOL
  file_extensions:
    - cob
    - cbl
  id: 4060
  name: COBOL - Fixed
  text: COBOL - Fixed (OpenCOBOL 1.1.0)
  version: 1.1.0
- category: null
  compile_to: null
  compiler_or_runtime: OpenCOBOL
  file_extensions:
    - cob
    - cbl
  id: 4061
  name: COBOL - Free
  text: COBOL - Free (OpenCOBOL 1.1.0)
  version: 1.1.0
- category: null
  compile_to: null
  compiler_or_runtime: bf
  file_extensions:
    - b
    - bf
  id: 4062
  name: Brainfuck
  text: Brainfuck (bf 20041219)
  version: '20041219'
- category: null
  compile_to: null
  compiler_or_runtime: GNAT
  file_extensions:
    - ada
  id: 4063
  name: Ada2012
  text: Ada2012 (GNAT 9.2.1)
  version: 9.2.1
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions: null
  id: 4064
  name: Unlambda
  text: Unlambda (2.0.0)
  version: 2.0.0
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - pyx
    - pxd
    - pxi
  id: 4065
  name: Cython
  text: Cython (0.29.16)
  version: 0.29.16
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - sed
  id: 4066
  name: Sed
  text: Sed (4.4)
  version: '4.4'
- category: null
  compile_to: null
  compiler_or_runtime: null
  file_extensions:
    - vim
  id: 4067
  name: Vim
  text: Vim (8.2.0460)
  version: 8.2.0460
"""
