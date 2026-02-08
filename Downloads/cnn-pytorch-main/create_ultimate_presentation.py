"""
ULTIMATE PowerPoint with ALL REAL Screenshots and Results
Week 1-4: Real training data
Week 5-8: Real Streamlit app screenshots
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

def create_ultimate_presentation():
    """Create the ULTIMATE PowerPoint with all real screenshots"""
    
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Colors
    TITLE_COLOR = RGBColor(46, 125, 50)
    SUBTITLE_COLOR = RGBColor(67, 160, 71)
    TEXT_COLOR = RGBColor(33, 33, 33)
    ACCENT_COLOR = RGBColor(76, 175, 80)
    HIGHLIGHT_COLOR = RGBColor(255, 152, 0)
    
    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = "AI-Driven Crop Disease Diagnosis System"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(44)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Empowering Farmers Through AI Technology"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(24)
    subtitle_para.font.color.rgb = SUBTITLE_COLOR
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    icon_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.8), Inches(9), Inches(0.6))
    icon_frame = icon_box.text_frame
    icon_frame.text = "Agriculture + AI + Innovation"
    icon_para = icon_frame.paragraphs[0]
    icon_para.font.size = Pt(20)
    icon_para.font.italic = True
    icon_para.font.color.rgb = TEXT_COLOR
    icon_para.alignment = PP_ALIGN.CENTER
    
    # Slide 2: Introduction
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Introduction to AI-Driven Web Application"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Platform: Web-based AI solution for agricultural disease detection"
    
    for point in ["Target Crops: Rice and Pulse crops", "Technology: Deep Learning (CNN) with PyTorch", 
                  "Interface: Streamlit web application with integrated chatbot", 
                  "Purpose: Empowering farmers with instant, accurate disease diagnosis"]:
        p = tf.add_paragraph()
        p.text = point
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nKey Highlights:"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = SUBTITLE_COLOR
    
    for highlight in ["Real-time disease detection from crop images", "AI-powered chatbot for agricultural assistance",
                      "Confidence-based predictions with treatment recommendations", "Downloadable diagnosis reports (PDF/Text)"]:
        p = tf.add_paragraph()
        p.text = highlight
        p.font.size = Pt(16)
        p.font.color.rgb = TEXT_COLOR
    
    # Slide 3: Problem Statement
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Problem Statement & Challenges"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "The Agricultural Challenge"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(22)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    p = tf.add_paragraph()
    p.text = "Crop diseases cause significant yield losses globally"
    p.font.size = Pt(18)
    p.font.italic = True
    p.font.color.rgb = TEXT_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nKey Problems Identified:"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = SUBTITLE_COLOR
    
    for problem in ["Limited Expert Access - Farmers in remote areas lack access to agricultural experts",
                    "Manual Diagnosis Limitations - Time-consuming and requires specialized knowledge",
                    "Economic Impact - Crop diseases reduce agricultural productivity by 20-40%"]:
        p = tf.add_paragraph()
        p.text = problem
        p.font.size = Pt(16)
        p.font.color.rgb = TEXT_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nOur Solution: AI-powered instant diagnosis accessible to all farmers"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = ACCENT_COLOR
    
    # Slide 4: Purpose
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Purpose of the Project"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Vision: Democratize agricultural expertise through AI technology"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    for obj_title, obj_desc in [("Accessibility", "Web-based platform accessible from any device"),
                                 ("Accuracy", "Deep learning model with confidence scores"),
                                 ("Actionable Insights", "Disease identification + treatment recommendations"),
                                 ("Farmer Empowerment", "Instant diagnosis 24/7 with chatbot support")]:
        p = tf.add_paragraph()
        p.text = f"\n{obj_title}"
        p.font.bold = True
        p.font.size = Pt(18)
        p.font.color.rgb = ACCENT_COLOR
        
        p = tf.add_paragraph()
        p.text = obj_desc
        p.level = 1
        p.font.size = Pt(16)
        p.font.color.rgb = TEXT_COLOR
    
    # Slide 5: System Design
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "System Design and Flow"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER
    
    diagram_path = r"C:\Users\gkm09\.gemini\antigravity\brain\329d739e-bf3b-48a4-8784-12302c2c1604\system_architecture_diagram_1768450688244.png"
    if os.path.exists(diagram_path):
        slide.shapes.add_picture(diagram_path, Inches(1.5), Inches(1.2), width=Inches(7))
    
    # Slide 6: Core Modules
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Core Modules of the System"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "7 Major Modules Working Together"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    for module in ["Authentication Module - User registration, login, session management",
                   "Inference Engine - Custom CNN with PyTorch for disease classification",
                   "Image Processing - Preprocessing, normalization, tensor conversion",
                   "Configuration Management - JSON-based flexible configuration",
                   "Treatment Guide System - Comprehensive disease information database",
                   "Report Generation - Professional PDF reports with ReportLab",
                   "Chatbot Integration - Botpress for agricultural assistance"]:
        p = tf.add_paragraph()
        p.text = module
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_COLOR
    
    # Slide 7: Week 1&2 with REAL DATA
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "Week 1&2: Dataset & Preprocessing"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.9), Inches(9), Inches(0.4))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Foundation of Accuracy - 'Garbage In, Garbage Out'"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(20)
    subtitle_para.font.italic = True
    subtitle_para.font.color.rgb = SUBTITLE_COLOR
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    preprocessing_img = r"C:\Users\gkm09\.gemini\antigravity\brain\329d739e-bf3b-48a4-8784-12302c2c1604\data_preprocessing_visual_1768451620654.png"
    if os.path.exists(preprocessing_img):
        slide.shapes.add_picture(preprocessing_img, Inches(0.8), Inches(1.5), width=Inches(8.4))
    
    stats_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.2), Inches(9), Inches(1))
    stats_frame = stats_box.text_frame
    stats_frame.text = "Dataset: 3 Disease Classes | 270 Training Samples | 68 Validation Samples | 224x224 Input Size"
    stats_para = stats_frame.paragraphs[0]
    stats_para.font.size = Pt(14)
    stats_para.font.bold = True
    stats_para.font.color.rgb = ACCENT_COLOR
    stats_para.alignment = PP_ALIGN.CENTER
    
    # Slide 8: Week 3&4 with REAL TRAINING RESULTS
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.5))
    title_frame = title_box.text_frame
    title_frame.text = "Week 3&4: Model Training & Evaluation"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.75), Inches(9), Inches(0.35))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Precision in Prediction - Real Training Results"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(18)
    subtitle_para.font.italic = True
    subtitle_para.font.color.rgb = SUBTITLE_COLOR
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    training_graph = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\models\training_history.png"
    if os.path.exists(training_graph):
        slide.shapes.add_picture(training_graph, Inches(1), Inches(1.3), width=Inches(8))
    
    metrics_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(9), Inches(1.7))
    metrics_frame = metrics_box.text_frame
    
    p = metrics_frame.paragraphs[0]
    p.text = "ACTUAL MODEL PERFORMANCE"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = HIGHLIGHT_COLOR
    p.alignment = PP_ALIGN.CENTER
    
    for metric in ["Best Validation Accuracy: 81.82% | Final Training Accuracy: 83.70%",
                   "30 Epochs | Adam Optimizer | Cross-Entropy Loss",
                   "Diseases Detected: Bacterial Leaf Blight, Brown Spot, Leaf Scald",
                   "Improvement: 31.85% -> 83.70% (Training) | 36.36% -> 81.82% (Validation)"]:
        p = metrics_frame.add_paragraph()
        p.text = metric
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_COLOR
        p.alignment = PP_ALIGN.CENTER
    
    # Slide 9: Week 5&6 - REAL APP SCREENSHOTS (Upload & Analysis)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.5))
    title_frame = title_box.text_frame
    title_frame.text = "Week 5&6: Web Application - Upload & Analysis"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER
    
    # Upload interface screenshot
    upload_img = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\output image\Screenshot 2026-01-15 121547.png"
    if os.path.exists(upload_img):
        slide.shapes.add_picture(upload_img, Inches(0.5), Inches(0.9), width=Inches(4.5))
    
    # Image analysis screenshot
    analysis_img = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\output image\Screenshot 2026-01-15 121624.png"
    if os.path.exists(analysis_img):
        slide.shapes.add_picture(analysis_img, Inches(5), Inches(0.9), width=Inches(4.5))
    
    features_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.8))
    features_frame = features_box.text_frame
    features_frame.text = "REAL APP: Drag-Drop Upload | Image Preview | Instant Analysis | User-Friendly Interface"
    features_para = features_frame.paragraphs[0]
    features_para.font.size = Pt(14)
    features_para.font.bold = True
    features_para.font.color.rgb = ACCENT_COLOR
    features_para.alignment = PP_ALIGN.CENTER
    
    # Slide 10: Week 5&6 - Diagnosis Results & Treatment
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.5))
    title_frame = title_box.text_frame
    title_frame.text = "Week 5&6: Diagnosis Results & Treatment Guide"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER
    
    # Diagnosis results screenshot
    results_img = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\output image\Screenshot 2026-01-15 121643.png"
    if os.path.exists(results_img):
        slide.shapes.add_picture(results_img, Inches(0.5), Inches(0.9), width=Inches(4.5))
    
    # Treatment guide screenshot
    treatment_img = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\output image\Screenshot 2026-01-15 121702.png"
    if os.path.exists(treatment_img):
        slide.shapes.add_picture(treatment_img, Inches(5), Inches(0.9), width=Inches(4.5))
    
    results_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.8))
    results_frame = results_box.text_frame
    results_frame.text = "REAL RESULTS: 100% Confidence | Top-3 Predictions | Treatment Recommendations | Fertilizer Links"
    results_para = results_frame.paragraphs[0]
    results_para.font.size = Pt(14)
    results_para.font.bold = True
    results_para.font.color.rgb = HIGHLIGHT_COLOR
    results_para.alignment = PP_ALIGN.CENTER
    
    # Slide 11: Week 5&6 - Chatbot & Downloads
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.5))
    title_frame = title_box.text_frame
    title_frame.text = "Week 5&6: Chatbot Assistant & Report Downloads"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.color.rgb = TITLE_COLOR
    title_para.alignment = PP_ALIGN.CENTER
    
    # Chatbot screenshot
    chatbot_img = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\output image\Screenshot 2026-01-15 121836.png"
    if os.path.exists(chatbot_img):
        slide.shapes.add_picture(chatbot_img, Inches(1.5), Inches(1), width=Inches(3.5))
    
    # Download buttons screenshot
    download_img = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\output image\Screenshot 2026-01-15 121717.png"
    if os.path.exists(download_img):
        slide.shapes.add_picture(download_img, Inches(5.5), Inches(1), width=Inches(4))
    
    chatbot_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.8))
    chatbot_frame = chatbot_box.text_frame
    chatbot_frame.text = "24/7 AgriTech Assistant | Natural Language Queries | PDF & Text Downloads | Complete Support System"
    chatbot_para = chatbot_frame.paragraphs[0]
    chatbot_para.font.size = Pt(14)
    chatbot_para.font.bold = True
    chatbot_para.font.color.rgb = ACCENT_COLOR
    chatbot_para.alignment = PP_ALIGN.CENTER
    
    # Slide 12: Week 7&8
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Week 7&8: Testing & Quality Assurance"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Comprehensive Testing & Code Excellence"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(22)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nTesting Strategy:"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = ACCENT_COLOR
    
    for point in ["Unit Testing: pytest framework for component validation",
                  "Integration Testing: End-to-end workflow verification",
                  "Bug Fixes: Model loading, image processing, UI/UX improvements"]:
        p = tf.add_paragraph()
        p.text = point
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nSOLID Principles Applied (All 5!):"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = ACCENT_COLOR
    
    for point in ["SRP: Separated UserRepository from AuthManager",
                  "OCP: Abstract ConfigLoader for extensibility",
                  "LSP: Substitutable implementations maintain type safety",
                  "ISP: Focused, specific interfaces",
                  "DIP: IAuthenticator & IPredictor interfaces"]:
        p = tf.add_paragraph()
        p.text = point
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nResult: Production-ready, maintainable, well-documented system"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = ACCENT_COLOR
    
    # Slide 13: Tools & Technologies
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Tools and Technologies Used"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Modern Tech Stack"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    for category, tools in [("Machine Learning & AI", "PyTorch, PIL, NumPy, Custom CNN"),
                            ("Web Development", "Streamlit, Python 3.x"),
                            ("Security", "bcrypt, Session Management"),
                            ("Data Management", "JSON, Dataclasses, Pathlib"),
                            ("Report Generation", "ReportLab, io"),
                            ("Chatbot", "Botpress Webchat"),
                            ("Development Tools", "Git, pytest, VS Code"),
                            ("Design", "Custom CSS, Google Fonts (Inter, Poppins)")]:
        p = tf.add_paragraph()
        p.text = f"{category}: {tools}"
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_COLOR
    
    # Slide 14: Project Timeline
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Project Development Period"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "8-Week Development Cycle"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(22)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    for phase, desc in [("Phase 1 (Weeks 1-2)", "Dataset collection, preprocessing pipeline, configuration"),
                        ("Phase 2 (Weeks 3-4)", "CNN architecture, model training, evaluation, deployment"),
                        ("Phase 3 (Weeks 5-6)", "Streamlit app, authentication, chatbot, PDF reports"),
                        ("Phase 4 (Weeks 7-8)", "Testing, bug fixes, SOLID refactoring, documentation")]:
        p = tf.add_paragraph()
        p.text = phase
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = ACCENT_COLOR
        
        p = tf.add_paragraph()
        p.text = desc
        p.level = 1
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nMethodology: Iterative development, test-driven, user-centric"
    p.font.italic = True
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_COLOR
    
    # Slide 15: Conclusions
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Conclusions"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Project Achievements"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(22)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    for achievement in ["Functional AI System: 81.82% validation accuracy on crop disease classification",
                        "Robust Architecture: SOLID principles for maintainability",
                        "Complete Pipeline: End-to-end solution from upload to report",
                        "User Impact: Accessible to all farmers with instant diagnosis",
                        "Quality Code: Well-tested, documented, and modular"]:
        p = tf.add_paragraph()
        p.text = achievement
        p.font.size = Pt(16)
        p.font.color.rgb = TEXT_COLOR
    
    p = tf.add_paragraph()
    p.text = "\nImpact Statement:"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = SUBTITLE_COLOR
    
    p = tf.add_paragraph()
    p.text = "This project demonstrates how AI can bridge the gap between agricultural expertise and farmers, providing accessible, accurate, and actionable disease diagnosis to improve crop yields and farmer livelihoods."
    p.font.italic = True
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_COLOR
    
    # Slide 16: Future Scope
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Future Scope"
    title.text_frame.paragraphs[0].font.color.rgb = TITLE_COLOR
    
    content = slide.placeholders[1]
    tf = content.text_frame
    tf.text = "Continuous Improvement & Expansion"
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.color.rgb = SUBTITLE_COLOR
    
    for item in ["Expand disease coverage and crop types", "Model optimization with transfer learning (ResNet, EfficientNet)",
                 "Mobile app with offline capability (TensorFlow Lite)", "Multi-language support for regional accessibility",
                 "Geolocation integration for disease prevalence tracking", "Weather integration for disease risk prediction",
                 "Partnership with agricultural organizations", "Cloud deployment (AWS/Azure) for global scalability",
                 "Farmer education and training programs"]:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_COLOR
    
    # Slide 17: Thank You
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    thanks_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1))
    thanks_frame = thanks_box.text_frame
    thanks_frame.text = "Thank You!"
    thanks_para = thanks_frame.paragraphs[0]
    thanks_para.font.size = Pt(54)
    thanks_para.font.bold = True
    thanks_para.font.color.rgb = TITLE_COLOR
    thanks_para.alignment = PP_ALIGN.CENTER
    
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.7), Inches(9), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "AI-Driven Crop Disease Diagnosis System"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(28)
    subtitle_para.font.color.rgb = SUBTITLE_COLOR
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    tagline_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.6), Inches(9), Inches(0.5))
    tagline_frame = tagline_box.text_frame
    tagline_frame.text = "Empowering Farmers Through Technology"
    tagline_para = tagline_frame.paragraphs[0]
    tagline_para.font.size = Pt(20)
    tagline_para.font.italic = True
    tagline_para.font.color.rgb = TEXT_COLOR
    tagline_para.alignment = PP_ALIGN.CENTER
    
    questions_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(9), Inches(0.5))
    questions_frame = questions_box.text_frame
    questions_frame.text = "Questions & Discussion"
    questions_para = questions_frame.paragraphs[0]
    questions_para.font.size = Pt(24)
    questions_para.font.bold = True
    questions_para.font.color.rgb = ACCENT_COLOR
    questions_para.alignment = PP_ALIGN.CENTER
    
    # Save
    output_path = r"C:\Users\gkm09\Downloads\cnn-pytorch-main\AI_Crop_Disease_Diagnosis_ULTIMATE.pptx"
    prs.save(output_path)
    print("ULTIMATE presentation created successfully!")
    print(f"Saved to: {output_path}")
    print("\nIncludes:")
    print("- Week 1-2: Real dataset stats + preprocessing diagram")
    print("- Week 3-4: Real training graph + 81.82% accuracy")
    print("- Week 5-6: REAL app screenshots (upload, analysis, results, treatment, chatbot, downloads)")
    print("- Week 7-8: Testing & SOLID principles")
    print("- Total: 17 slides with ALL REAL data and screenshots!")
    return output_path

if __name__ == "__main__":
    create_ultimate_presentation()
