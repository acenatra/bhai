import Cocoa
import SwiftUI

// High-visibility premium AI Agent overlay
struct AgentView: View {
    var body: some View {
        VStack(spacing: 5) {
            Text("🤖🤖🤖🤖")
                .font(.system(size: 100))
            Text("BHAI ON DUTY")
                .font(.system(size: 18, weight: .bold, design: .rounded))
                .foregroundColor(Color(red: 0, green: 1, blue: 0.5)) // Vibrant green
        }
        .frame(width: 200, height: 200)
        .background(Color.black.opacity(0.85))
        .cornerRadius(30)
        .overlay(
            RoundedRectangle(cornerRadius: 30)
                .stroke(Color(red: 0, green: 1, blue: 0.5), lineWidth: 4)
        )
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!

    func applicationDidFinishLaunching(_ notification: Notification) {
        let screen = NSScreen.main!.frame
        let width: CGFloat = 200
        let height: CGFloat = 200
        
        // Position at bottom right
        let x = screen.width - width - 50
        let y: CGFloat = 100
        
        window = NSWindow(
            contentRect: NSRect(x: x, y: y, width: width, height: height),
            styleMask: [.borderless],
            backing: .buffered, defer: false)
        
        window.isOpaque = false
        window.backgroundColor = .clear
        window.level = .floating
        window.hasShadow = true
        
        let contentView = NSHostingView(rootView: AgentView())
        window.contentView = contentView
        
        window.makeKeyAndOrderFront(nil)
        
        // Auto-close after 4 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 4.0) {
            NSApp.terminate(nil)
        }
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()
