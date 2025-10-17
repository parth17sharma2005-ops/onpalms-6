<?php
/**
 * PALMS Enhanced Chatbot - Final Production Version
 * Features: Conversational AI, Inline Forms, Business Email Validation
 * API: https://onpalms-6.onrender.com
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

if ( ! function_exists( 'elementor_theme_do_location' ) || ! elementor_theme_do_location( 'footer' ) ) {
	if ( hello_elementor_display_header_footer() ) {
		if ( did_action( 'elementor/loaded' ) && hello_header_footer_experiment_active() ) {
			get_template_part( 'template-parts/dynamic-footer' );
		} else {
			get_template_part( 'template-parts/footer' );
		}
	}
}
?>

<?php wp_footer(); ?>
<!-- PALMS Enhanced Chatbot - Production Ready -->
<?php if (!wp_is_mobile() || true) { // Show on all devices ?>

<style>
/* PALMS Enhanced Chatbot - Production CSS */
#palms-enhanced-chatbot * {
    box-sizing: border-box !important;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

/* Demo Form Styles */
.palms-demo-form {
    background: white !important;
    padding: 16px !important;
    border-radius: 8px !important;
    margin: 8px 0 !important;
    border: 1px solid #E1E4E8 !important;
}

.palms-demo-form input {
    width: 100% !important;
    padding: 8px 12px !important;
    margin: 4px 0 12px !important;
    border: 1px solid #E1E4E8 !important;
    border-radius: 4px !important;
    font-size: 14px !important;
}

.palms-demo-form button {
    background: #2F5D50 !important;
    color: white !important;
    border: none !important;
    padding: 8px 16px !important;
    border-radius: 4px !important;
    cursor: pointer !important;
    font-size: 14px !important;
    width: 100% !important;
}

.palms-demo-form button:hover {
    background: #3A80BA !important;
}

#palms-enhanced-chatbot {
    position: fixed !important;
    bottom: 24px !important;
    right: 24px !important;
    z-index: 999999 !important;
    display: flex !important;
    flex-direction: column !important;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
}

/* Minimized state */
#palms-enhanced-chatbot.minimized {
    width: 64px !important;
    height: 64px !important;
    border-radius: 50% !important;
    background: #2F5D50 !important;
    cursor: pointer !important;
    align-items: center !important;
    justify-content: center !important;
}

#palms-enhanced-chatbot.minimized:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 8px 25px rgba(47, 93, 80, 0.3) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}

/* Header */
.palms-header {
    background: linear-gradient(135deg, #2F5D50 0%, #3A80BA 100%) !important;
    color: #fff !important;
    padding: 16px 20px !important;
    border-radius: 12px 12px 0 0 !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

.palms-minimize-btn {
    background: transparent !important;
    border: none !important;
    color: #fff !important;
    cursor: pointer !important;
    padding: 4px !important;
    border-radius: 4px !important;
    width: 24px !important;
    height: 24px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background 0.2s !important;
}

.palms-minimize-btn:hover {
    background: rgba(255,255,255,0.1) !important;
}

/* Chat icon */
.palms-chat-icon {
    cursor: pointer !important;
    display: none !important;
}

#palms-enhanced-chatbot.minimized .palms-chat-icon {
    display: flex !important;
}

#palms-enhanced-chatbot.minimized .palms-header {
    display: none !important;
}

/* Body */
.palms-body {
    flex: 1 !important;
    padding: 16px !important;
    overflow-y: auto !important;
    height: 400px !important;
    max-height: 400px !important;
    min-height: 400px !important;
    background: #FAFBFC !important;
}

/* Messages */
.palms-message {
    margin-bottom: 12px !important;
    padding: 12px 16px !important;
    border-radius: 18px !important;
    max-width: 85% !important;
    word-wrap: break-word !important;
    font-size: 0.95rem !important;
    line-height: 1.4 !important;
    display: inline-block !important;
    clear: both !important;
}

.palms-message.user {
    background: #F2F4F6 !important;
    color: #1E1E1E !important;
    float: right !important;
    border-bottom-right-radius: 6px !important;
}

.palms-message.bot {
    background: #2F5D50 !important;
    color: #fff !important;
    float: left !important;
    border-bottom-left-radius: 6px !important;
}

.palms-message.system {
    background: #E3F2FD !important;
    color: #1565C0 !important;
    float: left !important;
    border: 1px solid #BBDEFB !important;
    font-size: 0.9rem !important;
}

/* Inline Form Styles */
.palms-inline-form {
    background: #FFFFFF !important;
    border: 2px solid #E0E7FF !important;
    border-radius: 12px !important;
    padding: 16px !important;
    margin: 12px 0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    clear: both !important;
    width: 100% !important;
}

.palms-form-title {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #2F5D50 !important;
    margin-bottom: 12px !important;
    text-align: center !important;
}

.palms-form-row {
    margin-bottom: 12px !important;
}

.palms-form-input {
    width: 100% !important;
    padding: 10px 12px !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    background: #FFFFFF !important;
    color: #1F2937 !important;
    outline: none !important;
    transition: border-color 0.2s !important;
}

.palms-form-input:focus {
    border-color: #3A80BA !important;
    box-shadow: 0 0 0 3px rgba(58, 128, 186, 0.1) !important;
}

.palms-form-input::placeholder {
    color: #9CA3AF !important;
}

.palms-form-submit {
    width: 100% !important;
    padding: 12px !important;
    background: #3A80BA !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: background 0.2s !important;
}

.palms-form-submit:hover {
    background: #2F5D50 !important;
}

.palms-form-error {
    background: #FEF2F2 !important;
    color: #DC2626 !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    font-size: 0.85rem !important;
    margin-top: 8px !important;
    border-left: 4px solid #DC2626 !important;
}

/* Typing animation */
.palms-message.typing {
    background: #2F5D50 !important;
    color: #fff !important;
    float: left !important;
    padding: 16px !important;
}

.palms-typing-dots {
    display: flex !important;
    gap: 4px !important;
}

.palms-typing-dots span {
    width: 8px !important;
    height: 8px !important;
    background: #fff !important;
    border-radius: 50% !important;
    animation: palmsTyping 1.4s infinite ease-in-out !important;
}

.palms-typing-dots span:nth-child(1) { animation-delay: -0.32s !important; }
.palms-typing-dots span:nth-child(2) { animation-delay: -0.16s !important; }

@keyframes palmsTyping {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

/* Input form */
.palms-input-form {
    display: flex !important;
    flex-direction: column !important;
    padding: 16px 16px 8px 16px !important;
    background: #F2F4F6 !important;
    border-radius: 0 0 12px 12px !important;
}

.palms-input-row {
    display: flex !important;
    gap: 8px !important;
    align-items: center !important;
    margin-bottom: 12px !important;
}

.palms-input {
    flex: 1 !important;
    padding: 12px 16px !important;
    border: 1px solid #D9DEE2 !important;
    border-radius: 24px !important;
    font-size: 0.95rem !important;
    background: #fff !important;
    color: #1E1E1E !important;
    outline: none !important;
    font-family: inherit !important;
}

.palms-input:focus {
    border-color: #3A80BA !important;
    box-shadow: 0 0 0 3px rgba(58, 128, 186, 0.1) !important;
}

.palms-send-btn {
    background: #3A80BA !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    font-size: 1.5rem !important;
    transition: background 0.2s !important;
}

.palms-send-btn:hover {
    background: #2F5D50 !important;
}

/* Disclaimer */
.palms-disclaimer {
    margin: 0 !important;
    padding: 8px 12px !important;
    font-size: 0.8rem !important;
    color: #6E7B85 !important;
    text-align: center !important;
    line-height: 1.2 !important;
}

/* Hidden states */
.palms-hidden {
    display: none !important;
}

/* Responsive design */
@media (max-width: 1200px) {
    #palms-enhanced-chatbot:not(.minimized) {
        width: 420px !important;
        height: 600px !important;
    }
}

@media (max-width: 768px) {
    #palms-enhanced-chatbot:not(.minimized) {
        width: calc(100vw - 24px) !important;
        height: calc(100vh - 80px) !important;
        bottom: 12px !important;
        right: 12px !important;
    }
    
    .palms-body {
        height: calc(100vh - 180px) !important;
        max-height: calc(100vh - 180px) !important;
    }

    .palms-message {
        max-width: 90% !important;
        font-size: 0.9rem !important;
    }
}

@media (max-width: 480px) {
    #palms-enhanced-chatbot:not(.minimized) {
        width: calc(100vw - 16px) !important;
        height: calc(100vh - 60px) !important;
        bottom: 8px !important;
        right: 8px !important;
    }

    .palms-header {
        padding: 12px 16px !important;
        font-size: 1rem !important;
    }

    .palms-input {
        padding: 10px 14px !important;
        font-size: 0.9rem !important;
    }

    .palms-send-btn {
        width: 42px !important;
        height: 42px !important;
        font-size: 1.3rem !important;
    }
}
</style>

<div id="palms-enhanced-chatbot" class="minimized">
    <div class="palms-header">
        <span>PALMS Assistant</span>
        <button class="palms-minimize-btn" onclick="palmsMinimize()">
            <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;">
                <rect x="4" y="9" width="12" height="2" rx="1" fill="currentColor"/>
            </svg>
        </button>
    </div>
    
    <div class="palms-chat-icon" onclick="palmsMaximize()" style="width:64px;height:64px;background:white;border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:8px;box-sizing:border-box;border:3px solid #2F5D50;">
        <img src="https://smartwms.onpalms.com/wp-content/uploads/2025/09/palmslogo.png" alt="PALMS Logo" style="width:48px;height:48px;object-fit:contain;border-radius:4px;" />
    </div>
    
    <div class="palms-body palms-hidden"></div>
    
    <form class="palms-input-form palms-hidden" onsubmit="palmsSendMessage(event)">
        <div class="palms-input-row">
            <input type="text" class="palms-input" placeholder="Ask about PALMS™..." autocomplete="off" />
            <button type="submit" class="palms-send-btn">➤</button>
        </div>
        <div class="palms-disclaimer">Powered by PALMS™ AI Assistant</div>
    </form>
</div>

<script>
// PALMS Enhanced Chatbot JavaScript - Production Version
(function() {
    let minimized = true;
    let hasAutoOpened = false;
    let sessionId = null;
    
    const widget = document.getElementById('palms-enhanced-chatbot');
    const body = widget.querySelector('.palms-body');
    const form = widget.querySelector('.palms-input-form');
    const input = widget.querySelector('.palms-input');
    
    // Production API Configuration
    const API_URL = 'https://onpalms-6.onrender.com';
    
    // Generate session ID
    function generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    // Initialize session
    sessionId = generateSessionId();
    
    window.palmsMinimize = function() {
        minimized = true;
        
        widget.style.cssText = `
            position: fixed !important;
            bottom: 24px !important;
            right: 24px !important;
            width: 64px !important;
            height: 64px !important;
            border-radius: 50% !important;
            background: #2F5D50 !important;
            z-index: 999999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.16) !important;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
            transform: scale(1) !important;
        `;
        
        widget.classList.add('minimized');
        body.classList.add('palms-hidden');
        form.classList.add('palms-hidden');
    };
    
    window.palmsMaximize = function() {
        minimized = false;
        
        // Dynamic responsive sizing
        const screenWidth = window.innerWidth;
        let width, height, bottom, right;
        
        if (screenWidth <= 480) {
            width = 'calc(100vw - 16px)';
            height = 'calc(100vh - 60px)';
            bottom = '8px';
            right = '8px';
        } else if (screenWidth <= 768) {
            width = 'calc(100vw - 24px)';
            height = 'calc(100vh - 80px)';
            bottom = '12px';
            right = '12px';
        } else if (screenWidth <= 1200) {
            width = '420px';
            height = '600px';
            bottom = '24px';
            right = '24px';
        } else {
            width = '480px';
            height = '650px';
            bottom = '32px';
            right = '32px';
        }
        
        widget.style.cssText = `
            position: fixed !important;
            bottom: ${bottom} !important;
            right: ${right} !important;
            width: ${width} !important;
            height: ${height} !important;
            max-height: ${height} !important;
            min-height: ${height} !important;
            border-radius: 12px !important;
            background: #FAFBFC !important;
            z-index: 999999 !important;
            display: flex !important;
            flex-direction: column !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.16) !important;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
            transform: scale(1) !important;
        `;
        
        if (body) {
            let bodyHeight;
            if (screenWidth <= 480) {
                bodyHeight = 'calc(100vh - 160px)';
            } else if (screenWidth <= 768) {
                bodyHeight = 'calc(100vh - 180px)';
            } else {
                bodyHeight = '450px';
            }
            
            body.style.cssText = `
                flex: 1 !important;
                padding: 16px !important;
                overflow-y: auto !important;
                height: ${bodyHeight} !important;
                max-height: ${bodyHeight} !important;
                min-height: 300px !important;
                background: #FAFBFC !important;
            `;
        }
        
        widget.classList.remove('minimized');
        body.classList.remove('palms-hidden');
        form.classList.remove('palms-hidden');
        
        // Add welcome message if first time
        if (body.children.length === 0) {
            setTimeout(() => {
                palmsAddMessage("Welcome to PALMS™. I'm here to assist you with optimizing your warehouse operations.", false);
            }, 400);
        }
        
        // Focus input
        setTimeout(() => input.focus(), 500);
    };
    
    function palmsAddMessage(text, isUser = false, messageType = 'normal') {
        const msg = document.createElement('div');
        let className = 'palms-message ';
        
        if (messageType === 'system') {
            className += 'system';
        } else {
            className += isUser ? 'user' : 'bot';
        }
        
        msg.className = className;
        // Format messages with comprehensive markdown-like styling (matching backend)
        const formattedMessage = text
            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>') // **bold** to <b>
            .replace(/### (.*?):/g, '<h4 style="margin: 10px 0 5px 0; font-weight: bold; color: #2c5aa0;">$1:</h4>') // ### Header: to <h4>
            .replace(/^• (.*$)/gm, '<div style="margin: 5px 0; padding-left: 15px;">• $1</div>') // • bullet to div
            .replace(/^\- (.*$)/gm, '<div style="margin: 5px 0; padding-left: 15px;">• $1</div>') // - bullet to div
            .replace(/\n/g, '<br>'); // Line breaks
        
        msg.innerHTML = formattedMessage;
        body.appendChild(msg);
        
        // Add clearfix
        const clearfix = document.createElement('div');
        clearfix.style.clear = 'both';
        clearfix.style.height = '0';
        body.appendChild(clearfix);
        
        body.scrollTop = body.scrollHeight;
        return msg;
    }
    
    function palmsAddDemoForm() {
        const formContainer = document.createElement('div');
        formContainer.className = 'palms-inline-form';
        formContainer.innerHTML = `
            <div class="palms-form-title">Schedule Your Demo</div>
            <div class="palms-form-row">
                <input type="text" class="palms-form-input" name="name" placeholder="Full Name *" required />
            </div>
            <div class="palms-form-row">
                <input type="email" class="palms-form-input" name="email" placeholder="Business Email *" required />
            </div>
            <div class="palms-form-row">
                <input type="tel" class="palms-form-input" name="phone" placeholder="Phone Number (optional)" />
            </div>
            <button type="button" class="palms-form-submit" onclick="palmsSubmitDemo(this)">Schedule Demo</button>
            <div class="palms-form-error palms-hidden"></div>
        `;
        
        body.appendChild(formContainer);
        body.scrollTop = body.scrollHeight;
        
        // Focus first input
        setTimeout(() => {
            const nameInput = formContainer.querySelector('input[name="name"]');
            if (nameInput) nameInput.focus();
        }, 300);
        
        return formContainer;
    }

    function palmsAddInlineForm() {
        const formContainer = document.createElement('div');
        formContainer.className = 'palms-inline-form';
        formContainer.innerHTML = `
            <div class="palms-form-title">To proceed with your request, we require the following information</div>
            <div class="palms-form-row">
                <input type="text" class="palms-form-input" name="name" placeholder="Full Name" required />
            </div>
            <div class="palms-form-row">
                <input type="email" class="palms-form-input" name="email" placeholder="Your business email" required />
            </div>
            <button type="button" class="palms-form-submit" onclick="palmsSubmitInfo(this)">Continue</button>
            <div class="palms-form-error palms-hidden"></div>
        `;
        
        body.appendChild(formContainer);
        body.scrollTop = body.scrollHeight;
        
        // Focus first input
        setTimeout(() => {
            const nameInput = formContainer.querySelector('input[name="name"]');
            if (nameInput) nameInput.focus();
        }, 300);
        
        return formContainer;
    }
    
    function palmsAddTyping() {
        const msg = document.createElement('div');
        msg.className = 'palms-message typing';
        msg.innerHTML = '<span class="palms-typing-dots"><span></span><span></span><span></span></span>';
        body.appendChild(msg);
        body.scrollTop = body.scrollHeight;
        return msg;
    }
    
    function palmsRemoveTyping() {
        const typing = body.querySelector('.palms-message.typing');
        if (typing) typing.remove();
    }
    
    window.palmsSubmitInfo = async function(button) {
        const form = button.closest('.palms-inline-form');
        const nameInput = form.querySelector('input[name="name"]');
        const emailInput = form.querySelector('input[name="email"]');
        const errorDiv = form.querySelector('.palms-form-error');
        
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        
        // Hide previous errors
        errorDiv.classList.add('palms-hidden');
        
        // Basic validation
        if (!name || !email) {
            errorDiv.textContent = 'Please fill in both fields.';
            errorDiv.classList.remove('palms-hidden');
            return;
        }
        
        if (!email.includes('@') || !email.includes('.')) {
            errorDiv.textContent = 'Please enter a valid email address.';
            errorDiv.classList.remove('palms-hidden');
            return;
        }
        
        // Disable form during submission
        button.disabled = true;
        button.textContent = 'Submitting...';
        nameInput.disabled = true;
        emailInput.disabled = true;
        
        try {
            const response = await fetch(`${API_URL}/submit_info`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-Session-Id': sessionId,
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include',
                body: JSON.stringify({ name, email })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Remove the form and show success message
                form.remove();
                palmsAddMessage(data.message, false, 'system');
                // Refocus main input
                setTimeout(() => input.focus(), 500);
            } else {
                // Show error and keep form
                errorDiv.textContent = data.message;
                errorDiv.classList.remove('palms-hidden');
                button.disabled = false;
                button.textContent = 'Continue';
                nameInput.disabled = false;
                emailInput.disabled = false;
                
                if (!data.show_form_again) {
                    setTimeout(() => form.remove(), 2000);
                }
            }
        } catch (err) {
            console.error('Info submission error details:', {
                error: err,
                message: err.message,
                stack: err.stack,
                apiUrl: API_URL,
                sessionId: sessionId
            });
            errorDiv.textContent = `Connection error: ${err.message || 'Unknown error'}`;
            errorDiv.classList.remove('palms-hidden');
            button.disabled = false;
            button.textContent = 'Continue';
            nameInput.disabled = false;
            emailInput.disabled = false;
        }
    };
    
    window.palmsSendMessage = async function(event) {
        event.preventDefault();
        
        const message = input.value.trim();
        if (!message) return;
        
        palmsAddMessage(message, true);
        input.value = '';
        
        const typing = palmsAddTyping();
        
        try {
            console.log('Attempting to connect to API...', {
                url: `${API_URL}/chat`,
                sessionId: sessionId,
                message: message,
                timestamp: new Date().toISOString()
            });
            
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include',
                body: JSON.stringify({ 
                    message: message,
                    session_id: sessionId 
                })
            });
            
            console.log('Response received:', {
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries()),
                ok: response.ok
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('Response data:', data);
            palmsRemoveTyping();
            
            if (data.error) {
                palmsAddMessage(data.error, false);
                return;
            }
            
            const botText = data.message || "Sorry, I couldn't process your request.";
            palmsAddMessage(botText, false);
            
            // Show demo form if requested (matching backend trigger)
            if (data.show_demo_form) {
                setTimeout(() => {
                    palmsAddDemoForm();
                }, 800);
            }
            
            // Show inline form if requested
            if (data.show_info_form) {
                setTimeout(() => {
                    palmsAddInlineForm();
                }, 800);
            }
            
        } catch (err) {
            console.error('Chat error details:', {
                error: err,
                message: err.message,
                stack: err.stack,
                apiUrl: API_URL,
                sessionId: sessionId
            });
            palmsRemoveTyping();
            palmsAddMessage(`Connection error: ${err.message || 'Unknown error'}`, false);
        }
        
        // Refocus input
        setTimeout(() => input.focus(), 100);
    };
    
    // Demo form submission handler  
    window.palmsSubmitDemo = async function(button) {
        const form = button.closest('.palms-inline-form');
        const nameInput = form.querySelector('input[name="name"]');
        const emailInput = form.querySelector('input[name="email"]');
        const phoneInput = form.querySelector('input[name="phone"]');
        const errorDiv = form.querySelector('.palms-form-error');
        
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const phone = phoneInput.value.trim();
        
        // Hide previous errors
        errorDiv.classList.add('palms-hidden');
        
        // Basic validation
        if (!name || !email) {
            errorDiv.textContent = 'Please fill in all mandatory fields (Name and Business Email).';
            errorDiv.classList.remove('palms-hidden');
            return;
        }
        
        // Disable form during submission
        button.disabled = true;
        button.textContent = 'Submitting...';
        nameInput.disabled = true;
        emailInput.disabled = true;
        phoneInput.disabled = true;
        
        try {
            // Submit to your backend API
            const response = await fetch(`${API_URL}/submit_demo`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                credentials: 'include',
                body: JSON.stringify({ 
                    name: name,
                    email: email,
                    phone: phone,
                    session_id: sessionId
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Also submit to Google Sheets
                await submitToGoogleSheets(name, email, phone);
                
                // Remove the form and show success message
                form.remove();
                palmsAddMessage(data.message, false, 'system');
            } else {
                // Show error and keep form
                errorDiv.textContent = data.message;
                errorDiv.classList.remove('palms-hidden');
                button.disabled = false;
                button.textContent = 'Schedule Demo';
                nameInput.disabled = false;
                emailInput.disabled = false;
                phoneInput.disabled = false;
            }
        } catch (err) {
            console.error('Demo submission error:', err);
            errorDiv.textContent = `Connection error: ${err.message || 'Unknown error'}`;
            errorDiv.classList.remove('palms-hidden');
            button.disabled = false;
            button.textContent = 'Schedule Demo';
            nameInput.disabled = false;
            emailInput.disabled = false;
            phoneInput.disabled = false;
        }
    };
    
    // Google Sheets integration function
    async function submitToGoogleSheets(name, email, phone) {
        // Replace with your Google Apps Script Web App URL
        const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwJiB_aMzjZyBywk63UW4UwNajFHqOiFlSBJY8A2M0RxjEzvKeLKFuzwFWeu9Bwt4Ml/exec';
        
        try {
            const currentDate = new Date().toLocaleString();
            
            await fetch(GOOGLE_SCRIPT_URL, {
                method: 'POST',
                mode: 'no-cors', // Required for Google Apps Script
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    timestamp: currentDate,
                    name: name,
                    email: email,
                    phone: phone || '',
                    source: 'Website Chatbot'
                })
            });
            
            console.log('Successfully submitted to Google Sheets');
        } catch (err) {
            console.error('Error submitting to Google Sheets:', err);
            // Don't show error to user since main submission succeeded
        }
    }
    
    // Handle enter key in input
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            palmsSendMessage(e);
        }
    });
    
    // Auto-resize on window resize
    window.addEventListener('resize', function() {
        if (!minimized) {
            palmsMaximize();
        }
    });
    
    // Initialize chatbot
    function initializeChatbot() {
        palmsMinimize();
        
        // Auto-open after 3 seconds on first visit
        setTimeout(() => {
            if (!hasAutoOpened && minimized) {
                hasAutoOpened = true;
                palmsMaximize();
                
                // Auto-minimize after 10 seconds if no interaction
                setTimeout(() => {
                    if (body.children.length <= 2) { // Only welcome message
                        palmsMinimize();
                    }
                }, 10000);
            }
        }, 3000);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeChatbot);
    } else {
        initializeChatbot();
    }
})();
</script>

<?php } ?>
</body>
</html>
