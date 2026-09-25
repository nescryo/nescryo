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
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
    ("Fix the cause, not the symptom.", "Steve Maguire"),
    ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
    ("Walking on water and developing software from a specification are easy if both are frozen.", "Edward V. Berard"),
]

def fetch_quote():
    # 50% chance to pick an iconic anime/dev quote, 50% chance to fetch from API
    if random.random() < 0.5:
        return random.choice(CURATED_QUOTES)

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
                if q and a:
                    return q, a
    except Exception:
        pass

    return random.choice(CURATED_QUOTES)

def main():
    quote, author = fetch_quote()
    quote = quote.replace('"', '\\"')

    replacement = f"""<!-- quote-start -->
<div align="center">

>  *"{quote}"* — **{author}**

</div>
<!-- quote-end -->"""

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

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
