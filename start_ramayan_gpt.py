#!/usr/bin/env python3
"""
Ramayan GPT Launcher
Starts the bilingual server and opens the web interface
"""

import subprocess
import webbrowser
import time
import os
import sys

def start_ramayan_gpt():
    """Start Ramayan GPT system"""
    
    print("🕉️ STARTING RAMAYAN GPT")
    print("=" * 50)
    
    # Check if server file exists
    if not os.path.exists("bilingual_ramayan_server.py"):
        print("❌ Error: bilingual_ramayan_server.py not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Check if UI file exists
    if not os.path.exists("ramayan_gpt_ui.html"):
        print("❌ Error: ramayan_gpt_ui.html not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    print("🚀 Starting Ramayan GPT server...")
    
    try:
        # Start the server in background
        server_process = subprocess.Popen([
            sys.executable, "bilingual_ramayan_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Check if server is running
        if server_process.poll() is None:
            print("✅ Server started successfully on port 8001")
            
            # Get the full path to the HTML file
            html_file = os.path.abspath("ramayan_gpt_ui.html")
            
            print("🌐 Opening web interface...")
            webbrowser.open(f"file://{html_file}")
            
            print("\n" + "=" * 50)
            print("🎉 RAMAYAN GPT IS READY!")
            print("=" * 50)
            print("📱 Web Interface: Opened in your browser")
            print("🖥️  Server: Running on http://localhost:8001")
            print("📚 Knowledge Base: Hindi + English Ramayana")
            print("🗣️  Languages: Hindi (हिंदी) + English")
            print("=" * 50)
            print("\n💡 You can now:")
            print("   • Ask questions about Ramayana stories")
            print("   • Learn about characters like Rama, Sita, Hanuman")
            print("   • Explore spiritual teachings and wisdom")
            print("   • Use voice input (click microphone)")
            print("   • Switch between Hindi and English")
            print("\n📝 Example questions:")
            print("   • Who were the sons of Dasharatha?")
            print("   • दशरथ के पुत्रों के नाम क्या थे?")
            print("   • Tell me about Hanuman")
            print("   • रावण ने सीता को कहाँ रखा था?")
            
            print(f"\n🔄 To stop: Press Ctrl+C")
            
            try:
                # Keep the server running
                server_process.wait()
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping Ramayan GPT...")
                server_process.terminate()
                print("✅ Server stopped. Thank you for using Ramayan GPT!")
                
        else:
            print("❌ Failed to start server")
            stdout, stderr = server_process.communicate()
            if stderr:
                print(f"Error: {stderr.decode()}")
                
    except Exception as e:
        print(f"❌ Error starting Ramayan GPT: {e}")
        print("\n💡 Troubleshooting:")
        print("   • Make sure Python is installed")
        print("   • Install required packages: pip install -r requirements.txt")
        print("   • Check if port 8001 is available")

if __name__ == "__main__":
    start_ramayan_gpt()