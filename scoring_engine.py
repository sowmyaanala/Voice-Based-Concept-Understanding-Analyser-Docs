def evaluate_understanding(similarity, filler_ratio, audio):
    score = 0

    score += 50 if similarity > 0.7 else 30 if similarity > 0.4 else 10
    score += 20 if filler_ratio < 0.05 else 10
    score += 15 if audio["pause_ratio"] < 0.25 else 5
    score += 15 if audio["rms_energy"] > 0.01 else 5

    if score >= 80:
        return score, "Strong Understanding", "#2ecc71"
    elif score >= 50:
        return score, "Moderate Understanding", "#f39c12"
    else:
        return score, "Poor Understanding", "#e74c3c"


if __name__ == "__main__":
    audio = {
        "pause_ratio": 0.10,
        "rms_energy": 0.03
    }

    score, level, color = evaluate_understanding(
        similarity=0.85,
        filler_ratio=0.02,
        audio=audio
    )

    print("Score:", score)
    print("Level:", level)
    print("Color:", color)