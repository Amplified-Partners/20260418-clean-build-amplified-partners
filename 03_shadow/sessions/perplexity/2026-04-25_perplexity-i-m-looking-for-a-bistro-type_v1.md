---
title: "Untitled"
slug: i-m-looking-for-a-bistro-type-4GbhXjhtSAOxpi_trMQw3w
source: perplexity
exported: 2026-01-20T04:30:38.909Z
---

# Untitled

## Question

I'm looking for a bistro type restaurant in Newcastle or surrounding area we want somewhere that's up-and-coming not fussy but good food and good atmosphere

---

## Question

do do do do do/Users/ewanbramley/TodayMirrorXcode/TodayMirror/Services/StorageService.swift:81:30 Cannot find type 'StreakData' in scope

/Users/ewanbramley/TodayMirrorXcode/TodayMirror/Services/StorageService.swift:90:28 Cannot find 'StreakData' in scope

/Users/ewanbramley/TodayMirrorXcode/TodayMirror/Services/StorageService.swift:101:39 Type of expression is ambiguous without a type annotation

/Users/ewanbramley/TodayMirrorXcode/TodayMirror/Services/StorageService.swift:101:46 Cannot find 'StreakData' in scope

/Users/ewanbramley/TodayMirrorXcode/TodayMirror/Services/StorageService.swift:111:39 Cannot find type 'StreakData' in scope

---

## Question

write me a prompt for kilo code

---

## Question

//
//  StorageService.swift
//  TodayMirror
//
//  Created on 2024-12-16
//

import Foundation

class StorageService {
    static let shared = StorageService()
    
    private let fileManager = FileManager.default
    private let dataDirectory: URL
    
    private init() {
        // ~/.today-mirror/data/
        let homeDir = fileManager.homeDirectoryForCurrentUser
        dataDirectory = homeDir
            .appendingPathComponent(".today-mirror")
            .appendingPathComponent("data")
        
        print("🔍 DEBUG: StorageService.init() - dataDirectory: \(dataDirectory.path)")
        
        // Create directory if needed
        do {
            try fileManager.createDirectory(
                at: dataDirectory,
                withIntermediateDirectories: true
            )
            print("🔍 DEBUG: StorageService.init() - directory created/verified successfully")
        } catch {
            print("❌ DEBUG: StorageService.init() - FAILED to create directory: \(error)")
        }
    }
    
    // MARK: - Tasks
    
    func loadTasks() -> [Task] {
        let url = dataDirectory.appendingPathComponent("tasks.json")
        guard let data = try? Data(contentsOf: url) else { return [] }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return (try? decoder.decode([Task].self, from: data)) ?? []
    }
    
    func saveTasks(_ tasks: [Task]) {
        let url = dataDirectory.appendingPathComponent("tasks.json")
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(tasks) else { return }
        try? data.write(to: url)
    }
    
    // MARK: - Interactions
    
    func loadInteractions() -> [Interaction] {
        let url = dataDirectory.appendingPathComponent("interactions.json")
        guard let data = try? Data(contentsOf: url) else { return [] }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return (try? decoder.decode([Interaction].self, from: data)) ?? []
    }
    
    func saveInteractions(_ interactions: [Interaction]) {
        let url = dataDirectory.appendingPathComponent("interactions.json")
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(interactions) else { return }
        try? data.write(to: url)
    }
    
    // MARK: - Streak Data
    
    func loadStreakData() -> StreakData {
        let url = dataDirectory.appendingPathComponent("streak_data.json")
        print("🔍 DEBUG: StorageService.loadStreakData() - attempting to load from: \(url.path)")
        
        guard let data = try? Data(contentsOf: url) else {
            print("🔍 DEBUG: StorageService.loadStreakData() - file not found, creating demo data")
            // First-time user: Initialize with demo data to show what the app looks like
            // Loss Aversion (Kahneman & Tversky, 1979): Show existing progress to create
            // psychological investment immediately
            let demoData = StreakData.withDemoData()
            print("🔍 DEBUG: StorageService.loadStreakData() - demo data created: currentStreak=\(demoData.currentStreak)")
            saveStreakData(demoData)
            return demoData
        }
        
        print("🔍 DEBUG: StorageService.loadStreakData() - file found, decoding...")
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        
        do {
            let decoded = try decoder.decode(StreakData.self, from: data)
            print("🔍 DEBUG: StorageService.loadStreakData() - successfully decoded: currentStreak=\(decoded.currentStreak)")
            return decoded
        } catch {
            print("❌ DEBUG: StorageService.loadStreakData() - FAILED to decode: \(error)")
            print("🔍 DEBUG: StorageService.loadStreakData() - falling back to demo data")
            return StreakData.withDemoData()
        }
    }
    
    func saveStreakData(_ streakData: StreakData) {
        let url = dataDirectory.appendingPathComponent("streak_data.json")
        print("🔍 DEBUG: StorageService.saveStreakData() - saving to: \(url.path)")
        print("🔍 DEBUG: StorageService.saveStreakData() - data: currentStreak=\(streakData.currentStreak)")
        
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        do {
            let data = try encoder.encode(streakData)
            try data.write(to: url)
            print("🔍 DEBUG: StorageService.saveStreakData() - successfully saved")
        } catch {
            print("❌ DEBUG: StorageService.saveStreakData() - FAILED: \(error)")
        }
    }
    
    // MARK: - Daily Logs
    
    func loadDailyLogs() -> [DailyLog] {
        let url = dataDirectory.appendingPathComponent("daily_logs.json")
        guard let data = try? Data(contentsOf: url) else { return [] }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return (try? decoder.decode([DailyLog].self, from: data)) ?? []
    }
    
    func saveDailyLogs(_ logs: [DailyLog]) {
        let url = dataDirectory.appendingPathComponent("daily_logs.json")
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(logs) else { return }
        try? data.write(to: url)
    }
} errors in build

---

## Question

write a kilo code prompt for that

---

## Question

why dont we write the perfect kilo code rules and workflows to optimise the work i am trying to do

---

---
Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd
