"""
Sample script to generate a test Chroma vector database
"""

import os

def create_sample_chroma_db(output_dir="examples/sample_chroma"):
    """Create a sample Chroma database for testing"""
    
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        print("❌ chromadb is not installed")
        print("Install it with: pip install chromadb")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Creating Chroma database in {output_dir}...")
    
    # Initialize Chroma client
    client = chromadb.PersistentClient(path=output_dir)
    
    # Create or get collection
    try:
        collection = client.get_collection(name="ai_documents")
        client.delete_collection(name="ai_documents")
    except:
        pass
    
    collection = client.create_collection(
        name="ai_documents",
        metadata={"description": "Sample AI and ML documents for testing"}
    )
    
    # Sample documents
    documents = [
        "Artificial Intelligence (AI) is the simulation of human intelligence by machines. AI systems can learn, reason, and self-correct.",
        "Machine Learning is a subset of AI that enables systems to learn from data without being explicitly programmed.",
        "Deep Learning uses artificial neural networks with multiple layers to progressively extract higher-level features from raw input.",
        "Natural Language Processing (NLP) focuses on the interaction between computers and human language.",
        "Computer Vision enables machines to derive meaningful information from digital images and videos.",
        "Reinforcement Learning is a type of machine learning where agents learn to make decisions by interacting with an environment.",
        "Neural Networks are computing systems inspired by biological neural networks in animal brains.",
        "Transformers are a type of neural network architecture that has revolutionized NLP tasks.",
        "BERT (Bidirectional Encoder Representations from Transformers) is a pre-trained model for NLP.",
        "GPT (Generative Pre-trained Transformer) models can generate human-like text based on context.",
        "Vector embeddings represent data as points in high-dimensional space, capturing semantic relationships.",
        "FAISS (Facebook AI Similarity Search) is a library for efficient similarity search of dense vectors.",
        "ChromaDB is an open-source embedding database designed for AI applications.",
        "Semantic search finds results based on meaning rather than exact keyword matches.",
        "RAG (Retrieval Augmented Generation) combines information retrieval with text generation.",
        "Fine-tuning adapts pre-trained models to specific tasks with additional training.",
        "Transfer learning applies knowledge learned from one task to a different but related task.",
        "Attention mechanisms allow models to focus on relevant parts of input when making predictions.",
        "Large Language Models (LLMs) are neural networks trained on massive amounts of text data.",
        "Prompt engineering is the practice of designing inputs to get desired outputs from AI models.",
        "Few-shot learning enables models to learn from a small number of examples.",
        "Zero-shot learning allows models to perform tasks without specific training examples.",
        "Embeddings compress information into fixed-size vectors while preserving semantic relationships.",
        "Cosine similarity measures the similarity between two vectors based on the angle between them.",
        "Dimensionality reduction techniques like t-SNE help visualize high-dimensional data.",
        "Tokenization breaks text into smaller units (tokens) for processing by language models.",
        "Hyperparameters are configuration settings that control the learning process of models.",
        "Overfitting occurs when a model learns training data too well, including noise and outliers.",
        "Regularization techniques prevent overfitting by adding constraints to model training.",
        "Backpropagation is the algorithm used to train neural networks by computing gradients.",
        "Gradient descent is an optimization algorithm for minimizing loss functions.",
        "Convolutional Neural Networks (CNNs) are specialized for processing grid-like data such as images.",
        "Recurrent Neural Networks (RNNs) are designed for sequential data processing.",
        "Long Short-Term Memory (LSTM) networks are a type of RNN that can learn long-term dependencies.",
        "Generative Adversarial Networks (GANs) consist of two neural networks competing against each other.",
        "Autoencoders learn efficient representations of data through unsupervised learning.",
        "Batch normalization improves training speed and stability of neural networks.",
        "Dropout is a regularization technique that prevents overfitting by randomly dropping neurons.",
        "Activation functions introduce non-linearity into neural networks enabling complex pattern learning.",
        "Cross-entropy loss is commonly used for classification tasks in machine learning.",
        "Data augmentation artificially expands training datasets to improve model generalization.",
        "Ensemble methods combine multiple models to improve prediction accuracy and robustness.",
        "Model evaluation metrics like accuracy, precision, and recall measure model performance.",
        "Confusion matrices provide detailed breakdowns of classification model performance.",
        "Feature engineering creates new input features from existing data to improve model performance.",
        "Principal Component Analysis (PCA) reduces dimensionality while preserving variance.",
        "K-means clustering groups similar data points together in unsupervised learning.",
        "Decision trees are interpretable models that make predictions through a series of decisions.",
        "Random forests combine multiple decision trees to improve accuracy and reduce overfitting.",
        "Support Vector Machines (SVMs) find optimal hyperplanes to separate different classes.",
        "Gradient boosting builds models sequentially, with each model correcting errors of previous ones.",
        "Learning rate determines the step size during gradient descent optimization.",
        "Batch size affects training speed and model convergence during neural network training.",
        "Epochs represent complete passes through the training dataset during model training.",
        "Validation sets help tune hyperparameters and prevent overfitting during training.",
        "Test sets provide unbiased evaluation of final model performance.",
        "Cross-validation assesses model performance by training on different data subsets.",
        "Bias-variance tradeoff balances model complexity with generalization capability.",
        "Model interpretability helps understand how AI systems make decisions.",
        "Explainable AI (XAI) makes AI decision-making processes transparent and understandable.",
        "Edge AI deploys AI models on edge devices for real-time processing without cloud dependency.",
        "Federated learning trains models across decentralized devices while keeping data local.",
        "Transfer learning accelerates model development by leveraging pre-trained models.",
        "Meta-learning enables models to learn how to learn from limited data.",
        "Multi-task learning trains models to perform multiple related tasks simultaneously.",
        "Continual learning allows models to learn new tasks without forgetting previous ones.",
        "Active learning selectively queries informative data points to improve learning efficiency.",
        "Synthetic data generation creates artificial training data to supplement real data.",
        "Data privacy techniques protect sensitive information in AI training and deployment.",
        "Model compression reduces model size for efficient deployment on resource-constrained devices.",
        "Quantization reduces numerical precision to decrease model size and increase inference speed.",
        "Knowledge distillation transfers knowledge from large models to smaller, more efficient ones.",
        "Neural architecture search automates the design of optimal neural network architectures.",
        "AutoML automates the process of applying machine learning to real-world problems.",
        "Hyperparameter optimization systematically searches for optimal model configuration.",
        "Curriculum learning trains models by gradually increasing task difficulty.",
        "Self-supervised learning learns representations from unlabeled data using pretext tasks.",
        "Contrastive learning learns representations by contrasting positive and negative examples.",
        "Vision transformers apply transformer architecture to image recognition tasks.",
        "Multimodal learning combines information from multiple modalities like text, images, and audio.",
        "Graph neural networks process data represented as graphs with nodes and edges.",
        "Attention-based models focus on relevant information when processing sequential data.",
        "Prompt tuning optimizes prompts instead of model parameters for task adaptation.",
        "In-context learning enables models to perform tasks based on examples in the prompt.",
        "Chain-of-thought prompting improves reasoning by encouraging step-by-step thinking.",
        "Instruction tuning trains models to follow natural language instructions.",
        "RLHF (Reinforcement Learning from Human Feedback) aligns models with human preferences.",
        "Constitutional AI incorporates ethical principles into AI behavior through training.",
        "Red teaming tests AI systems for potential harmful behaviors and vulnerabilities.",
        "AI safety research addresses risks and ensures beneficial AI development.",
        "Adversarial examples are inputs designed to fool machine learning models.",
        "Robust machine learning develops models resistant to adversarial attacks.",
        "Fairness in AI ensures models don't discriminate based on protected attributes.",
        "Bias mitigation techniques reduce unfair discrimination in AI systems.",
        "AI governance establishes frameworks for responsible AI development and deployment.",
        "Model cards document machine learning model details for transparency and accountability.",
        "Data cards provide documentation for datasets used in machine learning.",
        "AI ethics addresses moral implications of artificial intelligence systems.",
        "Responsible AI practices ensure AI systems are trustworthy, fair, and beneficial.",
    ]
    
    # Create IDs
    ids = [f"doc_{i:04d}" for i in range(len(documents))]
    
    # Create metadata
    topics = ["AI Basics", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", 
              "Neural Networks", "Model Training", "Evaluation", "Advanced Topics"]
    
    metadatas = [
        {
            "source": f"ai_textbook_chapter_{(i // 10) + 1}.pdf",
            "page": (i % 50) + 1,
            "topic": topics[i % len(topics)],
            "author": ["Dr. Smith", "Prof. Johnson", "Dr. Lee"][i % 3],
            "year": 2023 + (i % 2)
        }
        for i in range(len(documents))
    ]
    
    # Add to collection (Chroma will generate embeddings automatically)
    print(f"Adding {len(documents)} documents to collection...")
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )
    
    # Verify
    count = collection.count()
    print(f"✓ Added {count} documents to collection '{collection.name}'")
    
    # Create README for this example
    readme_content = f"""# Sample Chroma Database

This is a sample Chroma vector database for testing Vector Explorer.

## Contents
- Chroma database with {len(documents)} AI/ML-related documents
- Automatically generated embeddings
- Rich metadata including source, topic, author, and year

## Collection Details
- Name: ai_documents
- Documents: {len(documents)}
- Embeddings: Auto-generated by Chroma

## Topics Covered
- Artificial Intelligence basics
- Machine Learning fundamentals
- Deep Learning architectures
- Natural Language Processing
- Computer Vision
- Model training and evaluation
- Advanced AI topics
- AI Ethics and Safety

## Usage
1. Open VS Code
2. Press Ctrl+Shift+P (Cmd+Shift+P on Mac)
3. Type "Vector Explorer: Open Vector Database"
4. Select the `sample_chroma` directory

## Sample Queries
Try searching for:
- "transformers" - Find documents about transformer models
- "neural networks" - Discover neural network concepts
- "training" - Locate model training information
- "embeddings" - Find embedding-related content
"""
    
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"✓ Saved README to {readme_path}")
    
    print("\n✅ Sample Chroma database created successfully!")
    print(f"📁 Location: {os.path.abspath(output_dir)}")
    print("\nTo use with Vector Explorer:")
    print("1. Open VS Code")
    print("2. Run 'Vector Explorer: Open Vector Database'")
    print(f"3. Select directory: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    create_sample_chroma_db()
