import re

def restore_truncated_string(context, original_string):
    # Define the regex pattern for words in the context
    pattern = r'\b[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*\b'
    
    # Search for the truncated part in the context
    match = re.search(pattern, context)
    
    if match:
        truncated_part = match.group(0)
        # Use regex to find the match in the original string
        full_match = re.search(re.escape(truncated_part), original_string)
        if full_match:
            # Extract the full word from the original string
            start_index = full_match.start()
            end_index = start_index
            while end_index < len(original_string) and original_string[end_index].isalnum():
                end_index += 1
            return original_string[start_index:end_index]
    
    return None

# Example usage:
context = "select * from ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzaazyuauauaipsdfghjklm where 1 = 1"
original = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzaazyuauaua"

restored = restore_truncated_string(context, original)

if restored:
    print(f"Restored string: {restored}")
else:
    print("Could not restore the string.")

