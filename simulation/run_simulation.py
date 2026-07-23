from isaacsim import SimulationApp

from drone_sim.scenarios import Scenario

def choose_scenario() -> str:
    """Prompt the user to choose a scenario and return its name.

    Returns the name rather than an instance: instantiating a scenario imports
    Isaac Sim modules, which is only possible after SimulationApp is created.
    """
    scenarios = Scenario.available()
    print("Available scenarios:")
    for index, scenario_name in enumerate(scenarios, start=1):
        print(f"{index}. {scenario_name}")

    choice = input("Choose a scenario (number or name): ").strip()
    if choice.isdigit():
        number = int(choice)
        if not 1 <= number <= len(scenarios):
            raise SystemExit(
                f"Invalid number '{choice}'. Choose between 1 and {len(scenarios)}."
            )
        choice = scenarios[number - 1]
    elif choice not in scenarios:
        raise SystemExit(
            f"Unknown scenario '{choice}'. Available: {', '.join(scenarios)}"
        )

    print(f"Selected scenario: {choice}")
    return choice

def main():
    """Main entry point for the simulation script."""
    name = choose_scenario()

    simulation_app = SimulationApp({"headless": False})
    try:
        scenario = Scenario.create(name)
        print(f"Running scenario '{name}'...")
        scenario.run(simulation_app)
    finally:
        simulation_app.close()

if __name__ == "__main__":
    main()
