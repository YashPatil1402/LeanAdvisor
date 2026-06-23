from categories.material_management import material_management
from categories.concrete_works import concrete_works
from categories.reinforcement_works import reinforcement_works
from categories.shuttering_formwork import shuttering_formwork
from categories.planning_scheduling import planning_scheduling
from categories.masonry_works import masonry_works
from categories.plastering_works import plastering_works
from categories.finishing_works import finishing_works
from categories.quality_management import quality_management
from categories.safety_management import safety_management
from categories.productivity_management import productivity_management
from categories.labour_management import labour_management
from categories.equipment_management import equipment_management
from categories.communication_coordination import communication_coordination
from categories.supply_chain_management import supply_chain_management
from categories.waste_reduction_5s import waste_reduction_5s
from categories.site_logistics_management import site_logistics_management
from categories.inventory_storage import inventory_storage
from categories.client_design_management import client_design_management
from categories.project_control_performance_management import (
    project_control_performance_management
)


problems = {

    "Material Management": material_management,

    "Concrete Works": concrete_works,

    "Reinforcement Works": reinforcement_works,

    "Shuttering and Formwork": shuttering_formwork,

    "Planning and Scheduling": planning_scheduling,

    "Masonry Works": masonry_works,

    "Plastering Works": plastering_works,

    "Finishing Works": finishing_works,

    "Quality Management": quality_management,

    "Safety Management": safety_management,

    "Productivity Management": productivity_management,

    "Labour Management": labour_management,

    "Equipment Management": equipment_management,

    "Communication and Coordination": communication_coordination,

    "Supply Chain Management": supply_chain_management,

    "Waste Reduction and 5S": waste_reduction_5s,

    "Site Logistics Management": site_logistics_management,

    "Inventory and Storage": inventory_storage,

    "Client and Design Management": client_design_management,

    "Project Control and Performance Management":
        project_control_performance_management

}


# Calculate total number of problems
total_problems = sum(len(category) for category in problems.values())

print("Categories:", len(problems))
print("Total Problems:", total_problems)