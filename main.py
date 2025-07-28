#!/usr/bin/env python3
"""
Ollama Fact Generator Script
Generates 2500 unique facts about a given keyword using Ollama and saves to Excel.
"""

import subprocess
import json
import time
import re
import pandas as pd
from typing import Set, List
import sys

def clean_fact(fact: str) -> str:
    """Clean a fact by removing leading numbers, bullets, and extra whitespace."""
    # Remove leading numbers (1., 2., etc.) and bullets (-, *, •)
    fact = re.sub(r'^\s*[\d]+[\.\)]\s*', '', fact)
    fact = re.sub(r'^\s*[-\*•]\s*', '', fact)
    # Remove extra whitespace and strip
    fact = ' '.join(fact.split()).strip()
    return fact

def call_ollama(keyword: str, model: str = "llama3") -> List[str]:
    """Call Ollama to generate facts about a keyword."""
    prompt = f"""Generate exactly 10 unique and imaginative myths or legendary FAKE beliefs related to "{keyword}".
Each myth must be a complete sentence between 400 and 700 characters long.
Do not include any heading, numbering, or formatting — just plain text.
Avoid repetition. Myths should feel mysterious, culturally inspired, and entirely fictional.
Only output the 10 sentences, each on a new line.
"""


    
    try:
        # Prepare the command for Ollama
        cmd = ["ollama", "run", model]
        
        # Run the command with the prompt, using UTF-8 encoding
        result = subprocess.run(
            cmd,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=120,  # Increased timeout
            encoding='utf-8',
            errors='replace'  # Replace problematic characters
        )
        
        if result.returncode != 0:
            print(f"Error running Ollama: {result.stderr}")
            return []
        
        # Parse the output into individual facts
        output = result.stdout.strip()
        if not output:
            print("No output received from Ollama")
            return []
            
        facts = [line.strip() for line in output.split('\n') if line.strip()]
        
        # Clean each fact
        cleaned_facts = []
        for fact in facts:
            cleaned = clean_fact(fact)
            if cleaned and len(cleaned) > 10:  # Only keep substantial facts
                cleaned_facts.append(cleaned)
        
        return cleaned_facts
    
    except subprocess.TimeoutExpired:
        print("Ollama call timed out (this is normal for larger models)")
        return []
    except UnicodeDecodeError as e:
        print(f"Unicode encoding error: {e}")
        return []
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return []

