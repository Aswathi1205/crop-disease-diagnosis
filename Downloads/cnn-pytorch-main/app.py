"""
SOLID Principles Applied
1. Single Responsibility Principle (SRP) :
Easier to test each component independently
Can change storage mechanism without touching authentication logic
2. Open/Closed Principle (OCP) :
Open for extension (new loaders) but closed for modification
Can add YAML, environment variable, or database config loaders without modifying existing code
More flexible and extensible architecture
3. Dependency Inversion Principle (DIP) : Loose coupling between components
Easy to create mock implementations for testing
Can swap implementations without changing high-level code
4. Interface Segregation Principle (ISP) : Segregate interfaces into smaller, specific ones
Easy to implement only the methods needed for each component
Prevents unnecessary dependencies and complexity
5. Liskov Substitution Principle (LSP) : Subclasses must be substitutable for their base classes
Easy to swap implementations without changing high-level code
Prevents unexpected behavior and maintains type safety  
"""

import streamlit as st
import streamlit.components.v1 as components
import torch
import json
import bcrypt
import os
from PIL import Image
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
import io


from src.model import CropDiseaseClassifier
from src.transforms import ImageTransformer


from interfaces import IAuthenticator, IPredictor
from user_repository import UserRepository
from config_loader import ConfigLoader, JsonConfigLoader
from pdf_report_generator import PDFReportGenerator
from treatment_guide import get_treatment_guide



@dataclass
class User:
    """User account information"""
    username: str
    password_hash: str
    created_at: datetime
    last_login: datetime


@dataclass
class Session:
    """User session information"""
    session_id: str
    username: str
    created_at: datetime
    is_active: bool


@dataclass
class UploadedImage:
    """Uploaded image metadata"""
    filename: str
    image_data: Image.Image
    upload_timestamp: datetime
    file_size: int


@dataclass
class Prediction:
    """Single prediction result"""
    class_name: str
    confidence: float


@dataclass
class DiagnosisResult:
    """Complete diagnosis result"""
    disease_name: str
    confidence: float
    image_filename: str
    timestamp: datetime
    all_predictions: List[Prediction]




class AuthManager(IAuthenticator):
    """
    Manages user authentication and sessions.
    
    SOLID Principles Applied:
    - SRP: Delegates data persistence to UserRepository
    - DIP: Implements IAuthenticator interface
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Initialize AuthManager with dependency injection.
        
        Args:
            user_repository: Repository for user data operations
        """
        self.user_repository = user_repository
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user credentials.
        Property 1: Valid credentials grant access
        Property 2: Invalid credentials are rejected
        """
        if not username or not password:
            return False
        
        try:
            user_data = self.user_repository.get_user(username)
            
            if user_data is None:
                return False
            
            stored_hash = user_data['password_hash'].encode('utf-8')
            
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                # Update last login via repository
                self.user_repository.update_last_login(username)
                return True
            
            return False
        
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return False
    
    def create_session(self, username: str):
       
        import uuid
        session = Session(
            session_id=str(uuid.uuid4()),
            username=username,
            created_at=datetime.now(),
            is_active=True
        )
        
        st.session_state['authenticated'] = True
        st.session_state['username'] = username
        st.session_state['session'] = asdict(session)
    
    def logout(self):
      
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.session_state['session'] = None
        st.session_state['uploaded_image'] = None
        st.session_state['diagnosis_result'] = None
    
    def register(self, username: str, password: str, confirm_password: str) -> tuple[bool, str]:
        """
        Register a new user account.
        
        Args:
            username: Desired username
            password: User's password
            confirm_password: Password confirmation
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate inputs
        if not username or not password or not confirm_password:
            return False, "All fields are required"
        
        if password != confirm_password:
            return False, "Passwords do not match"
        
        # Delegate to repository
        return self.user_repository.create_user(username, password)



class InferenceEngine(IPredictor):

    
    def __init__(self, config_loader: ConfigLoader, 
                 model_config_path: str = "config/model_config.json",
                 class_names_path: str = "config/class_names.json"):
        
        # Get absolute path to config files based on script location
        base_dir = Path(__file__).parent
        model_config_path = str(base_dir / model_config_path)
        class_names_path = str(base_dir / class_names_path)
        
        self.config_loader = config_loader
        self.config = self._load_config(model_config_path)
        self.class_names = self._load_class_names(class_names_path)
        self.model = None
        self.transform = None
        self.device = torch.device(self.config.get('inference', {}).get('device', 'cpu'))
    
    def _load_config(self, config_path: str) -> dict:
        
        try:
            return self.config_loader.load(config_path)
        except Exception as e:
            st.error(f"❌ Error loading configuration: {str(e)}")
            return {}
    
    def _load_class_names(self, class_names_path: str) -> List[str]:
        try:
            data = self.config_loader.load(class_names_path)
            return data.get('classes', [])
        except Exception as e:
            st.error(f"Error loading class names: {str(e)}")
            return []
    
    def load_model(self) -> bool:
        
        try:
            model_path = self.config['model']['model_path']
            num_classes = self.config['model']['num_classes']
            
            if not Path(model_path).exists():
                st.error(f" Model file not found at: {model_path}")
                st.info("Please ensure the trained model file exists at the specified location.")
                return False
            
    
            self.model = CropDiseaseClassifier(num_classes=num_classes)
            
          
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            
            mean = self.config['preprocessing']['mean']
            std = self.config['preprocessing']['std']
            target_size = tuple(self.config['model']['input_size'])
            
            transformer = ImageTransformer(
                target_size=target_size,
                mean=mean,
                std=std
            )
            self.transform = transformer.transform
            
            return True
        
        except Exception as e:
            st.error(f" Error loading model: {str(e)}")
            st.info("Please check the model file and try again.")
            return False
    
    def predict(self, image: Image.Image) -> Optional[DiagnosisResult]:
      
        try:
            if self.model is None:
                if not self.load_model():
                    return None
            
            
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
          
            with torch.no_grad():
                output = self.model(image_tensor)
            
            probabilities = output[0].cpu().numpy()
            
            predicted_idx = probabilities.argmax()
            confidence = float(probabilities[predicted_idx])
            disease_name = self.class_names[predicted_idx]
            
            top_k = min(3, len(self.class_names))
            top_indices = probabilities.argsort()[-top_k:][::-1]
            
            all_predictions = [
                Prediction(
                    class_name=self.class_names[idx],
                    confidence=float(probabilities[idx])
                )
                for idx in top_indices
            ]
            
            return DiagnosisResult(
                disease_name=disease_name,
                confidence=confidence,
                image_filename=st.session_state.get('current_filename', 'unknown'),
                timestamp=datetime.now(),
                all_predictions=all_predictions
            )
        
        except Exception as e:
            st.error(f"Inference error: {str(e)}")
            st.info("Please try uploading a different image.")
            return None


def render_botpress_chatbot():
    """Render Botpress chatbot in the sidebar using simplified script approach"""
    botpress_html = """
    <style>
      .chatbot-wrapper {
        background: rgba(46, 125, 50, 0.1);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      }
      
      #webchat {
        background: transparent !important;
        border-radius: 8px;
        overflow: hidden;
      }
      
      #webchat * {
        background: transparent !important;
      }
      
      #webchat iframe {
        background: white !important;
        border-radius: 8px;
      }
      
      #webchat .bpWebchat {
        position: unset;
        width: 100%;
        height: 100%;
        max-height: 100%;
        max-width: 100%;
      }

      #webchat .bpFab {
        display: none;
      }
      
      /* Remove any container backgrounds */
      div[class*="bp-"] {
        background: transparent !important;
      }
    </style>

    <div class="chatbot-wrapper">
      <div id="webchat" style="width: 100%; height: 480px;"></div>
    </div>

    <script src="https://cdn.botpress.cloud/webchat/v3.5/inject.js" defer></script>
    <script src="https://files.bpcontent.cloud/2026/01/04/07/20260104073059-4L5UTD1M.js" defer></script>
    """
    components.html(botpress_html, height=550, scrolling=True)


def render_sidebar(auth_manager: IAuthenticator):

    with st.sidebar:
        st.title("🌾 Crop Disease Diagnosis")
        
        if st.session_state.get('authenticated', False):
            st.success(f"👤 Logged in as: **{st.session_state['username']}**")
            
            st.divider()
            
            # Botpress Chatbot Integration
            st.subheader("💬 AgriTech Assistant")
            render_botpress_chatbot()
            
            st.divider()
            
            st.subheader("Navigation")
            st.info("📤 Upload an image to get started")
            
            st.divider()
            
            st.subheader("About")
            st.write("AI-powered disease detection for rice and pulse crops")
            st.write("Supported diseases:")
            st.write("• Bacterial Leaf Blight")
            st.write("• Brown Spot")
            st.write("• Leaf Scald")
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                auth_manager.logout()
                st.rerun()


def render_login_page(auth_manager: IAuthenticator):
    
    st.title("🌾 Crop Disease Diagnosis System")
    
    st.markdown("""
    Welcome! Please login or create a new account to access the disease diagnosis system.
    """)
    
    # Create tabs for Login and Signup
    tab1, tab2 = st.tabs(["🔐 Login", "✍️ Sign Up"])
    
    # Login Tab
    with tab1:
        st.subheader("Login to Your Account")
        st.markdown("""
        **Demo Credentials:**
        - Username: `admin`
        - Password: `admin123`
        """)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if submit:
                if not username or not password:
                    st.error("⚠️ Please enter both username and password")
                elif auth_manager.authenticate(username, password):
                    auth_manager.create_session(username)
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password. Please try again.")
    
    # Signup Tab
    with tab2:
        st.subheader("Create a New Account")
        st.markdown("""
        Join us to start diagnosing crop diseases with AI!
        
        **Password Requirements:**
        - Minimum 6 characters
        """)
        
        with st.form("signup_form"):
            new_username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
            new_password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="signup_confirm")
            signup_submit = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
            
            if signup_submit:
                success, message = auth_manager.register(new_username, new_password, confirm_password)
                
                if success:
                    st.success(f"✅ {message}")
                    st.info("👉 Please switch to the Login tab to sign in with your new account.")
                else:
                    st.error(f"❌ {message}")


def render_upload_page(inference_engine: IPredictor):
 
    st.title("📤 Upload Crop Image for Diagnosis")
    
    st.markdown("""
    Upload an image of a crop leaf to diagnose potential diseases.
    
    **Supported formats:** JPEG, PNG, JPG
    """)
    
   
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the crop leaf"
    )
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            file_size = len(uploaded_file.getvalue())
            
            st.session_state['uploaded_image'] = UploadedImage(
                filename=uploaded_file.name,
                image_data=image,
                upload_timestamp=datetime.now(),
                file_size=file_size
            )
            st.session_state['current_filename'] = uploaded_file.name
            
            st.success(f"✅ Image uploaded successfully: {uploaded_file.name}")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📷 Image Preview")
                st.image(image, use_container_width=True)
                st.caption(f"Size: {file_size / 1024:.2f} KB")
            
            with col2:
                st.subheader("🔬 Analysis")
                
                if st.button("🚀 Analyze Image", use_container_width=True, type="primary"):
                    with st.spinner("Analyzing image..."):
                        result = inference_engine.predict(image)
                        
                        if result:
                            st.session_state['diagnosis_result'] = result
                            st.rerun()
        
        except Exception as e:
            st.error(f" Error processing image: {str(e)}")
            st.info("Please upload a valid image file (JPEG, PNG, JPG)")
    
    if st.session_state.get('diagnosis_result'):
        render_results_page(st.session_state['diagnosis_result'])


def render_results_page(result: DiagnosisResult):
 
    st.divider()
    st.header("🎯 Diagnosis Results")
    
    st.subheader(f"Detected Disease: **{result.disease_name.replace('_', ' ').title()}**")
    
    confidence_pct = result.confidence * 100
    
    if result.confidence < 0.6:
        st.warning(f"⚠️ Low confidence: {confidence_pct:.2f}%")
        st.info("The model is uncertain about this diagnosis. Please consider consulting an expert or uploading a clearer image.")
    else:
        st.success(f"✅ Confidence: {confidence_pct:.2f}%")
    

    st.progress(result.confidence)
    

    st.subheader("📊 Top Predictions")
    
    for i, pred in enumerate(result.all_predictions, 1):
        pred_pct = pred.confidence * 100
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{i}. {pred.class_name.replace('_', ' ').title()}")
        with col2:
            st.write(f"{pred_pct:.2f}%")
        st.progress(pred.confidence)
    
    # Metadata
    st.divider()
    st.caption(f"📅 Analysis Time: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption(f"📁 Image: {result.image_filename}")
    
    # Treatment Guide Section
    st.divider()
    treatment_guide = get_treatment_guide(result.disease_name)
    
    if treatment_guide:
        with st.expander("📚 **Treatment Guide**", expanded=True):
            st.markdown(f"### {treatment_guide.disease_name}")
            
            # Disease Overview
            st.markdown("#### 🔍 Disease Overview")
            st.write(treatment_guide.overview)
            
            # Prevention Tips
            st.markdown("#### 🛡️ Prevention Tips")
            for tip in treatment_guide.prevention_tips:
                st.markdown(f"• {tip}")
            
            # Treatment Guidance
            st.markdown("#### 💊 Practical Treatment Guidance")
            st.markdown(treatment_guide.treatment_guidance)
            
            # Important Advisory
            st.markdown("#### ⚠️ Important Advisory")
            st.warning(treatment_guide.advisory)
            
            # References
            st.markdown("#### 📖 References")
            for ref in treatment_guide.references:
                st.markdown(f"• {ref}")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Upload Another Image", use_container_width=True):
            st.session_state['uploaded_image'] = None
            st.session_state['diagnosis_result'] = None
            st.rerun()
    
    with col2:
        if st.button("💾 Download Results", use_container_width=True):
            # Text download option
            results_text = f"""
Crop Disease Diagnosis Results
===============================
Disease: {result.disease_name.replace('_', ' ').title()}
Confidence: {confidence_pct:.2f}%
Image: {result.image_filename}
Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

Top Predictions:
"""
            for i, pred in enumerate(result.all_predictions, 1):
                results_text += f"{i}. {pred.class_name.replace('_', ' ').title()}: {pred.confidence * 100:.2f}%\n"
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.download_button(
                    label="📄 Download as Text",
                    data=results_text,
                    file_name=f"diagnosis_{result.timestamp.strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_b:
                # PDF download option
                try:
                    pdf_generator = PDFReportGenerator()
                    uploaded_image = st.session_state.get('uploaded_image')
                    
                    if uploaded_image and uploaded_image.image_data:
                        pdf_bytes = pdf_generator.generate_report(result, uploaded_image.image_data)
                        
                        st.download_button(
                            label="📑 Download as PDF",
                            data=pdf_bytes,
                            file_name=f"diagnosis_report_{result.timestamp.strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.warning("Image not available for PDF generation")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")






def apply_custom_styling():
    """Apply custom CSS for enhanced visual design"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2e7d32 0%, #1b5e20 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Ensure chatbot iframe is visible in sidebar */
    [data-testid="stSidebar"] iframe {
        background-color: white !important;
        border-radius: 10px;
        border: none;
    }
    
    /* Make sure components.html content is visible */
    [data-testid="stSidebar"] [data-testid="stHtml"] {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Main content text visibility */
    .main * {
        color: #212121;
    }
    
    .main h1, .main h2, .main h3 {
        color: #2e7d32 !important;
    }
    
    .main p, .main span, .main div, .main label {
        color: #212121 !important;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(67, 160, 71, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(67, 160, 71, 0.4);
        background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
    }
    
    /* Primary Button Style */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.4);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%);
        box-shadow: 0 6px 25px rgba(76, 175, 80, 0.5);
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 12px 16px;
        font-size: 15px;
        transition: all 0.3s ease;
        background-color: white;
        color: #212121 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4caf50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        color: #212121 !important;
    }
    
    /* Input placeholder text */
    .stTextInput > div > div > input::placeholder {
        color: #9e9e9e !important;
    }
    
    /* Input labels */
    .stTextInput label {
        color: #212121 !important;
        font-weight: 500;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: white !important;
        border-radius: 16px;
        padding: 24px;
        border: 2px dashed #4caf50;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"] > div {
        background-color: white !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: #f5f5f5 !important;
        border-radius: 12px;
        padding: 20px;
    }
    
    [data-testid="stFileUploader"] section > div {
        background-color: transparent !important;
    }
    
    [data-testid="stFileUploader"] button {
        background-color: white !important;
        color: #4caf50 !important;
        border: 2px solid #4caf50 !important;
        border-radius: 8px;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #388e3c;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Cards and Containers */
    .stMarkdown, .stAlert {
        border-radius: 12px;
    }
    
    /* Success/Info/Warning/Error Messages - Fixed for proper text display */
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%) !important;
        border-left: 4px solid #4caf50 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: #1b5e20 !important;
    }
    
    .stSuccess * {
        color: #1b5e20 !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
        border-left: 4px solid #2196f3 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: #0d47a1 !important;
    }
    
    .stInfo * {
        color: #0d47a1 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%) !important;
        border-left: 4px solid #ff9800 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: #e65100 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    .stWarning * {
        color: #e65100 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%) !important;
        border-left: 4px solid #f44336 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        color: #b71c1c !important;
    }
    
    .stError * {
        color: #b71c1c !important;
    }
    
    /* Header buttons (Deploy, Stop, etc.) visibility fix */
    header[data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
    }
    
    header[data-testid="stHeader"] button {
        color: #212121 !important;
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    header[data-testid="stHeader"] button:hover {
        background-color: #f5f5f5 !important;
        border-color: #4caf50 !important;
    }
    
    header[data-testid="stHeader"] svg {
        fill: #212121 !important;
    }
    
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4caf50 0%, #8bc34a 100%);
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        font-weight: 500;
        border: 2px solid #e0e0e0;
        border-bottom: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f5f5f5;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        color: white !important;
        border-color: #4caf50;
    }
    
    /* Divider */
    hr {
        margin: 24px 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #4caf50 50%, transparent 100%);
    }
    
    /* Image Container */
    [data-testid="stImage"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transition: all 0.3s ease;
    }
    
    [data-testid="stImage"]:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
    }
    
    /* Column Containers */
    [data-testid="column"] {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Headers - Fixed for visibility */
    h1 {
        color: #2e7d32 !important;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #2e7d32 !important;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #388e3c !important;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    /* Regular text visibility */
    p, span, div {
        color: #212121 !important;
    }
    
    /* Caption Styling */
    .stCaption {
        color: #757575;
        font-size: 14px;
        font-style: italic;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(33, 150, 243, 0.4);
    }
    
    /* Form Container */
    [data-testid="stForm"] {
        background: white;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border: 1px solid #e0e0e0;
    }
    
    /* Subheader Styling */
    .stSubheader {
        color: #2e7d32;
        font-weight: 600;
        padding-bottom: 8px;
        border-bottom: 2px solid #4caf50;
        margin-bottom: 16px;
    }
    
    /* Animation for page load */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main .block-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Expander Styling - Fix for Treatment Guide visibility */
    [data-testid="stExpander"] {
        background-color: white !important;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stExpander"] > div {
        background-color: white !important;
    }
    
    [data-testid="stExpander"] details {
        background-color: white !important;
    }
    
    [data-testid="stExpander"] summary {
        background-color: #f5f5f5 !important;
        color: #2e7d32 !important;
        font-weight: 600;
        padding: 16px;
        border-radius: 12px;
    }
    
    [data-testid="stExpander"] summary:hover {
        background-color: #e8f5e9 !important;
    }
    
    /* Expander content area */
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
        background-color: white !important;
        color: #212121 !important;
    }
    
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] * {
        color: #212121 !important;
    }
    
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] h4 {
        color: #2e7d32 !important;
    }
    
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] a {
        color: #1976d2 !important;
        text-decoration: underline;
    }
    
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] a:hover {
        color: #1565c0 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'session' not in st.session_state:
        st.session_state['session'] = None
    if 'uploaded_image' not in st.session_state:
        st.session_state['uploaded_image'] = None
    if 'diagnosis_result' not in st.session_state:
        st.session_state['diagnosis_result'] = None


def main():
    """Main application entry point"""
    
    
    st.set_page_config(
        page_title="Crop Disease Diagnosis System",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styling
    apply_custom_styling()
    
    initialize_session_state()
    
    user_repository = UserRepository()
    auth_manager = AuthManager(user_repository)
    
    config_loader = JsonConfigLoader()
    inference_engine = InferenceEngine(config_loader)
    
    
    render_sidebar(auth_manager)
    
    if not st.session_state.get('authenticated', False):
        render_login_page(auth_manager)
    else:

        render_upload_page(inference_engine)


if __name__ == "__main__":
    main()
