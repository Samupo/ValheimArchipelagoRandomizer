from typing import Dict, NamedTuple, List, TYPE_CHECKING
from BaseClasses import Location, LocationProgressType

if TYPE_CHECKING:
    from . import ValheimWorld


class ValheimLocation(NamedTuple):
    id: int
    location_type: str  # Type of the location (e.g., Chest, Boss, Emblem, etc.)
    user_friendly_name: str  # Human-readable name
    game_id: str  # Game-specific ID (not used in APWorld, just for reference)
    classification: str  # Missable or Not Missable
    region: str  # The region where the location is found


# Location data will be parsed from a text file
location_data_table: List[ValheimLocation] = []

# Example text data for locations
locations_txt = '''
// Location Type,User Friendly Name,ID,Classification,Region
Research,Crafting,loc:researchWorkbench,Not Missable,Tier0
Research,Clubs Tier 1,loc:researchClubTier1,Not Missable,Tier0
Research,Lighting Tier 1,loc:researchLightingTier1,Not Missable,Tier0
Research,Axes Tier 1,loc:researchAxeTier1,Not Missable,Tier1
Research,Workbench Upgrade 1,loc:researchWorkbenchUpgrade1,Not Missable,Tier1
Research,Workbench Upgrade 2,loc:researchWorkbenchUpgrade2,Not Missable,Tier1
Research,Cape Tier 1,loc:researchCapeTier1,Not Missable,Tier1
Research,Cape Tier 2,loc:researchCapeTier2,Not Missable,Tier1
Research,Rag Armor,loc:researchRagArmor,Not Missable,Tier1
Research,Leather Armor,loc:researchLeatherArmor,Not Missable,Tier1
Research,Troll Armor,loc:researchTrollArmor,Not Missable,Tier1
Research,Bear Armor,loc:researchBearArmor,Not Missable,Tier1
Research,Blades Tier 1,loc:researchBladesTier1,Not Missable,Tier1
Research,Spears Tier 1,loc:researchSpearTier1,Not Missable,Tier1
Research,Short Blades Tier 1,loc:researchShortBladesTier1,Not Missable,Tier1
Research,Knuckles Tier 1,loc:researchKnucklesTier1,Not Missable,Tier1
Research,Bows Tier 1,loc:researchBowsTier1,Not Missable,Tier1
Research,Arrows Tier 1,loc:researchArrowsTier1,Not Missable,Tier1
Research,Arrows Tier 2,loc:researchArrowsTier2,Not Missable,Tier1
Research,Hoe,loc:researchHoe,Not Missable,Tier1
Research,Beekeping,loc:researchBeekeping,Not Missable,Tier1
Research,Wooden Floors,loc:researchFloorWood,Not Missable,Tier1
Research,Wooden Stairs,loc:researchStairsWood,Not Missable,Tier1
Research,Wooden Walls,loc:researchWallsWood,Not Missable,Tier1
Research,Wooden Roofs,loc:researchRoofsWood,Not Missable,Tier1
Research,Wooden Beams,loc:researchBeamsWood,Not Missable,Tier1
Research,Wooden Doors,loc:researchDoorsWood,Not Missable,Tier1
Research,Cooking Station,loc:researchCookingStation,Not Missable,Tier1
Research,Storage Tier 1,loc:researchStorageTier1,Not Missable,Tier1
Research,Storage Tier 2,loc:researchStorageTier2,Not Missable,Tier1
Research,Bed Tier 1,loc:researchBedTier1,Not Missable,Tier1
Research,Shields Tier 1,loc:researchShieldTier1,Not Missable,Tier1
Research,Tower Shields Tier 1,loc:researchTowerShieldTier1,Not Missable,Tier1
Research,Charcoal Kiln,loc:researchCharcoalKiln,Not Missable,Tier1
Research,Pickaxes Tier 1,loc:researchPickaxeTier1,Not Missable,Tier2
Research,Boat Tier 1,loc:researchBoatTier1,Not Missable,Tier2
Research,Smelter,loc:researchSmelter,Not Missable,Tier2
Research,Forge,loc:researchForge,Not Missable,Tier2
Research,Sledgehammers Tier 1,loc:researchSledgehammerTier1,Not Missable,Tier2
Research,Corewood Beams,loc:researchBeamsCorewood,Not Missable,Tier2
Research,Bronze,loc:researchBronze,Not Missable,Tier3
Research,Short Blades Tier 2,loc:researchShortBladesTier2,Not Missable,Tier3
Research,Harpoon,loc:researchHarpoon,Not Missable,Tier3
Research,Darkwood Roofs,loc:researchRoofsDarkwood,Not Missable,Tier3
Research,Darkwood Beams,loc:researchBeamsDarkwood,Not Missable,Tier3
Research,Darkwood Decorations,loc:researchDecorationsDarkwod,Not Missable,Tier3
Research,Cauldron,loc:researchCauldron,Not Missable,Tier3
Research,Cauldron Upgrade 1,loc:researchCauldronUpgrade1,Not Missable,Tier3
Research,Mead ketill,loc:researchMeadketill,Not Missable,Tier3
Research,Knife Butcher,loc:researchKnifeButcher,Not Missable,Tier3
Research,Nails Tier 1,loc:researchNailsTier1,Not Missable,Tier4
Research,Axes Tier 2,loc:researchAxeTier2,Not Missable,Tier4
Research,Workbench Upgrade 3,loc:researchWorkbenchUpgrade3,Not Missable,Tier4
Research,Bronze Armor,loc:researchBronzeArmor,Not Missable,Tier4
Research,Clubs Tier 2,loc:researchClubTier2,Not Missable,Tier4
Research,Blades Tier 2,loc:researchBladesTier2,Not Missable,Tier4
Research,Spears Tier 2,loc:researchSpearTier2,Not Missable,Tier4
Research,Polearms Tier 1,loc:researchPolearmsTier1,Not Missable,Tier4
Research,Arrows Tier 3,loc:researchArrowsTier3,Not Missable,Tier4
Research,Trinkets Tier 1,loc:researchTrinketTier1,Not Missable,Tier4
Research,Transportation Tier 1,loc:researchTransportationTier1,Not Missable,Tier4
Research,Transportation Tier 2,loc:researchTransportationTier2,Not Missable,Tier4
Research,Boat Tier 2,loc:researchBoatTier2,Not Missable,Tier4
Research,Cultivator,loc:researchCultivator,Not Missable,Tier4
Research,Bucklers Tier 1,loc:researchBucklerTier1,Not Missable,Tier4
Research,Pickaxes Tier 2,loc:researchPickaxeTier2,Not Missable,Tier5
Research,Root Armor,loc:researchRootArmor,Not Missable,Tier5
Research,Short Blades Tier 3,loc:researchShortBladesTier3,Not Missable,Tier5
Research,Bows Tier 2,loc:researchBowsTier2,Not Missable,Tier5
Research,Fermenter,loc:researchFermenter,Not Missable,Tier5
Research,Bonfire,loc:researchWarmthTier2,Not Missable,Tier5
Research,Shields Tier 2,loc:researchShieldTier2,Not Missable,Tier5
Research,Pickaxes Tier 3,loc:researchPickaxeTier3,Not Missable,Tier6
Research,Warmth Tier 1,loc:researchWarmthTier1,Not Missable,Tier1
Research,Forge Upgrade 1,loc:researchForgeUpgrade1,Not Missable,Tier6
Research,Forge Upgrade 4,loc:researchForgeUpgrade4,Not Missable,Tier6
Research,Forge Upgrade 5,loc:researchForgeUpgrade5,Not Missable,Tier6
Research,Forge Upgrade 6,loc:researchForgeUpgrade6,Not Missable,Tier6
Research,Stonecutter,loc:researchStonecutter,Not Missable,Tier6
Research,Iron Armor,loc:researchIronArmor,Not Missable,Tier6
Research,Axes Tier 3,loc:researchAxeTier3,Not Missable,Tier6
Research,Battleaxes Tier 1,loc:researchBattleaxeTier1,Not Missable,Tier6
Research,Clubs Tier 3,loc:researchClubTier3,Not Missable,Tier6
Research,Sledgehammers Tier 2,loc:researchSledgehammerTier2,Not Missable,Tier6
Research,Blades Tier 3,loc:researchBladesTier3,Not Missable,Tier6
Research,Spears Tier 3,loc:researchSpearTier3,Not Missable,Tier6
Research,Polearms Tier 2,loc:researchPolearmsTier2,Not Missable,Tier6
Research,Bows Tier 3,loc:researchBowsTier3,Not Missable,Tier6
Research,Arrows Tier 4,loc:researchArrowsTier4,Not Missable,Tier6
Research,Trinkets Tier 2,loc:researchTrinketTier2,Not Missable,Tier6
Research,Darkwood Doors,loc:reserachDoorsDarkwood,Not Missable,Tier6
Research,Windmill,loc:researchWindmill,Not Missable,Tier6
Research,Iron Cooking Station,loc:researchIronCookingStation,Not Missable,Tier6
Research,Food Preparation Table,loc:researchPreparationTable,Not Missable,Tier6
Research,Storage Tier 3,loc:researchStorageTier3,Not Missable,Tier6
Research,Boat Tier 3,loc:researchBoatTier3,Not Missable,Tier6
Research,Bed Tier 2,loc:researchBedTier2,Not Missable,Tier6
Research,Hearth,loc:researchWarmthTier3,Not Missable,Tier6
Research,Tower Shields Tier 2,loc:researchTowerShieldTier2,Not Missable,Tier6
Research,Bucklers Tier 2,loc:researchBucklerTier2,Not Missable,Tier6
Research,Workbench Upgrade 4,loc:researchWorkbenchUpgrade4,Not Missable,Tier7
Research,Artisan Table,loc:researchArtisanTable,Not Missable,Tier7
Research,Blast Furnace,loc:researchBlastFurnace,Not Missable,Tier7
Research,Fenris Armor,loc:researchFenrisArmor,Not Missable,Tier7
Research,Wolf Armor,loc:researchWolfArmor,Not Missable,Tier7
Research,Battleaxes Tier 2,loc:researchBattleaxeTier2,Not Missable,Tier7
Research,Clubs Tier 4,loc:researchClubTier4,Not Missable,Tier7
Research,Blades Tier 4,loc:researchBladesTier4,Not Missable,Tier7
Research,Spears Tier 4,loc:researchSpearTier4,Not Missable,Tier7
Research,Short Blades Tier 4,loc:researchShortBladesTier4,Not Missable,Tier7
Research,Knuckles Tier 2,loc:researchKnucklesTier2,Not Missable,Tier7
Research,Bows Tier 4,loc:researchBowsTier4,Not Missable,Tier7
Research,Arrows Tier 5,loc:researchArrowsTier5,Not Missable,Tier7
Research,Arrows Tier 6,loc:researchArrowsTier6,Not Missable,Tier7
Research,Arrows Tier 7,loc:researchArrowsTier7,Not Missable,Tier7
Research,Arrows Tier 8,loc:researchArrowsTier8,Not Missable,Tier7
Research,Arrows Tier 9,loc:researchArrowsTier9,Not Missable,Tier7
Research,Trinkets Tier 3,loc:researchTrinketTier3,Not Missable,Tier7
Research,Cauldron Upgrade 2,loc:researchCauldronUpgrade2,Not Missable,Tier7
Research,Shields Tier 3,loc:researchShieldTier3,Not Missable,Tier7
Research,Nails Tier 2,loc:researchNailsTier2,Not Missable,Tier6
Research,Axes Tier 4,loc:researchAxeTier4,Not Missable,Tier8
Research,Wisp Fountain,loc:researchWispFountain,Not Missable,Tier8
Research,Wisplight,loc:researchWisplight,Not Missable,Tier8
Research,Forge Upgrade 2,loc:researchForgeUpgrade2,Not Missable,Tier8
Research,Forge Upgrade 3,loc:researchForgeUpgrade3,Not Missable,Tier8
Research,Spinning Wheel,loc:researchSpinningWheel,Not Missable,Tier8
Research,Cape Tier 3,loc:researchCapeTier3,Not Missable,Tier8
Research,Cape Tier 4,loc:researchCapeTier4,Not Missable,Tier8
Research,Cape Tier 5,loc:researchCapeTier5,Not Missable,Tier8
Research,Vilebone Armor,loc:researchVileboneArmor,Not Missable,Tier8
Research,Padded Armor,loc:researchPaddedArmor,Not Missable,Tier8
Research,Battleaxes Tier 3,loc:researchBattleaxeTier3,Not Missable,Tier8
Research,Clubs Tier 5,loc:researchClubTier5,Not Missable,Tier8
Research,Blades Tier 5,loc:researchBladesTier5,Not Missable,Tier8
Research,Polearms Tier 3,loc:researchPolearmsTier3,Not Missable,Tier8
Research,Short Blades Tier 5,loc:researchShortBladesTier5,Not Missable,Tier8
Research,Short Blades Tier 6,loc:researchShortBladesTier6,Not Missable,Tier8
Research,Knuckles Tier 3,loc:researchKnucklesTier3,Not Missable,Tier8
Research,Trinkets Tier 4,loc:researchTrinketTier4,Not Missable,Tier8
Research,Stone Oven,loc:researchStoneOven,Not Missable,Tier8
Research,Cauldron Upgrade 3,loc:researchCauldronUpgrade3,Not Missable,Tier8
Research,Cauldron Upgrade 4,loc:researchCauldronUpgrade4,Not Missable,Tier8
Research,Storage Tier 4,loc:researchStorageTier4,Not Missable,Tier8
Research,Scythe,loc:researchScythe,Not Missable,Tier8
Research,Shields Tier 4,loc:researchShieldTier4,Not Missable,Tier8
Research,Tower Shields Tier 3,loc:researchTowerShieldTier3,Not Missable,Tier8
Research,Pickaxes Tier 4,loc:researchPickaxeTier4,Not Missable,Tier9
Research,Sap Extractor,loc:researchSapExtractor,Not Missable,Tier9
Research,Eitr Refinery,loc:researchEitrRefinery,Not Missable,Tier9
Research,Black Forge,loc:researchBlackForge,Not Missable,Tier9
Research,Black Forge Upgrade 1,loc:researchBlackForgeUpgrade1,Not Missable,Tier9
Research,Black Forge Upgrade 2,loc:researchBlackForgeUpgrade2,Not Missable,Tier9
Research,Carapace Armor,loc:researchCarapaceArmor,Not Missable,Tier9
Research,Long Blades Tier 1,loc:researchLongBladesTier1,Not Missable,Tier9
Research,Spears Tier 5,loc:researchSpearTier5,Not Missable,Tier9
Research,Arrows Tier 10,loc:researchArrowsTier10,Not Missable,Tier9
Research,Crossbows Tier 1,loc:researchCrossbowsTier1,Not Missable,Tier9
Research,Bolts Tier 1,loc:researchBoltsTier1,Not Missable,Tier9
Research,Bolts Tier 2,loc:researchBoltsTier2,Not Missable,Tier9
Research,Bolts Tier 3,loc:researchBoltsTier3,Not Missable,Tier9
Research,Dvergr Doors,loc:researchDvergrDoors,Not Missable,Tier9
Research,Dvergr Fences,loc:researchDvergrFences,Not Missable,Tier9
Research,Dvergr Stairs,loc:researchDvergrStairs,Not Missable,Tier9
Research,Ceramic Plates,loc:researchCeramicPlate,Not Missable,Tier10
Research,Boat Tier 4,loc:researchBoatTier4,Not Missable,Tier10
Research,Artisan Press,loc:researchArtisanUpgrade1,Not Missable,Tier10
Research,Galdr Table,loc:researchGaldrTable,Not Missable,Tier10
Research,Galdr Table Upgrade 1,loc:researchGaldrTableUpgrade1,Not Missable,Tier10
Research,Galdr Table Upgrade 2,loc:researchGaldrTableUpgrade2,Not Missable,Tier10
Research,Cape Tier 6,loc:researchCapeTier6,Not Missable,Tier10
Research,Eitr Armor,loc:researchEitrArmor,Not Missable,Tier10
Research,Axes Tier 5,loc:researchAxeTier5,Not Missable,Tier10
Research,Battleaxes Tier 4,loc:researchBattleaxeTier4,Not Missable,Tier10
Research,Sledgehammers Tier 3,loc:researchSledgehammerTier3,Not Missable,Tier10
Research,Blades Tier 6,loc:researchBladesTier6,Not Missable,Tier10
Research,Polearms Tier 4,loc:researchPolearmsTier4,Not Missable,Tier10
Research,Bows Tier 5,loc:researchBowsTier5,Not Missable,Tier10
Research,Elemental Magic Tier 1,loc:researchElementalMagicTier1,Not Missable,Tier10
Research,Blood Magic Tier 1,loc:reserachBloodMagicTier1,Not Missable,Tier10
Research,Trinkets Tier 5,loc:researchTrinketTier5,Not Missable,Tier10
Research,Shields Tier 5,loc:researchShieldTier5,Not Missable,Tier10
Research,Bucklers Tier 3,loc:researchBucklerTier3,Not Missable,Tier10
Research,Black Forge Upgrade 3,loc:researchBlackForgeUpgrade3,Not Missable,Tier11
Research,Black Forge Upgrade 4,loc:researchBlackForgeUpgrade4,Not Missable,Tier11
Research,Galdr Table Upgrade 3,loc:researchGaldrTableUpgrade3,Not Missable,Tier11
Research,Cape Tier 7,loc:researchCapeTier7,Not Missable,Tier11
Research,Cape Tier 8,loc:researchCapeTier8,Not Missable,Tier11
Research,Ask Armor,loc:researchAskArmor,Not Missable,Tier11
Research,Embla Armor,loc:researchEmblaArmor,Not Missable,Tier11
Research,Flametal Armor,loc:researchFlametalArmor,Not Missable,Tier11
Research,Battleaxes Tier 5,loc:researchBattleaxeTier5,Not Missable,Tier11
Research,Battleaxes Tier 6,loc:researchBattleaxeTier6,Not Missable,Tier11
Research,Clubs Tier 6,loc:researchClubTier6,Not Missable,Tier11
Research,Clubs Tier 7,loc:researchClubTier7,Not Missable,Tier11
Research,Blades Tier 7,loc:researchBladesTier7,Not Missable,Tier11
Research,Blades Tier 8,loc:researchBladesTier8,Not Missable,Tier11
Research,Long Blades Tier 2,loc:researchLongBladesTier2,Not Missable,Tier11
Research,Long Blades Tier 3,loc:researchLongBladesTier3,Not Missable,Tier11
Research,Spears Tier 6,loc:researchSpearTier6,Not Missable,Tier11
Research,Spears Tier 7,loc:researchSpearTier7,Not Missable,Tier11
Research,Bows Tier 6,loc:researchBowsTier6,Not Missable,Tier11
Research,Bows Tier 7,loc:researchBowsTier7,Not Missable,Tier11
Research,Arrows Tier 11,loc:researchArrowsTier11,Not Missable,Tier11
Research,Crossbows Tier 2,loc:researchCrossbowsTier2,Not Missable,Tier11
Research,Crossbows Tier 3,loc:researchCrossbowsTier3,Not Missable,Tier11
Research,Bolts Tier 4,loc:researchBoltsTier4,Not Missable,Tier11
Research,Elemental Magic Tier 2,loc:researchElementalMagicTier2,Not Missable,Tier11
Research,Elemental Magic Tier 3,loc:researchElementalMagicTier3,Not Missable,Tier11
Research,Blood Magic Tier 2,loc:researchBloodMagicTier2,Not Missable,Tier11
Research,Siege,loc:researchSiege,Not Missable,Tier11
Research,Trinkets Tier 6,loc:researchTrinketTier6,Not Missable,Tier11
Research,Ashwood Floors,loc:researchAshwoodFloor,Not Missable,Tier11
Research,Ashwood Walls,loc:researchAshwoodWalls,Not Missable,Tier11
Research,Ashwood Decorations,loc:researchAshwoodDecoration,Not Missable,Tier11
Research,Ashwood Beams,loc:researchAshwoodBeams,Not Missable,Tier11
Research,Ashwood Stairs,loc:researchAshwoodStairs,Not Missable,Tier11
Research,Ashwood Doors,loc:researchAshwoodDoors,Not Missable,Tier11
Research,Transportation Tier 3,loc:researchTransportationTier3,Not Missable,Tier11
Research,Cauldron Upgrade 5,loc:researchCauldronUpgrade5,Not Missable,Tier11
Research,Bed Tier 3,loc:researchBedTier3,Not Missable,Tier11
Research,Shields Tier 6,loc:researchShieldTier6,Not Missable,Tier11
Research,Tower Shields Tier 4,loc:researchTowerShieldTier4,Not Missable,Tier11
Trophy,Trophy: TrophyNeck,loc:researchTrophyNeck,Not Missable,Tier0
Trophy,Trophy: TrophyBoar,loc:researchTrophyBoar,Not Missable,Tier0
Trophy,Trophy: TrophyDeer,loc:researchTrophyDeer,Not Missable,Tier0
Trophy,Trophy: TrophyGreydwarfBrute,loc:researchTrophyGreydwarfBrute,Not Missable,Tier1
Trophy,Trophy: TrophyBjorn,loc:researchTrophyBear,Not Missable,Tier1
Trophy,Trophy: TrophyForestTroll,loc:researchTrophyTroll,Not Missable,Tier1
Trophy,Trophy: TrophySkeleton,loc:researchTrophySkeleton,Not Missable,Tier1
Trophy,Trophy: TrophyGreydwarfShaman,loc:researchTrophyGreydwarfShaman,Not Missable,Tier1
Trophy,Trophy: TrophySkeletonPoison,loc:researchTrophyRancidRemains,Not Missable,Tier1
Trophy,Trophy: TrophyEikthyr,loc:researchTrophyEikthyr,Not Missable,Tier1
Trophy,Trophy: TrophyGreydwarf,loc:researchTrophyGreydwarf,Not Missable,Tier1
Trophy,Trophy: TrophyGhost,loc:researchTrophyGhost,Not Missable,Tier1
Trophy,Trophy: TrophySkeletonHildir,loc:researchTrophyBrenna,Not Missable,Tier4
Trophy,Trophy: TrophyDraugrElite,loc:researchTrophyDraugrElite,Not Missable,Tier4
Trophy,Trophy: TrophyAbomination,loc:researchTrophyAbomination,Not Missable,Tier4
Trophy,Trophy: TrophyBonemass,loc:researchTrophyBonemass,Not Missable,Tier4
Trophy,Trophy: TrophyKvastur,loc:researchTrophyKvastur,Not Missable,Tier4
Trophy,Trophy: TrophyBlob,loc:researchTrophyBlob,Not Missable,Tier4
Trophy,Trophy: TrophyLeech,loc:researchTrophyLeech,Not Missable,Tier4
Trophy,Trophy: TrophyWraith,loc:researchTrophyWraith,Not Missable,Tier4
Trophy,Trophy: TrophyTheElder,loc:researchTrophyTheElder,Not Missable,Tier4
Trophy,Trophy: TrophyDraugr,loc:researchTrophyDraugr,Not Missable,Tier4
Trophy,Trophy: TrophySurtling,loc:researchTrophySurtling,Not Missable,Tier4
Trophy,Trophy: TrophySerpent,loc:researchTrophySerpent,Not Missable,Tier4
Trophy,Trophy: TrophyCultist_Hildir,loc:researchTrophyGeirrhafa,Not Missable,Tier7
Trophy,Trophy: TrophyFenring,loc:researchTrophyFenring,Not Missable,Tier7
Trophy,Trophy: TrophyWolf,loc:researchTrophyWolf,Not Missable,Tier7
Trophy,Trophy: TrophySGolem,loc:researchTrophyStoneGolem,Not Missable,Tier7
Trophy,Trophy: TrophyDragonQueen,loc:researchTrophyModer,Not Missable,Tier7
Trophy,Trophy: TrophyCultist,loc:researchTrophyCultist,Not Missable,Tier7
Trophy,Trophy: TrophyHatchling,loc:researchTrophyDrake,Not Missable,Tier7
Trophy,Trophy: TrophyUlv,loc:researchTrophyUlv,Not Missable,Tier7
Trophy,Trophy: TrophyGoblinBruteBrosBrute,loc:researchTrophyThungr,Not Missable,Tier8
Trophy,Trophy: TrophyDeathsquito,loc:researchTrophyDeathsquito,Not Missable,Tier8
Trophy,Trophy: TrophyGoblinBrute,loc:researchTrophyFulingBerserker,Not Missable,Tier8
Trophy,Trophy: TrophyLox,loc:researchTrophyLox,Not Missable,Tier8
Trophy,Trophy: TrophyBjornUndead,loc:researchTrophyVile,Not Missable,Tier8
Trophy,Trophy: TrophyGoblinBruteBrosShaman,loc:researchTrophyZil,Not Missable,Tier8
Trophy,Trophy: TrophyGoblinKing,loc:researchTrophyYagluth,Not Missable,Tier8
Trophy,Trophy: TrophyGoblin,loc:researchTrophyFuling,Not Missable,Tier8
Trophy,Trophy: TrophyGrowth,loc:researchTrophyGrowth,Not Missable,Tier8
Trophy,Trophy: TrophyGoblinShaman,loc:researchTrophyFulingShaman,Not Missable,Tier8
Trophy,Trophy: TrophySeekerBrute,loc:researchTrophySeekerSoldier,Not Missable,Tier9
Trophy,Trophy: TrophyGjall,loc:researchTrophyGjall,Not Missable,Tier9
Trophy,Trophy: TrophySeeker,loc:researchTrophySeeker,Not Missable,Tier9
Trophy,Trophy: TrophyTick,loc:researchTrophyTick,Not Missable,Tier9
Trophy,Trophy: TrophyDvergr,loc:researchTrophyDvergr,Not Missable,Tier9
Trophy,Trophy: TrophyHare,loc:researchTrophyHare,Not Missable,Tier9
Trophy,Trophy: TrophySeekerQueen,loc:researchTrophyTheQueen,Not Missable,Tier10
Trophy,Trophy: TrophyBonemawSerpent,loc:researchTrophyBonemaw,Not Missable,Tier11
Trophy,Trophy: TrophyCharredArcher,loc:researchTrophyCharredMarksman,Not Missable,Tier11
Trophy,Trophy: TrophyMorgen,loc:researchTrophyMorgen,Not Missable,Tier11
Trophy,Trophy: TrophyCharredMage,loc:researchTrophyCharredWarlock,Not Missable,Tier11
Trophy,Trophy: TrophyFallenValkyrie,loc:researchTrophyFallenValkyrie,Not Missable,Tier11
Trophy,Trophy: TrophyCharredMelee,loc:researchTrophyCharredWarrior,Not Missable,Tier11
Trophy,Trophy: TrophyFader,loc:researchTrophyFader,Not Missable,Tier11
Trophy,Trophy: TrophyAsksvin,loc:researchTrophyAsksvin,Not Missable,Tier11
Trophy,Trophy: TrophyVolture,loc:researchTrophyVolture,Not Missable,Tier11
'''

# Map string classifications to `LocationProgressType`
progress_type_map = {
    "Not Missable": LocationProgressType.DEFAULT,
    "Missable": LocationProgressType.EXCLUDED,
}

# Parse the location data from the text
current_id = 1
for line in locations_txt.strip().splitlines():
    if line.startswith("//"):  # Skip comments
        continue
    parts = line.split(",")
    if len(parts) < 5:
        print(f"Malformed line: {line}")  # Debugging output
        continue

    location_data_table.append(ValheimLocation(
        id=current_id,
        location_type=parts[0].strip(),
        user_friendly_name=parts[1].strip(),
        game_id=parts[2].strip(),  # Only for reference; not used in APWorld
        classification=parts[3].strip(),
        region=parts[4].strip(),
    ))
    current_id += 1


def create_locations(world: "ValheimWorld"):
    """
    Dynamically create locations for the game world and assign them to regions.
    """
    for location in location_data_table:
        # Use the user-friendly name as the location name
        location_name = location.user_friendly_name

        # Determine the progress type based on classification
        progress_type = progress_type_map.get(location.classification, LocationProgressType.DEFAULT)

        # Get the region where the location belongs
        try:
            region = world.multiworld.get_region(location.region, world.player)
        except KeyError:
            raise ValueError(f"Region '{location.region}' not found for location '{location_name}'.")

        # Create the location and assign it to the region
        game_location = Location(world.player, location_name, location.id, region)
        game_location.progress_type = progress_type

        # Assign the location to its parent region
        region.locations.append(game_location)
        
        
location_table: Dict[str, int] = {location.user_friendly_name: location.id for location in location_data_table}
