# This script converts the AI Studio code gen to a markdown format

class MockTypes:
    class Part:
        @staticmethod
        def from_text(text):
            return {"text": text}
    
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
    for content in contents:
        dict_content = content.to_dict()
        if "user" in dict_content:
            print("## Me")
            print(dict_content["user"])
        if "model" in dict_content:
            print("## Gemini")
            print(dict_content["model"])
        print()

def main():
    ## START COPY HERE
    
    contents = []
    
    ## END COPY HERE
    process_contents(contents)

if __name__ == "__main__":
    main()

