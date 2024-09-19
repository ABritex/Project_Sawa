def generate_subtitle(chat_now, result_id):
    with open("output.txt", "w", encoding="utf-8") as outfile:
        try:
            text = result_id
            words = text.split()
            lines = [words[i:i+10] for i in range(0, len(words), 10)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")
        except:
            print("Error writing to output.txt")

    with open("chat.txt", "w", encoding="utf-8") as outfile:
        try:
            words = chat_now.split()
            lines = [words[i:i+10] for i in range(0, len(words), 10)]
            for line in lines:
                outfile.write(" ".join(line) + "\n")
        except:
            print("Error writing to chat.txt")
