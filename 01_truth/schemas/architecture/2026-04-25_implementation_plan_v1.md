---
title: "Today Mirror - Implementation Plan v0.1"
id: "implementation_plan"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "implementation-plan"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Today Mirror - Implementation Plan v0.1

**Tech Stack:** SwiftUI Native macOS App  
**Target:** macOS 13.0+ (Ventura)  
**Language:** Swift 5.9+  
**Date:** 2024-12-16

---

## 1. Project Structure

```
today-mirror/
├── TodayMirror.xcodeproj          # Xcode project
├── TodayMirror/
│   ├── TodayMirrorApp.swift       # App entry point
│   ├── Models/
│   │   ├── Task.swift             # Task data model
│   │   ├── Interaction.swift      # LLM interaction model
│   │   ├── DailyLog.swift         # Daily summary model
│   │   └── AppMode.swift          # Mode enum and rules
│   ├── ViewModels/
│   │   ├── TaskViewModel.swift    # Task management logic
│   │   ├── LLMViewModel.swift     # LLM interaction logic
│   │   └── SummaryViewModel.swift # Daily summary logic
│   ├── Views/
│   │   ├── MainView.swift         # Main dashboard
│   │   ├── TaskRowView.swift      # Individual task row
│   │   ├── DoneStripView.swift    # Right column (done tasks)
│   │   ├── ModePickerView.swift   # Mode selector dropdown
│   │   ├── InputView.swift        # "What's on your mind?" input
│   │   └── SummaryView.swift      # Daily summary display
│   ├── Services/
│   │   ├── StorageService.swift   # JSON file I/O
│   │   ├── ObsidianService.swift  # Markdown file writer
│   │   ├── LLMService.swift       # HTTP client for Ollama
│   │   └── ConfigService.swift    # Config file management
│   ├── Utilities/
│   │   ├── Constants.swift        # App constants
│   │   ├── Extensions.swift       # Swift extensions
│   │   └── Logger.swift           # Logging utility
│   └── Resources/
│       ├── Assets.xcassets        # Images, colors
│       └── Info.plist             # App metadata
├── TodayMirrorTests/              # Unit tests
│   ├── ModelTests.swift
│   ├── ServiceTests.swift
│   └── ViewModelTests.swift
├── README.md                      # Setup instructions
├── SPEC.md                        # Specification (already created)
└── smoke-test.sh                  # Automated smoke test
```

---

## 2. Data Models (Swift Implementation)

### 2.1 Task.swift
```swift
import Foundation

enum TaskLane: String, Codable {
    case revenue
    case delivery
    case life
}

enum TaskStatus: String, Codable {
    case intended
    case done
    case archived
}

enum TaskSource: String, Codable {
    case manual
    case llmSuggested
}

struct Task: Identifiable, Codable {
    let id: UUID
    var title: String
    var lane: TaskLane
    var status: TaskStatus
    let createdAt: Date
    var completedAt: Date?
    var archivedAt: Date?
    let source: TaskSource
    
    init(
        id: UUID = UUID(),
        title: String,
        lane: TaskLane,
        status: TaskStatus = .intended,
        createdAt: Date = Date(),
        completedAt: Date? = nil,
        archivedAt: Date? = nil,
        source: TaskSource = .manual
    ) {
        self.id = id
        self.title = title
        self.lane = lane
        self.status = status
        self.createdAt = createdAt
        self.completedAt = completedAt
        self.archivedAt = archivedAt
        self.source = source
    }
}
```

### 2.2 AppMode.swift
```swift
import Foundation

enum AppMode: String, Codable, CaseIterable {
    case moneyFirst = "money_first"
    case balance
    case recovery
    
    var displayName: String {
        switch self {
        case .moneyFirst: return "Money-First"
        case .balance: return "Balance"
        case .recovery: return "Recovery"
        }
    }
    
    // Lane allocation rules
    func maxTasksForLane(_ lane: TaskLane) -> Int {
        switch (self, lane) {
        case (.moneyFirst, .revenue): return 2
        case (.moneyFirst, .delivery): return 1
        case (.moneyFirst, .life): return 0
            
        case (.balance, .revenue): return 1
        case (.balance, .delivery): return 1
        case (.balance, .life): return 1
            
        case (.recovery, .revenue): return 0
        case (.recovery, .delivery): return 1
        case (.recovery, .life): return 2
        }
    }
    
    // Calculate actual mode from completed tasks
    static func calculateActual(from tasks: [Task]) -> String {
        let completed = tasks.filter { $0.status == .done }
        let revenue = completed.filter { $0.lane == .revenue }.count
        let delivery = completed.filter { $0.lane == .delivery }.count
        let life = completed.filter { $0.lane == .life }.count
        
        if revenue >= 2 { return "money_first" }
        if life >= 2 { return "recovery" }
        if revenue == 1 && delivery == 1 && life == 1 { return "balance" }
        return "mixed"
    }
}
```

### 2.3 Interaction.swift
```swift
import Foundation

struct LLMResponse: Codable {
    let cleanedText: String
    let tasks: [SuggestedTask]
    let confidence: Double
}

struct SuggestedTask: Codable {
    let title: String
    let lane: TaskLane
    let confidence: Double
}

enum InteractionAction: String, Codable {
    case added
    case ignored
    case modified
}

struct Interaction: Identifiable, Codable {
    let id: UUID
    let timestamp: Date
    let userInput: String
    let llmResponse: LLMResponse
    var actionTaken: InteractionAction
    var notes: String?
    
    init(
        id: UUID = UUID(),
        timestamp: Date = Date(),
        userInput: String,
        llmResponse: LLMResponse,
        actionTaken: InteractionAction = .ignored,
        notes: String? = nil
    ) {
        self.id = id
        self.timestamp = timestamp
        self.userInput = userInput
        self.llmResponse = llmResponse
        self.actionTaken = actionTaken
        self.notes = notes
    }
}
```

### 2.4 DailyLog.swift
```swift
import Foundation

struct DailyLog: Codable {
    let date: String // YYYY-MM-DD
    let modeSet: AppMode
    let modeActual: String
    let tasksCommitted: [Task]
    let tasksCompleted: [Task]
    let tasksArchived: [Task]
    let interactions: [Interaction]
    let summaryText: String
    var patternNotes: String?
    
    init(
        date: String,
        modeSet: AppMode,
        modeActual: String,
        tasksCommitted: [Task],
        tasksCompleted: [Task],
        tasksArchived: [Task],
        interactions: [Interaction],
        summaryText: String,
        patternNotes: String? = nil
    ) {
        self.date = date
        self.modeSet = modeSet
        self.modeActual = modeActual
        self.tasksCommitted = tasksCommitted
        self.tasksCompleted = tasksCompleted
        self.tasksArchived = tasksArchived
        self.interactions = interactions
        self.summaryText = summaryText
        self.patternNotes = patternNotes
    }
}
```

---

## 3. Services Layer

### 3.1 StorageService.swift
```swift
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
        
        // Create directory if needed
        try? fileManager.createDirectory(
            at: dataDirectory,
            withIntermediateDirectories: true
        )
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
}
```

### 3.2 ObsidianService.swift
```swift
import Foundation

class ObsidianService {
    static let shared = ObsidianService()
    
    private let fileManager = FileManager.default
    private var vaultPath: URL?
    
    private init() {
        // Load vault path from config
        if let config = ConfigService.shared.loadConfig() {
            vaultPath = URL(fileURLWithPath: config.obsidianVaultPath)
        }
    }
    
    func setVaultPath(_ path: String) {
        vaultPath = URL(fileURLWithPath: path)
        
        // Create subdirectories
        let interactions = vaultPath!.appendingPathComponent("interactions")
        let dailyLogs = vaultPath!.appendingPathComponent("daily_logs")
        let weeklyPatterns = vaultPath!.appendingPathComponent("weekly_patterns")
        
        try? fileManager.createDirectory(at: interactions, withIntermediateDirectories: true)
        try? fileManager.createDirectory(at: dailyLogs, withIntermediateDirectories: true)
        try? fileManager.createDirectory(at: weeklyPatterns, withIntermediateDirectories: true)
    }
    
    // MARK: - Interaction Markdown
    func writeInteraction(_ interaction: Interaction) {
        guard let vaultPath = vaultPath else { return }
        
        let formatter = ISO8601DateFormatter()
        let timestamp = formatter.string(from: interaction.timestamp)
        let filename = timestamp.replacingOccurrences(of: ":", with: "-") + ".md"
        
        let url = vaultPath
            .appendingPathComponent("interactions")
            .appendingPathComponent(filename)
        
        var markdown = """
        ---
        date: \(timestamp)
        type: interaction
        ---
        
        # Interaction
        
        **User Input:**
        \(interaction.userInput)
        
        **LLM Response:**
        \(interaction.llmResponse.cleanedText)
        
        **Tasks Extracted:**
        
        """
        
        for task in interaction.llmResponse.tasks {
            markdown += "- [ ] \(task.title) [lane: \(task.lane.rawValue)]\n"
        }
        
        markdown += "\n**Action Taken:** \(interaction.actionTaken.rawValue)\n"
        
        if let notes = interaction.notes {
            markdown += "\n**Notes:** \(notes)\n"
        }
        
        try? markdown.write(to: url, atomically: true, encoding: .utf8)
    }
    
    // MARK: - Daily Log Markdown
    func writeDailyLog(_ log: DailyLog) {
        guard let vaultPath = vaultPath else { return }
        
        let filename = "\(log.date).md"
        let url = vaultPath
            .appendingPathComponent("daily_logs")
            .appendingPathComponent(filename)
        
        var markdown = """
        ---
        date: \(log.date)
        mode_set: \(log.modeSet.rawValue)
        mode_actual: \(log.modeActual)
        ---
        
        # Daily Log - \(formatDate(log.date))
        
        ## Mode
        **Set:** \(log.modeSet.displayName)  
        **Actual:** \(log.modeActual.capitalized)
        
        ## Tasks
        **Committed:** \(log.tasksCommitted.count)  
        **Completed:** \(log.tasksCompleted.count)  
        **Archived:** \(log.tasksArchived.count)
        
        ### Completed
        
        """
        
        for task in log.tasksCompleted {
            markdown += "- [x] \(task.title) [\(task.lane.rawValue)]\n"
        }
        
        if !log.tasksArchived.isEmpty {
            markdown += "\n### Archived\n\n"
            for task in log.tasksArchived {
                markdown += "- [-] \(task.title) [\(task.lane.rawValue)]\n"
            }
        }
        
        markdown += "\n## Summary\n\(log.summaryText)\n"
        
        if let notes = log.patternNotes {
            markdown += "\n## Notes\n\(notes)\n"
        }
        
        try? markdown.write(to: url, atomically: true, encoding: .utf8)
    }
    
    private func formatDate(_ dateString: String) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        guard let date = formatter.date(from: dateString) else { return dateString }
        
        formatter.dateFormat = "MMMM d, yyyy"
        return formatter.string(from: date)
    }
}
```

### 3.3 LLMService.swift
```swift
import Foundation

struct LLMRequest: Codable {
    let model: String
    let prompt: String
    let stream: Bool
    let format: String
}

struct LLMAPIResponse: Codable {
    let response: String
}

class LLMService {
    static let shared = LLMService()
    
    private let endpoint: URL
    private let model: String
    
    private init() {
        let config = ConfigService.shared.loadConfig()
        endpoint = URL(string: config?.llmEndpoint ?? "http://localhost:11434/api/generate")!
        model = config?.llmModel ?? "llama3.2"
    }
    
    func extractTasks(from input: String) async -> Result<LLMResponse, Error> {
        let prompt = """
        Extract actionable tasks from this text. Return JSON with cleaned_text and tasks array. 
        Each task needs title and lane (revenue/delivery/life).
        
        User input: \(input)
        """
        
        let request = LLMRequest(
            model: model,
            prompt: prompt,
            stream: false,
            format: "json"
        )
        
        var urlRequest = URLRequest(url: endpoint)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.timeoutInterval = 30
        
        do {
            let encoder = JSONEncoder()
            urlRequest.httpBody = try encoder.encode(request)
            
            let (data, response) = try await URLSession.shared.data(for: urlRequest)
            
            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                return .failure(LLMError.invalidResponse)
            }
            
            // Parse Ollama response
            let apiResponse = try JSONDecoder().decode(LLMAPIResponse.self, from: data)
            
            // Parse the JSON string in the response
            guard let responseData = apiResponse.response.data(using: .utf8) else {
                return .failure(LLMError.invalidJSON)
            }
            
            let llmResponse = try JSONDecoder().decode(LLMResponse.self, from: responseData)
            return .success(llmResponse)
            
        } catch {
            return .failure(error)
        }
    }
    
    // Fallback for testing when LLM is offline
    func dummyResponse(for input: String) -> LLMResponse {
        return LLMResponse(
            cleanedText: input,
            tasks: [
                SuggestedTask(title: "Example task from: \(input)", lane: .delivery, confidence: 0.5)
            ],
            confidence: 0.5
        )
    }
}

enum LLMError: Error {
    case invalidResponse
    case invalidJSON
    case timeout
}
```

### 3.4 ConfigService.swift
```swift
import Foundation

struct AppConfig: Codable {
    var obsidianVaultPath: String
    var llmEndpoint: String
    var llmModel: String
    var defaultMode: AppMode
    var theme: String
    
    static let `default` = AppConfig(
        obsidianVaultPath: NSHomeDirectory() + "/Documents/Obsidian/TodayMirror",
        llmEndpoint: "http://localhost:11434/api/generate",
        llmModel: "llama3.2",
        defaultMode: .balance,
        theme: "light"
    )
}

class ConfigService {
    static let shared = ConfigService()
    
    private let fileManager = FileManager.default
    private let configURL: URL
    
    private init() {
        let homeDir = fileManager.homeDirectoryForCurrentUser
        configURL = homeDir
            .appendingPathComponent(".today-mirror")
            .appendingPathComponent("config.json")
        
        // Create directory if needed
        let directory = configURL.deletingLastPathComponent()
        try? fileManager.createDirectory(at: directory, withIntermediateDirectories: true)
    }
    
    func loadConfig() -> AppConfig? {
        guard let data = try? Data(contentsOf: configURL) else {
            // Create default config
            saveConfig(.default)
            return .default
        }
        
        let decoder = JSONDecoder()
        return try? decoder.decode(AppConfig.self, from: data)
    }
    
    func saveConfig(_ config: AppConfig) {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        
        guard let data = try? encoder.encode(config) else { return }
        try? data.write(to: configURL)
    }
}
```

---

## 4. ViewModels

### 4.1 TaskViewModel.swift
```swift
import Foundation
import Combine

@MainActor
class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = []
    @Published var currentMode: AppMode = .balance
    @Published var errorMessage: String?
    
    private let storage = StorageService.shared
    private let obsidian = ObsidianService.shared
    
    init() {
        loadTasks()
        loadMode()
    }
    
    var intendedTasks: [Task] {
        tasks.filter { $0.status == .intended }
    }
    
    var doneTasks: [Task] {
        tasks.filter { $0.status == .done }
    }
    
    func loadTasks() {
        tasks = storage.loadTasks()
    }
    
    func loadMode() {
        if let config = ConfigService.shared.loadConfig() {
            currentMode = config.defaultMode
        }
    }
    
    func addTask(title: String, lane: TaskLane, source: TaskSource = .manual) {
        // Check if we can add this task based on mode rules
        let currentLaneTasks = intendedTasks.filter { $0.lane == lane }
        let maxAllowed = currentMode.maxTasksForLane(lane)
        
        if currentLaneTasks.count >= maxAllowed {
            errorMessage = "Cannot add more \(lane.rawValue) tasks in \(currentMode.displayName) mode. Maximum: \(maxAllowed)"
            return
        }
        
        if intendedTasks.count >= 3 {
            errorMessage = "Today is full. Replace or archive a task first."
            return
        }
        
        let task = Task(title: title, lane: lane, source: source)
        tasks.append(task)
        saveTasks()
    }
    
    func completeTask(_ task: Task) {
        guard let index = tasks.firstIndex(where: { $0.id == task.id }) else { return }
        
        tasks[index].status = .done
        tasks[index].completedAt = Date()
        saveTasks()
    }
    
    func archiveTask(_ task: Task) {
        guard let index = tasks.firstIndex(where: { $0.id == task.id }) else { return }
        
        tasks[index].status = .archived
        tasks[index].archivedAt = Date()
        saveTasks()
    }
    
    func replaceTask(_ oldTask: Task, with newTask: Task) {
        archiveTask(oldTask)
        tasks.append(newTask)
        saveTasks()
    }
    
    func changeMode(to mode: AppMode) {
        currentMode = mode
        
        // Save to config
        var config = ConfigService.shared.loadConfig() ?? .default
        config.defaultMode = mode
        ConfigService.shared.saveConfig(config)
    }
    
    private func saveTasks() {
        storage.saveTasks(tasks)
    }
}
```

### 4.2 LLMViewModel.swift
```swift
import Foundation
import Combine

@MainActor
class LLMViewModel: ObservableObject {
    @Published var userInput: String = ""
    @Published var isProcessing: Bool = false
    @Published var suggestedTasks: [SuggestedTask] = []
    @Published var errorMessage: String?
    @Published var interactions: [Interaction] = []
    
    private let llmService = LLMService.shared
    private let storage = StorageService.shared
    private let obsidian = ObsidianService.shared
    
    init() {
        loadInteractions()
    }
    
    func loadInteractions() {
        interactions = storage.loadInteractions()
    }
    
    func processInput() async {
        guard !userInput.isEmpty else { return }
        
        isProcessing = true
        errorMessage = nil
        
        let result = await llmService.extractTasks(from: userInput)
        
        switch result {
        case .success(let response):
            suggestedTasks = response.tasks
            
            // Save interaction
            let interaction = Interaction(
                userInput: userInput,
                llmResponse: response
            )
            interactions.append(interaction)
            storage.saveInteractions(interactions)
            obsidian.writeInteraction(interaction)
            
        case .failure(let error):
            errorMessage = "LLM error: \(error.localizedDescription). Using fallback."
            
            // Use dummy response for testing
            let dummyResponse = llmService.dummyResponse(for: userInput)
            suggestedTasks = dummyResponse.tasks
        }
        
        isProcessing = false
        userInput = ""
    }
    
    func clearSuggestions() {
        suggestedTasks = []
    }
}
```

### 4.3 SummaryViewModel.swift
```swift
import Foundation
import Combine

@MainActor
class SummaryViewModel: ObservableObject {
    @Published var dailyLogs: [DailyLog] = []
    @Published var currentSummary: String?
    @Published var isGenerating: Bool = false
    
    private let storage = StorageService.shared
    private let obsidian = ObsidianService.shared
    
    init() {
        loadDailyLogs()
    }
    
    func loadDailyLogs() {
        dailyLogs = storage.loadDailyLogs()
    }
    
    func generateTodaySummary(
        mode: AppMode,
        tasks: [Task],
        interactions: [Interaction]
    ) {
        isGenerating = true
        
        let today = formatDate(Date())
        let committed = tasks.filter { $0.status == .intended || $0.status == .done }
        let completed = tasks.filter { $0.status == .done }
        let archived = tasks.filter { $0.status == .archived }
        
        let modeActual = AppMode.calculateActual(from: tasks)
        
        // Generate factual summary
        let summary = generateSummaryText(
            mode: mode,
            committed: committed.count,
            completed: completed,
            archived: archived.count,
            modeActual: modeActual
        )
        
        let log = DailyLog(
            date: today,
            modeSet: mode,
            modeActual: modeActual,
            tasksCommitted: committed,
            tasksCompleted: completed,
            tasksArchived: archived,
            interactions: interactions,
            summaryText: summary
        )
        
        dailyLogs.append(log)
        storage.saveDailyLogs(dailyLogs)
        obsidian.writeDailyLog(log)
        
        currentSummary = summary
        isGenerating = false
    }
    
    private func generateSummaryText(
        mode: AppMode,
        committed: Int,
        completed: [Task],
        archived: Int,
        modeActual: String
    ) -> String {
        let revenue = completed.filter { $0.lane == .revenue }.count
        let delivery = completed.filter { $0.lane == .delivery }.count
        let life = completed.filter { $0.lane == .life }.count
        
        var breakdown = [String]()
        if revenue > 0 { breakdown.append("\(revenue) revenue") }
        if delivery > 0 { breakdown.append("\(delivery) delivery") }
        if life > 0 { breakdown.append("\(life) life") }
        
        let breakdownText = breakdown.isEmpty ? "none" : breakdown.joined(separator: ", ")
        
        var summary = "You committed to \(committed) tasks in \(mode.displayName) mode. "
        summary += "You completed \(completed.count) tasks (\(breakdownText)). "
        
        if archived > 0 {
            summary += "You archived \(archived) task\(archived == 1 ? "" : "s"). "
        }
        
        if modeActual == mode.rawValue {
            summary += "Your actual mode matched your intended mode."
        } else {
            summary += "Your actual mode was \(modeActual.capitalized)."
        }
        
        return summary
    }
    
    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: date)
    }
}
```

---

## 5. Views (SwiftUI)

### 5.1 TodayMirrorApp.swift
```swift
import SwiftUI

@main
struct TodayMirrorApp: App {
    @StateObject private var taskVM = TaskViewModel()
    @StateObject private var llmVM = LLMViewModel()
    @StateObject private var summaryVM = SummaryViewModel()
    
    var body: some Scene {
        WindowGroup {
            MainView()
                .environmentObject(taskVM)
                .environmentObject(llmVM)
                .environmentObject(summaryVM)
                .frame(minWidth: 800, minHeight: 600)
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
    }
}
```

### 5.2 MainView.swift
```swift
import SwiftUI

struct MainView: View {
    @EnvironmentObject var taskVM: TaskViewModel
    @EnvironmentObject var llmVM: LLMViewModel
    @EnvironmentObject var summaryVM: SummaryViewModel
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Text("Today Mirror")
                    .font(.title)
                    .fontWeight(.bold)
                
                Spacer()
                
                ModePickerView()
                
                Button(action: {}) {
                    Image(systemName: "gear")
                }
                .buttonStyle(.plain)
            }
            .padding()
            .background(Color(NSColor.windowBackgroundColor))
            
            Divider()
            
            // Main content: Left (Intended) | Right (Done)
            HStack(spacing: 0) {
                // Left column: Today's 3
                VStack(alignment: .leading, spacing: 0) {
                    Text("Today's 3")
                        .font(.headline)
                        .padding()
                    
                    Text("(Intended)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .padding(.horizontal)
                        .padding(.bottom)
                    
                    ForEach(0..<3) { index in
                        if index < taskVM.intendedTasks.count {
                            TaskRowView(task: taskVM.intendedTasks[index])
                        } else {
                            EmptyTaskSlot(index: index)
                        }
                        
                        if index < 2 {
                            Divider()
                        }
                    }
                    
                    Spacer()
                }
                .frame(maxWidth: .infinity)
                .background(Color(NSColor.controlBackgroundColor))
                
                Divider()
                
                // Right column: Done
                DoneStripView()
                    .frame(maxWidth: .infinity)
                    .background(Color(NSColor.controlBackgroundColor).opacity(0.5))
            }
            .frame(maxHeight: .infinity)
            
            Divider()
            
            // Bottom: Input
            InputView()
                .padding()
            
            // Summary button
            Button("Generate Today's Summary") {
                summaryVM.generateTodaySummary(
                    mode: taskVM.currentMode,
                    tasks: taskVM.tasks,
                    interactions: llmVM.interactions
                )
            }
            .padding(.bottom)
        }
        .alert("Error", isPresented: .constant(taskVM.errorMessage != nil)) {
            Button("OK") {
                taskVM.errorMessage = nil
            }
        } message: {
            Text(taskVM.errorMessage ?? "")
        }
    }
}

struct EmptyTaskSlot: View {
    let index: Int
    
    var body: some View {
        HStack {
            Image(systemName: "square")
                .foregroundColor(.secondary)
            
            Text("Empty slot \(index + 1)")
                .foregroundColor(.secondary)
            
            Spacer()
        }
        .padding()
        .frame(height: 80)
    }
}
```

### 5.3 TaskRowView.swift
```swift
import SwiftUI

struct TaskRowView: View {
    @EnvironmentObject var taskVM: TaskViewModel
    let task: Task
    
    @State private var isCompleting = false
    
    var body: some View {
        HStack(spacing: 12) {
            // Checkbox
            Button(action: {
                withAnimation(.easeInOut(duration: 0.3)) {
                    isCompleting = true
                }
                
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                    taskVM.completeTask(task)
                }
            }) {
                Image(systemName: task.status == .done ? "checkmark.square.fill" : "square")
                    .font(.title2)
                    .foregroundColor(task.status == .done ? .blue : .primary)
            }
            .buttonStyle(.plain)
            
            // Task content
            VStack(alignment: .leading, spacing: 4) {
                Text(task.title)
                    .strikethrough(task.status == .done)
                    .foregroundColor(task.status == .done ? .secondary : .primary)
                
                Text("[\(task.lane.rawValue)]")
                    .font(.caption)
                    .foregroundColor(laneColor(task.lane))
            }
            
            Spacer()
            
            // Archive button
            Button(action: {
                taskVM.archiveTask(task)
            }) {
                Image(systemName: "archivebox")
                    .foregroundColor(.secondary)
            }
            .buttonStyle(.plain)
        }
        .padding()
        .frame(height: 80)
        .background(
            task.status == .done
                ? Color(red: 0.91, green: 0.93, blue: 0.95)
                : Color.white
        )
        .opacity(isCompleting ? 0.5 : 1.0)
    }
    
    private func laneColor(_ lane: TaskLane) -> Color {
        switch lane {
        case .revenue: return .green
        case .delivery: return .blue
        case .life: return .purple
        }
    }
}
```

### 5.4 DoneStripView.swift
```swift
import SwiftUI

struct DoneStripView: View {
    @EnvironmentObject var taskVM: TaskViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Text("Done")
                .font(.headline)
                .padding()
            
            Text("(Completed)")
                .font(.caption)
                .foregroundColor(.secondary)
                .padding(.horizontal)
                .padding(.bottom)
            
            ForEach(taskVM.doneTasks) { task in
                HStack {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                    
                    Text(task.title)
                        .strikethrough()
                        .foregroundColor(.secondary)
                    
                    Spacer()
                    
                    Text("[\(task.lane.rawValue)]")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .padding()
                .frame(height: 80)
                
                Divider()
            }
            
            Spacer()
        }
    }
}
```

### 5.5 ModePickerView.swift
```swift
import SwiftUI

struct ModePickerView: View {
    @EnvironmentObject var taskVM: TaskViewModel
    
    var body: some View {
        Picker("Mode", selection: $taskVM.currentMode) {
            ForEach(AppMode.allCases, id: \.self) { mode in
                Text(mode.displayName).tag(mode)
            }
        }
        .pickerStyle(.menu)
        .frame(width: 150)
    }
}
```

### 5.6 InputView.swift
```swift
import SwiftUI

struct InputView: View {
    @EnvironmentObject var llmVM: LLMViewModel
    @EnvironmentObject var taskVM: TaskViewModel
    
    var body: some View {
        VStack(spacing: 12) {
            HStack {
                TextField("What's on your mind?", text: $llmVM.userInput)
                    .textFieldStyle(.roundedBorder)
                    .disabled(llmVM.isProcessing)
                
                Button("Send") {
                    Task {
                        await llmVM.processInput()
                    }
                }
                .disabled(llmVM.userInput.isEmpty || llmVM.isProcessing)
            }
            
            // Show suggested tasks
            if !llmVM.suggestedTasks.isEmpty {
                VStack(alignment: .leading, spacing: 8) {
                    Text("Suggested tasks:")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    ForEach(llmVM.suggestedTasks, id: \.title) { suggested in
                        HStack {
                            Text(suggested.title)
                                .font(.caption)
                            
                            Text("[\(suggested.lane.rawValue)]")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                            
                            Spacer()
                            
                            Button("Add") {
                                taskVM.addTask(
                                    title: suggested.title,
                                    lane: suggested.lane,
                                    source: .llmSuggested
                                )
                                llmVM.clearSuggestions()
                            }
                            .buttonStyle(.borderedProminent)
                            .controlSize(.small)
                        }
                        .padding(8)
                        .background(Color(NSColor.controlBackgroundColor))
                        .cornerRadius(4)
                    }
                }
            }
        }
    }
}
```

---

## 6. Implementation Steps

### Phase 1: Project Setup (Day 1)
1. Create new Xcode project (macOS App, SwiftUI)
2. Set minimum deployment target to macOS 13.0
3. Create folder structure as outlined above
4. Initialize Git repository
5. Create `.gitignore` for Xcode
6. **Commit:** "Initial project setup"

### Phase 2: Data Models (Day 1)
1. Implement `Task.swift`
2. Implement `AppMode.swift`
3. Implement `Interaction.swift`
4. Implement `DailyLog.swift`
5. Add unit tests for models
6. **Commit:** "Data models complete"

### Phase 3: Services Layer (Day 2)
1. Implement `StorageService.swift`
2. Implement `ConfigService.swift`
3. Implement `ObsidianService.swift`
4. Implement `LLMService.swift`
5. Add unit tests for services
6. **Commit:** "Services layer complete"

### Phase 4: ViewModels (Day 2-3)
1. Implement `TaskViewModel.swift`
2. Implement `LLMViewModel.swift`
3. Implement `SummaryViewModel.swift`
4. Add unit tests for view models
5. **Commit:** "ViewModels complete"

### Phase 5: UI Views (Day 3-4)
1. Implement `TodayMirrorApp.swift`
2. Implement `MainView.swift`
3. Implement `TaskRowView.swift`
4. Implement `DoneStripView.swift`
5. Implement `ModePickerView.swift`
6. Implement `InputView.swift`
7. **Commit:** "UI views complete"

### Phase 6: Micro-Win Animation (Day 4)
1. Add completion animation to `TaskRowView`
2. Add slide transition to `DoneStripView`
3. Test animation timing and smoothness
4. **Commit:** "Micro-win animation complete"

### Phase 7: Testing & Polish (Day 5)
1. Write smoke test script
2. Test all features manually
3. Fix bugs
4. Add README with setup instructions
5. Test on clean machine (if possible)
6. **Commit:** "v0.1 MVP complete"

---

## 7. Testing Strategy

### 7.1 Unit Tests
```swift
// TodayMirrorTests/ModelTests.swift
import XCTest
@testable import TodayMirror

class ModelTests: XCTestCase {
    func testTaskCreation() {
        let task = Task(title: "Test", lane: .revenue)
        XCTAssertEqual(task.status, .intended)
        XCTAssertEqual(task.source, .manual)
    }
    
    func testModeRules() {
        let mode = AppMode.moneyFirst
        XCTAssertEqual(mode.maxTasksForLane(.revenue), 2)
        XCTAssertEqual(mode.maxTasksForLane(.delivery), 1)
        XCTAssertEqual(mode.maxTasksForLane(.life), 0)
    }
    
    func testModeCalculation() {
        let tasks = [
            Task(title: "T1", lane: .revenue, status: .done),
            Task(title: "T2", lane: .revenue, status: .done)
        ]
        let actual = AppMode.calculateActual(from: tasks)
        XCTAssertEqual(actual, "money_first")
    }
}
```

### 7.2 Smoke Test Script
```bash
#!/bin/bash
# smoke-test.sh

echo "🧪 Today Mirror Smoke Test"
echo "=========================="

# Check if app builds
echo "1. Building app..."
xcodebuild -project TodayMirror.xcodeproj -scheme TodayMirror -configuration Debug build
if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi
echo "✅ Build successful"

# Check if data directory is created
echo "2. Checking data directory..."
if [ -d ~/.today-mirror/data ]; then
    echo "✅ Data directory exists"
else
    echo "❌ Data directory not found"
    exit 1
fi

# Check if config file is created
echo "3. Checking config file..."
if [ -f ~/.today-mirror/config.json ]; then
    echo "✅ Config file exists"
else
    echo "❌ Config file not found"
    exit 1
fi

# Run unit tests
echo "4. Running unit tests..."
xcodebuild test -project TodayMirror.xcodeproj -scheme TodayMirror
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi
echo "✅ All tests passed"

echo ""
echo "🎉 All smoke tests passed!"
```

### 7.3 Manual Testing Checklist
```markdown
## Manual Test Checklist

### Basic Functionality
- [ ] App launches without crashing
- [ ] Main window displays correctly
- [ ] Mode selector shows all 3 modes
- [ ] Can switch between modes

### Task Management
- [ ] Can add task manually (up to 3)
- [ ] Cannot add 4th task (shows error)
- [ ] Can mark task as done
- [ ] Task moves to Done strip
- [ ] Micro-win animation plays smoothly
- [ ] Can archive task
- [ ] Lane validation works per mode

### LLM Integration
- [ ] Can enter text in input field
- [ ] LLM processes input (or shows fallback)
- [ ] Suggested tasks appear
- [ ] Can add suggested task
- [ ] Interaction saved to JSON
- [ ] Interaction saved to Obsidian

### Storage
- [ ] tasks.json created and valid
- [ ] interactions.json created and valid
- [ ] daily_logs.json created and valid
- [ ] config.json created and valid
- [ ] Obsidian markdown files created

### Daily Summary
- [ ] Can generate summary
- [ ] Summary text is factual
- [ ] Summary saved to JSON
- [ ] Summary saved to Obsidian
- [ ] Mode actual calculated correctly
```

---

## 8. README Template

```markdown
# Today Mirror v0.1

A Mac-first daily task assistant with behavioral science principles.

## Features

- **3-Task Limit:** Focus on what matters most
- **Three Modes:** Money-First, Balance, Recovery
- **Local LLM:** Privacy-first AI assistance
- **Obsidian Integration:** Markdown mirror of all data
- **Micro-Wins:** Subtle visual feedback, no manipulation

## Requirements

- macOS 13.0+ (Ventura or later)
- Xcode 15.0+ (for building)
- Ollama (for local LLM)
- Obsidian (optional, for markdown mirror)

## Installation

### 1. Install Ollama
```bash
brew install ollama
ollama pull llama3.2
```

### 2. Clone and Build
```bash
git clone <repo-url>
cd today-mirror
open TodayMirror.xcodeproj
# Build and run in Xcode (Cmd+R)
```

### 3. Configure Obsidian (Optional)
1. Open Today Mirror
2. Go to Settings
3. Set Obsidian vault path (e.g., `~/Documents/Obsidian/TodayMirror`)

## Usage

1. **Select Mode:** Choose Money-First, Balance, or Recovery
2. **Add Tasks:** Manually or via "What's on your mind?" input
3. **Complete Tasks:** Check boxes to mark done (micro-win animation)
4. **Generate Summary:** Click button at end of day

## Data Storage

- **JSON:** `~/.today-mirror/data/`
- **Obsidian:** `<vault-path>/interactions/` and `<vault-path>/daily_logs/`
- **Config:** `~/.today-mirror/config.json`

## Testing

```bash
# Run unit tests
xcodebuild test -project TodayMirror.xcodeproj -scheme TodayMirror

# Run smoke test
./smoke-test.sh
```

## Behavioral Rules

- Maximum 3 tasks in "Today" at any time
- Mode rules enforced (lane allocation)
- Factual summaries only (no praise/guilt)
- Micro-wins instead of gamification

## License

[Your License]

## Support

[Your Contact]
```

---

## 9. Definition of Done

### Must Have ✅
- [ ] App builds and runs on macOS 13.0+
- [ ] Main dashboard displays with 3-task layout
- [ ] Can add tasks manually (up to 3)
- [ ] Can mark tasks as done
- [ ] Micro-win animation on completion
- [ ] Tasks move to Done strip
- [ ] Mode selector works (3 modes)
- [ ] Mode rules enforced
- [ ] JSON storage working
- [ ] Obsidian markdown files created
- [ ] LLM client implemented (with fallback)
- [ ] "What's on your mind?" input functional
- [ ] Daily summary generation works
- [ ] Smoke test passes
- [ ] README complete

### Nice to Have ⭐
- [ ] Keyboard shortcuts
- [ ] Task editing
- [ ] Better error messages
- [ ] Settings panel
- [ ] Dark mode

### Out of Scope ❌
- Weekly pattern aggregation (v0.2)
- Multiple users
- Cloud sync
- Mobile app

---

## 10. Next Steps After v0.1

1. **User Testing:** Get feedback from 3-5 users
2. **Bug Fixes:** Address critical issues
3. **Weekly Patterns:** Implement full aggregation
4. **Settings UI:** Add configuration panel
5. **Keyboard Shortcuts:** Add power-user features
6. **v0.2 Release:** Ship improvements

---

**END OF IMPLEMENTATION PLAN**

This plan provides a complete roadmap for building Today Mirror v0.1 as a native macOS app using SwiftUI. Follow the phases sequentially, commit after each major milestone, and test thoroughly before considering the MVP complete.