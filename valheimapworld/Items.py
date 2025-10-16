from typing import Dict, NamedTuple, List, TYPE_CHECKING
from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import ValheimWorld


class ValheimItem(NamedTuple):
    id: int
    item_name: str  # Name of the item
    game_id: str  # Unique ID for the item (used internally in the game)
    count: int  # Total count of this item
    item_type: str  # Type of the item (e.g., KeyItem, CharacterSkill, etc.)
    classification: ItemClassification  # Progression, Useful, Filler, Trap


# Item data will be parsed from a text file
item_data_table: List[ValheimItem] = []

# Example text data for items
items_txt = '''
// Item User Friendly Name,ID,Count,Type,Classification
Crafting,item:researchWorkbench,1,Item,Progression
Clubs Tier 1,item:researchClubTier1,1,Item,Useful
Lighting Tier 1,item:researchLightingTier1,1,Item,Filler
Axes Tier 1,item:researchAxeTier1,1,Item,Progression
Workbench Upgrade 1,item:researchWorkbenchUpgrade1,1,Item,Useful
Workbench Upgrade 2,item:researchWorkbenchUpgrade2,1,Item,Useful
Cape Tier 1,item:researchCapeTier1,1,Item,Useful
Cape Tier 2,item:researchCapeTier2,1,Item,Useful
Rag Armor,item:researchRagArmor,1,Item,Useful
Leather Armor,item:researchLeatherArmor,1,Item,Useful
Troll Armor,item:researchTrollArmor,1,Item,Useful
Bear Armor,item:researchBearArmor,1,Item,Useful
Blades Tier 1,item:researchBladesTier1,1,Item,Useful
Spears Tier 1,item:researchSpearTier1,1,Item,Useful
Short Blades Tier 1,item:researchShortBladesTier1,1,Item,Useful
Knuckles Tier 1,item:researchKnucklesTier1,1,Item,Useful
Bows Tier 1,item:researchBowsTier1,1,Item,Useful
Arrows Tier 1,item:researchArrowsTier1,1,Item,Useful
Arrows Tier 2,item:researchArrowsTier2,1,Item,Useful
Hoe,item:researchHoe,1,Item,Useful
Beekeping,item:researchBeekeping,1,Item,Useful
Wooden Floors,item:researchFloorWood,1,Item,Useful
Wooden Stairs,item:researchStairsWood,1,Item,Useful
Wooden Walls,item:researchWallsWood,1,Item,Useful
Wooden Roofs,item:researchRoofsWood,1,Item,Useful
Wooden Beams,item:researchBeamsWood,1,Item,Useful
Wooden Doors,item:researchDoorsWood,1,Item,Useful
Cooking Station,item:researchCookingStation,1,Item,Useful
Storage Tier 1,item:researchStorageTier1,1,Item,Useful
Storage Tier 2,item:researchStorageTier2,1,Item,Useful
Bed Tier 1,item:researchBedTier1,1,Item,Useful
Shields Tier 1,item:researchShieldTier1,1,Item,Useful
Tower Shields Tier 1,item:researchTowerShieldTier1,1,Item,Useful
Charcoal Kiln,item:researchCharcoalKiln,1,Item,Useful
Pickaxes Tier 1,item:researchPickaxeTier1,1,Item,Progression
Boat Tier 1,item:researchBoatTier1,1,Item,Progression
Smelter,item:researchSmelter,1,Item,Progression
Forge,item:researchForge,1,Item,Progression
Sledgehammers Tier 1,item:researchSledgehammerTier1,1,Item,Useful
Corewood Beams,item:researchBeamsCorewood,1,Item,Filler
Bronze,item:researchBronze,1,Item,Progression
Short Blades Tier 2,item:researchShortBladesTier2,1,Item,Useful
Harpoon,item:researchHarpoon,1,Item,Useful
Darkwood Roofs,item:researchRoofsDarkwood,1,Item,Filler
Darkwood Beams,item:researchBeamsDarkwood,1,Item,Filler
Darkwood Decorations,item:researchDecorationsDarkwod,1,Item,Filler
Cauldron,item:researchCauldron,1,Item,Useful
Cauldron Upgrade 1,item:researchCauldronUpgrade1,1,Item,Useful
Mead ketill,item:researchMeadketill,1,Item,Useful
Knife Butcher,item:researchKnifeButcher,1,Item,Useful
Nails Tier 1,item:researchNailsTier1,1,Item,Useful
Axes Tier 2,item:researchAxeTier2,1,Item,Progression
Workbench Upgrade 3,item:researchWorkbenchUpgrade3,1,Item,Useful
Bronze Armor,item:researchBronzeArmor,1,Item,Useful
Clubs Tier 2,item:researchClubTier2,1,Item,Useful
Blades Tier 2,item:researchBladesTier2,1,Item,Useful
Spears Tier 2,item:researchSpearTier2,1,Item,Useful
Polearms Tier 1,item:researchPolearmsTier1,1,Item,Useful
Arrows Tier 3,item:researchArrowsTier3,1,Item,Useful
Trinkets Tier 1,item:researchTrinketTier1,1,Item,Useful
Transportation Tier 1,item:researchTransportationTier1,1,Item,Useful
Transportation Tier 2,item:researchTransportationTier2,1,Item,Useful
Boat Tier 2,item:researchBoatTier2,1,Item,Useful
Cultivator,item:researchCultivator,1,Item,Useful
Bucklers Tier 1,item:researchBucklerTier1,1,Item,Useful
Pickaxes Tier 2,item:researchPickaxeTier2,1,Item,Progression
Root Armor,item:researchRootArmor,1,Item,Useful
Short Blades Tier 3,item:researchShortBladesTier3,1,Item,Useful
Bows Tier 2,item:researchBowsTier2,1,Item,Useful
Fermenter,item:researchFermenter,1,Item,Useful
Bonfire,item:researchWarmthTier2,1,Item,Useful
Shields Tier 2,item:researchShieldTier2,1,Item,Useful
Pickaxes Tier 3,item:researchPickaxeTier3,1,Item,Progression
Warmth Tier 1,item:researchWarmthTier1,1,Item,Progression
Forge Upgrade 1,item:researchForgeUpgrade1,1,Item,Progression
Forge Upgrade 4,item:researchForgeUpgrade4,1,Item,Useful
Forge Upgrade 5,item:researchForgeUpgrade5,1,Item,Useful
Forge Upgrade 6,item:researchForgeUpgrade6,1,Item,Useful
Stonecutter,item:researchStonecutter,1,Item,Useful
Iron Armor,item:researchIronArmor,1,Item,Useful
Axes Tier 3,item:researchAxeTier3,1,Item,Useful
Battleaxes Tier 1,item:researchBattleaxeTier1,1,Item,Useful
Clubs Tier 3,item:researchClubTier3,1,Item,Useful
Sledgehammers Tier 2,item:researchSledgehammerTier2,1,Item,Useful
Blades Tier 3,item:researchBladesTier3,1,Item,Useful
Spears Tier 3,item:researchSpearTier3,1,Item,Useful
Polearms Tier 2,item:researchPolearmsTier2,1,Item,Useful
Bows Tier 3,item:researchBowsTier3,1,Item,Useful
Arrows Tier 4,item:researchArrowsTier4,1,Item,Useful
Trinkets Tier 2,item:researchTrinketTier2,1,Item,Useful
Darkwood Doors,item:reserachDoorsDarkwood,1,Item,Useful
Windmill,item:researchWindmill,1,Item,Useful
Iron Cooking Station,item:researchIronCookingStation,1,Item,Useful
Food Preparation Table,item:researchPreparationTable,1,Item,Useful
Storage Tier 3,item:researchStorageTier3,1,Item,Useful
Boat Tier 3,item:researchBoatTier3,1,Item,Useful
Bed Tier 2,item:researchBedTier2,1,Item,Useful
Hearth,item:researchWarmthTier3,1,Item,Useful
Tower Shields Tier 2,item:researchTowerShieldTier2,1,Item,Useful
Bucklers Tier 2,item:researchBucklerTier2,1,Item,Useful
Workbench Upgrade 4,item:researchWorkbenchUpgrade4,1,Item,Useful
Artisan Table,item:researchArtisanTable,1,Item,Progression
Blast Furnace,item:researchBlastFurnace,1,Item,Progression
Fenris Armor,item:researchFenrisArmor,1,Item,Useful
Wolf Armor,item:researchWolfArmor,1,Item,Useful
Battleaxes Tier 2,item:researchBattleaxeTier2,1,Item,Useful
Clubs Tier 4,item:researchClubTier4,1,Item,Useful
Blades Tier 4,item:researchBladesTier4,1,Item,Useful
Spears Tier 4,item:researchSpearTier4,1,Item,Useful
Short Blades Tier 4,item:researchShortBladesTier4,1,Item,Useful
Knuckles Tier 2,item:researchKnucklesTier2,1,Item,Useful
Bows Tier 4,item:researchBowsTier4,1,Item,Useful
Arrows Tier 5,item:researchArrowsTier5,1,Item,Useful
Arrows Tier 6,item:researchArrowsTier6,1,Item,Useful
Arrows Tier 7,item:researchArrowsTier7,1,Item,Useful
Arrows Tier 8,item:researchArrowsTier8,1,Item,Useful
Arrows Tier 9,item:researchArrowsTier9,1,Item,Useful
Trinkets Tier 3,item:researchTrinketTier3,1,Item,Useful
Cauldron Upgrade 2,item:researchCauldronUpgrade2,1,Item,Useful
Shields Tier 3,item:researchShieldTier3,1,Item,Useful
Nails Tier 2,item:researchNailsTier2,1,Item,Progression
Axes Tier 4,item:researchAxeTier4,1,Item,Progression
Wisp Fountain,item:researchWispFountain,1,Item,Progression
Wisplight,item:researchWisplight,1,Item,Progression
Forge Upgrade 2,item:researchForgeUpgrade2,1,Item,Progression
Forge Upgrade 3,item:researchForgeUpgrade3,1,Item,Progression
Spinning Wheel,item:researchSpinningWheel,1,Item,Progression
Cape Tier 3,item:researchCapeTier3,1,Item,Useful
Cape Tier 4,item:researchCapeTier4,1,Item,Useful
Cape Tier 5,item:researchCapeTier5,1,Item,Useful
Vilebone Armor,item:researchVileboneArmor,1,Item,Useful
Padded Armor,item:researchPaddedArmor,1,Item,Useful
Battleaxes Tier 3,item:researchBattleaxeTier3,1,Item,Useful
Clubs Tier 5,item:researchClubTier5,1,Item,Useful
Blades Tier 5,item:researchBladesTier5,1,Item,Useful
Polearms Tier 3,item:researchPolearmsTier3,1,Item,Useful
Short Blades Tier 5,item:researchShortBladesTier5,1,Item,Useful
Short Blades Tier 6,item:researchShortBladesTier6,1,Item,Useful
Knuckles Tier 3,item:researchKnucklesTier3,1,Item,Useful
Trinkets Tier 4,item:researchTrinketTier4,1,Item,Useful
Stone Oven,item:researchStoneOven,1,Item,Useful
Cauldron Upgrade 3,item:researchCauldronUpgrade3,1,Item,Useful
Cauldron Upgrade 4,item:researchCauldronUpgrade4,1,Item,Useful
Storage Tier 4,item:researchStorageTier4,1,Item,Useful
Scythe,item:researchScythe,1,Item,Useful
Shields Tier 4,item:researchShieldTier4,1,Item,Useful
Tower Shields Tier 3,item:researchTowerShieldTier3,1,Item,Useful
Pickaxes Tier 4,item:researchPickaxeTier4,1,Item,Progression
Sap Extractor,item:researchSapExtractor,1,Item,Useful
Eitr Refinery,item:researchEitrRefinery,1,Item,Useful
Black Forge,item:researchBlackForge,1,Item,Useful
Black Forge Upgrade 1,item:researchBlackForgeUpgrade1,1,Item,Useful
Black Forge Upgrade 2,item:researchBlackForgeUpgrade2,1,Item,Useful
Carapace Armor,item:researchCarapaceArmor,1,Item,Useful
Long Blades Tier 1,item:researchLongBladesTier1,1,Item,Useful
Spears Tier 5,item:researchSpearTier5,1,Item,Useful
Arrows Tier 10,item:researchArrowsTier10,1,Item,Useful
Crossbows Tier 1,item:researchCrossbowsTier1,1,Item,Useful
Bolts Tier 1,item:researchBoltsTier1,1,Item,Useful
Bolts Tier 2,item:researchBoltsTier2,1,Item,Useful
Bolts Tier 3,item:researchBoltsTier3,1,Item,Useful
Dvergr Doors,item:researchDvergrDoors,1,Item,Filler
Dvergr Fences,item:researchDvergrFences,1,Item,Filler
Dvergr Stairs,item:researchDvergrStairs,1,Item,Filler
Ceramic Plates,item:researchCeramicPlate,1,Item,Progression
Boat Tier 4,item:researchBoatTier4,1,Item,Progression
Artisan Press,item:researchArtisanUpgrade1,1,Item,Progression
Galdr Table,item:researchGaldrTable,1,Item,Useful
Galdr Table Upgrade 1,item:researchGaldrTableUpgrade1,1,Item,Useful
Galdr Table Upgrade 2,item:researchGaldrTableUpgrade2,1,Item,Useful
Cape Tier 6,item:researchCapeTier6,1,Item,Useful
Eitr Armor,item:researchEitrArmor,1,Item,Useful
Axes Tier 5,item:researchAxeTier5,1,Item,Useful
Battleaxes Tier 4,item:researchBattleaxeTier4,1,Item,Useful
Sledgehammers Tier 3,item:researchSledgehammerTier3,1,Item,Useful
Blades Tier 6,item:researchBladesTier6,1,Item,Useful
Polearms Tier 4,item:researchPolearmsTier4,1,Item,Useful
Bows Tier 5,item:researchBowsTier5,1,Item,Useful
Elemental Magic Tier 1,item:researchElementalMagicTier1,1,Item,Useful
Blood Magic Tier 1,item:reserachBloodMagicTier1,1,Item,Useful
Trinkets Tier 5,item:researchTrinketTier5,1,Item,Useful
Shields Tier 5,item:researchShieldTier5,1,Item,Useful
Bucklers Tier 3,item:researchBucklerTier3,1,Item,Useful
Black Forge Upgrade 3,item:researchBlackForgeUpgrade3,1,Item,Useful
Black Forge Upgrade 4,item:researchBlackForgeUpgrade4,1,Item,Useful
Galdr Table Upgrade 3,item:researchGaldrTableUpgrade3,1,Item,Useful
Cape Tier 7,item:researchCapeTier7,1,Item,Useful
Cape Tier 8,item:researchCapeTier8,1,Item,Useful
Ask Armor,item:researchAskArmor,1,Item,Useful
Embla Armor,item:researchEmblaArmor,1,Item,Useful
Flametal Armor,item:researchFlametalArmor,1,Item,Useful
Battleaxes Tier 5,item:researchBattleaxeTier5,1,Item,Useful
Battleaxes Tier 6,item:researchBattleaxeTier6,1,Item,Useful
Clubs Tier 6,item:researchClubTier6,1,Item,Useful
Clubs Tier 7,item:researchClubTier7,1,Item,Useful
Blades Tier 7,item:researchBladesTier7,1,Item,Useful
Blades Tier 8,item:researchBladesTier8,1,Item,Useful
Long Blades Tier 2,item:researchLongBladesTier2,1,Item,Useful
Long Blades Tier 3,item:researchLongBladesTier3,1,Item,Useful
Spears Tier 6,item:researchSpearTier6,1,Item,Useful
Spears Tier 7,item:researchSpearTier7,1,Item,Useful
Bows Tier 6,item:researchBowsTier6,1,Item,Useful
Bows Tier 7,item:researchBowsTier7,1,Item,Useful
Arrows Tier 11,item:researchArrowsTier11,1,Item,Useful
Crossbows Tier 2,item:researchCrossbowsTier2,1,Item,Useful
Crossbows Tier 3,item:researchCrossbowsTier3,1,Item,Useful
Bolts Tier 4,item:researchBoltsTier4,1,Item,Useful
Elemental Magic Tier 2,item:researchElementalMagicTier2,1,Item,Useful
Elemental Magic Tier 3,item:researchElementalMagicTier3,1,Item,Useful
Blood Magic Tier 2,item:researchBloodMagicTier2,1,Item,Useful
Siege,item:researchSiege,1,Item,Useful
Trinkets Tier 6,item:researchTrinketTier6,1,Item,Useful
Ashwood Floors,item:researchAshwoodFloor,1,Item,Filler
Ashwood Walls,item:researchAshwoodWalls,1,Item,Filler
Ashwood Decorations,item:researchAshwoodDecoration,1,Item,Filler
Ashwood Beams,item:researchAshwoodBeams,1,Item,Filler
Ashwood Stairs,item:researchAshwoodStairs,1,Item,Filler
Ashwood Doors,item:researchAshwoodDoors,1,Item,Filler
Transportation Tier 3,item:researchTransportationTier3,1,Item,Useful
Cauldron Upgrade 5,item:researchCauldronUpgrade5,1,Item,Useful
Bed Tier 3,item:researchBedTier3,1,Item,Useful
Shields Tier 6,item:researchShieldTier6,1,Item,Useful
Tower Shields Tier 4,item:researchTowerShieldTier4,1,Item,Useful
Trophy: TrophyNeck,item:researchTrophyNeck,1,Item,Useful
Trophy: TrophyBoar,item:researchTrophyBoar,1,Item,Useful
Trophy: TrophyDeer,item:researchTrophyDeer,1,Item,Useful
Trophy: TrophyGreydwarfBrute,item:researchTrophyGreydwarfBrute,1,Item,Useful
Trophy: TrophyBjorn,item:researchTrophyBear,1,Item,Useful
Trophy: TrophyForestTroll,item:researchTrophyTroll,1,Item,Useful
Trophy: TrophySkeleton,item:researchTrophySkeleton,1,Item,Useful
Trophy: TrophyGreydwarfShaman,item:researchTrophyGreydwarfShaman,1,Item,Useful
Trophy: TrophySkeletonPoison,item:researchTrophyRancidRemains,1,Item,Useful
Trophy: TrophyEikthyr,item:researchTrophyEikthyr,1,Item,Useful
Trophy: TrophyGreydwarf,item:researchTrophyGreydwarf,1,Item,Useful
Trophy: TrophyGhost,item:researchTrophyGhost,1,Item,Useful
Trophy: TrophySkeletonHildir,item:researchTrophyBrenna,1,Item,Useful
Trophy: TrophyDraugrElite,item:researchTrophyDraugrElite,1,Item,Useful
Trophy: TrophyAbomination,item:researchTrophyAbomination,1,Item,Useful
Trophy: TrophyBonemass,item:researchTrophyBonemass,1,Item,Useful
Trophy: TrophyKvastur,item:researchTrophyKvastur,1,Item,Useful
Trophy: TrophyBlob,item:researchTrophyBlob,1,Item,Useful
Trophy: TrophyLeech,item:researchTrophyLeech,1,Item,Useful
Trophy: TrophyWraith,item:researchTrophyWraith,1,Item,Useful
Trophy: TrophyTheElder,item:researchTrophyTheElder,1,Item,Useful
Trophy: TrophyDraugr,item:researchTrophyDraugr,1,Item,Useful
Trophy: TrophySurtling,item:researchTrophySurtling,1,Item,Useful
Trophy: TrophySerpent,item:researchTrophySerpent,1,Item,Useful
Trophy: TrophyCultist_Hildir,item:researchTrophyGeirrhafa,1,Item,Useful
Trophy: TrophyFenring,item:researchTrophyFenring,1,Item,Useful
Trophy: TrophyWolf,item:researchTrophyWolf,1,Item,Useful
Trophy: TrophySGolem,item:researchTrophyStoneGolem,1,Item,Useful
Trophy: TrophyDragonQueen,item:researchTrophyModer,1,Item,Useful
Trophy: TrophyCultist,item:researchTrophyCultist,1,Item,Useful
Trophy: TrophyHatchling,item:researchTrophyDrake,1,Item,Useful
Trophy: TrophyUlv,item:researchTrophyUlv,1,Item,Useful
Trophy: TrophyGoblinBruteBrosBrute,item:researchTrophyThungr,1,Item,Useful
Trophy: TrophyDeathsquito,item:researchTrophyDeathsquito,1,Item,Useful
Trophy: TrophyGoblinBrute,item:researchTrophyFulingBerserker,1,Item,Useful
Trophy: TrophyLox,item:researchTrophyLox,1,Item,Useful
Trophy: TrophyBjornUndead,item:researchTrophyVile,1,Item,Useful
Trophy: TrophyGoblinBruteBrosShaman,item:researchTrophyZil,1,Item,Useful
Trophy: TrophyGoblinKing,item:researchTrophyYagluth,1,Item,Useful
Trophy: TrophyGoblin,item:researchTrophyFuling,1,Item,Useful
Trophy: TrophyGrowth,item:researchTrophyGrowth,1,Item,Useful
Trophy: TrophyGoblinShaman,item:researchTrophyFulingShaman,1,Item,Useful
Trophy: TrophySeekerBrute,item:researchTrophySeekerSoldier,1,Item,Useful
Trophy: TrophyGjall,item:researchTrophyGjall,1,Item,Useful
Trophy: TrophySeeker,item:researchTrophySeeker,1,Item,Useful
Trophy: TrophyTick,item:researchTrophyTick,1,Item,Useful
Trophy: TrophyDvergr,item:researchTrophyDvergr,1,Item,Useful
Trophy: TrophyHare,item:researchTrophyHare,1,Item,Useful
Trophy: TrophySeekerQueen,item:researchTrophyTheQueen,1,Item,Useful
Trophy: TrophyBonemawSerpent,item:researchTrophyBonemaw,1,Item,Useful
Trophy: TrophyCharredArcher,item:researchTrophyCharredMarksman,1,Item,Useful
Trophy: TrophyMorgen,item:researchTrophyMorgen,1,Item,Useful
Trophy: TrophyCharredMage,item:researchTrophyCharredWarlock,1,Item,Useful
Trophy: TrophyFallenValkyrie,item:researchTrophyFallenValkyrie,1,Item,Useful
Trophy: TrophyCharredMelee,item:researchTrophyCharredWarrior,1,Item,Useful
Trophy: TrophyFader,item:researchTrophyFader,1,Item,Useful
Trophy: TrophyAsksvin,item:researchTrophyAsksvin,1,Item,Useful
Trophy: TrophyVolture,item:researchTrophyVolture,1,Item,Useful
'''

# Map string classifications to `ItemClassification`
classification_map = {
    "Progression": ItemClassification.progression,
    "Useful": ItemClassification.useful,
    "Filler": ItemClassification.filler,
    "Trap": ItemClassification.trap,
}

# Parse the item data from the text
current_id = 2000
for line in items_txt.strip().splitlines():
    if line.startswith("//"):  # Skip comments
        continue
    parts = line.split(",")
    if len(parts) < 5:
        print(f"Malformed line: {line}")  # Debugging output
        continue

    item_data_table.append(ValheimItem(
        id=current_id,
        item_name=parts[0].strip(),
        game_id=parts[1].strip(),
        count=int(parts[2].strip()),
        item_type=parts[3].strip(),
            classification=classification_map[parts[4].strip()],
    ))
    current_id += 1


def create_items(world: "ValheimWorld"):
    """
    Dynamically create items for the game world using BaseClasses.Item.
    """
    for item in item_data_table:
        for _ in range(item.count):  # Create as many instances as specified by `count`
            # Create the item using Archipelago's Item class
            game_item = Item(item.item_name, item.classification, item.id, world.player)
            world.multiworld.itempool.append(game_item)
            
            
item_table: Dict[str, int] = {item.item_name: item.id for item in item_data_table}