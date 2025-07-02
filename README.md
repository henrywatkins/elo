# ELO ratings tool

A simple command-line ELO ratings tool for calculating and ranking players in zero-sum games. 

## Installation

```bash
pip install elo
```

## Usage

This command line tool can be used to track and calculate Elo ratings for any binary (win/lose) game (chess, fencing, judo, football, etc.) 

First create a table e.g. chess
```bash
elo create chess
```

Then log the results of successive games, with the winner and loser named in the format 'winner-loser' e.g.
```bash
elo log chess john-tom
```

You can print the table of ratings using
```bash
elo show chess
```