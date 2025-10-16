from typing import Dict, List, NamedTuple, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, CollectionState

if TYPE_CHECKING:
    from . import ValheimWorld


class ValheimConnection(NamedTuple):
    destination: str  # Name of the region the connection leads to
    required_items: Dict[str, int]  # Item name → Count required


class ValheimRegion(NamedTuple):
    connections: List[ValheimConnection]  # List of connections from this region


def create_connection_rule(required_items: Dict[str, int], world: "ValheimWorld") -> Callable[[CollectionState], bool]:
    """
    Generate an access rule for a connection based on required items.
    """
    def rule(state: CollectionState) -> bool:
        return state.has_all_counts(required_items, world.player)
    return rule


# Define regions and their connections parsed from a text file
region_data_table: Dict[str, ValheimRegion] = {}

# Example region connections text data
region_txt = '''
Menu,Tier0
Tier0,Tier1,item:researchWorkbench
Tier1,Tier2,item:researchAxeTier1
Tier2,Tier3,item:researchBoatTier1,item:researchForge,item:researchPickaxeTier1,item:researchSmelter
Tier3,Tier4,item:researchBronze
Tier4,Tier5,item:researchAxeTier2
Tier5,Tier6,item:researchPickaxeTier2
Tier6,Tier7,item:researchForgeUpgrade1,item:researchNailsTier2,item:researchPickaxeTier3,item:researchWarmthTier1
Tier7,Tier8,item:researchArtisanTable,item:researchBlastFurnace
Tier8,Tier9,item:researchAxeTier4,item:researchForgeUpgrade2,item:researchForgeUpgrade3,item:researchSpinningWheel,item:researchWispFountain,item:researchWisplight
Tier9,Tier10,item:researchPickaxeTier4
Tier10,Tier11,item:researchArtisanUpgrade1,item:researchBoatTier4,item:researchCeramicPlate
'''

# Parse region data
for line in region_txt.strip().splitlines():
    if not line or line.startswith("//"):
        continue

    parts = line.split(",")
    if len(parts) < 2:
        print(f"Malformed line: {line}")  # Debugging output
        continue

    source_region = parts[0].strip()
    destination_region = parts[1].strip()
    required_items = {}

    # Parse item requirements if available
    if len(parts) > 2:
        for i in range(2, len(parts), 2):
            item = parts[i].strip()
            count = int(parts[i + 1].strip())
            required_items[item] = count

    # Ensure the source region exists
    if source_region not in region_data_table:
        region_data_table[source_region] = ValheimRegion(connections=[])

    # Add the connection to the source region
    region_data_table[source_region].connections.append(
        ValheimConnection(destination=destination_region, required_items=required_items)
    )

    # Ensure the destination region exists (even if it has no connections initially)
    if destination_region not in region_data_table:
        region_data_table[destination_region] = ValheimRegion(connections=[])


def create_regions(world: "ValheimWorld"):
    """
    Step 1: Create all regions and add them to the multiworld.
    """
    created_regions = {
        region_name: Region(region_name, world.player, world.multiworld)
        for region_name in region_data_table
    }
    world.multiworld.regions.extend(created_regions.values())

    """
    Step 2: Add connections between regions using entrances.
    """
    for region_name, region in region_data_table.items():
        source_region = created_regions[region_name]

        for connection in region.connections:
            destination_region = created_regions[connection.destination]

            # Create an entrance in the source region leading to the destination
            entrance_name = f"{source_region.name} -> {destination_region.name}"
            entrance = Entrance(world.player, entrance_name, source_region)

            # Connect the entrance to the destination region
            entrance.connect(destination_region)

            # If the connection has access rules, assign them to the entrance
            if connection.required_items:
                entrance.access_rule = create_connection_rule(connection.required_items, world)

            # Add the entrance to the source region's exits
            source_region.exits.append(entrance)