"""
Genetic Optimiser — Evolutionary Parameter Search
===================================================
WHEN TO USE: You have a system with tuneable numeric parameters and you
want to find the best combination without exhaustive search. Especially
useful when the parameter space is large and interactions between
parameters are non-obvious.

EXAMPLES:
- Marketing: optimal posting cadence × time of day × hashtag count × CTA style
- Content: which combination of length, tone, format works best per platform
- Interview: which question ordering produces best Business Bible output
- Pricing: price point × discount structure × payment terms × bundling
- Agent config: temperature × max_tokens × system_prompt_length × retry_count

HOW IT WORKS (genetic algorithm):
1. Create population of random parameter combinations
2. Evaluate fitness of each (backtest, simulate, or score)
3. Select top 20% (elite)
4. Breed next generation: crossover between elite + random mutations
5. Repeat for N generations
6. Top survivors are your best parameter sets

INPUTS:
- Base parameters (current config)
- Fitness function (you provide this — how to score a parameter set)
- Config (population size, generations, mutation rate)

OUTPUTS:
- Ranked list of best parameter combinations
- Fitness scores for each

Provenance: Nexus V2 kaizen_l3_tournament.py (470 lines) → generalised.
Devon-b3d8 | 2026-05-15
"""

import copy
import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import numpy as np


@dataclass
class GeneticConfig:
    """Genetic optimiser configuration."""

    population_size: int = 50           # Variants per generation
    generations: int = 10               # Rounds of evolution
    mutation_rate: float = 0.15         # Probability of mutating each parameter
    crossover_rate: float = 0.30        # Probability of crossover vs pure mutation
    elitism: int = 2                    # Top N survive unchanged

    # Fitness weights (for composite scoring)
    # Users override these based on what they care about
    weight_primary: float = 0.35        # Main metric (e.g., Sharpe, conversion rate)
    weight_secondary: float = 0.25      # Secondary (e.g., return, revenue)
    weight_safety: float = 0.20         # Safety (e.g., max drawdown, churn)
    weight_efficiency: float = 0.10     # Efficiency (e.g., Calmar, cost per acquisition)
    weight_consistency: float = 0.10    # Consistency (e.g., % months positive)


@dataclass
class Organism:
    """A parameter set being evolved."""
    org_id: str
    generation: int
    parameters: dict
    parent_ids: List[str] = field(default_factory=list)
    fitness_score: float = 0.0
    metrics: dict = field(default_factory=dict)


def mutate(params: dict, rate: float = 0.15) -> dict:
    """
    Mutate parameters with gaussian perturbation.

    Each numeric parameter has `rate` probability of being mutated.
    Mutation: value × (1 + gauss(0, 0.15)) — roughly ±15% typical change.
    Integers stay as integers. Lists have elements mutated individually.
    """
    mutated = {}

    for key, value in params.items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if random.random() < rate:
                noise = random.gauss(0, 0.15)
                new_value = value * (1 + noise)

                if isinstance(value, int):
                    new_value = max(1, int(round(new_value)))
                else:
                    new_value = round(new_value, 6)

                mutated[key] = new_value
            else:
                mutated[key] = value
        elif isinstance(value, list):
            mutated[key] = [
                max(1, int(round(v * (1 + random.gauss(0, 0.1)))))
                if isinstance(v, (int, float)) and random.random() < rate
                else v
                for v in value
            ]
        else:
            mutated[key] = value

    return mutated


def crossover(parent_a: dict, parent_b: dict) -> dict:
    """
    Uniform crossover: for each parameter, randomly pick from parent A or B.
    """
    child = {}
    for key in parent_a:
        if key in parent_b:
            child[key] = parent_a[key] if random.random() < 0.5 else parent_b[key]
        else:
            child[key] = parent_a[key]
    return child


def create_population(
    base_params: dict,
    cfg: Optional[GeneticConfig] = None,
) -> List[Organism]:
    """
    Create initial population. First organism is the current live params
    (defending champion). Rest are random mutations with wider spread.
    """
    if cfg is None:
        cfg = GeneticConfig()

    population = []

    # Champion: current params unchanged
    champion = Organism(
        org_id="g0_champion",
        generation=0,
        parameters=copy.deepcopy(base_params),
        parent_ids=["live"],
    )
    population.append(champion)

    # Random mutations with wider initial spread
    for i in range(cfg.population_size - 1):
        mutated = mutate(base_params, rate=0.30)
        org = Organism(
            org_id=f"g0_org{i}",
            generation=0,
            parameters=mutated,
            parent_ids=["random"],
        )
        population.append(org)

    return population


def breed_next_generation(
    population: List[Organism],
    generation: int,
    cfg: Optional[GeneticConfig] = None,
) -> List[Organism]:
    """
    Create next generation from top performers.

    Selection: top 20% survive.
    Elitism: top N survive unchanged.
    Rest: crossover between elite + mutation.
    """
    if cfg is None:
        cfg = GeneticConfig()

    # Select elite (top 20%)
    elite_count = max(2, len(population) // 5)
    elite = population[:elite_count]  # Assumes sorted by fitness

    next_gen = []

    # Elitism: top N survive unchanged
    for i, org in enumerate(elite[:cfg.elitism]):
        survivor = Organism(
            org_id=f"g{generation}_elite{i}",
            generation=generation,
            parameters=copy.deepcopy(org.parameters),
            parent_ids=[org.org_id],
        )
        next_gen.append(survivor)

    # Fill rest via crossover + mutation
    while len(next_gen) < cfg.population_size:
        if random.random() < cfg.crossover_rate and len(elite) >= 2:
            parent_a = random.choice(elite)
            parent_b = random.choice(elite)
            child_params = crossover(parent_a.parameters, parent_b.parameters)
            child_params = mutate(child_params, cfg.mutation_rate)
            parents = [parent_a.org_id, parent_b.org_id]
        else:
            parent = random.choice(elite)
            child_params = mutate(parent.parameters, cfg.mutation_rate)
            parents = [parent.org_id]

        child = Organism(
            org_id=f"g{generation}_child{len(next_gen)}",
            generation=generation,
            parameters=child_params,
            parent_ids=parents,
        )
        next_gen.append(child)

    return next_gen


def run_tournament(
    base_params: dict,
    fitness_fn: Callable[[dict], dict],
    cfg: Optional[GeneticConfig] = None,
) -> List[Organism]:
    """
    Run a full genetic tournament.

    Args:
        base_params: Current live parameters (the defending champion)
        fitness_fn: Function that takes a parameter dict and returns a dict
                    with keys: 'primary', 'secondary', 'safety', 'efficiency',
                    'consistency' (all floats). Missing keys default to 0.
        cfg: Tournament configuration

    Returns:
        Final population sorted by fitness (best first).

    Example fitness_fn:
        def my_fitness(params):
            # Simulate/backtest with these params
            result = simulate(params)
            return {
                'primary': result.sharpe_ratio,
                'secondary': result.total_return,
                'safety': 1 + result.max_drawdown,  # Less negative = better
                'efficiency': result.calmar_ratio,
                'consistency': result.pct_months_positive,
            }
    """
    if cfg is None:
        cfg = GeneticConfig()

    # Create initial population
    population = create_population(base_params, cfg)

    for gen_i in range(cfg.generations):
        # Evaluate fitness
        for org in population:
            metrics = fitness_fn(org.parameters)
            org.metrics = metrics
            org.fitness_score = (
                metrics.get("primary", 0) * cfg.weight_primary +
                metrics.get("secondary", 0) * cfg.weight_secondary +
                metrics.get("safety", 0) * cfg.weight_safety +
                metrics.get("efficiency", 0) * cfg.weight_efficiency +
                metrics.get("consistency", 0) * cfg.weight_consistency
            )

        # Sort by fitness
        population.sort(key=lambda o: o.fitness_score, reverse=True)

        # Breed next generation (except last iteration)
        if gen_i < cfg.generations - 1:
            population = breed_next_generation(
                population, gen_i + 1, cfg
            )

    # Final evaluation
    for org in population:
        metrics = fitness_fn(org.parameters)
        org.metrics = metrics
        org.fitness_score = (
            metrics.get("primary", 0) * cfg.weight_primary +
            metrics.get("secondary", 0) * cfg.weight_secondary +
            metrics.get("safety", 0) * cfg.weight_safety +
            metrics.get("efficiency", 0) * cfg.weight_efficiency +
            metrics.get("consistency", 0) * cfg.weight_consistency
        )

    population.sort(key=lambda o: o.fitness_score, reverse=True)
    return population
