import json
import random
import re
import urllib.request

CURATED_QUOTES = [
    ("No one knows what the future holds. That is why its potential is infinite.", "Rintaro Okabe (Steins;Gate)"),
    ("If you do not like your destiny, do not accept it. Instead, have the courage to change it.", "Naruto Uzumaki"),
    ("Whatever you do, enjoy it to the fullest. That is the secret of life.", "Rider (Fate/Zero)"),
    ("The world is not perfect. But it is there for us, doing the best it can.", "Roy Mustang (Fullmetal Alchemist)"),
    ("If you don't take risks, you can't create a future.", "Monkey D. Luffy (One Piece)"),
    ("Fear is not evil. It tells you what your weakness is.", "Gildarts Clive (Fairy Tail)"),
    ("Hard work is worthless for those that don't believe in themselves.", "Naruto Uzumaki"),
    ("The ticket to the future is always open.", "Vash the Stampede (Trigun)"),
    ("Push through the pain, giving up hurts more.", "Vegeta (Dragon Ball)"),
    ("A person grows once they could defeat the defeatism inside them.", "Tatsuhiro Sato (Welcome to the N.H.K.)"),
    ("Whether a fish lives in a clear stream or a water ditch, so long as it continues swimming forward, it will grow up beautifully.", "Koro-sensei (Assassination Classroom)"),
    ("If you just submit to fate, that's the end of it.", "C.C. (Code Geass)"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("Fix the cause, not the symptom.", "Steve Maguire"),
    ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
    ("Walking on water and developing software from a specification are easy if both are frozen.", "Edward V. Berard"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Truth can only be found in one place: the code.", "Robert C. Martin"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("The best error message is the one that never shows up.", "Thomas Fuchs"),
]

def extract_current_quote(content):
    match = re.search(
        r'<!-- quote-start -->.*?>(?:\s*)\*"(.*?)"\*.*?<!-- quote-end -->',
        content,
        flags=re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return ""

def fetch_api_quote():
    try:
        req = urllib.request.Request(
            "https://zenquotes.io/api/random",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode())
            if isinstance(data, list) and len(data) > 0:
                q = data[0].get("q", "").strip()
                a = data[0].get("a", "").strip()
                if q and a and "Too many requests" not in q:
                    return q, a
    except Exception:
        pass
    return None

def fetch_quote(current_quote=""):
    # Filter curated quotes to exclude the quote currently displayed
    available_curated = [
        (q, a) for (q, a) in CURATED_QUOTES
        if q.strip().replace('"', '\\"') != current_quote.strip()
    ]
    if not available_curated:
        available_curated = CURATED_QUOTES

    # Try up to 5 times to get a quote that differs from current_quote
    for _ in range(5):
        if random.random() >= 0.5:
            api_result = fetch_api_quote()
            if api_result:
                q, a = api_result
                if q.replace('"', '\\"').strip() != current_quote.strip():
                    return q, a

        selected = random.choice(available_curated)
        if selected[0].replace('"', '\\"').strip() != current_quote.strip():
            return selected

    return random.choice(available_curated)

def main():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    current_quote = extract_current_quote(content)
    quote, author = fetch_quote(current_quote)
    quote = quote.replace('"', '\\"')

    replacement = f"""<!-- quote-start -->
<div align="center">

>  *"{quote}"* — **{author}**

</div>
<!-- quote-end -->"""

    new_content = re.sub(
        r"<!-- quote-start -->.*?<!-- quote-end -->",
        replacement,
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated quote: {quote} — {author}")

if __name__ == "__main__":
    main()
