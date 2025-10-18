using HarmonyLib;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System;
using UnityEngine;
using TMPro; // optional, but harmless

public static class Patches
{
    // ---------- Piece (building) gating ----------
    // Patch all Player.HaveRequirements overloads whose first parameter is Piece
    [HarmonyPatch]
    private static class Player_HaveRequirements_Piece_Patch
    {
        static IEnumerable<MethodBase> TargetMethods()
        {
            return typeof(Player)
                .GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
                .Where(m => m.Name == "HaveRequirements")
                .Where(m =>
                {
                    var p = m.GetParameters();
                    return p.Length > 0 && p[0].ParameterType == typeof(Piece);
                });
        }

        // We only need the first parameter (Piece) and __result; Harmony will ignore the rest
        static bool Prefix(Piece piece, ref bool __result)
        {
            if (piece == null) return true;

            // Use the prefab/component name (e.g., "piece_workbench")
            string id = piece.name;
            if (!string.IsNullOrEmpty(id) && RandomizerUtils.CanResearchBeCrafted(id))
            {
                ValheimRandomizer.Log?.LogDebug($"Blocked building '{id}' (missing research).");
                __result = false; // pretend requirements not met
                return false;     // skip original method
            }

            return true; // run original
        }
    }

    // ---------- Recipe (crafting) gating ----------
    // Patch all Player.HaveRequirements overloads whose first parameter is Recipe
    [HarmonyPatch]
    private static class Player_HaveRequirements_Recipe_Patch
    {
        static IEnumerable<MethodBase> TargetMethods()
        {
            return typeof(Player)
                .GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)
                .Where(m => m.Name == "HaveRequirements")
                .Where(m =>
                {
                    var p = m.GetParameters();
                    return p.Length > 0 && p[0].ParameterType == typeof(Recipe);
                });
        }

        // Only grab the recipe; Harmony will pass extra args we don't declare
        static bool Prefix(Recipe recipe, ref bool __result)
        {
            if (recipe == null) return true;

            // Prefer the prefab name of the result item
            string id = null;
            try
            {
                // In Valheim, the prefab name is accessible via ItemDrop.name (component) or gameObject.name.
                // Either is fine; .name typically mirrors the prefab name.
                id = recipe.m_item ? recipe.m_item.name : null;
            }
            catch
            {
                // ignore
            }

            if (!string.IsNullOrEmpty(id) && RandomizerUtils.CanResearchBeCrafted(id))
            {
                ValheimRandomizer.Log?.LogDebug($"Blocked crafting '{id}' (missing research).");
                __result = false; // pretend requirements not met
                return false;     // skip original method
            }

            return true; // run original
        }
    }

    [HarmonyPatch(typeof(InventoryGui), "AddRecipeToList",
    new Type[] { typeof(Player), typeof(Recipe), typeof(ItemDrop.ItemData), typeof(bool) })]
    public static class InventoryGui_AddRecipeToList_Patch
    {
        static void Postfix(
            InventoryGui __instance,
            Player player,
            Recipe recipe,
            ItemDrop.ItemData item,
            bool canCraft,
            Transform ___m_recipeListRoot)
        {
            try
            {
                if (recipe?.m_item == null || ___m_recipeListRoot == null) return;

                // Prefab/component name of the crafted item
                string id = recipe.m_item.name;
                if (string.IsNullOrEmpty(id)) return;

                // Only tag research items, and only if already unlocked
                if (!ValheimRandomizer.research.Contains(id)) return;
                if (!ValheimRandomizer.IsResearchCrafted(id)) return;

                // The element created by AddRecipeToList is the last child under m_recipeListRoot
                int childCount = ___m_recipeListRoot.childCount;
                if (childCount <= 0) return;

                Transform last = ___m_recipeListRoot.GetChild(childCount - 1);
                if (last == null) return;

                // Find "name" -> TMP_Text and prefix if not already prefixed
                var nameTf = last.Find("name");
                if (nameTf == null) return;

                var label = nameTf.GetComponent<TMP_Text>();
                if (label == null) return;

                const string prefix = "(Completed) ";
                if (!label.text.StartsWith(prefix, StringComparison.Ordinal))
                {
                    label.text = prefix + label.text;
                }
            }
            catch (Exception e)
            {
                ValheimRandomizer.Log?.LogWarning($"AddRecipeToList postfix failed: {e.Message}");
            }
        }
    }

    // ========================= Carry weight =========================
    [HarmonyPatch(typeof(Player), nameof(Player.GetMaxCarryWeight))]
    private static class Player_GetMaxCarryWeight_Patch
    {
        private const int LoadPerTier = 10; // +10 carry weight per tier

        private static void Postfix(Player __instance, ref float __result)
        {
            if (__instance == null || !__instance.IsPlayer()) return;
            int tiers = ValheimRandomizer.GetBoost(ValheimRandomizer.TrophyResearch.TrophyBoost.Load);
            if (tiers <= 0) return;
            __result += LoadPerTier * tiers;
        }
    }

    [HarmonyPatch]
    internal static class Player_GetTotalFoodValue_Patch
    {
        private const float HpPerFoodPerTier = 2f;
        private const float StaminaPerFoodPerTier = 2f;
        private const float EitrPerFoodPerTier = 5f;

        // Cached direct field ref => fastest way to access a private field with Harmony
        private static readonly AccessTools.FieldRef<Player, List<Player.Food>> FoodsRef =
            AccessTools.FieldRefAccess<Player, List<Player.Food>>("m_foods");

        static MethodBase TargetMethod()
        {
            // private void GetTotalFoodValue(out float hp, out float stamina, out float eitr)
            var paramTypes = new[]
            {
            typeof(float).MakeByRefType(),
            typeof(float).MakeByRefType(),
            typeof(float).MakeByRefType()
        };
            return AccessTools.Method(typeof(Player), "GetTotalFoodValue", paramTypes);
        }

        static bool Prepare() => TargetMethod() != null && FoodsRef != null;

        // Postfix so we bump the already-accumulated totals
        static void Postfix(Player __instance, ref float hp, ref float stamina, ref float eitr)
        {
            if (__instance == null) return;

            // Read private m_foods via FieldRef
            var foodsList = FoodsRef(__instance);
            int foods = foodsList != null ? foodsList.Count : 0;
            if (foods <= 0) return;

            // HP
            int hpTiers = ValheimRandomizer.GetBoost(ValheimRandomizer.TrophyResearch.TrophyBoost.HP);
            if (hpTiers > 0) hp += HpPerFoodPerTier * foods * hpTiers;

            // Stamina
            int stTiers = ValheimRandomizer.GetBoost(ValheimRandomizer.TrophyResearch.TrophyBoost.Stamina);
            if (stTiers > 0) stamina += StaminaPerFoodPerTier * foods * stTiers;

            // Eitr
            int eiTiers = ValheimRandomizer.GetBoost(ValheimRandomizer.TrophyResearch.TrophyBoost.Eitr);
            if (eiTiers > 0) eitr += EitrPerFoodPerTier * foods * eiTiers;
        }
    }

    [HarmonyPatch]
    internal static class Player_AddAdrenaline_Patch
    {
        static MethodBase TargetMethod() =>
            AccessTools.Method(typeof(Player), "AddAdrenaline", new[] { typeof(float) });

        static bool Prepare() => TargetMethod() != null;

        // Add +3 per tier to the incoming value before the game processes it.
        static void Prefix(Player __instance, ref float v)
        {
            if (__instance == null || __instance != Player.m_localPlayer) return;

            int tiers = ValheimRandomizer.GetBoost(
                ValheimRandomizer.TrophyResearch.TrophyBoost.Adrenaline);

            if (tiers <= 0) return;

            v += 3f * tiers; // stacks linearly with total unlocked trophy tiers
        }
    }

    internal static class SEManPatchHelpers
    {
        // SEMan -> Character owner
        public static readonly AccessTools.FieldRef<SEMan, Character> OwnerRef =
            AccessTools.FieldRefAccess<SEMan, Character>("m_character");

        // Player -> private List<Player.Food> m_foods
        public static readonly AccessTools.FieldRef<Player, List<Player.Food>> FoodsRef =
            AccessTools.FieldRefAccess<Player, List<Player.Food>>("m_foods");

        public static bool IsLocalPlayer(SEMan se)
        {
            var ch = OwnerRef != null ? OwnerRef(se) : null;
            return ch is Player p && p == Player.m_localPlayer;
        }

        public static int GetActiveFoodCount(Player p)
        {
            if (FoodsRef == null || p == null) return 0;
            var foods = FoodsRef(p);
            return foods != null ? foods.Count : 0;
        }
    }

    // ======================= HEALTH REGEN (ref float) =======================
    [HarmonyPatch]
    internal static class SEMan_ModifyHealthRegen_RefOnly_Patch
    {
        private const float HpRegenPerFoodPerTier = 1f;

        static MethodBase TargetMethod()
        {
            // Try: void ModifyHealthRegen(ref float regen)
            var param = new[] { typeof(float).MakeByRefType() };
            return AccessTools.Method(typeof(SEMan), "ModifyHealthRegen", param);
        }

        static bool Prepare() => TargetMethod() != null && SEManPatchHelpers.OwnerRef != null && SEManPatchHelpers.FoodsRef != null;

        static void Postfix(SEMan __instance, ref float regenMultiplier)
        {
            if (!SEManPatchHelpers.IsLocalPlayer(__instance)) return;
            var player = Player.m_localPlayer;
            int foods = SEManPatchHelpers.GetActiveFoodCount(player);
            if (foods <= 0) return;

            int tiers = ValheimRandomizer.GetBoost(ValheimRandomizer.TrophyResearch.TrophyBoost.HPRegen);
            if (tiers <= 0) return;

            regenMultiplier += HpRegenPerFoodPerTier * foods * tiers;
        }
    }

    // ======================= STAMINA REGEN (ref float) =======================
    [HarmonyPatch]
    internal static class SEMan_ModifyStaminaRegen_RefOnly_Patch
    {
        private const float StaminaRegenPerFoodPerTier = 1f;

        static MethodBase TargetMethod()
        {
            // Try: void ModifyStaminaRegen(ref float regen)
            var param = new[] { typeof(float).MakeByRefType() };
            return AccessTools.Method(typeof(SEMan), "ModifyStaminaRegen", param);
        }

        static bool Prepare() => TargetMethod() != null && SEManPatchHelpers.OwnerRef != null && SEManPatchHelpers.FoodsRef != null;

        static void Postfix(SEMan __instance, ref float staminaMultiplier)
        {
            if (!SEManPatchHelpers.IsLocalPlayer(__instance)) return;
            var player = Player.m_localPlayer;
            int foods = SEManPatchHelpers.GetActiveFoodCount(player);
            if (foods <= 0) return;

            int tiers = ValheimRandomizer.GetBoost(ValheimRandomizer.TrophyResearch.TrophyBoost.StaminaRegen);
            if (tiers <= 0) return;

            staminaMultiplier += StaminaRegenPerFoodPerTier * foods * tiers;
        }
    }

    [HarmonyPatch(typeof(Player), nameof(Player.GetBodyArmor))]
    internal static class Player_GetBodyArmor_DefenseBoost_Patch
    {
        private const float DefensePerTier = 0.05f; // +5% per tier

        // Postfix: multiply final armor value
        private static void Postfix(Player __instance, ref float __result)
        {
            if (__instance != Player.m_localPlayer) return;

            int tiers = ValheimRandomizer.GetBoost(
                ValheimRandomizer.TrophyResearch.TrophyBoost.Defense);

            if (tiers <= 0) return;

            float mul = 1f + DefensePerTier * tiers;
            __result *= mul;
        }
    }

    [HarmonyPatch(typeof(Character), nameof(Character.Damage))]
    internal static class Character_Damage_AttackBoost_Patch
    {
        private const float AttackPerTier = 0.05f; // +5% per tier

        // Prefix: scale outgoing damage when the attacker is the local player
        private static void Prefix(Character __instance, HitData hit)
        {
            if (hit == null) return;

            var attacker = hit.GetAttacker();
            if (!(attacker is Player p) || p != Player.m_localPlayer) return;

            int tiers = ValheimRandomizer.GetBoost(
                ValheimRandomizer.TrophyResearch.TrophyBoost.Attack);

            if (tiers <= 0) return;

            float mul = 1f + AttackPerTier * tiers;
            ScaleDamageTypes(ref hit.m_damage, mul);
        }

        private static void ScaleDamageTypes(ref HitData.DamageTypes dmg, float mul)
        {
            dmg.m_damage *= mul;
            dmg.m_blunt *= mul;
            dmg.m_slash *= mul;
            dmg.m_pierce *= mul;
            dmg.m_fire *= mul;
            dmg.m_frost *= mul;
            dmg.m_lightning *= mul;
            dmg.m_poison *= mul;
            dmg.m_spirit *= mul;
            // include tool-like damages in case something uses them offensively
            dmg.m_pickaxe *= mul;
            dmg.m_chop *= mul;
        }
    }
}
