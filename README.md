# Structural-Matrix-Solver
A high-performance Python library for structural engineering, featuring custom matrix operations and an optimized Banded Cholesky Solver for large-scale Finite Element systems. Computational analysis of two 2D truss structures is performed.
# 🧮 Structural Matrix Solver (V1.0)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Type](https://img.shields.io/badge/Algorithm-Banded%20Cholesky-green.svg)
![Context](https://img.shields.io/badge/Field-Structural%20Engineering-orange.svg)

This library is the mathematical core of a custom-built Finite Element Method (FEM) engine. Developed entirely from scratch without external numerical libraries (such as NumPy), it demonstrates a deep understanding of memory management, matrix bandwidth optimization, and structural mechanics mathematics.

## 🚀 The Challenge
Large-scale structural systems generate massive stiffness matrices. Storing these as standard $N \times N$ arrays is memory-inefficient. This project implements a **Symmetric Banded Matrix** approach to solve these systems using a fraction of the RAM.

## ✨ Core Features

### 📐 1. Custom Linear Algebra Engine
- **Dense Matrix Operations:** Pure Python implementation of matrix multiplication, transposition, and vector mapping.
- **Symmetric Banded Storage:** Only the significant semi-bandwidth ($m$) is stored, reducing memory footprint from $O(N^2)$ to $O(N \times m)$.

### ⚡ 2. Optimized Banded Cholesky Solver
- Implements the **$A = U^T U$ (or $LDL^T$) Factorization** specifically for banded systems.
- Skips zero-value calculations outside the bandwidth, dramatically increasing computational speed for large structural frames.

### 🏗️ 3. FEM Integration Ready
- Designed to integrate directly with 2D Frame/Truss analysis routines.
- Handles Global Stiffness Matrix ($[K]$) assembly with automated symmetry enforcement.

## 🛠️ Implementation Details

### Banded Storage Logic
Standard $N \times N$ matrix is stored in an $N \times (m+1)$ structure where $m$ is the semi-bandwidth.

### Solving Scheme
1. **Factorization:** The banded matrix is decomposed into an upper triangular matrix within the band.
2. **Forward/Backward Substitution:** Efficiently solves $\{F\} = [K]\{D\}$ strictly within the banded memory space.

## 👨‍💻 Engineering Insights
Developing this library provided deep insights into:
- **Numerical Stability:** Managing floating-point precision in large systems.
- **Algorithm Efficiency:** The transition from $O(N^3)$ complexity to $O(N \times m^2)$.
- **Software Architecture:** Building decoupled, reusable modules for future structural analysis projects.

## 🏁 Author
**Muratcan Kılıçtepe**
*Developed as the foundational library for CE 4011 - Structural Analysis.*
