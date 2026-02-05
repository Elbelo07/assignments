[![CI](https://github.com/Elbelo07/assignments/actions/workflows/ci.yml/badge.svg)](https://github.com/Elbelo07/assignments/actions/workflows/ci.yml)

# Foundations Learning Path – Assignments

This repository contains my work for the Foundations Learning Path.

The Foundations Learning Path is designed as a progressive sequence of assignments whose goal is to apply software engineering best practices to data-oriented projects. Instead of treating each assignment as an isolated exercise, the learning path builds a cumulative codebase that is continuously extended, refactored, and improved over time.

The topics covered throughout the learning path include clean code, testing, linting, packaging, continuous integration, object-oriented programming, and design patterns.

---

## Project Structure

assignments/
├── assignment_0/
├── assignment_1/
├── assignment_2/
├── assignment_3/
├── assignment_4/
├── assignment_5/
├── life_expectancy/
│ ├── data/
│ ├── tests/
│ ├── cleaning.py
│ └── init.py
├── pyproject.toml
├── README.md

Each `assignment_*` directory contains the instructions and context for a specific assignment.  
The `life_expectancy` package is the shared project that is reused and evolved across multiple assignments.

---

## Current Progress

### Assignment 0 – Project Setup (Completed)

The initial assignment focused on setting up the project correctly from the start. This included packaging the project using `pyproject.toml`, configuring a virtual environment, installing the project in editable mode with pip, and validating the setup using automated tests.

---

### Assignment 1 – EU Life Expectancy: Data Cleaning & Code Quality (Completed)

In this assignment, a full data cleaning pipeline was implemented using Eurostat life expectancy data. The work included reshaping the dataset from wide to long format, separating and cleaning the different dimensions, validating year and value fields, filtering data by country through a command-line interface, and exporting the cleaned dataset to CSV.

In addition to the data processing logic, this assignment introduced code quality practices such as unit testing with pytest, test coverage enforcement, linting with pylint, and continuous integration using GitHub Actions.

---

### Upcoming Assignments

The following assignments are not yet completed and will further extend and refactor the existing codebase:

- Assignment 2 – Linting and Formatting
- Assignment 3 – Continuous Integration
- Assignment 4 – Object-Oriented Programming
- Assignment 5 – Design Patterns

Each new assignment builds on top of the previous ones, progressively improving the structure, quality, and robustness of the project.

---

## Author

Lourenço Shirley Belo

---

## Notes

This repository is a learning project. While the assignments are educational in nature, the codebase is intentionally structured to reflect real-world practices for writing clean, maintainable, and production-oriented Python code.
