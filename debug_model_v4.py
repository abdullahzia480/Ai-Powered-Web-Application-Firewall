from waftool.ai_engine import AIEngine

def test():
    engine = AIEngine()
    payloads = ["q=cpu", "q=1=1", "cpu", "1=1"]
    for p in payloads:
        is_mal, score = engine.predict(p)
        print(f"'{p}': Malicious={is_mal}, Score={score}")

if __name__ == "__main__":
    test()
