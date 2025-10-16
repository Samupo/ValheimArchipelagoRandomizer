INSTALLATION
...

FILES USED
research.tsv
	Contains all the available researches in the game. They will appear on the Research Bench and are used to gate repices behind a tiered list of researches.
trophy.tsv
	Contains special researches that'll unlock automatically upon collecting a specified item. It'll result in a permanent player boost unless None is specified.

TIER EXPLANATION
Tier 0 - Hammer
		Wood Stone Resin Feathers BoneFragments LeatherScraps Flint Dandelion Honey Raspberry Blueberries CarrotSeeds GreydwarfEye Mushroom SurtlingCore Thistle MushroomYellow
	[GATE] Workbench
Tier 1 - Stone/Wood/Flint
		BjornHide BjornPaw Ectoplasm TrollHide AncientSeed
	[GATE] Stone Axe
Tier 2 - Corewoord
		RoundLog
	[GATE] Antler pickaxe + Forge + Smelter + Charcoal Source(any of Raft (Surtlings in swamp)/Charcoal Kiln/(Cooking station + Firepit))
Tier 3 - Tin/Copper/Chitin
		Tin Copper CopperOre TinOre Chitin
	[GATE] Bronze
Tier 4 - Bronze
		Bloodbag Chain Entrails Guck Ooze Root TurnipSeeds 
	[GATE] BronzeAxe + Any ship
Tier 5 - Finewood/Ancient Bark AmberPearl Ruby Amber
		Finewood ElderBark
	[GATE] Bronze pickaxe
Tier 6 - Iron
		Iron WitheredBone Coins SilverNecklace
	[GATE] Iron Pickaxe + Any cold resist (Lox Cape/Wolf Fur Cape/Frost Resistance Mead/Firepit)
Tier 7 - Silver
		Silver SilverOre Obsidian Crystal WolfClaw WolfHairBundle FreezeGland Onion JuteRed WolfFang WolfPelt
	[GATE] Blast Furnace + Artisan Table
Tier 8 - Black Metal + Spinning wheel
		BlackMetalScrap Barley Cloudberry Flax LoxPelt Needle Tar UndeadBjornRibcage
	[GATE] Spinning wheel + Black Metal Axe + Wisp
Tier 9 - Yggdrassil
		YggdrasilWood Bilebag BlackCore GiantBloodSack JuteBlue Carapace DvergrNeedle MushroomJotunPuffs MushroomMagecap Mandible RoyalJelly ScaleHide
	[GATE] Black Metal Pickaxe + Sap Extractor + Eitr Refinery
Tier 10 - Refined Eitr
		Eitr Softtissue Sap Wisp BlackMarble
	[GATE] Drakkar
Tier 11 - Flametal
		Grausten FlametalNew Blackwood AskBladder AskHide AsksvinCarrionNeck AsksvinCarrionPelvic AsksvinCarrionRibcage AsksvinCarrionSkull BonemawSerpentTooth CelestialFeather CharcoalResin CharredBone Fiddleheadfern MoltenCore MorgenHeart Pot_Shard_Green ProustitePowder MushroomSmokePuff SulfurStone Vineberry


CUSTOMIZATION
Both research and trophies files can be modified. Upon launching the game the mod will create two files for the pieces and recipes that are not yet mentioned in the researches. Mod content can be added to these files.
If those files are modified the apworld needs to change accordingly. Use the tool ValheimRandomizerParser by putting both research.tsv and trophies.tsv files in the same folder. New files will be created to substitute the ones in the apworld.
To recreate a new apworld just modify the python files accordingly, zip them (not the folder) and change the extension to apworld.