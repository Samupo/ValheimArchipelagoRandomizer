using Jotunn.Configs;
using Jotunn.Entities;
using Jotunn.Managers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

public static class RandomizerUtils
{
    public static void RegisterResearchBench()
    {
        PrefabManager.OnVanillaPrefabsAvailable -= RegisterResearchBench;
        ValheimRandomizer.Log.LogInfo("RegisterResearchBench: Vanilla prefabs available, cloning Forge…");

        UnityEngine.GameObject clone = PrefabManager.Instance.CreateClonedPrefab(ValheimRandomizer.ResearchBenchPrefabName, "forge");
        if (!clone)
        {
            ValheimRandomizer.Log.LogError("Failed to clone 'forge'");
            return;
        }

        var piece = clone.GetComponent<Piece>() ?? clone.AddComponent<Piece>();
        piece.m_craftingStation = null; // do not inherit forge station

        var researchCS = clone.GetComponent<CraftingStation>() ?? clone.AddComponent<CraftingStation>();

        var forge = PrefabManager.Instance.GetPrefab("forge");
        if (forge != null)
        {
            var forgeCS = forge.GetComponent<CraftingStation>();
            if (forgeCS != null)
            {
                researchCS.m_name = "Research Bench";
                researchCS.m_useDistance = forgeCS.m_useDistance;
                researchCS.m_rangeBuild = forgeCS.m_rangeBuild;
                researchCS.m_areaMarker = forgeCS.m_areaMarker;
            }
        }

        researchCS.m_craftRequireRoof = false;
        researchCS.m_craftRequireFire = false;

        ValheimRandomizer.ResearchBenchCraftingStation = researchCS;


        PieceConfig pieceCfg = new PieceConfig
        {
            Name = "Research Bench",
            Description = "Randomizer Research Bench (Forge-like, own recipes)",
            PieceTable = "Hammer",
            Category = "Randomizer",
            Requirements = new[]
            {
                new RequirementConfig("Wood", 20, recover: true),
                new RequirementConfig("Stone", 10, recover: true)
            }
        };

        PieceManager.Instance.AddPiece(new CustomPiece(clone, true, pieceCfg));
        ValheimRandomizer.Log.LogInfo("Research Bench registered");
    }

    public static void CreateResearch(
    string iconFromItemPrefab,
    string researchItemID,
    string displayName,
    string description,
    string[] requiredResearchIDs,
    RequirementConfig[] researchRecipeRequirements,
    params string[] gatedItemPrefabIDs)
    {
        ValheimRandomizer.Log.LogInfo("Registering research: " + displayName);

        // --- Safety: ensure bench exists ---
        var benchGO = PrefabManager.Instance.GetPrefab(ValheimRandomizer.ResearchBenchPrefabName);
        if (!benchGO)
        {
            ValheimRandomizer.Log.LogError($"Research bench '{ValheimRandomizer.ResearchBenchPrefabName}' not found; aborting CreateResearchAndGateRecipes.");
            return;
        }

        // --- 1) Make the research item prefab ---
        // Use a simple 3D model base. Amber is a safe vanilla item to clone.
        var baseItemName = "Amber";
        if (!PrefabManager.Instance.GetPrefab(baseItemName))
        {
            ValheimRandomizer.Log.LogError("Base item 'Amber' missing; cannot clone research item.");
            return;
        }

        var researchGO = PrefabManager.Instance.CreateClonedPrefab(researchItemID, baseItemName);
        if (!researchGO)
        {
            ValheimRandomizer.Log.LogError($"Failed to clone base item '{baseItemName}' as '{researchItemID}'.");
            return;
        }

        var researchDrop = researchGO.GetComponent<ItemDrop>();
        if (researchDrop == null || researchDrop.m_itemData == null)
        {
            ValheimRandomizer.Log.LogError("Cloned research item is missing ItemDrop/ItemData.");
            return;
        }

        // Name/description
        researchDrop.m_itemData.m_shared.m_name = displayName;

        if (requiredResearchIDs.Length > 0)
        {
            description += "\r\n\r\nRequires: ";
            foreach (var researchID in requiredResearchIDs)
            {
                description += researchID + ", ";
            }
            description.Substring(0, description.Length - 2);
        }

        if (ValheimRandomizer.randomized.Value)
        {
            description += "\r\n\r\nUnlocks: Something?";
        }
        else
        {
            if (gatedItemPrefabIDs.Length > 0)
            {
                description += "\r\n\r\nUnlocks: ";
                foreach (var prefabID in gatedItemPrefabIDs)
                {
                    description += prefabID + ", ";
                }
                description.Substring(0, description.Length - 2);
            }
        }
        researchDrop.m_itemData.m_shared.m_description = description;

        // Copy ICON from the provided item
        var iconSrcGO = PrefabManager.Instance.GetPrefab(iconFromItemPrefab);
        if (iconSrcGO)
        {
            var iconSrcDrop = iconSrcGO.GetComponent<ItemDrop>();
            if (iconSrcDrop && iconSrcDrop.m_itemData?.m_shared?.m_icons != null && iconSrcDrop.m_itemData.m_shared.m_icons.Length > 0)
            {
                researchDrop.m_itemData.m_shared.m_icons = new[] { iconSrcDrop.m_itemData.m_shared.m_icons[0] };
            }
            else
            {
                ValheimRandomizer.Log.LogWarning($"Icon source '{iconFromItemPrefab}' has no icons; keeping cloned icon.");
            }
        }
        else
        {
            ValheimRandomizer.Log.LogWarning($"Icon source item '{iconFromItemPrefab}' not found; keeping cloned icon.");
        }

        // Optional: make it light, non-teleport-blocking, etc.
        researchDrop.m_itemData.m_shared.m_weight = 0.1f;
        researchDrop.m_itemData.m_shared.m_teleportable = true;
        researchDrop.m_itemData.m_shared.m_maxStackSize = 1;

        // Register the item
        ItemManager.Instance.AddItem(new CustomItem(researchGO, fixReference: true));

        // --- 2) Create the research's recipe at the Research Bench ---
        var researchRecipeCfg = new RecipeConfig
        {
            Name = $"Recipe_{researchItemID}",
            Item = researchItemID,
            Amount = 1,
            CraftingStation = ValheimRandomizer.ResearchBenchPrefabName, // our custom bench
            Requirements = researchRecipeRequirements
        };
        ItemManager.Instance.AddRecipe(new CustomRecipe(researchRecipeCfg));

        ValheimRandomizer.Log.LogInfo($"Created research item '{researchItemID}' and its recipe at '{ValheimRandomizer.ResearchBenchPrefabName}'.");

        // Research requirements
        ValheimRandomizer.AddResearchRequirement(researchItemID, requiredResearchIDs);
        foreach (string item in gatedItemPrefabIDs)
        {
            ValheimRandomizer.AddResearchRequirement(item, researchItemID);
        }

        ValheimRandomizer.research.Add(researchItemID);
        ValheimRandomizer.researchToArchipelago.Add(researchItemID, displayName);
        ValheimRandomizer.archipelagoToResearch.Add(displayName, researchItemID);
    }

    public static void CreateTrophyResearch(
    string itemID,
    string researchID,
    ValheimRandomizer.TrophyResearch.TrophyBoost boost)
    {
        var tr = new ValheimRandomizer.TrophyResearch(itemID, researchID, boost);
        ValheimRandomizer.trophyByItemID[itemID] = tr;

        // Note: these are not craftable researches, so we deliberately do NOT
        // add to ValheimRandomizer.research list, nor create a recipe.
        ValheimRandomizer.Log?.LogInfo($"Registered trophy research: {itemID} -> {researchID} ({boost}).");
        ValheimRandomizer.researchToArchipelago.Add(researchID, "Trophy: " + itemID);
        ValheimRandomizer.archipelagoToResearch.Add("Trophy: " + itemID, researchID);
    }

    public static bool CanResearchBeCrafted(string itemID)
    {
        if (ValheimRandomizer.research.Contains(itemID))
        {
            if (ValheimRandomizer.IsResearchCrafted(itemID))
            {
                return true; // Skip if already researched
            }
        }
        foreach (string research in ValheimRandomizer.GetResearchRequired(itemID))
        {
            if (!ValheimRandomizer.IsResearchUnlocked(research)) return true;
        }
        return false;
    }
}
