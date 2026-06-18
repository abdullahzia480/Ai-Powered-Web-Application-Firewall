import pandas as pd
import os

def augment_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'waftool', 'sqli-extended.csv')
    
    # Critical short patterns that must be detected
    short_patterns = [
        # Basic SQLi
        ("1=1", 1), ("'='", 1), ("OR 1=1", 1), ("admin' --", 1),
        ("1=1 --", 1), ("' OR '1'='1", 1), ("true=true", 1),
        # XSS patterns (User expects these blocked too)
        ("<script>", 1), ("javascript:", 1), ("onerror=", 1),
        ("alert(1)", 1), ("<img src=x", 1),
        # Heuristic-bypassing attempts
        ("q=1=1", 1), ("id=1=1", 1), ("user=admin'#", 1),
        
        # BENIGN Patterns (To prevent false positives on q=...)
        ("q=cpu", 0), ("q=search", 0), ("id=5", 0),
        ("category=processors", 0), ("page=1", 0),
        ("q=hello", 0), ("search=test", 0),
        ("q=shop", 0), ("user=john", 0)
    ]
    
    # Repeat them to give them weight in the large dataset
    # 50MB dataset is huge, so we need significant repetition
    # or rely on the vectorizer catching the grams.
    # Let's add 500 copies of each to ensure they are statistically significant
    
    new_data = []
    for pattern, label in short_patterns:
        for _ in range(500):
            new_data.append({'Sentence': pattern, 'Label': label})
            
    df_new = pd.DataFrame(new_data)
    
    # Append to CSV mode 'a' without header
    df_new.to_csv(csv_path, mode='a', header=False, index=False)
    print(f"Added {len(df_new)} critical patterns to {csv_path}")

if __name__ == "__main__":
    augment_data()
