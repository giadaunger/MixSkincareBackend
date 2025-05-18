from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

class ProductCompatibilityModel:
    _instance = None
    
    @staticmethod
    def get_instance():
        if ProductCompatibilityModel._instance is None:
            ProductCompatibilityModel._instance = ProductCompatibilityModel()
        return ProductCompatibilityModel._instance
    
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.initialized = False
    
    def _initialize(self):
        token = os.getenv("HUGGINGFACE_TOKEN") 
        if not self.initialized:
            print("Initializing ML model for product compatibility...")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    "gigiU/product-compatibility-classifier",
                    use_auth_token=token
                )
                self.model.eval()  
                self.initialized = True
                print("ML model initialized successfully!")
            except Exception as e:
                print(f"Error initializing ML model: {e}")
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-multilingual-cased")
                    self.model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-multilingual-cased", num_labels=2)
                    print("Fallback to base model succeeded")
                    self.initialized = True
                except Exception as e2:
                    print(f"Fatal error initializing even base model: {e2}")
                    raise
    
    def predict_compatibility(self, product1_name, product2_name):
        self._initialize()
        
        input_text = f"Produkt 1: {product1_name} Produkt 2: {product2_name}"
        
        inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = outputs.logits
            
        probabilities = torch.nn.functional.softmax(predictions, dim=-1)
        
        compatibility_score = probabilities[0][1].item()  
        is_compatible = compatibility_score > 0.5
        
        return {
            "is_compatible": bool(is_compatible),
            "compatibility_score": round(compatibility_score * 100, 2)  
        }