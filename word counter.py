# ================================================
# Word Counter Program
# ================================================

### User Input Section ###

def get_user_input():
    """
    Prompts the user to enter a sentence or paragraph.
    Returns the user's input as a string.
    """
    user_input = input("Please enter a sentence or paragraph: ")
    return user_input

### Word Counting Logic Section ###
def count_words(input_string):
    """
    Counts the number of words in the given input string.
    Returns the word count as an integer.
    """
    # Remove leading/trailing whitespaces and convert to lowercase
    cleaned_string = input_string.strip().lower()
    
    # Split the string into words (assuming spaces as delimiters)
    words = cleaned_string.split()
    
    # Return the number of words
    return len(words)

### Error Handling & Output Display Section ###
def main():
    """
    Orchestrates the program's flow, handles errors, and displays the output.
    """
    try:
        # Get user input
        user_text = get_user_input()
        
        # Check for empty input
        if not user_text.strip():
            print("Error: Input cannot be empty. Please try again.")
            return
        
        # Count the words
        word_count = count_words(user_text)
        
        # Display the word count
        print(f"Word Count: {word_count}")
    
    except Exception as e:
        # Catch any unexpected errors and display a friendly message
        print("An unexpected error occurred. Please try again later.")
        print(f"Error Details: {str(e)}")

### Program Entry Point ###

if __name__ == "__main__":
    main()




# short approach...

# ================================================
# Word Counter Program
# ================================================

# def main():
#     """
#     Prompts user for input, counts words, and displays the result.
#     """
#     try:
#         user_text = input("Please enter a sentence or paragraph: ").strip()
#         if not user_text:
#             print("Error: Input cannot be empty. Please try again.")
#             return
#         print(f"Word Count: {len(user_text.lower().split())}")
    
#     except Exception as e:
#         print("An unexpected error occurred. Please try again later.")
#         print(f"Error Details: {str(e)}")

# if __name__ == "__main__":
#     main()


#very short approach 

# ================================================
# Word Counter Program
# ================================================
    
#user=input("enter the sentence : ")
#words=user.split()
#print(f"total number of words : ",len(words))
