using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;
using UnityEngine.Windows;

public class ArchipelagoUI : MonoBehaviour
{

    // UI state
    private Rect _win = new Rect(30, 80, 420, 260);
    private bool _randomized;
    private string _host, _slot, _password;
    private int _port;

    // Connection state
    private string _status = "Not connected";
    private bool _connecting = false;

    // Optional: track main menu presence cheaply
    private float _fejdCheckTimer = 0f;
    private bool _inMainMenu = false;

    public void Init()
    {
        // load config values into fields
        _randomized = ValheimRandomizer.randomized.Value;
        _host = ValheimRandomizer.archipelagoHostname.Value;
        _port = ValheimRandomizer.archipelagoPort.Value;
        _slot = ValheimRandomizer.archipelagoSlot.Value;
        _password = ValheimRandomizer.archipelagoPassword.Value;
    }

    private void Update()
    {
        // Poll whether we’re in the FejdStartup (main menu) scene
        _fejdCheckTimer -= Time.unscaledDeltaTime;
        if (_fejdCheckTimer <= 0f)
        {
            _fejdCheckTimer = 0.5f;
            _inMainMenu = IsInMainMenu();
        }
    }

    private static bool IsInMainMenu()
    {
        // FejdStartup exists only in main menu
        return UnityEngine.Object.FindFirstObjectByType<FejdStartup>() != null;
    }

    private void OnGUI()
    {
        if (!_inMainMenu) return;

        // Pause UI scaling for different resolutions
        var oldColor = GUI.color;
        GUI.color = Color.white;

        _win = GUILayout.Window(GetInstanceID(), _win, DrawWindow, "Archipelago – Valheim Randomizer",
            GUILayout.ExpandHeight(true), GUILayout.ExpandWidth(true));

        GUI.color = oldColor;
    }

    private void DrawWindow(int id)
    {
        GUILayout.BeginVertical();

        GUILayout.Label("Connect to an Archipelago room to enable item/location randomization.");
        GUILayout.Space(6);

        _randomized = GUILayout.Toggle(_randomized, "Randomized?");

        GUILayout.BeginHorizontal();
        GUILayout.Label("Host", GUILayout.Width(60));
        _host = GUILayout.TextField(_host ?? "", GUILayout.Width(220));
        GUILayout.Label("Port", GUILayout.Width(40));
        var portStr = GUILayout.TextField((_port <= 0 ? "" : _port.ToString()), GUILayout.Width(70));
        if (int.TryParse(portStr, out var p)) _port = p;
        GUILayout.EndHorizontal();

        GUILayout.BeginHorizontal();
        GUILayout.Label("Slot", GUILayout.Width(60));
        _slot = GUILayout.TextField(_slot ?? "", GUILayout.Width(140));
        GUILayout.Label("Password", GUILayout.Width(80));
        _password = GUILayout.PasswordField(_password ?? "", '*', GUILayout.Width(140));
        GUILayout.EndHorizontal();

        GUILayout.Space(6);
        GUILayout.Label($"Status: {_status}");
        GUILayout.Space(6);

        GUILayout.BeginHorizontal();

        bool clientConnected = false;
        GUI.enabled = !_connecting && !clientConnected && ValidInputs();
        if (GUILayout.Button("Connect", GUILayout.Height(28)))
        {
            SaveInputs();
            StartConnect();
        }
        GUI.enabled = clientConnected && !_connecting;
        if (GUILayout.Button("Disconnect", GUILayout.Height(28)))
        {
            Disconnect();
        }
        GUI.enabled = true;

        GUILayout.FlexibleSpace();

        GUILayout.EndHorizontal();

        GUILayout.Space(6);

        GUILayout.EndVertical();

        GUI.DragWindow(new Rect(0, 0, 10000, 20));
    }

    private bool ValidInputs()
    {
        return !string.IsNullOrWhiteSpace(_host)
            && _port > 0 && _port < 65536
            && !string.IsNullOrWhiteSpace(_slot);
    }

    private void SaveInputs()
    {
        ValheimRandomizer.randomized.Value = _randomized;
        ValheimRandomizer.archipelagoHostname.Value = _host ?? "";
        ValheimRandomizer.archipelagoPort.Value = _port;
        ValheimRandomizer.archipelagoSlot.Value = _slot ?? "";
        ValheimRandomizer.archipelagoPassword.Value = _password ?? "";
    }

    private async void StartConnect()
    {
        // Cancel previous attempts if any


        _connecting = true;
        _status = "Connected";
        try
        {
            ArchipelagoConnection.Connect(_host, _port, _slot, _password);
        }
        catch (OperationCanceledException)
        {
            _status = "Canceled";
        }
        catch (Exception ex)
        {
            _status = $"Error: {ex.Message}";
            ValheimRandomizer.Log.LogError($"[AP] Connect error: {ex}");
        }
        finally
        {
            _connecting = false;
        }
    }

    private void Disconnect()
    {

    }
}