def calculate_rank(session, all_sessions):
    """Обчислює місце користувача в рейтингу"""
    for i, s in enumerate(all_sessions, 1):
        if s.id == session.id:
            return i
    return None

def format_time(seconds):
    """Форматує час у зручний вигляд"""
    if seconds is None:
        return "Без часу"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours} год")
    if minutes > 0:
        parts.append(f"{minutes} хв")
    if secs > 0 or not parts:
        parts.append(f"{secs} сек")
    
    return " ".join(parts)