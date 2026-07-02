import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        self.saveState()
        
        # Suppress headers/footers on the cover page (Page 1)
        if self._pageNumber == 1:
            self.restoreState()
            return
            
        # Draw Header
        self.setFont("Times-BoldItalic", 9)
        self.setFillColor(colors.HexColor('#2c3e50'))
        self.drawString(54, letter[1] - 40, "TECHNICAL INTERVIEW PREPARATION & DEFENSE GUIDE")
        self.setFont("Times-Roman", 9)
        self.drawRightString(letter[0] - 54, letter[1] - 40, "Hierarchical Federated Learning NIDS")
        
        # Header separator line
        self.setStrokeColor(colors.HexColor('#bdc3c7'))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 44, letter[0] - 54, letter[1] - 44)
        
        # Draw Footer
        text = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Times-Roman", 10)
        self.drawCentredString(letter[0] / 2.0, 30, text)
        
        # Footer separator line
        self.line(54, 44, letter[0] - 54, 44)
        
        self.restoreState()

def build_pdf(filename="Project_Interview_Defense_Guide.pdf"):
    # Target 0.75 in (54 pt) margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Times styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=20,
        leading=24,
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=1,
        spaceAfter=25
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=14,
        leading=17,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
        textColor=colors.HexColor('#2c3e50')
    )
    
    q_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True,
        textColor=colors.HexColor('#2980b9')
    )

    a_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14.5,
        spaceAfter=8
    )
    
    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=10.5,
        leftIndent=15,
        spaceAfter=6,
        textColor=colors.HexColor('#2c3e50')
    )

    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("TECHNICAL DEFENSE & INTERVIEW PREPARATION GUIDE", subtitle_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Hierarchical Federated Learning for Privacy-Preserving IoT Intrusion Detection Using Unsupervised Anomaly Detection", title_style))
    story.append(Spacer(1, 40))
    
    story.append(Paragraph("<b>Comprehensive Q&A Defense Manual covering Architectures, Machine Learning Engineering Decisions, Preprocessing Leakages, and System Debugging</b>", meta_style))
    story.append(Spacer(1, 100))
    
    story.append(Paragraph("<b>Prepared For:</b> Capstone Project Presentation and Technical Review Panels", meta_style))
    story.append(Paragraph("<b>Author Placeholder:</b> **[Information Needed]**", meta_style))
    story.append(Paragraph("<b>Institution Placeholder:</b> **[Information Needed]**", meta_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Date:</b> July 2026", meta_style))
    story.append(PageBreak())

    # ================= QUESTIONS AND ANSWERS =================

    # --- SECTION 1 ---
    story.append(Paragraph("1. Project Overview & Architectural Foundation", h1_style))
    
    story.append(Paragraph("Q1: Give me a brief overview of your IoT project.", q_style))
    story.append(Paragraph(
        "A: This project implements a privacy-preserving network intrusion detection system (NIDS) simulated across a "
        "5-layer IoT hierarchy (Edge, Gateway, Fog, Proxy, and Cloud). Local Edge nodes train a Mini Transformer "
        "Autoencoder in an unsupervised anomaly detection paradigm using only benign network flow records. Updates are "
        "relayed bottom-up and aggregated using Federated Averaging (FedAvg) at the Fog and Cloud levels. Anomalies are "
        "flagged at inference when reconstruction error (MSE) exceeds a dynamic threshold. Finally, a SHAP explainability "
        "module identifies which header features drive anomaly attributions.",
        a_style
    ))

    story.append(Paragraph("Q2: What problem were you trying to solve?", q_style))
    story.append(Paragraph(
        "A: Traditional NIDS requires sending raw network logs to the cloud. This incurs massive bandwidth overhead, high "
        "transmission latency, and major privacy violations. Additionally, standard centralized machine learning models "
        "suffer from: (1) target leakages where ground-truth indicators cheat during training, (2) zero-support data splits "
        "that produce deceptive evaluation accuracies, and (3) a high rate of false positive alarms due to rigid thresholds.",
        a_style
    ))

    story.append(Paragraph("Q3: Why did you choose this project?", q_style))
    story.append(Paragraph(
        "A: This project combines several critical aspects of modern computer engineering: decentralized systems, deep "
        "learning sequence models, network protocol security, data pipeline integrity, and explainable AI (XAI). It represents "
        "a highly practical approach to securing sensitive enterprise IoT installations under realistic bandwidth limitations.",
        a_style
    ))

    story.append(Paragraph("Q4: Can you explain the architecture from Edge to Cloud?", q_style))
    story.append(Paragraph(
        "A: The system consists of five distinct logical layers: (1) <b>Edge/Sensors</b> (Sensor 1 & 2) perform preprocessing, "
        "local autoencoder training, and float16 model updates. (2) <b>Gateway Node</b> (Bridge 1) buffers weights from "
        "both edges in a dictionary key structure to avoid overwriting. (3) <b>Fog Layer</b> performs regional weight "
        "aggregation using FedAvg. (4) <b>Proxy Node</b> acts as a transparent network relay. (5) <b>Cloud Node</b> aggregates "
        "the final global weights and broadcasts updates back down the hierarchy.",
        a_style
    ))

    story.append(Paragraph("Q5: Walk me through the data flow from start to finish.", q_style))
    story.append(Paragraph(
        "A: The pipeline flows as follows: Preprocessing isolates the target column 'Label', drop the ground-truth "
        "'Attack_categories', scale features, and execute StratifiedKFold into B.1/B.2/B.3 test splits. Train Part A is split "
        "into A.1 (Sensor 1) and A.2 (Sensor 2). Sensors filter out malicious traffic, keeping only benign samples, and train "
        "the Autoencoder. Trained weights are quantized to float16, relayed by Gateway, and aggregated at Fog and Cloud using "
        "FedAvg. The Cloud Node determines a dynamic anomaly threshold: Mean(MSE) + 4*Std(MSE) on normal test records. "
        "Test splits are reconstructed, flagging anomalies if their reconstruction MSE exceeds the threshold. The App node "
        "then runs SHAP explainability on flagged flows.",
        a_style
    ))

    story.append(Paragraph("Q6: What is your role in this project?", q_style))
    story.append(Paragraph(
        "A: I designed and implemented the entire project from scratch. This includes formulating the Mini Transformer "
        "Autoencoder model, implementing the hierarchical network simulation nodes, developing the leak-free data "
        "preprocessing pipeline, writing the stratified partitioning logic, resolving weight overwriting bugs in the "
        "Gateway, implementing float16 quantization, and writing the ReportLab PDF compilation scripts.",
        a_style
    ))

    story.append(Paragraph("Q7: What would happen if one Edge node fails?", q_style))
    story.append(Paragraph(
        "A: Because the Gateway buffers updates in a key-value dictionary, the system survives the failure of a client. "
        "If Sensor 1 goes offline, Bridge 1 forwards only Sensor 2's weights. The Fog node aggregates updates from the active "
        "client. This demonstrates the decentralized fault-tolerance of Federated Learning architectures.",
        a_style
    ))

    # --- SECTION 2 ---
    story.append(Paragraph("2. Federated Learning & Weight Aggregation", h1_style))

    story.append(Paragraph("Q1: Why Federated Learning instead of centralized learning?", q_style))
    story.append(Paragraph(
        "A: Centralized NIDS is a privacy hazard that exposes sensitive local IP headers and payloads. It also creates a "
        "massive bandwidth bottleneck when uploading millions of flow records. Federated Learning transmits only model weight "
        "adjustments, leaving raw user traffic isolated on local devices.",
        a_style
    ))

    story.append(Paragraph("Q2: What problem does Federated Learning solve?", q_style))
    story.append(Paragraph(
        "A: It solves the privacy-utility trade-off. Organizations can benefit from a shared global model trained on massive, "
        "diverse datasets without compromising user data privacy or incurring prohibitive WAN data transfer costs.",
        a_style
    ))

    story.append(Paragraph("Q3: What is FedAvg?", q_style))
    story.append(Paragraph(
        "A: Federated Averaging (FedAvg) is the standard algorithm for aggregating model updates. It takes the weight matrices "
        "from decentralized clients, scales them proportionally based on the local sample size, and performs an element-wise "
        "arithmetic average to compile a new global weight dictionary.",
        a_style
    ))

    story.append(Paragraph("Q4: How does weight aggregation work?", q_style))
    story.append(Paragraph(
        "A: Weights are aggregated by extracting state dicts from the client models. For each parameter tensor key, the "
        "aggregator performs: global_tensor = sum(client_tensors) / N. The resulting aggregated state dict is then loaded "
        "back into the global model.",
        a_style
    ))

    story.append(Paragraph("Q5: Why not send raw data?", q_style))
    story.append(Paragraph(
        "A: Raw packet logs contain unencrypted payloads, credentials, and network mapping indicators that violate corporate "
        "privacy policies. Furthermore, transmitting raw data consumes heavy network bandwidth, whereas transmitting model weights "
        "is a fixed, predictable, and highly compressible payload.",
        a_style
    ))

    story.append(Paragraph("Q6: What happens during one communication round?", q_style))
    story.append(Paragraph(
        "A: 1. Cloud broadcasts current global weights. 2. Edge clients pull global weights and load them. 3. Edge clients "
        "train locally for 5 epochs on benign data. 4. Clients extract weights, cast to float16, and upload to the Gateway. "
        "5. Gateway buffers updates, and Fog averages them. 6. Aggregated weights are passed up to Cloud to establish "
        "the final global weights.",
        a_style
    ))

    story.append(Paragraph("Q7: Why did you simulate multiple layers?", q_style))
    story.append(Paragraph(
        "A: Industrial IoT systems are naturally hierarchical. Direct client-to-cloud updates suffer from high latency and "
        "WAN packet loss. Simulating a 5-layer topology replicates realistic enterprise routing where regional Gateways and "
        "Fog nodes aggregate local clusters before sending summary checkpoints to the cloud.",
        a_style
    ))

    story.append(Paragraph("Q8: If there were 100 Edge nodes instead of 2, what changes?", q_style))
    story.append(Paragraph(
        "A: The Gateway buffer must scale from 2 to 100 dictionary slots. To handle uneven client datasets, we would implement "
        "weighted FedAvg: weight_global = sum(n_k * weight_k) / sum(n_k), where n_k is the number of benign packets trained "
        "at client k.",
        a_style
    ))

    story.append(Paragraph("Q9: What communication bottlenecks exist?", q_style))
    story.append(Paragraph(
        "A: Network latency, asymmetric cellular channels (slow upload speeds), and client dropouts ('stragglers') who stall "
        "the aggregation loop by failing to complete local training rounds in time.",
        a_style
    ))

    story.append(Paragraph("Q10: How would Secure Aggregation improve your project?", q_style))
    story.append(Paragraph(
        "A: Secure Aggregation (SecAgg) uses cryptographic protocols (like secret sharing or homomorphic encryption) to combine "
        "client updates such that the aggregator can only decrypt the averaged sum, preventing the coordinator from inspecting "
        "individual weights, which eliminates potential model-poisoning or model-inversion privacy threats.",
        a_style
    ))

    # --- SECTION 3 ---
    story.append(PageBreak())
    story.append(Paragraph("3. Deep Learning & Sequence Reconstruction", h1_style))

    story.append(Paragraph("Q1: Why Transformer?", q_style))
    story.append(Paragraph(
        "A: Transformers leverage self-attention mechanisms to map dependencies across time steps without relying on sequential "
        "recurrent steps. This allows the model to capture complex temporal interactions between different network packets "
        "in a sliding window much more effectively.",
        a_style
    ))

    story.append(Paragraph("Q2: Why not CNN?", q_style))
    story.append(Paragraph(
        "A: Convolutional Neural Networks (CNNs) assume local spatial grid structures (e.g. adjacent pixels). They are not "
        "natively designed to capture long-range temporal correlations across sequence windows in network protocol streams.",
        a_style
    ))

    story.append(Paragraph("Q3: Why not LSTM?", q_style))
    story.append(Paragraph(
        "A: Long Short-Term Memory (LSTM) models process sequences step-by-step, preventing parallel training. They also "
        "suffer from information bottlenecks and vanishing gradients over longer seq_len inputs, whereas self-attention "
        "enables direct connections between any two packets in a sequence.",
        a_style
    ))

    story.append(Paragraph("Q4: Why Autoencoder?", q_style))
    story.append(Paragraph(
        "A: Autoencoders compress input sequences into a low-dimensional latent space and attempt to reconstruct the original "
        "input. By training the network exclusively on normal traffic, it learns to reconstruct normal traffic with low error. "
        "Anomalous traffic, having features unseen during training, cannot be compressed and reconstructed accurately, creating "
        "a high reconstruction error that serves as an anomaly indicator.",
        a_style
    ))

    story.append(Paragraph("Q5: Why an unsupervised approach?", q_style))
    story.append(Paragraph(
        "A: Supervised models are unable to detect zero-day attacks because they require labeled examples of every attack class "
        "to train. Unsupervised models learn the boundary of normal behavior and flag any deviation, enabling them to detect "
        "novel, unseen security threats.",
        a_style
    ))

    story.append(Paragraph("Q6: What is reconstruction error?", q_style))
    story.append(Paragraph(
        "A: It is the Mean Squared Error (MSE) between the input feature vector sequence and the model's output reconstructed "
        "sequence. It measures how much the input packet sequence deviates from the normal baseline patterns the model has learned.",
        a_style
    ))

    story.append(Paragraph("Q7: What loss function are you using?", q_style))
    story.append(Paragraph(
        "A: PyTorch's `nn.MSELoss()`, which calculates the squared Euclidean distance between the input and reconstructed tensors.",
        a_style
    ))

    story.append(Paragraph("Q8: Why only train on benign traffic?", q_style))
    story.append(Paragraph(
        "A: If the autoencoder trained on attack traffic, it would learn to reconstruct attacks with low error. This would "
        "eliminate the reconstruction error difference between normal and anomalous packets, making the model blind to intrusions.",
        a_style
    ))

    story.append(Paragraph("Q9: How is anomaly detection performed?", q_style))
    story.append(Paragraph(
        "A: A threshold is calculated from normal validation sequences: Threshold = Mean(MSE) + 4 * Std(MSE). During testing, "
        "reconstruction MSE is calculated. If the MSE exceeds the threshold, the packet sequence is flagged as an attack (1); "
        "otherwise, it is normal (0).",
        a_style
    ))

    story.append(Paragraph("Q10: What is the latent representation?", q_style))
    story.append(Paragraph(
        "A: The compressed vector bottleneck output by the encoder (dimension = 32). It represents the most critical low-dimensional "
        "temporal signatures of the packet sequence, discarding noise and high-frequency fluctuations.",
        a_style
    ))

    # --- SECTION 4 ---
    story.append(Paragraph("4. Data Engineering & Integrity", h1_style))

    story.append(Paragraph("Q1: Why remove Attack_categories?", q_style))
    story.append(Paragraph(
        "A: The column `Attack_categories` contains string values like 'DDoS' or 'normal'. When one-hot encoded, it creates "
        "features like `Attack_categories_normal` (which is exactly equivalent to `1 - Label`). This column leaks the ground "
        "truth label directly into features, allowing the model to cheat during training.",
        a_style
    ))

    story.append(Paragraph("Q2: What is feature leakage?", q_style))
    story.append(Paragraph(
        "A: Feature leakage occurs when training features contain direct information about the target label that would not "
        "be available at inference. It artificially inflates validation accuracy during training but fails in production.",
        a_style
    ))

    story.append(Paragraph("Q3: Why is leakage dangerous?", q_style))
    story.append(Paragraph(
        "A: It creates an illusion of high accuracy. The model appears to be 99.9% accurate, but it is just performing a "
        "database lookup of the leaked column. In a live system, the leaked column is absent, and the model's actual accuracy "
        "collapses.",
        a_style
    ))

    story.append(Paragraph("Q4: What is target leakage?", q_style))
    story.append(Paragraph(
        "A: A specific form of leakage where the target variable (the class label) is present in the input feature set, either "
        "directly or through a highly correlated proxy variable.",
        a_style
    ))

    story.append(Paragraph("Q5: Why was your previous accuracy misleading?", q_style))
    story.append(Paragraph(
        "A: Sequential test data slicing gave Gateway, Fog, and Cloud test splits containing 100% normal samples. A model "
        "that predicted 'normal' 100% of the time achieved 99% accuracy while having a recall of 0% for attack detection. "
        "This is a classic 'Zero Support' class imbalance trap.",
        a_style
    ))

    story.append(Paragraph("Q6: Why StratifiedKFold?", q_style))
    story.append(Paragraph(
        "A: It guarantees that each partition (B.1, B.2, B.3) maintains the exact same ratio of normal and attack samples "
        "as the parent dataset (~8.4% attacks). This ensures that evaluation support is non-zero and consistent.",
        a_style
    ))

    story.append(Paragraph("Q7: What happens with sequential splitting?", q_style))
    story.append(Paragraph(
        "A: In sorted network logs, all normal packets sit at the top and attacks are at the bottom. Sequential slicing "
        "causes early splits to receive 0% attacks, and late splits to receive 100% attacks, introducing extreme test bias.",
        a_style
    ))

    story.append(Paragraph("Q8: Why normalize the data?", q_style))
    story.append(Paragraph(
        "A: Network features like byte counts range in the millions, while port flags range from 0 to 1. Without scaling, "
        "features with massive numeric ranges dominate the gradient updates, preventing convergence.",
        a_style
    ))

    story.append(Paragraph("Q9: Why SelectKBest?", q_style))
    story.append(Paragraph(
        "A: It uses univariate statistical tests to select the top $K$ features most strongly correlated with the target, "
        "removing irrelevant features and reducing computation overhead.",
        a_style
    ))

    story.append(Paragraph("Q10: Why VarianceThreshold?", q_style))
    story.append(Paragraph(
        "A: It removes zero-variance features (columns where every single row has the same value). These columns contain "
        "no statistical information and waste model weights.",
        a_style
    ))

    # --- SECTION 5 ---
    story.append(PageBreak())
    story.append(Paragraph("5. Engineering Decisions & Parameters", h1_style))

    story.append(Paragraph("Q1: Why float16?", q_style))
    story.append(Paragraph(
        "A: Casting model weights from 32-bit floats to 16-bit half-precision (`float16`) reduces the parameter payload size "
        "by approximately 50%, saving bandwidth over cellular/satellite IoT connection links.",
        a_style
    ))

    story.append(Paragraph("Q2: Why convert back to float32?", q_style))
    story.append(Paragraph(
        "A: PyTorch's mathematical operations (like FedAvg tensor addition and division) are prone to underflow or overflow "
        "instability in float16. We cast back to float32 before aggregation to preserve numerical stability.",
        a_style
    ))

    story.append(Paragraph("Q3: Why 5 epochs?", q_style))
    story.append(Paragraph(
        "A: Through empirical testing, local losses converged stably at 5 epochs (Sensor 1 loss: 0.6425, Sensor 2: 0.6563). "
        "Fewer epochs caused underfitting, while more epochs wasted computational resources at edge devices.",
        a_style
    ))

    story.append(Paragraph("Q4: Why Mean + 4*Std?", q_style))
    story.append(Paragraph(
        "A: Network traffic exhibits natural bursts and spikes. A relaxed boundary of 4 standard deviations accommodates "
        "normal flow variance, clearing out false positives (1,504 under 4-sigma vs. 3,817 under 3-sigma).",
        a_style
    ))

    story.append(Paragraph("Q5: Why not Mean + 3*Std?", q_style))
    story.append(Paragraph(
        "A: A 3-sigma threshold is too restrictive. It flags normal high-traffic bursts as anomalies, resulting in a high "
        "false alarm rate and low precision on benign data.",
        a_style
    ))

    story.append(Paragraph("Q6: Why SHAP?", q_style))
    story.append(Paragraph(
        "A: SHAP (SHapley Additive exPlanations) is based on cooperative game theory. It provides mathematically consistent "
        "feature attribution values, ensuring that features are ranked reliably.",
        a_style
    ))

    story.append(Paragraph("Q7: Why not LIME?", q_style))
    story.append(Paragraph(
        "A: LIME builds local surrogate models by perturbing inputs, which makes it highly unstable (can give different "
        "explanations for the same input between runs). SHAP provides globally consistent additive values.",
        a_style
    ))

    story.append(Paragraph("Q8: Why remove the classifier head?", q_style))
    story.append(Paragraph(
        "A: The legacy hybrid design had a classifier head to output logits. By focusing strictly on unsupervised anomaly "
        "detection, we evaluate anomalies via reconstruction error MSE, making the classification head redundant.",
        a_style
    ))

    story.append(Paragraph("Q9: Why only reconstruct sequences?", q_style))
    story.append(Paragraph(
        "A: Removing the classification head reduced the model parameter footprint, making weights more lightweight for "
        "decentralized transfers and focusing the model's capacity on reconstruction.",
        a_style
    ))

    story.append(Paragraph("Q10: Why sequence length = 10?", q_style))
    story.append(Paragraph(
        "A: A sequence length of 10 provides enough historical context to capture temporal flow dynamics while keeping "
        "the input dimensions small enough to fit in low-memory edge devices.",
        a_style
    ))

    # --- SECTION 6 ---
    story.append(Paragraph("6. Debugging & Troubleshooting", h1_style))

    story.append(Paragraph("Q1: Tell me about the biggest bug you fixed.", q_style))
    story.append(Paragraph(
        "A: The biggest bug was the target leakage from the `Attack_categories` column. The encoder cheat-memorized "
        "the class label via the one-hot encoded proxy column. Fixing it required restructuring the preprocessing "
        "pipeline to explicitly isolate `Label` and drop `Attack_categories` from features.",
        a_style
    ))

    story.append(Paragraph("Q2: What was the Gateway overwrite issue?", q_style))
    story.append(Paragraph(
        "A: The Gateway class had a single instance variable `received_weights`. When Edge 1 and Edge 2 uploaded "
        "their weights asynchronously, the second upload overwrote the first, meaning only Edge 2's weights reached "
        "the Fog node for aggregation.",
        a_style
    ))

    story.append(Paragraph("Q3: How did you find it?", q_style))
    story.append(Paragraph(
        "A: I printed the weights dictionary keys at the Gateway during aggregation and noticed only one client's weight "
        "dict was present, and the Fog aggregated loss matched Sensor 2's training loss exactly.",
        a_style
    ))

    story.append(Paragraph("Q4: How long did it take to resolve?", q_style))
    story.append(Paragraph(
        "A: It took one troubleshooting cycle to isolate the reference overwrite and refactor Gateway `receive_data` "
        "to store weights in a dictionary keyed by node ID.",
        a_style
    ))

    story.append(Paragraph("Q5: How did you verify the fix?", q_style))
    story.append(Paragraph(
        "A: I logged the length of the Gateway's weights list, verifying it contained exactly two weight dictionaries "
        "before performing the average aggregation loop.",
        a_style
    ))

    story.append(Paragraph("Q6: Which bug taught you the most?", q_style))
    story.append(Paragraph(
        "A: The target leakage bug. It taught me that high model accuracy (e.g. 99.9%) is often a sign of data "
        "leakage or evaluation errors rather than a perfect model. Debugging the pipeline is as critical as debugging the model.",
        a_style
    ))

    story.append(Paragraph("Q7: What was the hardest part of the project?", q_style))
    story.append(Paragraph(
        "A: Designing the sequence alignment window. Network packet records are continuous. Aligning sequence batches of "
        "shape (batch, 10, features) with target vectors corresponding to the label of the *last* packet in the sequence "
        "required precise indexing to avoid off-by-one errors.",
        a_style
    ))

    # --- SECTION 7 ---
    story.append(PageBreak())
    story.append(Paragraph("7. Evaluation & Metrics", h1_style))

    story.append(Paragraph("Q1: Why is your precision only around 22%?", q_style))
    story.append(Paragraph(
        "A: The model operates in an unsupervised anomaly detection paradigm with an imbalanced test split (~8.4% attacks). "
        "Because normal packets outnumber attacks 12:1, even a small false-positive rate (11% normal packets incorrectly flagged) "
        "yields a high absolute number of false positives (1,504 normal vs. 438 true attacks caught). This mathematically "
        "limits precision to 22.5%, representing the standard precision-recall trade-off.",
        a_style
    ))

    story.append(Paragraph("Q2: Is 84% accuracy good?", q_style))
    story.append(Paragraph(
        "A: Yes, for unsupervised reconstruction models. It represents a realistic, leak-free evaluation on a stratified "
        "dataset, capturing 36% of attacks while maintaining 89% recall on normal traffic.",
        a_style
    ))

    story.append(Paragraph("Q3: Why did accuracy decrease?", q_style))
    story.append(Paragraph(
        "A: In early tests, accuracy was 99% due to target leakage and sequential split issues. Once the target leak was "
        "resolved and test support was stratified, the accuracy adjusted to a realistic, leak-free 84.5%.",
        a_style
    ))

    story.append(Paragraph("Q4: Would you rather have higher recall or higher precision?", q_style))
    story.append(Paragraph(
        "A: In network intrusion detection, **Recall** is prioritized. Missing an attack (False Negative) can result in a "
        "breach. A False Positive (low precision) creates a false alarm that can be filtered by secondary logs.",
        a_style
    ))

    story.append(Paragraph("Q5: Explain your confusion matrix.", q_style))
    story.append(Paragraph(
        "A: In the final Cloud evaluation: TN = 11,777 (normal packets correctly identified), FP = 1,504 (normal flagged "
        "as attack), FN = 784 (attacks missed), TP = 438 (attacks correctly caught).",
        a_style
    ))

    story.append(Paragraph("Q6: Why did you choose those metrics?", q_style))
    story.append(Paragraph(
        "A: Accuracy evaluates overall correct classifications. Precision, Recall, and F1 measure performance specifically "
        "on the minority attack class.",
        a_style
    ))

    story.append(Paragraph("Q7: How do you know the model isn't overfitting?", q_style))
    story.append(Paragraph(
        "A: Edge devices train only on benign traffic from Part A, while testing is conducted on entirely unseen stratified "
        "partitions from Part B, ensuring the model generalizes to new flows.",
        a_style
    ))

    story.append(Paragraph("Q8: Why balanced test splits?", q_style))
    story.append(Paragraph(
        "A: Stratifying test splits (B.1, B.2, B.3) ensures that evaluation support is identical across layers, preventing "
        "deceptive metrics caused by imbalanced evaluation sets.",
        a_style
    ))

    # --- SECTION 8 ---
    story.append(Paragraph("8. Explainability & Interpretation", h1_style))

    story.append(Paragraph("Q1: What is and why SHAP?", q_style))
    story.append(Paragraph(
        "A: SHAP (SHapley Additive exPlanations) is a model explanation tool. We use it to explain the reconstruction "
        "MSE of the Mini Transformer Autoencoder, making its anomaly classifications interpretable.",
        a_style
    ))

    story.append(Paragraph("Q2: What does SHAP actually tell us?", q_style))
    story.append(Paragraph(
        "A: It computes Shapley attribution values for each input feature. A positive value indicates the feature increased "
        "the reconstruction error (pushing the sequence toward an anomaly classification).",
        a_style
    ))

    story.append(Paragraph("Q3: Can SHAP be trusted?", q_style))
    story.append(Paragraph(
        "A: Yes. SHAP is based on cooperative game theory axioms, guaranteeing mathematical consistency and local accuracy "
        "that heuristic explainers lack.",
        a_style
    ))

    story.append(Paragraph("Q4: What feature contributed the most?", q_style))
    story.append(Paragraph(
        "A: Features related to network addresses, port mappings, flag states, and byte lengths show the highest attributions "
        "during reconstruction anomalies.",
        a_style
    ))

    story.append(Paragraph("Q5: How is SHAP helping an analyst?", q_style))
    story.append(Paragraph(
        "A: A security analyst receives an alert alongside a SHAP chart explaining *why* the flow was flagged (e.g. source "
        "port spikes), reducing diagnostic time from hours to seconds.",
        a_style
    ))

    # --- SECTION 9 ---
    story.append(PageBreak())
    story.append(Paragraph("9. Optimization, Future Work & Code Implementation", h1_style))

    story.append(Paragraph("Q1: Why float16 and what performance did it provide?", q_style))
    story.append(Paragraph(
        "A: It reduces the weight dictionary payload size by approximately 50%, halving bandwidth costs on edge channels.",
        a_style
    ))

    story.append(Paragraph("Q2: Would INT8 be better?", q_style))
    story.append(Paragraph(
        "A: INT8 reduces payload sizes by 75%, but can lead to quantization error and loss of precision on continuous features. "
        "It would require quantization-aware training (QAT) to implement successfully.",
        a_style
    ))

    story.append(Paragraph("Q3: What other optimizations would you make?", q_style))
    story.append(Paragraph(
        "A: Implement model pruning (removing redundant attention weights) and communication compression (gradient sparsification).",
        a_style
    ))

    story.append(Paragraph("Q4: What would you improve if given another month?", q_style))
    story.append(Paragraph(
        "A: Integrate homomorphic encryption for secure aggregation, implement multi-round federated training, and benchmark "
        "the model on real-world edge hardware like a Raspberry Pi.",
        a_style
    ))

    story.append(Paragraph("Q5: How would you deploy this in production?", q_style))
    story.append(Paragraph(
        "A: Compile the PyTorch model to ONNX format, deploy ONNX Runtime on edge nodes, and ingestion network packet flows "
        "via Kafka message brokers.",
        a_style
    ))

    story.append(Paragraph("Q6: Write code to compute reconstruction error and detect anomalies.", q_style))
    
    code_snippet = (
        "import torch\n"
        "import torch.nn as nn\n"
        "\n"
        "def detect_anomalies(model, dataloader, threshold, device):\n"
        "    model.eval()\n"
        "    criterion = nn.MSELoss(reduction='none')\n"
        "    predictions = []\n"
        "    \n"
        "    with torch.no_grad():\n"
        "        for X, y in dataloader:\n"
        "            X = X.to(device)\n"
        "            reconstructed = model(X)\n"
        "            \n"
        "            # Calculate MSE per sequence (mean over seq_len and input_dim)\n"
        "            mse = criterion(reconstructed, X).mean(dim=[1, 2])\n"
        "            preds = (mse > threshold).long()\n"
        "            predictions.extend(preds.cpu().numpy())\n"
        "            \n"
        "    return predictions"
    )
    story.append(Paragraph(code_snippet.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style))

    story.append(Paragraph("Q7: Implement the Federated Averaging (FedAvg) aggregation loop in Python.", q_style))
    
    fedavg_snippet = (
        "import copy\n"
        "\n"
        "def federated_averaging(client_weights_list):\n"
        "    # Assumes client weights are in a list of PyTorch state_dicts\n"
        "    global_weights = copy.deepcopy(client_weights_list[0])\n"
        "    num_clients = len(client_weights_list)\n"
        "    \n"
        "    for key in global_weights.keys():\n"
        "        # Sum weights from all clients for the parameter key\n"
        "        for i in range(1, num_clients):\n"
        "            global_weights[key] += client_weights_list[i][key]\n"
        "            \n"
        "        # Average the parameters\n"
        "        global_weights[key] = global_weights[key] / num_clients\n"
        "        \n"
        "    return global_weights"
    )
    story.append(Paragraph(fedavg_snippet.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style))

    story.append(Paragraph("Q8: If accuracy dropped, why do you say the project improved?", q_style))
    story.append(Paragraph(
        "A: High accuracy driven by target leakage is a system flaw. Correcting target leakage dropped accuracy to a realistic, "
        "leak-free 84.5%. This makes the model robust, generalizable, and mathematically valid for real-world deployment.",
        a_style
    ))

    # --- SECTION 10 ---
    story.append(PageBreak())
    story.append(Paragraph("10. Rapid Fire Explanations", h1_style))

    story.append(Paragraph("Q1: Explain your project in 30 seconds.", q_style))
    story.append(Paragraph(
        "A: I designed and implemented a hierarchical Federated Learning simulation for IoT network intrusion detection from scratch. "
        "Edge nodes pre-process traffic into packet sequences and train a custom PyTorch Mini Transformer Autoencoder strictly on "
        "benign flows. The updates are quantized to float16, relayed by a Gateway buffer, aggregated at Fog and Cloud layers via "
        "FedAvg, and evaluated using stratified test splits. Anomalies are flagged based on a dynamic reconstruction error threshold, "
        "and SHAP is integrated to provide interpretability for the security alerts.",
        a_style
    ))

    story.append(Paragraph("Q2: Explain your project in 2 minutes.", q_style))
    story.append(Paragraph(
        "A: Centralized network intrusion detection (NIDS) creates major data privacy risks and network bandwidth bottlenecks. "
        "My project addresses these by implementing a hierarchical Federated Learning simulation across a 5-layer IoT topology. "
        "Edge sensors pre-process network traffic, exclude target leakage features, and train a Mini Transformer Autoencoder "
        "strictly on benign traffic to model normal sequence behaviors. To optimize communication costs, local weights are "
        "quantized to float16 prior to transmission. A Gateway buffers updates in dictionaries to prevent overwrites, and the Fog "
        "and Cloud aggregate parameters via FedAvg in float32. The final model establishes a relaxed mean + 4*std reconstruction threshold. "
        "Test sets are partitioned using StratifiedKFold to prevent the 'Zero Support' trap. Reconstruction errors exceeding "
        "the threshold flag anomalies, and SHAP is applied to interpret feature attributions for incident analysts.",
        a_style
    ))

    story.append(Paragraph("Q3: Explain it to HR.", q_style))
    story.append(Paragraph(
        "A: I built an AI-based cybersecurity system that protects smart internet-connected devices. Instead of collecting private user "
        "data onto a central server, the devices learn local security patterns and share only anonymous mathematical updates. This "
        "system ensures high privacy compliance, saves internet bandwidth, and uses explainable AI so engineers know exactly what "
        "triggered an intrusion alarm.",
        a_style
    ))

    story.append(Paragraph("Q4: Explain it to a non-technical manager.", q_style))
    story.append(Paragraph(
        "A: This project secures network traffic across distributed IoT environments without centralizing raw packet logs. By performing "
        "unsupervised anomaly detection, the system learns normal baseline behaviors and automatically flags new, zero-day attacks "
        "when traffic patterns deviate. It optimizes communication overhead by 50% via weight compression, buffers uploads to prevent "
        "data loss during transmission, and provides visual SHAP feature importance charts so operations teams can understand and act "
        "on security alerts immediately.",
        a_style
    ))

    story.append(Paragraph("Q5: Explain it to a Machine Learning engineer.", q_style))
    story.append(Paragraph(
        "A: I designed an unsupervised anomaly detection system simulated across a 5-layer Federated Learning topology. Edge nodes scale "
        "continuous flow features, exclude target leakage columns, and construct sliding sequence windows of length 10. They train a custom "
        "MiniTransformerAutoencoder (with sinusoidal positional encodings and latent dimension 32) strictly on benign data to minimize "
        "reconstruction MSE. Model parameter weights are quantized to float16 during uploads to halve payload transmission sizes, buffered "
        "at the Gateway, and aggregated at the Fog layer via FedAvg. The Cloud Node establishes a global dynamic threshold of Mean(MSE) + 4*Std(MSE) "
        "and tests it on stratified folds to prevent support bias. Finally, SHAP KernelExplainer is mapped to the model's reconstruction MSE "
        "output space to visualize feature attribution values.",
        a_style
    ))

    # --- SECTION 11 ---
    story.append(Spacer(1, 10))
    story.append(Paragraph("11. Common Interview Pitfalls & Mistakes to Avoid", h1_style))

    story.append(Paragraph("Pitfall 1: Claiming 'Federated Learning is completely secure.'", q_style))
    story.append(Paragraph(
        "<b>❌ Avoid saying</b>: 'Federated Learning is completely secure.'<br/>"
        "<b>✔ Say instead</b>: 'Federated Learning improves data privacy by keeping raw data local, but it is not inherently secure against "
        "all threats. Additional defenses like secure multi-party aggregation (SecAgg) or differential privacy (DP) are required to protect "
        "the shared weights from model-inversion or membership-inference reconstruction attacks.'",
        a_style
    ))

    story.append(Paragraph("Pitfall 2: Saying 'Transformers are always better than other architectures.'", q_style))
    story.append(Paragraph(
        "<b>❌ Avoid saying</b>: 'Transformers are always better.'<br/>"
        "<b>✔ Say instead</b>: 'For this project, the Transformer was selected because its self-attention mechanism excels at modeling "
        "non-sequential dependencies across flow packets. However, for resource-constrained edge hardware with tight memory limits, "
        "lightweight LSTMs or traditional Gated Recurrent Units (GRUs) might be preferred depending on latency trade-offs.'",
        a_style
    ))

    story.append(Paragraph("Pitfall 3: Stating 'Model accuracy decreased' in a defensive tone.", q_style))
    story.append(Paragraph(
        "<b>❌ Avoid saying</b>: 'The model accuracy decreased.'<br/>"
        "<b>✔ Say instead</b>: 'The early evaluation accuracy was inflated due to target column leakage and sequential test split bias. "
        "After filtering out the leakage column (Attack_categories) and stratifying test partitions, the evaluation adjusted to a realistic, "
        "leak-free 84.5% baseline. This represents a robust system improvement rather than a performance drop.'",
        a_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    build_pdf()
    print("Project_Interview_Defense_Guide.pdf generated successfully.")
