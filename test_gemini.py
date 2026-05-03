from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

response = client.chat.completions.create(
    model = "llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Explain fuel efficiency"}]
)

print(response.choices[0].message.content)