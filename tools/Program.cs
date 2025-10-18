using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;

class Program
{
    // ===== research.tsv (0-based indices; adjust as needed) =====
    const int RESEARCH_ID_COL = 1; // e.g., "researchAxeTier1"
    const int RESEARCH_DISPLAY_NAME_COL = 2; // user-friendly name
    const int RESEARCH_TIER_COL = 7; // "0".."11"
    const int RESEARCH_CATEGORY_COL = 8; // "0".."11"

    // ===== trophies.tsv (0-based indices; adjust as needed) =====
    const int TROPHY_NAME_COL = 0; // user-friendly (e.g., "Seeker")
    const int TROPHY_ID_COL = 1; // e.g., "researchTrophySeeker" / "TrophySeeker"
    const int TROPHY_TIER_COL = 3; // numeric tier

    // ===== outputs =====
    const string RegionsCsv = "regions.csv";
    const string ItemsCsv = "items.csv";
    const string LocationsCsv = "locations.csv";

    const int MaxTier = 11;

    static void Main(string[] args)
    {
        string researchPath = args.Length > 0 ? args[0] : "research.tsv";
        string trophiesPath = args.Length > 1 ? args[1] : "trophies.tsv";

        if (!File.Exists(researchPath)) { Console.Error.WriteLine($"Missing {researchPath}"); return; }
        if (!File.Exists(trophiesPath)) { Console.Error.WriteLine($"Missing {trophiesPath}"); return; }

        var researchRows = LoadTsv(researchPath, skipHeader: true);
        var trophyRows = LoadTsv(trophiesPath, skipHeader: true);

        // ===== regions.txt =====
        // Each line: FromRegion,ToRegion,(zero or more progression item IDs for FromRegion, comma-separated)

        // Build a map of tier -> progression item IDs ("item:<researchId>")
        var tierToItems = new Dictionary<int, SortedSet<string>>();
        for (int t = 0; t <= MaxTier; t++)
            tierToItems[t] = new SortedSet<string>(StringComparer.Ordinal);

        foreach (var row in researchRows)
        {
            if (!HasCols(row, Math.Max(RESEARCH_DISPLAY_NAME_COL, RESEARCH_TIER_COL))) continue;
            if (row[RESEARCH_CATEGORY_COL] != "Progression") continue;

            string baseId = (row[RESEARCH_DISPLAY_NAME_COL] ?? "").Trim();
            if (string.IsNullOrEmpty(baseId)) continue;

            int tier = ClampTier(SafeInt(row[RESEARCH_TIER_COL], 0));
            tierToItems[tier].Add(baseId + "," + 1);
        }

        // Write regions.txt with items appended to each tier line
        using (var sw = new StreamWriter("regions.csv", false, new UTF8Encoding(false)))
        {
            // Menu -> Tier0 (no items on the Menu line)
            sw.WriteLine(Csv("Menu", "Tier0"));

            for (int t = 0; t < MaxTier; t++)
            {
                sw.Write("Tier" + t + ",Tier" + (t+1));
                foreach (string item in tierToItems[t])
                {
                    sw.Write("," + item);
                }
                sw.WriteLine("");
            }
        }

        // ===== items.csv =====
        // Schema (no header): Item User Friendly Name,ID,Count,Type,Classification
        using (var sw = new StreamWriter(ItemsCsv, false, new UTF8Encoding(false)))
        {
            sw.WriteLine("// Item User Friendly Name,ID,Count,Type,Classification");
            // Research -> items
            foreach (var row in researchRows)
            {
                if (!HasCols(row, Math.Max(RESEARCH_ID_COL, RESEARCH_DISPLAY_NAME_COL))) continue;

                string baseId = (row[RESEARCH_ID_COL] ?? "").Trim();            // raw research ID
                string disp = (row[RESEARCH_DISPLAY_NAME_COL] ?? "").Trim();  // friendly
                string category = (row[RESEARCH_CATEGORY_COL] ?? "Filler").Trim();
                if (string.IsNullOrEmpty(disp)) disp = baseId;

                string internalId = $"item:{baseId}";   // prefixed internal ID
                string friendly = disp;

                sw.WriteLine(Csv(friendly, internalId, "1", "Item", category));
            }

            // Trophies -> items (Useful), display "Trophy: <Name>"
            foreach (var row in trophyRows)
            {
                if (!HasCols(row, Math.Max(TROPHY_ID_COL, TROPHY_NAME_COL))) continue;

                string baseId = (row[TROPHY_ID_COL] ?? "").Trim();
                string tname = (row[TROPHY_NAME_COL] ?? "").Trim();
                if (string.IsNullOrEmpty(tname)) tname = baseId;

                string internalId = $"item:{baseId}";
                string friendly = $"Trophy: {tname}";

                sw.WriteLine(Csv(friendly, internalId, "1", "Item", "Useful"));
            }
        }

        // ===== locations.csv =====
        // Schema (no header): Location Type,User Friendly Name,ID,Classification,Region
        using (var sw = new StreamWriter(LocationsCsv, false, new UTF8Encoding(false)))
        {
            sw.WriteLine("// Location Type,User Friendly Name,ID,Classification,Region");
            // Research -> locations
            foreach (var row in researchRows)
            {
                if (!HasCols(row, Math.Max(RESEARCH_ID_COL, Math.Max(RESEARCH_TIER_COL, RESEARCH_DISPLAY_NAME_COL)))) continue;

                string baseId = (row[RESEARCH_ID_COL] ?? "").Trim();
                string disp = (row[RESEARCH_DISPLAY_NAME_COL] ?? "").Trim();
                if (string.IsNullOrEmpty(disp)) disp = baseId;

                int tier = ClampTier(SafeInt(row[RESEARCH_TIER_COL], 0));

                string locType = "Research";
                string friendly = disp;
                string internalId = $"loc:{baseId}";      // prefixed internal ID
                string classification = "Not Missable";
                string region = $"Tier{tier}";

                sw.WriteLine(Csv(locType, friendly, internalId, classification, region));
            }

            // Trophies -> locations (tier respected), display "Trophy: <Name>"
            foreach (var row in trophyRows)
            {
                if (!HasCols(row, Math.Max(TROPHY_TIER_COL, Math.Max(TROPHY_ID_COL, TROPHY_NAME_COL)))) continue;

                string baseId = (row[TROPHY_ID_COL] ?? "").Trim();
                string tname = (row[TROPHY_NAME_COL] ?? "").Trim();
                if (string.IsNullOrEmpty(tname)) tname = baseId;

                int tier = ClampTier(SafeInt(row[TROPHY_TIER_COL], 0));

                string locType = "Trophy";
                string friendly = $"Trophy: {tname}";
                string internalId = $"loc:{baseId}";
                string classification = "Not Missable";
                string region = $"Tier{tier}";

                sw.WriteLine(Csv(locType, friendly, internalId, classification, region));
            }
        }

        Console.WriteLine($"Wrote {RegionsCsv}, {ItemsCsv}, {LocationsCsv}");
    }

    // ===== helpers =====
    static List<string[]> LoadTsv(string path, bool skipHeader)
    {
        var all = new List<string[]>();
        using (var sr = new StreamReader(path, Encoding.UTF8, detectEncodingFromByteOrderMarks: true))
        {
            string? line; bool first = true;
            while ((line = sr.ReadLine()) != null)
            {
                if (first && skipHeader) { first = false; continue; }
                first = false;
                if (string.IsNullOrWhiteSpace(line)) continue;
                all.Add(line.Split('\t'));
            }
        }
        return all;
    }

    static bool HasCols(string[] row, int idx) => row != null && row.Length > idx;

    static int SafeInt(string? s, int fallback)
        => int.TryParse((s ?? "").Trim(), NumberStyles.Integer, CultureInfo.InvariantCulture, out var v) ? v : fallback;

    static int ClampTier(int t) => t < 0 ? 0 : (t > MaxTier ? MaxTier : t);

    static string Csv(params string[] fields) => string.Join(",", fields.Select(EscapeCsv));

    static string EscapeCsv(string? s)
    {
        if (s == null) return "";
        bool needQuotes = s.Contains(',') || s.Contains('"') || s.Contains('\n') || s.Contains('\r');
        string t = s.Replace("\"", "\"\"");
        return needQuotes ? $"\"{t}\"" : t;
    }
}
