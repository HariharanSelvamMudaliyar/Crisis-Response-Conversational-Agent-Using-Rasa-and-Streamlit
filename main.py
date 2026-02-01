import streamlit as st
import requests
from datetime import datetime
import json

# ======================
# CONFIGURATION & SETUP
# ======================

# Page configuration
st.set_page_config(
    page_title="🚨 Crisis Response Assistant",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language configuration
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "icon": "🇺🇸"},
    "es": {"name": "Español", "icon": "🇪🇸"},
    "fr": {"name": "Français", "icon": "🇫🇷"},
    "ar": {"name": "العربية", "icon": "🇸🇦"},
    "zh": {"name": "中文", "icon": "🇨🇳"},
    "hi": {"name": "हिन्दी", "icon": "🇮🇳"},
    "bn": {"name": "বাংলা", "icon": "🇧🇩"},
    "ur": {"name": "اردو", "icon": "🇵🇰"},
}

# Translation dictionaries (in a real app, use proper translation service like Google Translate API)
TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to the Crisis Response Assistant",
        "emergency_description": "Please describe your emergency or use the quick action buttons below.",
        "set_location": "Set Your Location",
        "enter_address": "Enter address or city:",
        "save_location": "Save Location",
        "use_gps": "Use GPS",
        "emergency_contacts": "Emergency Contacts",
        "emergency_checklist": "Emergency Checklist",
        "response_status": "Response Status",
        "clear_chat": "Clear Chat",
        "export_log": "Export Log",
        "quick_actions": "Quick Emergency Actions",
        "emergency_types": "Emergency Types",
        "other_emergencies": "Other Emergencies",
        "describe_emergency": "Describe Your Emergency",
        "type_details": "Type details here:",
        "send_message": "Send Message",
        "voice_input": "Voice",
        "system_status": "System Status",
        "connected": "Connected to emergency server",
        "simulated_mode": "Using simulated emergency responses",
        "critical_alert": "CRITICAL EMERGENCY ACTIVE",
        "call_911": "CALL 911 DIRECTLY IF SAFE TO DO SO",
        "footer_text": "24/7 Emergency Support • Always call 911 in life-threatening situations",
        "fire_emergency": "Fire Emergency",
        "flood_alert": "Flood Alert",
        "earthquake": "Earthquake",
        "medical_help": "Medical Help",
        "accident": "Accident",
        "find_shelters": "Find Shelters",
        "instructions": "Instructions",
        "human_help": "Human Help",
        "checklist_items": [
            "Stay calm and assess situation",
            "Move to safe location",
            "Check for injuries",
            "Gather essential supplies",
            "Listen to official alerts",
            "Contact family/friends",
            "Follow evacuation routes",
            "Secure important documents",
            "Charge mobile devices",
            "Have emergency kit ready"
        ]
    },
    "es": {
        "welcome": "Bienvenido al Asistente de Respuesta a Crisis",
        "emergency_description": "Por favor describa su emergencia o use los botones de acción rápida a continuación.",
        "set_location": "Establecer su ubicación",
        "enter_address": "Ingrese dirección o ciudad:",
        "save_location": "Guardar Ubicación",
        "use_gps": "Usar GPS",
        "emergency_contacts": "Contactos de Emergencia",
        "emergency_checklist": "Lista de Verificación de Emergencia",
        "response_status": "Estado de Respuesta",
        "clear_chat": "Limpiar Chat",
        "export_log": "Exportar Registro",
        "quick_actions": "Acciones Rápidas de Emergencia",
        "emergency_types": "Tipos de Emergencia",
        "other_emergencies": "Otras Emergencias",
        "describe_emergency": "Describa Su Emergencia",
        "type_details": "Escriba detalles aquí:",
        "send_message": "Enviar Mensaje",
        "voice_input": "Voz",
        "system_status": "Estado del Sistema",
        "connected": "Conectado al servidor de emergencia",
        "simulated_mode": "Usando respuestas de emergencia simuladas",
        "critical_alert": "EMERGENCIA CRÍTICA ACTIVA",
        "call_911": "LLAME AL 911 DIRECTAMENTE SI ES SEGURO HACERLO",
        "footer_text": "Soporte de Emergencia 24/7 • Siempre llame al 911 en situaciones que amenacen la vida",
        "fire_emergency": "Emergencia de Incendio",
        "flood_alert": "Alerta de Inundación",
        "earthquake": "Terremoto",
        "medical_help": "Ayuda Médica",
        "accident": "Accidente",
        "find_shelters": "Encontrar Refugios",
        "instructions": "Instrucciones",
        "human_help": "Ayuda Humana",
        "checklist_items": [
            "Mantén la calma y evalúa la situación",
            "Muévete a un lugar seguro",
            "Revisa si hay heridos",
            "Reúne suministros esenciales",
            "Escucha las alertas oficiales",
            "Contacta a familiares/amigos",
            "Sigue las rutas de evacuación",
            "Asegura documentos importantes",
            "Carga dispositivos móviles",
            "Ten el kit de emergencia listo"
        ]
    },
    "fr": {
        "welcome": "Bienvenue dans l'Assistant de Réponse aux Crises",
        "emergency_description": "Veuillez décrire votre urgence ou utiliser les boutons d'action rapide ci-dessous.",
        "set_location": "Définir Votre Localisation",
        "enter_address": "Entrez l'adresse ou la ville :",
        "save_location": "Enregistrer la Localisation",
        "use_gps": "Utiliser GPS",
        "emergency_contacts": "Contacts d'Urgence",
        "emergency_checklist": "Liste de Contrôle d'Urgence",
        "response_status": "Statut de Réponse",
        "clear_chat": "Effacer le Chat",
        "export_log": "Exporter le Journal",
        "quick_actions": "Actions d'Urgence Rapides",
        "emergency_types": "Types d'Urgence",
        "other_emergencies": "Autres Urgences",
        "describe_emergency": "Décrivez Votre Urgence",
        "type_details": "Tapez les détails ici :",
        "send_message": "Envoyer le Message",
        "voice_input": "Voix",
        "system_status": "État du Système",
        "connected": "Connecté au serveur d'urgence",
        "simulated_mode": "Utilisation des réponses d'urgence simulées",
        "critical_alert": "URGENCE CRITIQUE ACTIVE",
        "call_911": "APPELER DIRECTEMENT LE 911 SI C'EST SANS DANGER",
        "footer_text": "Support d'Urgence 24/7 • Appelez toujours le 911 dans les situations mettant la vie en danger",
        "fire_emergency": "Urgence Incendie",
        "flood_alert": "Alerte Inondation",
        "earthquake": "Tremblement de Terre",
        "medical_help": "Aide Médicale",
        "accident": "Accident",
        "find_shelters": "Trouver des Abris",
        "instructions": "Instructions",
        "human_help": "Aide Humaine",
        "checklist_items": [
            "Restez calme et évaluez la situation",
            "Déplacez-vous vers un endroit sûr",
            "Vérifiez les blessures",
            "Rassemblez les fournitures essentielles",
            "Écoutez les alertes officielles",
            "Contactez la famille/les amis",
            "Suivez les routes d'évacuation",
            "Sécurisez les documents importants",
            "Chargez les appareils mobiles",
            "Ayez la trousse d'urgence prête"
        ]
    }
}

# ======================
# CUSTOM CSS STYLING
# ======================

st.markdown("""
<style>
    /* Main Container */
    .main-header {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 25px 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Conversation Cards */
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 16px 20px;
        border-radius: 18px 18px 4px 18px;
        margin: 12px 0;
        border-left: 5px solid #2196f3;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
        position: relative;
        max-width: 85%;
        margin-left: auto;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
        padding: 16px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 12px 0;
        border-left: 5px solid #4caf50;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
        position: relative;
        max-width: 85%;
        margin-right: auto;
    }
    
    /* Status Cards */
    .status-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .status-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.12);
    }
    
    /* Language Selector */
    .language-selector {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Emergency Type Buttons */
    .fire-btn button { background: linear-gradient(135deg, #ff5722 0%, #d84315 100%); color: white; }
    .flood-btn button { background: linear-gradient(135deg, #2196f3 0%, #0d47a1 100%); color: white; }
    .earthquake-btn button { background: linear-gradient(135deg, #795548 0%, #4e342e 100%); color: white; }
    .medical-btn button { background: linear-gradient(135deg, #f44336 0%, #b71c1c 100%); color: white; }
    .accident-btn button { background: linear-gradient(135deg, #ff9800 0%, #ef6c00 100%); color: white; }
    .shelter-btn button { background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); color: white; }
    .instructions-btn button { background: linear-gradient(135deg, #9c27b0 0%, #6a1b9a 100%); color: white; }
    
    /* Form Submit Button */
    .form-submit-btn button {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .form-submit-btn button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 68, 68, 0.3);
    }
    
    /* Critical Alert Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .critical-alert {
        animation: pulse 1.5s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 20px;
            font-size: 1.2rem;
        }
        .user-message, .bot-message {
            max-width: 95%;
        }
    }
    
    /* Right-to-left support */
    .rtl-text {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# MAIN APPLICATION CLASS
# ======================

class CrisisChatbot:
    def __init__(self):
        self.rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"
        self.initialize_session()
    
    def initialize_session(self):
        """Initialize session variables"""
        if 'conversation' not in st.session_state:
            st.session_state.conversation = []
        if 'location' not in st.session_state:
            st.session_state.location = None
        if 'risk_level' not in st.session_state:
            st.session_state.risk_level = "UNKNOWN"
        if 'emergency_type' not in st.session_state:
            st.session_state.emergency_type = "Not specified"
        if 'input_key' not in st.session_state:
            st.session_state.input_key = 0
        if 'language' not in st.session_state:
            st.session_state.language = "en"
        if 'rtl_mode' not in st.session_state:
            st.session_state.rtl_mode = False
    
    def get_text(self, key):
        """Get translated text for current language"""
        lang = st.session_state.language
        if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
            return TRANSLATIONS[lang][key]
        return TRANSLATIONS["en"][key]  # Fallback to English
    
    def display_header(self):
        """Display modern header with status and language selector"""
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown("""
            <div class="main-header">
                <h1 style="margin: 0; font-size: 2.5rem;">🚨 Crisis Response Assistant</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 1.1rem;">
                    24/7 Emergency Support • Multilingual Assistance
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.markdown("#### 🌐 Language")
            current_lang = st.selectbox(
                "Select language",
                options=list(SUPPORTED_LANGUAGES.keys()),
                format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['icon']} {SUPPORTED_LANGUAGES[x]['name']}",
                key="language_selector",
                label_visibility="collapsed"
            )
            
            if current_lang != st.session_state.language:
                st.session_state.language = current_lang
                st.session_state.rtl_mode = current_lang in ['ar', 'ur']
                st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    def send_to_rasa(self, message):
        """Send message to Rasa with language context"""
        payload = {
            "sender": "user", 
            "message": message,
            "metadata": {"language": st.session_state.language}
        }
        
        try:
            response = requests.post(self.rasa_endpoint, json=payload, timeout=5)
            if response.status_code == 200:
                return response.json()
            return self.get_simulated_response(message)
        except:
            return self.get_simulated_response(message)
    
    def get_simulated_response(self, message):
        """Multilingual simulated responses"""
        lang = st.session_state.language
        message_lower = message.lower()
        
        # Update emergency type based on keywords in any language
        emergency_keywords = {
            'fire': ['fire', 'incendio', 'feu', 'حريق'],
            'flood': ['flood', 'inundación', 'inondation', 'فيضان'],
            'earthquake': ['earthquake', 'terremoto', 'tremblement', 'زلزال'],
            'medical': ['medical', 'médico', 'médical', 'طبي']
        }
        
        for emergency_type, keywords in emergency_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                st.session_state.emergency_type = emergency_type.capitalize()
                st.session_state.risk_level = "HIGH" if emergency_type != 'medical' else "CRITICAL"
                break
        
        # Return responses based on language
        if lang == "es":
            return [{"text": """
🚨 **EMERGENCIA DETECTADA** ⚡

**ACCIONES INMEDIATAS:**
1. **EVACÚE** - Salga inmediatamente
2. **MANTÉNGASE BAJO** - Gatee si hay humo
3. **VERIFIQUE PUERTAS** - Toque con el dorso de la mano
4. **USE ESCALERAS** - Nunca use ascensores
5. **LLAME AL 911** desde un lugar seguro

Servicios de emergencia han sido alertados.
            """}]
        elif lang == "fr":
            return [{"text": """
🚨 **URGENCE DÉTECTÉE** ⚡

**ACTIONS IMMÉDIATES:**
1. **ÉVACUEZ** - Partez immédiatement
2. **RESTEZ BAS** - Rampez s'il y a de la fumée
3. **VÉRIFIEZ LES PORTES** - Touchez avec le dos de la main
4. **UTILISEZ LES ESCALIERS** - N'utilisez jamais les ascenseurs
5. **APPELEZ LE 911** depuis un endroit sûr

Les services d'urgence ont été alertés.
            """}]
        else:
            return [{"text": """
🚨 **EMERGENCY DETECTED** ⚡

**IMMEDIATE ACTIONS:**
1. **EVACUATE** - Leave immediately
2. **STAY LOW** - Crawl if there's smoke
3. **CHECK DOORS** - Feel with back of hand
4. **USE STAIRS** - Never use elevators
5. **CALL 911** from a safe location

Emergency services have been alerted.
            """}]
    def display_conversation(self):
        """Display conversation with RTL support"""
        st.markdown(
            f'<div class="status-card"><h3>💬 Conversation</h3></div>',
            unsafe_allow_html=True
    )

        if not st.session_state.conversation:
            welcome_text = self.get_text("welcome")
            description = self.get_text("emergency_description")

            st.markdown(f"""
            <div class="bot-message">
                <strong>🤖 Crisis Assistant:</strong><br>
                {welcome_text}<br><br>
                <span style="color: #666; font-size: 0.9em;">
                    {description}
                </span>
                <div class="message-time">Start by typing or selecting an emergency type</div>
            </div>
            """, unsafe_allow_html=True)
            return

        for msg in st.session_state.conversation[-10:]:
            time = msg["time"]

            if msg["sender"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong> {msg["message"]}
                    <div class="message-time">{time}</div>
                </div>
                """, unsafe_allow_html=True)

            else:
                formatted_message = msg["message"].replace("\n", "<br>")

                st.markdown(f"""
                <div class="bot-message">
                    <strong>🤖 Assistant:</strong><br>
                    {formatted_message}
                    <div class="message-time">{time}</div>
                </div>
                """, unsafe_allow_html=True)
        
    
    def process_message(self, message):
        """Process and add message to conversation"""
        if message.strip():
            st.session_state.conversation.append({
                'sender': 'user', 
                'message': message, 
                'time': datetime.now().strftime("%H:%M:%S")
            })
            
            with st.spinner("🔄 Processing..."):
                responses = self.send_to_rasa(message)
            
            for response in responses:
                bot_message = response.get('text', '')
                if bot_message:
                    st.session_state.conversation.append({
                        'sender': 'bot', 
                        'message': bot_message, 
                        'time': datetime.now().strftime("%H:%M:%S")
                    })
    
    def quick_action_buttons(self):
        """Multilingual quick action buttons"""
        st.markdown(f'<div class="status-card"><h3>🚨 {self.get_text("quick_actions")}</h3></div>', unsafe_allow_html=True)
        
        st.markdown(f"#### 🔥 {self.get_text('emergency_types')}")
        col1, col2, col3, col4 = st.columns(4)
        
        # Emergency buttons with translations
        emergency_buttons = [
            ("fire-btn", "🔥", self.get_text("fire_emergency"), "fire emergency"),
            ("flood-btn", "🌊", self.get_text("flood_alert"), "flood emergency"),
            ("earthquake-btn", "🌋", self.get_text("earthquake"), "earthquake"),
            ("medical-btn", "🚑", self.get_text("medical_help"), "medical emergency"),
        ]
        
        for idx, (btn_class, icon, text, message) in enumerate(emergency_buttons):
            with [col1, col2, col3, col4][idx]:
                if st.button(f"{icon} {text}", use_container_width=True):
                    self.process_message(message)
                    st.experimental_rerun()
        
        st.markdown(f"#### ⚡ {self.get_text('other_emergencies')}")
        col5, col6, col7, col8 = st.columns(4)
        
        other_buttons = [
            ("accident-btn", "💥", self.get_text("accident"), "accident"),
            ("shelter-btn", "🏠", self.get_text("find_shelters"), "where are shelters"),
            ("instructions-btn", "📋", self.get_text("instructions"), "safety instructions"),
            ("", "👨‍🚒", self.get_text("human_help"), "human operator"),
        ]
        
        for idx, (btn_class, icon, text, message) in enumerate(other_buttons):
            with [col5, col6, col7, col8][idx]:
                if st.button(f"{icon} {text}", use_container_width=True):
                    self.process_message(message)
                    st.experimental_rerun()
    
    def sidebar_content(self):
        """Enhanced multilingual sidebar"""
        with st.sidebar:
            # Language info
            current_lang = SUPPORTED_LANGUAGES[st.session_state.language]
            st.markdown(f"""
            <div class="language-selector">
                <h4 style="margin: 0;">🌐 Current Language</h4>
                <p style="margin: 5px 0 0 0; font-size: 1.2em;">
                    {current_lang['icon']} <strong>{current_lang['name']}</strong>
                </p>
                <p style="margin: 2px 0 0 0; font-size: 0.9em; opacity: 0.9;">
                    Full multilingual support
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Location Section
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            st.markdown(f"### 📍 **{self.get_text('set_location')}**")
            
            location = st.text_input(
                self.get_text("enter_address"),
                value=st.session_state.location or "",
                placeholder="e.g., 123 Main St, City",
                key="location_input"
            )
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                if st.button(f"✅ {self.get_text('save_location')}", use_container_width=True):
                    if location:
                        st.session_state.location = location
                        self.process_message(f"My location is {location}")
                        st.success("📍 Location saved!")
                        st.experimental_rerun()
            with col_s2:
                if st.button(f"🗺️ {self.get_text('use_gps')}", use_container_width=True):
                    st.info("📍 GPS location simulated")
                    st.session_state.location = "Current GPS Location"
                    self.process_message("My location is from GPS")
                    st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Emergency Checklist
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            st.markdown(f"### ✅ **{self.get_text('emergency_checklist')}**")
            
            checklist_items = self.get_text("checklist_items")
            for idx, item in enumerate(checklist_items):
                key = f"check_{idx}_{st.session_state.language}"
                if key not in st.session_state:
                    st.session_state[key] = False
                st.checkbox(item, key=key)
            
            if st.button("📋 Print Checklist", use_container_width=True):
                st.info("Checklist saved")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Response Status
            st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
            st.markdown(f"### 📊 **{self.get_text('response_status')}**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Messages", len(st.session_state.conversation))
            with col2:
                st.metric("Language", current_lang['name'])
            
            if st.button(f"🔄 {self.get_text('clear_chat')}", use_container_width=True):
                st.session_state.conversation = []
                st.session_state.input_key += 1
                st.experimental_rerun()
                
            if st.button(f"📝 {self.get_text('export_log')}", use_container_width=True):
                st.info("Conversation exported")
            st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Main application loop"""
        self.display_header()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            self.display_conversation()
            
            st.markdown(f'<div class="status-card"><h3>💭 {self.get_text("describe_emergency")}</h3></div>', unsafe_allow_html=True)
            
            with st.form(key="emergency_form", clear_on_submit=True):
                placeholder = "Describe your emergency in detail..."
                if st.session_state.language == "es":
                    placeholder = "Describa su emergencia en detalle..."
                elif st.session_state.language == "fr":
                    placeholder = "Décrivez votre urgence en détail..."
                
                user_input = st.text_area(
                    self.get_text("type_details"),
                    height=120,
                    placeholder=placeholder,
                    key=f"input_{st.session_state.input_key}"
                )
                
                col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
                with col_btn1:
                    st.markdown('<div class="form-submit-btn">', unsafe_allow_html=True)
                    submitted = st.form_submit_button(f"📤 {self.get_text('send_message')}", use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
               
                with col_btn3:
                    if st.form_submit_button(f"🎤 {self.get_text('voice_input')}", use_container_width=True):
                        st.info("🎤 Voice input activated...")
                
                if submitted and user_input.strip():
                    self.process_message(user_input)
                    st.session_state.input_key += 1
                    st.experimental_rerun()
            
            st.markdown("---")
            self.quick_action_buttons()
            
            # Critical Alert
            if st.session_state.risk_level == "CRITICAL":
                st.markdown(f"""
                <div class="critical-alert" style="
                    background: linear-gradient(135deg, #ff4444 0%, #b71c1c 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 16px;
                    margin: 20px 0;
                    border: 3px solid rgba(255, 255, 255, 0.3);
                ">
                    <h3 style="margin: 0 0 15px 0;">🚨 {self.get_text('critical_alert')}</h3>
                    <p style="margin: 0 0 10px 0; font-size: 1.1em;">
                        <strong>Emergency services dispatched</strong>
                    </p>
                    <p style="margin: 0; font-size: 1.2em; font-weight: bold;">
                        🔊 <strong>{self.get_text('call_911')}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            self.sidebar_content()
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style="
            text-align: {'right' if st.session_state.rtl_mode else 'center'};
            color: #666;
            font-size: 0.9rem;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 12px;
            margin-top: 20px;
            direction: {'rtl' if st.session_state.rtl_mode else 'ltr'};
        ">
            <p style="margin: 5px 0;"><strong>🚨 Crisis Response Assistant v3.0</strong></p>
            <p style="margin: 5px 0; font-size: 0.8rem;">
                {self.get_text('footer_text')}
            </p>
            <p style="margin: 5px 0; font-size: 0.8rem; color: #999;">
                Supporting {len(SUPPORTED_LANGUAGES)} languages • This system supplements but does not replace professional emergency services
            </p>
        </div>
        """, unsafe_allow_html=True)

# ======================
# APPLICATION ENTRY POINT
# ======================

if __name__ == "__main__":
    # System connection check
    with st.spinner("🔍 Checking emergency systems..."):
        try:
            response = requests.get("http://localhost:5005", timeout=2)
            if response.status_code == 200:
                st.sidebar.success("✅ Connected to emergency server")
            else:
                st.sidebar.warning("⚠️ Using simulated responses")
        except:
            st.sidebar.info("""
            **System Status:** Simulated Mode
            
            Full features require:
            ```
            rasa run actions
            rasa run --enable-api
            ```
            """)
    
    # Initialize and run chatbot
    chatbot = CrisisChatbot()
    chatbot.run()
