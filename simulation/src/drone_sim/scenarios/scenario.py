#!/usr/bin/env python

import importlib
import pkgutil
from abc import ABC, abstractmethod

class Scenario(ABC):
    @abstractmethod
    def run(self, simulation_app):
        pass

    @classmethod
    def available(cls) -> list[str]:
        """Return the scenario module names, without importing the modules.

        Every module in this package is a scenario, except this base module
        and helpers prefixed with an underscore. The filename is the scenario
        name.
        """
        import drone_sim.scenarios as pkg
        return sorted(
            module.name
            for module in pkgutil.iter_modules(pkg.__path__)
            if module.name != "scenario" and not module.name.startswith("_")
        )

    @classmethod
    def create(cls, name: str) -> "Scenario":
        """Import the chosen scenario module and instantiate its Scenario subclass.

        Scenario modules import Isaac Sim packages at the top level, so this
        must only be called after the SimulationApp has been created.
        """
        if name not in cls.available():
            raise ValueError(
                f"Unknown scenario '{name}'. Available: {', '.join(cls.available())}"
            )
        module = importlib.import_module(f"drone_sim.scenarios.{name}")
        for obj in vars(module).values():
            if isinstance(obj, type) and issubclass(obj, Scenario) and obj is not Scenario:
                return obj()
        raise ValueError(f"Module '{name}' does not define a Scenario subclass.")
