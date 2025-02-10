from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Optimized Prompt Template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** Only extract what matches the provided description: {parse_description}.\n"
    "2. **No Extra Content:** Do not include explanations or additional text.\n"
    "3. **Return an Empty String ('') if No Match:** If no relevant data is found, return an empty string.\n"
    "4. **Direct Data Only:** Output should contain only the required information."
)

# Load Ollama Model
model = OllamaLLM(model="llama3.1")

def parse_with_ollama(dom_chunks, parse_description):
    """Processes chunks of text with Ollama and returns extracted information."""
    prompt = ChatPromptTemplate.from_template(template)
    
    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start=1):
        chain = prompt.format_prompt(dom_content=chunk, parse_description=parse_description)
        response = model.invoke(chain.to_string())

        print(f"🟢 Ollama Response for Chunk {i}: {response}")

        if response:
            parsed_results.append(response)
        else:
            parsed_results.append("No relevant data found.")

    return "\n".join(parsed_results)
