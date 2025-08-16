# This script converts the AI Studio code gen to a markdown format

import base64

# Create a safe base64 decode function that handles invalid data
def safe_b64decode(data):
    try:
        return base64.b64decode(data)
    except Exception:
        # If decode fails, return the original data as bytes
        return data.encode('utf-8') if isinstance(data, str) else data

# Replace the base64.b64decode with our safe version
base64.b64decode = safe_b64decode

class MockTypes:
    class Part:
        @staticmethod
        def from_text(text):
            return {"text": text}
        
        @staticmethod
        def from_bytes(mime_type, data):
            # The data parameter might be the result of base64.b64decode() 
            # which could fail with invalid base64 strings like placeholder text
            # Just store whatever data we receive without trying to process it
            return {"mime_type": mime_type, "data": data, "type": "bytes"}
    
    class Content:
        def __init__(self, role, parts):
            self.role = role
            self.parts = parts
            
        def to_dict(self):
            # Extract text from all parts
            texts = []
            for part in self.parts:
                if isinstance(part, dict) and "text" in part:
                    texts.append(part["text"])
                elif isinstance(part, dict) and "type" in part and part["type"] == "bytes":
                    # Skip non-text parts (like PDFs, images, etc.) but add a placeholder
                    mime_type = part.get("mime_type", "unknown")
                    texts.append(f"[Attachment: {mime_type}]")
            
            # For model role, skip the first part (reasoning step)
            if self.role == "model" and len(texts) > 1:
                texts = texts[1:]
            
            # Return dict with role as key and concatenated text as value
            concatenated_text = "\n\n".join(texts)
            return {self.role: concatenated_text}

types = MockTypes()

def process_contents(contents):
    """Process the contents and print them as dictionaries"""
    contents = contents[:-1]
    q_count = 0
    a_count = 0
    for content in contents:
        dict_content = content.to_dict()
        if "user" in dict_content:
            print(f"## Question {q_count + 1}")
            print(dict_content["user"])
        if "model" in dict_content:
            print(f"## Answer {a_count + 1}")
            print(dict_content["model"])
        print()

def main():
    ## START COPY HERE
    
    contents = []
    
    ## END COPY HERE
    process_contents(contents)

if __name__ == "__main__":
    main()

