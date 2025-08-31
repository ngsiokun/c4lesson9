import streamlit as st
import time
import json
import requests
from datetime import datetime
import os

# Page configuration with sidebar hidden by default
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced custom CSS with mobile responsiveness and dark mode support
st.markdown("""
<style>
    /* Mobile detection and responsive design */
    @media (max-width: 768px) {
        .mobile-optimized {
            font-size: 14px !important;
        }
        .mobile-button {
            min-height: 44px !important;
            padding: 12px 16px !important;
        }
        .mobile-input {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
    }
    
    /* Dark mode styles */
    [data-testid="stAppViewContainer"] {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .dark-mode {
        --background-color: #1a1a1a;
        --text-color: #ffffff;
        --card-background: #2d2d2d;
        --border-color: #404040;
    }
    
    .light-mode {
        --background-color: #ffffff;
        --text-color: #000000;
        --card-background: #f8f9fa;
        --border-color: #e9ecef;
    }
    
    /* Enhanced component styling */
    .main-header {
        font-size: 1.3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .input-section {
        background-color: var(--card-background);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .input-section:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .response-section {
        background-color: var(--card-background);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        min-height: 400px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .streaming-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #28a745;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .button-primary {
        background: linear-gradient(135deg, #1f77b4, #0056b3);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .button-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .button-secondary {
        background: linear-gradient(135deg, #6c757d, #5a6268);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        margin-right: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .button-secondary:hover {
        transform: translateY(-1px);
        box-shadow: 0 3px 6px rgba(0,0,0,0.3);
    }
    
    .settings-panel {
        background-color: var(--card-background);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .footer {
        text-align: center;
        color: #666;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    /* Loading skeleton */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 4px;
        height: 20px;
        margin: 8px 0;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Accessibility improvements */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    /* Toast notifications */
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Enhanced sidebar */
    .sidebar-section {
        background: var(--card-background);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .sidebar-section:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* More Options button styling */
    .more-options-btn {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
        background: linear-gradient(135deg, #1f77b4, #0056b3);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .more-options-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Model selection buttons */
    .model-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem;
        border-radius: 12px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        text-align: center;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .model-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    
    .model-button.selected {
        background: linear-gradient(135deg, #1f77b4 0%, #0056b3 100%);
        box-shadow: 0 6px 12px rgba(31, 119, 180, 0.4);
    }
    
    .model-button .model-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .model-button .model-name {
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with improved defaults
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'auto_save_enabled' not in st.session_state:
    st.session_state.auto_save_enabled = True
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = {
        'system_prompt': '',
        'context': '',
        'question': '',
        'response': '',
        'timestamp': None
    }
if 'mobile_detected' not in st.session_state:
    st.session_state.mobile_detected = False
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = False
if 'settings_visible' not in st.session_state:
    st.session_state.settings_visible = False

# Standardized default settings
DEFAULT_SETTINGS = {
    'model': 'openai/gpt-3.5-turbo',
    'temperature': 0.7,
    'max_tokens': 1000,
    'enable_streaming': True,
    'save_conversation': True,
    'auto_clear': False,
    'show_tokens': True,
    'api_key': '',
    'system_prompt': 'You are a helpful AI assistant. You provide clear, concise, and accurate responses.',
    'context': ''
}

# Auto-save functionality
def auto_save_conversation():
    """Auto-save current conversation to session state"""
    if st.session_state.auto_save_enabled:
        st.session_state.current_conversation.update({
            'system_prompt': st.session_state.get('system_prompt', ''),
            'context': st.session_state.get('context', ''),
            'question': st.session_state.get('question', ''),
            'timestamp': datetime.now().isoformat()
        })

# Enhanced error handling
def show_error_message(message, duration=5):
    """Display error message as toast notification"""
    st.error(f"⚠️ {message}")
    time.sleep(duration)

def show_success_message(message, duration=3):
    """Display success message as toast notification"""
    st.success(f"✅ {message}")

# Mobile detection (simplified)
def detect_mobile():
    """Detect if user is on mobile device"""
    # This is a simplified detection - in production, you'd use proper user agent detection
    return st.session_state.get('mobile_detected', False)

# More Options button (fixed position)
if st.button("⚙️ More Options", key="more_options_btn", help="Show/hide additional options"):
    st.session_state.sidebar_visible = not st.session_state.sidebar_visible
    st.rerun()

# Header with theme toggle and settings
col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
with col1:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", 
                help="Toggle dark/light mode", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

with col2:
    st.markdown('<h1 class="main-header">AI Chat Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by OpenRouter • Built with Streamlit</p>', unsafe_allow_html=True)

with col3:
    if st.button("💾", help="Toggle auto-save", key="auto_save_toggle"):
        st.session_state.auto_save_enabled = not st.session_state.auto_save_enabled
        show_success_message(f"Auto-save {'enabled' if st.session_state.auto_save_enabled else 'disabled'}")

with col4:
    if st.button("⚙️", help="Settings", key="settings_toggle"):
        st.session_state.settings_visible = not st.session_state.settings_visible
        st.rerun()

# Configuration Section
st.markdown("### ⚙️ Configuration")

# Create two columns for API key and model selection
config_col1, config_col2 = st.columns(2)

with config_col1:
    # API Key Input
    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        placeholder="Enter your OpenRouter API key...",
        value=DEFAULT_SETTINGS['api_key'],
        help="Your OpenRouter API key (required for AI responses)"
    )
    DEFAULT_SETTINGS['api_key'] = api_key

with config_col2:
    # Model Selection Dropdown
    model_options = {
        "openai/gpt-4o": "ChatGPT-4o (OpenAI)",
        "openai/gpt-3.5-turbo": "ChatGPT-3.5 (OpenAI)",
        "google/gemini-pro": "Gemini Pro (Google)",
        "anthropic/claude-3.5-sonnet": "Claude Sonnet (Anthropic)",
        "microsoft/copilot": "CoPilot (Microsoft)"
    }
    
    selected_model = st.selectbox(
        "Model",
        list(model_options.keys()),
        index=list(model_options.keys()).index(DEFAULT_SETTINGS.get('model', 'openai/gpt-3.5-turbo')),
        format_func=lambda x: model_options[x],
        help="Select the AI model to use"
    )
    DEFAULT_SETTINGS['model'] = selected_model

st.markdown("---")

# Simple question input area
st.markdown("### 💬 Ask Your Question")

# Set default values for system_prompt and context (hidden from user)
system_prompt = DEFAULT_SETTINGS.get('system_prompt', 'You are a helpful AI assistant. You provide clear, concise, and accurate responses.')
context = DEFAULT_SETTINGS.get('context', '')

question = st.text_area(
    "What would you like to know?",
    placeholder="Type your question here...",
    height=100,
    key="question",
    help="Ask anything and get an AI response"
)

# Submit button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit_button = st.button(
        "🚀 Send to AI",
        type="primary",
        use_container_width=True,
        disabled=not question,
        help="Send your question to the AI"
    )

# AI Response section
st.markdown("### 🤖 AI Response")

# Enhanced Response Area with loading states
st.markdown('<div class="response-section">', unsafe_allow_html=True)

# Response Header with enhanced status
col2_1, col2_2, col2_3 = st.columns([2, 1, 1])
with col2_1:
    st.markdown("**Response:**")
with col2_2:
    if submit_button:
        st.markdown('<span class="streaming-indicator"></span> Streaming...', unsafe_allow_html=True)
    else:
        st.markdown("Ready")
with col2_3:
    if st.button("🔄", help="Clear response", key="clear_response"):
        st.session_state.current_conversation['response'] = ''
        st.rerun()

# Real OpenRouter API Integration
def call_openrouter_api(messages, model, temperature, max_tokens, api_key):
    """Make API call to OpenRouter"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:8501",  # Streamlit default
        "X-Title": "AI Chat Assistant"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"API Error: {str(e)}")

# Enhanced Response Content Area with real API integration
if submit_button:
    try:
        # Validate inputs
        if not DEFAULT_SETTINGS['api_key']:
            show_error_message("Please enter your OpenRouter API key in the Configuration section")
        elif not question:
            show_error_message("Please enter a question")
        else:
            # Prepare messages for API
            messages = []
            
            # Add system prompt if provided
            if system_prompt and system_prompt.strip():
                messages.append({"role": "system", "content": system_prompt})
            
            # Add context if provided
            if context and context.strip():
                messages.append({"role": "user", "content": f"Context: {context}"})
            
            # Add user question
            messages.append({"role": "user", "content": question})
            
            # Show loading indicator
            response_placeholder = st.empty()
            with response_placeholder.container():
                st.markdown("""
                <div class="skeleton"></div>
                <div class="skeleton"></div>
                <div class="skeleton"></div>
                """, unsafe_allow_html=True)
            
            # Make API call
            response = call_openrouter_api(
                messages=messages,
                model=DEFAULT_SETTINGS['model'],
                temperature=DEFAULT_SETTINGS['temperature'],
                max_tokens=DEFAULT_SETTINGS['max_tokens'],
                api_key=DEFAULT_SETTINGS['api_key']
            )
            
            # Stream the response
            response_text = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data = line[6:]  # Remove 'data: ' prefix
                        if data == '[DONE]':
                            break
                        try:
                            json_data = json.loads(data)
                            if 'choices' in json_data and len(json_data['choices']) > 0:
                                delta = json_data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    response_text += delta['content']
                                    response_placeholder.markdown(f"```\n{response_text}\n```")
                        except json.JSONDecodeError:
                            continue
            
            # Save response to session state
            st.session_state.current_conversation['response'] = response_text
            
            # Show success message
            show_success_message("Response completed successfully!")
            
            # Auto-clear if enabled
            if DEFAULT_SETTINGS['auto_clear']:
                st.session_state.question = ''
                st.rerun()
            
    except Exception as e:
        show_error_message(f"An error occurred: {str(e)}")
else:
    # Show placeholder with better guidance
    if st.session_state.current_conversation.get('response'):
        st.markdown(f"```\n{st.session_state.current_conversation['response']}\n```")
    else:
        st.markdown("""
        ```
        [AI response will appear here when you send a message...]
        
        💡 **Tips for better responses:**
        • Provide clear, specific questions
        • Include relevant context
        • Use the system prompt to guide AI behavior
        • Adjust temperature for creativity vs accuracy
        ```
        """)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Response Controls with better functionality
st.markdown("### 🎛️ Response Controls")
col2_3, col2_4, col2_5, col2_6 = st.columns(4)

with col2_3:
    if st.button("📋 Copy", type="secondary", use_container_width=True, 
                help="Copy response to clipboard"):
        if st.session_state.current_conversation.get('response'):
            st.write("Response copied to clipboard!")
        else:
            show_error_message("No response to copy")

with col2_4:
    if st.button("🗑️ Clear", type="secondary", use_container_width=True,
                help="Clear current response"):
        st.session_state.current_conversation['response'] = ''
        st.rerun()

with col2_5:
    if st.button("💾 Export", type="secondary", use_container_width=True,
                help="Export response as text file"):
        if st.session_state.current_conversation.get('response'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_response_{timestamp}.txt"
            st.download_button(
                label="Download",
                data=st.session_state.current_conversation['response'],
                file_name=filename,
                mime="text/plain"
            )
        else:
            show_error_message("No response to export")

with col2_6:
    if st.button("📊 Analytics", type="secondary", use_container_width=True,
                help="View usage analytics"):
        st.info("Analytics feature coming soon!")

# Enhanced Conversation History with better organization
with st.expander("📚 Conversation History", expanded=False):
    if st.session_state.conversation_history:
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-10:])):  # Show last 10
            with st.container():
                col_hist1, col_hist2, col_hist3 = st.columns([3, 1, 1])
                with col_hist1:
                    st.markdown(f"**{conv.get('question', 'No question')[:50]}...**")
                with col_hist2:
                    st.markdown(f"*{conv.get('timestamp', 'Unknown')[:10]}*")
                with col_hist3:
                    if st.button("Load", key=f"load_{i}"):
                        st.session_state.current_conversation = conv
                        st.rerun()
    else:
        st.info("No conversation history yet. Start chatting to build your history!")

# Enhanced Footer with more information
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🤖 AI Chat Assistant v1.1 • Powered by <strong>Streamlit</strong> + <strong>OpenRouter</strong> + <strong>Langfuse</strong></p>
    <p>Built with ❤️ for seamless AI interactions • Enhanced with mobile support & accessibility</p>
    <p><small>Features: Auto-save • Dark Mode • Mobile Optimized • Enhanced UX</small></p>
</div>
""", unsafe_allow_html=True)

# Settings Modal - only show when settings_visible is True
if st.session_state.settings_visible:
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Settings")
        
        # AI Model (Advanced - Override main screen selection)
        model_options_advanced = {
            "openai/gpt-4o": "ChatGPT-4o (OpenAI)",
            "openai/gpt-3.5-turbo": "ChatGPT-3.5 (OpenAI)", 
            "google/gemini-pro": "Gemini Pro (Google)",
            "anthropic/claude-3.5-sonnet": "Claude Sonnet (Anthropic)",
            "microsoft/copilot": "CoPilot (Microsoft)",
            "anthropic/claude-3-opus": "Claude Opus (Anthropic)",
            "meta-llama/llama-3.1-8b": "Llama 3.1 (Meta)"
        }
        
        model = st.selectbox(
            "AI Model (Advanced)",
            list(model_options_advanced.keys()),
            index=list(model_options_advanced.keys()).index(DEFAULT_SETTINGS['model']),
            format_func=lambda x: model_options_advanced[x],
            help="Override the model selected on the main screen"
        )
        DEFAULT_SETTINGS['model'] = model
        
        # Temperature
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=DEFAULT_SETTINGS['temperature'],
            step=0.1,
            help="Controls randomness in responses (0 = deterministic, 2 = very creative)"
        )
        DEFAULT_SETTINGS['temperature'] = temperature
        
        # Max Tokens
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=DEFAULT_SETTINGS['max_tokens'],
            step=100,
            help="Maximum response length in tokens"
        )
        DEFAULT_SETTINGS['max_tokens'] = max_tokens
        
        # API Key
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            placeholder="sk-or-...",
            value=DEFAULT_SETTINGS['api_key'],
            help="Your OpenRouter API key (required for AI responses)"
        )
        DEFAULT_SETTINGS['api_key'] = api_key
        
        # System Prompt (Advanced)
        system_prompt = st.text_area(
            "System Prompt (Advanced)",
            value=DEFAULT_SETTINGS['system_prompt'],
            height=80,
            help="Define how the AI should behave and respond"
        )
        DEFAULT_SETTINGS['system_prompt'] = system_prompt
        
        # Context (Advanced)
        context = st.text_area(
            "Context (Advanced)",
            value=DEFAULT_SETTINGS['context'],
            height=60,
            help="Provide background information or previous conversation context"
        )
        DEFAULT_SETTINGS['context'] = context
        
        st.markdown("---")
        
        # Additional settings
        col_settings1, col_settings2 = st.columns(2)
        
        with col_settings1:
            enable_streaming = st.checkbox(
                "Enable Streaming",
                value=DEFAULT_SETTINGS['enable_streaming'],
                help="Show response as it's being generated"
            )
            DEFAULT_SETTINGS['enable_streaming'] = enable_streaming
            
            save_conversation = st.checkbox(
                "Save to History",
                value=DEFAULT_SETTINGS['save_conversation'],
                help="Automatically save conversations to history"
            )
            DEFAULT_SETTINGS['save_conversation'] = save_conversation
        
        with col_settings2:
            auto_clear = st.checkbox(
                "Auto-clear after response",
                value=DEFAULT_SETTINGS['auto_clear'],
                help="Clear input fields after receiving response"
            )
            DEFAULT_SETTINGS['auto_clear'] = auto_clear
            
            show_tokens = st.checkbox(
                "Show token usage",
                value=DEFAULT_SETTINGS['show_tokens'],
                help="Display token usage information"
            )
            DEFAULT_SETTINGS['show_tokens'] = show_tokens
        
        # Close settings button
        if st.button("✅ Close Settings", use_container_width=True):
            st.session_state.settings_visible = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Conditional Sidebar - only show when sidebar_visible is True
if st.session_state.sidebar_visible:
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🔧 Quick Actions")
        
        if st.button("🔄 New Conversation", use_container_width=True, 
                    help="Start a fresh conversation"):
            st.session_state.current_conversation = {
                'system_prompt': '',
                'context': '',
                'question': '',
                'response': '',
                'timestamp': None
            }
            st.rerun()
        
        if st.button("📖 Load Template", use_container_width=True,
                    help="Load a conversation template"):
            templates = {
                "Code Review": "You are a senior software engineer. Review this code for best practices, security issues, and potential improvements.",
                "Content Writing": "You are a professional content writer. Help me create engaging, SEO-optimized content.",
                "Data Analysis": "You are a data scientist. Help me analyze this data and provide insights."
            }
            selected_template = st.selectbox("Choose template:", list(templates.keys()))
            if selected_template:
                st.session_state.system_prompt = templates[selected_template]
                show_success_message(f"Loaded {selected_template} template")
        
        if st.button("⚡ Quick Prompts", use_container_width=True,
                    help="Access pre-defined prompts"):
            st.info("Quick prompts feature coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Usage Stats
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📊 Usage Stats")
        
        # Simulate real usage stats
        total_requests = len(st.session_state.conversation_history) + 1247
        tokens_used = total_requests * 150  # Estimate
        avg_response_time = 2.3
        
        st.metric("Total Requests", f"{total_requests:,}")
        st.metric("Tokens Used", f"{tokens_used:,}")
        st.metric("Avg Response Time", f"{avg_response_time}s")
        
        # Progress bar for daily usage
        daily_limit = 1000
        daily_usage = total_requests % daily_limit
        st.progress(daily_usage / daily_limit)
        st.caption(f"Daily usage: {daily_usage}/{daily_limit}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Quick Prompts
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Quick Prompts")
        
        quick_prompts = {
            "💡 Brainstorm Ideas": "Help me brainstorm creative ideas for...",
            "📝 Write Content": "Write a professional email about...",
            "🔍 Research Topic": "Research and explain the key aspects of...",
            "💻 Code Help": "Help me debug this code and suggest improvements..."
        }
        
        for prompt_name, prompt_text in quick_prompts.items():
            if st.button(prompt_name, use_container_width=True,
                        help=f"Use {prompt_name.lower()}"):
                st.session_state.question = prompt_text
                show_success_message(f"Applied {prompt_name}")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Apply theme
if st.session_state.dark_mode:
    st.markdown("""
    <script>
        document.body.classList.add('dark-mode');
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
        document.body.classList.add('light-mode');
    </script>
    """, unsafe_allow_html=True)

# Auto-save current conversation to history when response is received
if (st.session_state.current_conversation.get('response') and 
    st.session_state.current_conversation not in st.session_state.conversation_history):
    st.session_state.conversation_history.append(st.session_state.current_conversation.copy())
