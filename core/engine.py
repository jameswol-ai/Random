from core.scheduler import tick_all
from meta.observation import collect_stats
from meta.rule_engine import evolve_rules

class SimulationEngine:
    def __init__(self, world, agents, architecture):
        self.world = world
        self.agents = agents
        self.architecture = architecture
        self.tick = 0

    def step(self):
        # 1. physics + world update
        self.world.update()

        # 2. agent behavior
        for agent in self.agents:
            agent.update(self.world)

        # 3. architecture evolution
        self.architecture.evolve_cycle()

        # 4. meta observation
        stats = collect_stats(self.world, self.agents, self.architecture)

        # 5. self-modifying rules
        evolve_rules(stats)

        self.tick += 1