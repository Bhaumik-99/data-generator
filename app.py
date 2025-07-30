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
    prompt = f"""Generate exactly 10 unique, interesting, and factual statements about "{keyword}".
     fact should be a standalone, complete sentence, and should be between 250 and 500 characters long.
    Avoid using numbers, bullets, or any formatting — just return plain text.
    Do not repeat facts. Ensure each statement is verifiable and reflects real-world knowledge.
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

def generate_unique_facts(keyword: str, target_count: int = 1500, model: str = "llama3") -> List[str]:
    """Generate unique facts about a keyword until target count is reached."""
    unique_facts: Set[str] = set()
    all_facts: List[str] = []
    
    print(f"Starting fact generation for keyword: '{keyword}'")
    print(f"Target: {target_count} unique facts")
    print("-" * 50)
    
    iteration = 0
    
    while len(unique_facts) < target_count:
        iteration += 1
        print(f"Iteration {iteration}: Generating facts... (Current unique count: {len(unique_facts)})")
        
        # Generate facts using Ollama
        new_facts = call_ollama(keyword, model)
        
        if not new_facts:
            print("No facts generated this iteration, continuing...")
            time.sleep(1)
            continue
        
        # Add new unique facts
        facts_added_this_iteration = 0
        for fact in new_facts:
            if fact not in unique_facts and len(fact) > 20:  # Ensure substantial facts
                unique_facts.add(fact)
                all_facts.append(fact)
                facts_added_this_iteration += 1
                print(f"  Added fact #{len(unique_facts)}: {fact[:80]}{'...' if len(fact) > 80 else ''}")
        
        print(f"  Added {facts_added_this_iteration} new facts this iteration")
        print(f"  Total unique facts: {len(unique_facts)}/{target_count}")
        print()
        
        # Sleep to avoid overloading
        time.sleep(1)
    
    print(f"Successfully generated {len(unique_facts)} unique facts!")
    return all_facts

def save_to_excel(facts: List[str], keyword: str, filename: str = None) -> str:
    """Save facts to an Excel file."""
    if filename is None:
        filename = f"{keyword}_facts_ollama.xlsx"
    
    # Create DataFrame
    df = pd.DataFrame({
        'Fact_Number': range(1, len(facts) + 1),
        'Fact': facts,
        'Keyword': [keyword] * len(facts),
        'Character_Count': [len(fact) for fact in facts]
    })
    
    # Save to Excel
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'{keyword}_Facts', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets[f'{keyword}_Facts']
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 100)  # Cap at 100 characters
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        
        print(f"Facts saved to: {filename}")
        return filename
    
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return ""

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
    prompt = f"""Generate exactly 10 unique, interesting, and factual statements about "{keyword}".
     fact should be a standalone, complete sentence, and should be between 250 and 500 characters long.
    Avoid using numbers, bullets, or any formatting — just return plain text.
    Do not repeat facts. Ensure each statement is verifiable and reflects real-world knowledge.
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

def generate_unique_facts(keyword: str, target_count: int = 1500, model: str = "llama3") -> List[str]:
    """Generate unique facts about a keyword until target count is reached."""
    unique_facts: Set[str] = set()
    all_facts: List[str] = []
    
    print(f"Starting fact generation for keyword: '{keyword}'")
    print(f"Target: {target_count} unique facts")
    print("-" * 50)
    
    iteration = 0
    
    while len(unique_facts) < target_count:
        iteration += 1
        print(f"Iteration {iteration}: Generating facts... (Current unique count: {len(unique_facts)})")
        
        # Generate facts using Ollama
        new_facts = call_ollama(keyword, model)
        
        if not new_facts:
            print("No facts generated this iteration, continuing...")
            time.sleep(1)
            continue
        
        # Add new unique facts
        facts_added_this_iteration = 0
        for fact in new_facts:
            if fact not in unique_facts and len(fact) > 20:  # Ensure substantial facts
                unique_facts.add(fact)
                all_facts.append(fact)
                facts_added_this_iteration += 1
                print(f"  Added fact #{len(unique_facts)}: {fact[:80]}{'...' if len(fact) > 80 else ''}")
        
        print(f"  Added {facts_added_this_iteration} new facts this iteration")
        print(f"  Total unique facts: {len(unique_facts)}/{target_count}")
        print()
        
        # Sleep to avoid overloading
        time.sleep(1)
    
    print(f"Successfully generated {len(unique_facts)} unique facts!")
    return all_facts

def save_to_excel(facts: List[str], keyword: str, filename: str = None) -> str:
    """Save facts to an Excel file."""
    if filename is None:
        filename = f"{keyword}_facts_ollama.xlsx"
    
    # Create DataFrame
    df = pd.DataFrame({
        'Fact_Number': range(1, len(facts) + 1),
        'Fact': facts,
        'Keyword': [keyword] * len(facts),
        'Character_Count': [len(fact) for fact in facts]
    })
    
    # Save to Excel
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'{keyword}_Facts', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets[f'{keyword}_Facts']
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 100)  # Cap at 100 characters
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        
        print(f"Facts saved to: {filename}")
        return filename
    
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return ""

def main():
    """Main function to run the fact generation script."""
    # Configuration
    keyword = input("Enter the keyword for fact generation (e.g., 'space'): ").strip()
    if not keyword:
        print("No keyword provided. Using 'space' as default.")
        keyword = "space"
    
    model = input("Enter Ollama model name (default: llama3): ").strip()
    if not model:
        model = "llama3"
    
    target_count = 1500
    
    print(f"\nConfiguration:")
    print(f"Keyword: {keyword}")
    print(f"Model: {model}")
    print(f"Target facts: {target_count}")
    print(f"Output file: {keyword}_facts_ollama.xlsx")
    print("\nStarting generation...\n")
    
    try:
        # Check if Ollama is available
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error: Ollama is not available or not installed.")
            print("Please make sure Ollama is installed and running.")
            sys.exit(1)
        
        # Generate facts
        facts = generate_unique_facts(keyword, target_count, model)
        
        if len(facts) >= target_count:
            # Save to Excel
            filename = save_to_excel(facts[:target_count], keyword)
            
            print(f"\n{'='*50}")
            print("GENERATION COMPLETE!")
            print(f"Generated: {len(facts[:target_count])} unique facts")
            print(f"Keyword: {keyword}")
            print(f"Saved to: {filename}")
            print(f"{'='*50}")
        else:
            print(f"Warning: Only generated {len(facts)} facts (target was {target_count})")
            
    except KeyboardInterrupt:
        print("\nGeneration interrupted by user.")
        if 'facts' in locals() and facts:
            save_partial = input(f"Save {len(facts)} facts generated so far? (y/n): ")
            if save_partial.lower() == 'y':
                save_to_excel(facts, keyword)
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()