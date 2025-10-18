using System;
using System.Linq;
using UnityEngine.Events;
using Archipelago.MultiClient.Net;
using Archipelago.MultiClient.Net.Enums;
using Archipelago.MultiClient.Net.Models;
using Archipelago.MultiClient.Net.Helpers;

internal static class ArchipelagoConnection
{
    private static ArchipelagoSession session;
    private static bool connected;

    public static void Connect(string host, int port, string slot, string password)
    {
        // Dispose previous session if any
        session?.Socket?.DisconnectAsync();
        session = null;
        connected = false;

        // Create & login
        session = ArchipelagoSessionFactory.CreateSession(host, port);
        var result = session.TryConnectAndLogin("Valheim", slot,
            ItemsHandlingFlags.AllItems, password: password);

        if (!result.Successful)
        {
            // Throw the first error up; UI handles it and shows the message
            var failure = (LoginFailure)result;
            throw new Exception(string.Join("; ", failure.Errors ?? Array.Empty<string>()));
        }

        // Hook item reception
        session.Items.ItemReceived += OnApItemReceived;

        connected = true;
    }

    public static void SendLocation(string locationName)
    {
        if (!ValheimRandomizer.randomized.Value) return;
        if (!WorldLoaded()) return;
        if (string.IsNullOrWhiteSpace(locationName)) return;

        ValheimRandomizer.Log.LogInfo("Queue location " + locationName);

        if (HasGlobal($"ap_sent:{locationName}")) return;

        SetGlobal($"ap_pending:{locationName}");
        TryFlushPendingLocations();
    }

    private static void OnApItemReceived(ReceivedItemsHelper helper)
    {
        if (!WorldLoaded()) return;
        while (true)
        {
            var item = helper.DequeueItem();
            if (item == null) break;

            var name = item.ItemName;
            if (string.IsNullOrEmpty(name)) continue;

            if (ValheimRandomizer.archipelagoToResearch.TryGetValue(name, out var researchId))
            {
                ValheimRandomizer.DoUnlockResearch(researchId);
            }
            else
            {
                ValheimRandomizer.Log.LogWarning(
                    $"Received AP item '{name}' but no research mapping was found.");
            }
        }
    }

    static System.Collections.Generic.List<string> gottenItems = new System.Collections.Generic.List<string>();
    static void TryGetAllItems()
    {
        if (!WorldLoaded()) return;

        foreach (var item in session.Items.AllItemsReceived)
        {
            var name = item.ItemName;
            if (string.IsNullOrEmpty(name)) continue;

            if (gottenItems.Contains(name)) continue;
            gottenItems.Add(name);

            if (ValheimRandomizer.archipelagoToResearch.TryGetValue(name, out var researchId))
            {
                ValheimRandomizer.DoUnlockResearch(researchId);
            }
            else
            {
                ValheimRandomizer.Log.LogWarning(
                    $"Received AP item '{name}' but no research mapping was found.");
            }
        }
    }

    public static void TryFlushPendingLocations()
    {
        if (!connected || session == null) return;
        if (!WorldLoaded()) return;
        TryGetAllItems();

        foreach (var key in ZoneSystem.instance.GetGlobalKeys())
        {
            if (!key.StartsWith("ap_pending:", StringComparison.Ordinal)) continue;

            var locationName = key.Substring("ap_pending:".Length);
            if (string.IsNullOrWhiteSpace(locationName)) continue;

            if (HasGlobal($"ap_sent:{locationName}")) continue;

            try
            {
                foreach (string str in ValheimRandomizer.archipelagoToResearch.Keys)
                {
                    if (str.ToLower() == locationName)
                    {
                        locationName = str;
                        break;
                    }
                }
                ValheimRandomizer.Log.LogInfo("Unlock location " + locationName);
                var id = session.Locations.GetLocationIdFromName("Valheim", locationName);
                session.Locations.CompleteLocationChecks(id);

                // NEW: mark success so we don't resend forever
                SetGlobal($"ap_sent:{locationName}");
                RemoveGlobal(key);
            }
            catch (Exception ex)
            {
                // NEW: make the problem visible
                ValheimRandomizer.Log.LogWarning(
                    $"AP location lookup failed for '{locationName}'. " +
                    $"Check the exact name in your AP world. Error: {ex.Message}");
                // keep pending; will retry next tick/reconnect
            }
        }
    }

    private static bool WorldLoaded()
        => ZoneSystem.instance != null && Player.m_localPlayer != null; // simple & reliable

    private static bool HasGlobal(string k)
        => ZoneSystem.instance != null && ZoneSystem.instance.GetGlobalKey(k);

    private static void SetGlobal(string k)
    {
        if (ZoneSystem.instance == null) return;
        ZoneSystem.instance.SetGlobalKey(k);
    }

    private static void RemoveGlobal(string k)
    {
        if (ZoneSystem.instance == null) return;
        ZoneSystem.instance.RemoveGlobalKey(k);
    }
}
