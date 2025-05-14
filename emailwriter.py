import openai

def generate_email(prompt, tone="professional", recipient="General"):
    """
    Generates an email based on the given prompt, tone, and recipient type.
    """
    client = openai.OpenAI(api_key="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")  # Replace with your actual API key

    response = client.chat.completions.create(
        model="gpt-3.5-turbo"
,
        messages=[
            {"role": "system", "content": f"Write a {tone} email addressed to {recipient}."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    subject = "Meeting Reschedule Request"
    body = "I need to reschedule our meeting originally set for Monday at 3 PM. Please let me know your availability."
    
    email_content = generate_email(body, tone="polite", recipient="Team")
    print(email_content)
