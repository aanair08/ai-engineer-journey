def analyze_text(text):
    words = text.split()
    
    return{
       "word_count": len(words),
       "char_count": len(text),
       "preview": text[:30]
    }

text = input("Enter text: ")

result =analyze_text(text)

print("Anlysis:")

for key, value in result.items():
    print(f"{key}: {value}")
